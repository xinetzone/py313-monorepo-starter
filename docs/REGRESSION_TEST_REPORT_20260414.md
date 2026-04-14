# 回归测试报告（Task4-6）

## 1. 执行信息

- 时间：2026-04-14
- 目录：`/media/pc/data/ai/server/daoApps/py313-monorepo-starter`
- 目标：验证 `pyproject.toml` 切换到 `pdm-backend` 后的质量门禁与测试结果

## 2. 执行命令与结果

| 序号 | 命令 | 退出码 | 结果摘要 |
|---|---|---:|---|
| 1 | `python -m pip install --dry-run -e '.[dev]'` | 0 | editable 元数据构建成功，依赖解析正常 |
| 2 | `python -m black --check src tests` | 0 | `4 files would be left unchanged.` |
| 3 | `python -m isort --check-only src tests` | 0 | 无输出，检查通过 |
| 4 | `python -m flake8 src tests` | 0 | 无输出，检查通过 |
| 5 | `python -m mypy --config-file pyproject.toml` | 0 | `Success: no issues found in 4 source files` |
| 6 | `python -m pytest -q` | 0 | `11 passed in 0.02s` |

## 3. 失败项

- 无失败项。

## 4. 结论

- 本次回归全部通过。
- `pdm-backend` 构建后端切换未引入 lint/type/test 回归。
- 当前版本可进入下一步 CI 联调或发布候选验证。

## 5. 风险说明

- 由于当前报告基于本地环境执行，远端 CI 仍需按同构命令再验证一次。
- 若后续调整依赖版本，需同步刷新 `pdm.lock` 与 `uv.lock` 并复跑本报告命令。
