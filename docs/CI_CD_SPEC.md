# CI/CD Specification

## 目标

定义 Python 3.13+ 项目的 CI/CD 最小可执行规范，保证本地与远端验证一致，且结果可追溯。

## CI 范围（当前已实现）

工作流文件：`.github/workflows/python313-ci.yml`

- 触发条件：
  - `push` 到 `main`
  - 对 `main` 发起 `pull_request`
- 运行环境：
  - `ubuntu-latest`
  - `python-version: 3.13`
- 任务名称：
  - `lint-type-test`
- 质量门禁步骤（全部必须通过）：
  - `python -m black --check src tests`
  - `python -m isort --check-only src tests`
  - `python -m flake8 src tests`
  - `python -m mypy --config-file pyproject.toml`
  - `python -m pytest -q`

## 本地与 CI 一致性约束

- 本地开发必须执行与 CI 同构命令，命令清单以 `README.md` 为准。
- 变更不得绕过 `lint-type-test`，如需调整门禁，必须同时更新：
  - `README.md`
  - 本文档
  - `.github/workflows/python313-ci.yml`
- 依赖安装入口统一为 `python -m pip install -e '.[dev]'`，以 `pyproject.toml` 作为单一依赖源。

## 失败处理规范

- 任一步骤失败即阻断合并。
- 修复流程：
  1. 在 PR 分支修复；
  2. 本地复跑同构命令；
  3. 推送后等待 CI 重新通过；
  4. 在 PR 中补充失败原因与修复说明。
- 若失败由平台权限/服务故障引发（非代码问题），需在 `docs/EVIDENCE_LOG.md` 记录原始报错与替代证据。

## CD 与发布约束（当前阶段）

- 当前仓库不自动发布制品，CD 处于“手动发布”阶段。
- 发布前置条件：
  - `main` 最新提交 CI 通过；
  - 版本标签符合 `vMAJOR.MINOR.PATCH`；
  - PR 模板中的 CI 运行链接已填写，或提供受限替代证据。
- 后续若引入自动发布工作流，需新增：
  - 发布触发条件；
  - 制品签名与校验；
  - 回滚策略与责任人。

## 证据链要求

- 远端证据（优先）：GitHub Actions Run URL。
- 替代证据（受限场景）：
  - 本地同构门禁命令完整输出；
  - CI 工作流文件存在性与关键步骤对照；
  - 环境受限错误原文（如无 `gh`、无远端凭据、容器权限受限）。
