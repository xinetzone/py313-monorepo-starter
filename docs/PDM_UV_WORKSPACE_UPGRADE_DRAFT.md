# PDM + uv Workspace 升级草稿（Task1-3）

## 1. 现状评估（Task1）

评估对象：`pyproject.toml`（2026-04-14）。

结论：

- 现有配置为 PEP 621 + `setuptools` backend，可正常作为单包工程使用。
- 依赖约束集中在 `project.optional-dependencies.dev`，版本均为固定值：
  - `black==25.1.0`
  - `flake8==7.1.1`
  - `isort==8.0.1`
  - `mypy==1.14.1`
  - `pre-commit==4.1.0`
  - `pytest==8.3.4`
- 缺少 PDM/uv 的 workspace 与 lock 约定，仓库此前无 `pdm.lock` / `uv.lock`。

风险判断：

- 依赖版本冲突风险：低（均已固定）。
- 多工具共存风险：中（若无统一 group/workspace 定义，团队安装行为易分叉）。

## 2. 配置改造（Task2）

目标：在 **不改变任何依赖版本约束** 的前提下，新增 `pdm + uv workspace` 兼容配置。

本次改动：

1. 在 `pyproject.toml` 新增 `[dependency-groups].dev`，内容与原 `project.optional-dependencies.dev` 保持一致（版本完全一致）。
2. 新增 `tool.pdm` 与 `tool.pdm.resolution` 基础配置。
3. 新增 `tool.uv` 与 `tool.uv.workspace`：
   - `default-groups = ["dev"]`
   - `members = ["."]`（当前为单成员 workspace，后续可扩展多子包）
4. 保留原 `build-system`（`setuptools`）与原 `project.optional-dependencies`，确保 `pip install -e '.[dev]'` 兼容性不回退。

补充清理：

- `.gitignore` 补充：
  - `.pdm-home/`
  - `__pypackages__/`

## 3. 工具安装、锁定与验证（Task3）

### 3.1 工具可用性

执行：

```bash
python --version
pdm --version
uv --version
```

结果：

- `pdm` 可用。
- 系统 `uv` 命令初次出现 DBus 内部错误；改为在当前 Python 环境升级并使用 `python -m uv` 后可正常运行。

### 3.2 生成锁文件

PDM 锁定：

```bash
mkdir -p .xdg-state .xdg-cache .pdm-home
export XDG_STATE_HOME=$PWD/.xdg-state
export XDG_CACHE_HOME=$PWD/.xdg-cache
export PDM_HOME=$PWD/.pdm-home
export PDM_USE_VENV=0
pdm lock -G dev --python '>=3.13'
```

关键输出：

```text
Changes are written to pdm.lock.
0:00:28 Lock successful.
```

uv 锁定：

```bash
python -m pip install -U uv
python -m uv lock
```

关键输出：

```text
Using CPython 3.13.5 interpreter at: .../envs/py313/bin/python
Resolved 27 packages in 3.73s
```

### 3.3 安装验证

uv 验证（冻结锁文件）：

```bash
python -m uv sync --frozen
```

关键输出（节选）：

```text
Creating virtual environment at: .venv
Installed 26 packages ...
+ black==25.1.0
+ flake8==7.1.1
+ isort==8.0.1
+ mypy==1.14.1
+ pre-commit==4.1.0
+ pytest==8.3.4
```

PDM 验证（本地 PEP 582 模式）：

```bash
mkdir -p .xdg-state .xdg-cache .pdm-home
export XDG_STATE_HOME=$PWD/.xdg-state
export XDG_CACHE_HOME=$PWD/.xdg-cache
export PDM_HOME=$PWD/.pdm-home
export PDM_USE_VENV=0
export PDM_IGNORE_ACTIVE_VENV=1
pdm sync -G dev --clean
```

关键输出：

```text
All packages are synced to date, nothing to do.
0:00:00 All complete! 0/0
```

## 4. 产物清单

- `pyproject.toml`（新增 pdm/uv workspace 兼容段）
- `pdm.lock`（新增）
- `uv.lock`（新增）
- `.gitignore`（新增 PDM 本地目录与 `__pypackages__` 忽略）

## 5. 后续建议（草稿）

- CI 可增加双路径校验：
  - `python -m uv sync --frozen`
  - `pdm sync -G dev --clean`（建议在隔离环境执行）
- 若后续扩为多包 monorepo，仅需在 `tool.uv.workspace.members` 增加子包路径，并将每个子包补齐独立 `pyproject.toml`。
