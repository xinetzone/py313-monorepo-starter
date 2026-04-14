# py313-monorepo-starter

一个面向 Python 3.13+ 的 Monorepo 启动模板仓库，内置基础目录规范、代码质量门禁、测试骨架与 GitHub Actions CI，开箱即可进入迭代开发。

## 项目目标

- 提供统一的 Python 3.13 工程脚手架，降低新项目冷启动成本。
- 通过 `black`、`isort`、`flake8`、`mypy`、`pytest` 建立稳定质量基线。
- 保证本地检查与 CI 检查命令一致，减少“本地通过但 CI 失败”。
- 提供容器化基础能力（`Dockerfile` + `docker-compose.yml`），便于标准化运行。
- 提供可追溯证据链模板（`docs/EVIDENCE_LOG.md`），用于记录 CI/容器受限场景下的替代证明。

## Python 版本要求

- 运行时与开发工具统一要求：`Python >= 3.13`。
- `pyproject.toml` 中已固定 `requires-python = ">=3.13"`，并将 `black/isort/mypy` 目标设为 3.13。
- 建议先确认版本：

```bash
python3.13 --version
```

## 安装步骤

1. 创建并激活虚拟环境。
2. 安装依赖（含开发质量工具）。
3. 安装并启用 pre-commit 钩子。

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e '.[dev]'
pre-commit install
```

可选：首次执行一次全量钩子检查，确保环境完整：

```bash
pre-commit run --all-files
```

## 开发指南

### 目录结构

```text
py313-monorepo-starter/
├── .github/workflows/     # CI 配置
├── docs/                  # 规范与设计文档
├── scripts/               # 脚本与工具说明
├── src/                   # 业务源码
├── tests/                 # pytest 测试
├── .gitignore
├── pyproject.toml
└── Dockerfile
```

### 日常开发命令

```bash
# Lint（只检查，不改写）
python -m black --check src tests
python -m isort --check-only src tests
python -m flake8 src tests

# 类型检查
python -m mypy --config-file pyproject.toml

# 单元测试
python -m pytest -q
```

### 本地与 CI 对齐的一键验证

```bash
python -m pip install -U pip
python -m pip install -e '.[dev]'
python -m black --check src tests
python -m isort --check-only src tests
python -m flake8 src tests
python -m mypy --config-file pyproject.toml
python -m pytest -q
```

## 贡献流程

1. 从 `main` 拉取最新代码并创建特性分支。
2. 在本地完成开发与测试，确保质量门禁全部通过。
3. 提交前运行 `pre-commit run --all-files`。
4. 发起 Pull Request，等待 GitHub Actions 通过后合并。

建议分支命名示例：`feat/<topic>`、`fix/<topic>`、`chore/<topic>`。

PR 提交时请填写 `.github/pull_request_template.md` 中的 CI 证据字段：
- 优先填写 GitHub Actions Run URL；
- 若环境受限，必须附 `docs/EVIDENCE_LOG.md` 中对应条目。

## 容器一键启动（Docker / Podman）

### Docker Compose

```bash
docker compose up -d --build
docker compose ps
curl http://localhost:8000
docker compose down
```

### Podman Compose

```bash
podman-compose up -d --build
podman ps
curl http://localhost:8000
podman-compose down
```

### 常见问题排查

- `permission denied /var/run/docker.sock`：
  - 将当前用户加入 `docker` 组并重新登录；
  - 或在具备权限的 CI Runner / 开发机执行。
- `podman-compose: command not found`：
  - 安装 `podman-compose`；
  - 或改用 `docker compose`。
- `podman` 报用户运行时目录只读：
  - 检查 `/run/user/<uid>` 是否可写；
  - 在本机完整用户会话中执行，而非受限沙箱。

## 验证步骤

### 本地验证（Local）

```bash
source .venv/bin/activate
python -m black --check src tests
python -m isort --check-only src tests
python -m flake8 src tests
python -m mypy --config-file pyproject.toml
python -m pytest -q
```

验收标准：
- 所有命令退出码为 `0`。
- 无 lint 报错、无 mypy 错误、无 pytest 失败。

### GitHub Actions 验证（GHA）

CI 工作流文件：`.github/workflows/python313-ci.yml`。

触发方式：
- 推送到 `main`。
- 对 `main` 发起 Pull Request。

校验内容：
- 安装依赖；
- `black --check`、`isort --check-only`、`flake8`；
- `mypy`；
- `pytest`。

验收标准：
- `lint-type-test` 任务状态为 `success`。
- 工作流日志中无失败步骤。
- PR 模板中的 CI Run URL 已填写；若无法填写，须提供 `docs/EVIDENCE_LOG.md` 替代证据条目。
