# Workflows

本目录存放 GitHub Actions 工作流定义。

## 当前工作流

- `python313-ci.yml`
  - 触发：`push main`、`pull_request -> main`
  - 任务：`lint-type-test`
  - 检查项：`black`、`isort`、`flake8`、`mypy`、`pytest`

## 证据链要求

- 优先证据：最近一次成功运行的 GitHub Actions Run URL。
- 若当前环境无法获取 Run URL（例如无 `gh`、无仓库权限），请在 `docs/EVIDENCE_LOG.md` 记录：
  - 时间
  - 执行命令
  - 原始错误
  - 替代证据（本地同构门禁结果）
