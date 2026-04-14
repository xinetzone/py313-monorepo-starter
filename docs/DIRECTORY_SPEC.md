# Directory Specification

## 目标

明确仓库目录职责、边界与评审规范，避免“代码放错层”“文档与实现脱节”。

## 分层原则

- `src/`: 生产代码，仅放可复用的业务/库逻辑。
- `tests/`: 测试代码，仅包含针对 `src/` 的单元/集成测试。
- `docs/`: 设计与规范文档，记录策略、流程、证据，不放可执行业务逻辑。
- `.github/workflows/`: CI 工作流定义，描述自动化校验流程。
- `scripts/`: 辅助脚本与脚本说明，不承载核心业务实现。

## 当前仓库结构对照

- `src/core.py`: 核心示例模块，符合“业务代码位于 `src/`”要求。
- `tests/test_core.py`: pytest 用例，符合“测试与实现分离”要求。
- `docs/BRANCH_STRATEGY.md`: 分支与发布策略文档。
- `docs/CI_CD_SPEC.md`: CI/CD 规范与失败处理文档。
- `docs/DIRECTORY_SPEC.md`: 当前目录规范文档。
- `.github/workflows/python313-ci.yml`: Python 3.13 质量门禁工作流。
- `Dockerfile` + `docker-compose.yml`: 容器化运行定义，位于仓库根目录便于发现。

## 命名与边界规则

- Python 包与模块名使用小写下划线风格。
- 测试文件命名使用 `test_*.py`。
- 文档文件使用大写蛇形或语义清晰命名（如 `CI_CD_SPEC.md`）。
- 禁止在 `tests/` 中复制生产逻辑实现；测试应引用 `src/`。
- 禁止将 CI 门禁逻辑散落到多个位置；以 `.github/workflows/` 与 `README.md` 为单一事实来源。

## 变更评审清单

- 涉及 `src/` 变更时：
  - 是否有对应 `tests/` 覆盖更新；
  - 是否通过 `black/isort/flake8/mypy/pytest`。
- 涉及 CI 变更时：
  - `README.md` 与 `docs/CI_CD_SPEC.md` 是否同步更新；
  - 是否评估了分支保护规则的影响。
- 涉及容器变更时：
  - `Dockerfile` 与 `docker-compose.yml` 是否保持一致；
  - 是否补充可追溯运行证据（见 `docs/EVIDENCE_LOG.md`）。
- 涉及文档变更时：
  - 是否具备可执行细节而非占位描述；
  - 是否与仓库当前实现逐项对照。
