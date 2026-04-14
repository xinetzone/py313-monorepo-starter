## 变更说明

- 变更类型：`feat` / `fix` / `docs` / `chore` / `refactor` / `test`
- 主要改动：
- 风险与回滚方案：

## 本地验证

- [ ] `python -m black --check src tests`
- [ ] `python -m isort --check-only src tests`
- [ ] `python -m flake8 src tests`
- [ ] `python -m mypy --config-file pyproject.toml`
- [ ] `python -m pytest -q`

## CI 证据（必填）

- GitHub Actions Run URL（必填其一）：
  - [ ] 已填写 Run URL：`<粘贴链接>`
  - [ ] 受环境限制无法提供 Run URL，已在 `docs/EVIDENCE_LOG.md` 记录替代证据条目：`<条目ID>`

## 容器验证（如本次改动涉及容器）

- [ ] `docker compose up -d --build` + `docker compose ps` + `curl http://localhost:8000`
- [ ] 或 `podman-compose up -d --build` + `podman ps` + `curl http://localhost:8000`
- [ ] 受环境限制时，已在 `docs/EVIDENCE_LOG.md` 记录原始错误与替代证据
