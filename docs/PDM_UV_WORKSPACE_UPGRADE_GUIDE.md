# PDM + uv Workspace 升级操作文档

## 1. 目标

- 将项目构建后端迁移为 `pdm-backend`，并保留现有依赖约束不变。
- 维持 `pip`、`pdm`、`uv` 三条安装/校验路径的兼容性。
- 为 CI 和本地提供可追溯的锁文件与回归验证流程。

## 2. 变更结果

- `pyproject.toml` 构建后端已切换：
  - `build-backend = "pdm.backend"`
  - `requires = ["pdm-backend>=2.4.0", "uv-build>=0.8.8"]`
- `tool.pdm` 已显式启用 uv 解析，并固定锁文件格式策略：
  - `use_uv = true`
  - `lock.format = "pdm"`（继续使用 `pdm.lock` 作为 PDM 锁文件）
- 依赖约束保持不变（`black/flake8/isort/mypy/pre-commit/pytest` 均为固定版本）。
- 已保留并可用：
  - `project.optional-dependencies.dev`
  - `dependency-groups.dev`
  - `tool.pdm` / `tool.uv` / `tool.uv.workspace`
- 锁文件已存在并可用于复现：
  - `pdm.lock`
  - `uv.lock`

## 3. 环境准备

在仓库根目录执行：

```bash
cd /media/pc/data/ai/server/daoApps/py313-monorepo-starter
python --version
pdm --version
uv --version
```

如果 `uv` 命令不可用，可回退为：

```bash
python -m pip install -U uv
python -m uv --version
```

## 4. 升级与锁文件流程

### 4.1 校验可编辑安装（PEP 517/660）

```bash
python -m pip install --dry-run -e '.[dev]'
```

通过标准：退出码 `0`，并出现 `Preparing editable metadata (pyproject.toml) ... done`。

### 4.2 刷新 PDM 锁文件

```bash
pdm lock -G dev
```

### 4.3 刷新 uv 锁文件

```bash
python -m uv lock
```

### 4.4 同步安装验证（可选，二选一或都执行）

```bash
pdm sync -G dev --clean
uv sync --frozen
```

## 5. 验证步骤

```bash
python -m black --check src tests
python -m isort --check-only src tests
python -m flake8 src tests
python -m mypy --config-file pyproject.toml
python -m pytest -q
```

通过标准：所有命令退出码 `0`。

## 6. 回滚建议

出现不可接受故障（如构建失败、CI 大面积安装失败）时：

1. 回滚 `pyproject.toml` 的 `[build-system]` 到上一版本。
2. 回滚与锁文件相关提交（`pdm.lock`、`uv.lock`）。
3. 复跑第 5 节回归命令，确认恢复。
4. 在 `docs/EVIDENCE_LOG.md` 补充故障根因与回滚记录。

## 7. 交付清单

- `pyproject.toml`（已切换为 `pdm-backend`）
- `pdm.lock`
- `uv.lock`
- `docs/PDM_UV_WORKSPACE_UPGRADE_GUIDE.md`
- `docs/CI_CACHE_STRATEGY.md`
- `docs/REGRESSION_TEST_REPORT_20260414.md`
