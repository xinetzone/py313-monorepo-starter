# py313-monorepo-starter 依赖迁移 Runbook

## 0. 目标与结论摘要

- 目标：评估并推进从 `requirements.txt` 到 `pyproject.toml`（SSOT，单一依赖源）的迁移。
- 结论：当前项目 **不存在实质依赖冲突**，但存在 CI/CD、容器构建、文档入口对 `requirements.txt` 的直接依赖，建议采用 **分阶段迁移**（并行期 -> 切换期 -> 清理期）。
- 实施建议：先完成安装入口统一与锁定策略落地，再移除 `requirements.txt`。

---

## 1. Task 1：依赖基线与差异审计

### 1.1 审计对象

- `requirements.txt`
- `pyproject.toml`

### 1.2 差异审计结果

审计命令（2026-04-14）：

```bash
python - <<'PY'
import tomllib
from pathlib import Path

req=[]
for line in Path('requirements.txt').read_text().splitlines():
    line=line.strip()
    if not line or line.startswith('#'):
        continue
    req.append(line)

p=tomllib.loads(Path('pyproject.toml').read_text())
py_deps=p['project'].get('dependencies', [])
py_dev=p['project'].get('optional-dependencies',{}).get('dev',[])

req_names={x.split('==')[0].lower():x for x in req}
dev_names={x.split('==')[0].lower():x for x in py_dev}

common=sorted(set(req_names)&set(dev_names))
req_only=sorted(set(req_names)-set(dev_names))
dev_only=sorted(set(dev_names)-set(req_names))

conflicts=[]
for n in common:
    if req_names[n]!=dev_names[n]:
        conflicts.append((req_names[n],dev_names[n]))

print('requirements_total=',len(req))
print('pyproject_dev_total=',len(py_dev))
print('pyproject_runtime_total=',len(py_deps))
print('common=',[req_names[n] for n in common])
print('req_only=',[req_names[n] for n in req_only])
print('dev_only=',[dev_names[n] for n in dev_only])
print('conflicts=',conflicts)
PY
```

关键输出：

```text
requirements_total= 6
pyproject_dev_total= 6
pyproject_runtime_total= 0
common= ['black==25.1.0', 'flake8==7.1.1', 'isort==8.0.1', 'mypy==1.14.1', 'pre-commit==4.1.0', 'pytest==8.3.4']
req_only= []
dev_only= []
conflicts= []
```

### 1.3 风险分级

- 重复项：6 个（全部版本一致），风险级别 `Low`（冗余维护风险）。
- 冲突项：0 个，风险级别 `Low`。
- 单侧项：0 个，风险级别 `Low`。
- 隐性风险：双源长期并行可能导致后续漂移，风险级别 `Medium`（治理风险）。

### 1.4 结论（是否存在实质冲突）

- 当前不存在“会导致安装结果不一致”的实质冲突。
- 主要问题是“治理层面的双源维护成本和未来漂移风险”，非当前版本冲突。

---

## 2. Task 2：迁移可行性评估（CI/CD、脚本、部署）

### 2.1 对 `requirements.txt` 的直接依赖盘点

盘点命令（2026-04-14）：

```bash
grep -RIn --exclude-dir=.git --exclude-dir=.venv --exclude-dir=.pytest_cache --exclude-dir=.mypy_cache -E 'requirements\.txt|pip install -r requirements\.txt' .
```

命中位置（关键）：

- `.github/workflows/python313-ci.yml`：CI 安装依赖使用 `pip install -r requirements.txt`
- `Dockerfile`：镜像构建 `COPY requirements.txt` 且按文件安装
- `README.md`：开发与 CI 对齐命令使用 `pip install -r requirements.txt`
- `docs/CI_CD_SPEC.md`：明确依赖版本由 `requirements.txt` 固定

### 2.2 完全迁移条件评估

- 工具链：`pip install --dry-run '.[dev]'` 成功，说明以 `pyproject.toml` 作为安装入口是可行的。
- 安装入口：尚未统一，CI/文档/容器均仍指向 `requirements.txt`。
- 锁定机制：未见 lock 文件或标准导出流程（可重现性治理尚未完成）。
- 结论：具备迁移基础，但未达到“可直接一键移除 requirements.txt”的成熟度。

### 2.3 迁移判定

- 判定：`需分阶段迁移`（不建议直接删除）。
- 原因：影响面集中在 CI、容器、文档与团队流程，需要兼容窗口避免中断。

---

## 3. Task 3：迁移与兼容方案设计

## 3.1 分阶段迁移步骤

### 阶段 A：并行期（建议 1-2 天）

目标：建立新入口，不破坏旧流程。

1. 保留 `requirements.txt`，将其定位为兼容产物（不再人工编辑）。
2. 新增统一安装入口并在文档中给出：
   - 开发依赖：`python -m pip install -e '.[dev]'`
   - 运行依赖：`python -m pip install -e .`
3. 在 CI 增加一条“新入口验证”步骤（先不替换主路径）。
4. 建立 lock/导出机制（见 3.3），生成并纳入版本管理。

### 阶段 B：切换期（建议 1 天）

目标：将主链路切换至 `pyproject.toml`。

1. CI `Install dependencies` 改为：`python -m pip install -e '.[dev]'`。
2. Dockerfile 改为以 `pyproject.toml` 为主安装入口（可选支持 `--build-arg INSTALL_DEV=1`）。
3. README/CI 规范文档同步更新安装命令。
4. `requirements.txt` 仅保留“自动导出兼容文件”角色（文件头注明“自动生成，不手改”）。

### 阶段 C：清理期（建议 1 天）

目标：完成治理收口。

1. 移除所有“手工维护 requirements.txt”的表述。
2. 若确认无外部消费者依赖 `requirements.txt`，可删除该文件或只保留锁文件。
3. 在 PR 模板与评审清单中加入依赖变更检查项。

## 3.2 兼容性验证矩阵

| 维度 | 验证命令 | 通过标准 | 失败定位 |
|---|---|---|---|
| 本地开发 | `pip install -e '.[dev]'` + black/isort/flake8/mypy/pytest | 全部退出码 0 | `pyproject.toml` extras、工具版本 |
| CI | 工作流安装步骤改为 `pip install -e '.[dev]'` | `lint-type-test=success` | workflow 安装步骤、缓存 |
| 容器构建 | `docker build .`（或 compose build） | 镜像构建成功、工具可运行 | Dockerfile COPY/安装入口 |
| 部署脚本 | 部署脚本改为统一安装入口 | 部署流程可复现 | 部署环境 pip 版本、网络镜像 |

## 3.3 锁定与可重现性策略

- 主声明：`pyproject.toml`
- 锁定建议（二选一，建议统一）：
  - `pip-tools`：`pip-compile pyproject.toml --extra dev -o requirements-dev.lock`
  - `uv`：`uv pip compile pyproject.toml --extra dev -o requirements-dev.lock`
- 安装策略：
  - 开发环境优先：`pip install -e '.[dev]'`
  - CI/容器可选强一致：`pip install -r requirements-dev.lock`
- 治理规则：禁止手改导出锁文件，必须通过导出命令更新并在 PR 说明。

---

## 4. Task 4：回滚与协作机制

## 4.1 回滚触发条件

满足任一条件立即触发回滚：

- 连续两次 CI 因依赖安装失败；
- 容器构建失败且 30 分钟内无法修复；
- 开发者普遍出现安装失败（>30% 反馈）。

## 4.2 回滚步骤（RTO 目标：30 分钟）

1. 回滚 CI 安装命令到 `pip install -r requirements.txt`。
2. 回滚 Dockerfile 到 `requirements.txt` 安装路径。
3. 回滚 README/CI 规范到旧入口，发布“迁移暂停”通知。
4. 执行最小回归：lint + mypy + pytest。
5. 在 Issue/变更记录中标注根因与二次迁移前置条件。

## 4.3 协作指南

- 分支策略：迁移期间使用 `chore/deps-ssot-migration` 主分支，子任务 PR 小步合并。
- 评审要点：只允许一个依赖源被人工维护；安装命令是否统一；文档是否同步。
- 沟通机制：每日同步一次迁移状态（风险、阻塞、决策）；关键变更提前公告迁移窗口。

---

## 5. Task 5：最终评估与执行清单

## 5.1 必要性结论

- 建议：`requirements.txt` 由“主依赖源”转为“过渡兼容产物”，最终视外部依赖方情况移除。
- 迁移模式：`分阶段迁移`（推荐），不建议一步到位删除。

## 5.2 影响范围与实施顺序

- 影响范围：
  - CI：`.github/workflows/python313-ci.yml`
  - 容器：`Dockerfile`
  - 文档：`README.md`、`docs/CI_CD_SPEC.md`
  - 依赖文件：`pyproject.toml`、`requirements.txt`（及未来 lock 文件）
- 实施顺序（建议）：
  1. 先落锁定方案；
  2. 再切 CI；
  3. 再切容器；
  4. 最后清理文档与兼容文件策略。

## 5.3 负责人建议（RACI 轻量版）

- DRI（主责）：仓库维护者/DevEx 负责人（1 人）
- Reviewer：CI 维护者（1 人）+ 运行环境维护者（1 人）
- Consulted：应用开发代表（1 人）
- Informed：全体贡献者（通过 README/PR 模板公告）

---

## 6. 证据清单（本次评估）

- 依赖差异审计命令与输出：本文件“1.2 差异审计结果”。
- `pip install --dry-run '.[dev]'` 可行性验证：确认 pyproject extras 安装可用。
- `requirements.txt` 引用面盘点：确认 CI、容器、文档存在直接依赖。

建议在实施阶段将每一步执行结果追加到 `docs/EVIDENCE_LOG.md`。

---

## 7. Task 6-9 执行记录（2026-04-14）

### 7.1 Task 6：`requirements.txt` 完整移除

- 已执行引用审计并保留证据。
- 已备份 `requirements.txt` 到 `docs/backups/requirements.txt.bak.20260414_133050`。
- 已删除仓库根目录 `requirements.txt`。

### 7.2 Task 7：CI / Docker / README / 文档联动更新

- CI：`.github/workflows/python313-ci.yml` 安装命令改为 `python -m pip install -e '.[dev]'`。
- Docker：`Dockerfile` 移除 `requirements.txt` 拷贝与安装逻辑，改为 `python -m pip install --no-cache-dir -e '.[dev]'`。
- README：安装与本地 CI 对齐命令改为 `python -m pip install -e '.[dev]'`，目录结构移除 `requirements.txt`。
- CI 规范：`docs/CI_CD_SPEC.md` 更新为 `pyproject.toml` 单一依赖源。

### 7.3 Task 8：清理与回归验证

- 清理 `.pytest_cache`、`.mypy_cache`、`__pycache__`。
- 执行并通过：
  - `python -m black --check src tests`
  - `python -m isort --check-only src tests`
  - `python -m flake8 src tests`
  - `python -m mypy --config-file pyproject.toml`
  - `python -m pytest -q`

### 7.4 Task 9：提交与推送尝试

- 已提交迁移收口改动。
- 已执行 `git push` 尝试；当前仓库未配置远端，推送被阻塞（详见 `docs/EVIDENCE_LOG.md`）。
