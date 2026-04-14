# CI 缓存方案（PDM + uv）

## 1. 目标

- 减少 CI 中依赖下载与解析时间。
- 通过锁文件哈希绑定缓存键，避免脏缓存污染。
- 支持 `pip`、`pdm`、`uv` 三类安装入口。

## 2. 缓存对象

- `pip` 下载缓存：由 `actions/setup-python` 的 `cache: pip` 管理。
- `pdm` 缓存目录（示例）：`~/.cache/pdm`。
- `uv` 缓存目录（示例）：`~/.cache/uv`。

## 3. 缓存键策略

- 主键建议包含：
  - OS：`${{ runner.os }}`
  - Python 版本：`${{ matrix.python-version || '3.13' }}`
  - 锁文件哈希：`hashFiles('pdm.lock', 'uv.lock', 'pyproject.toml')`
- 示例主键：
  - `deps-${{ runner.os }}-py313-${{ hashFiles('pdm.lock', 'uv.lock', 'pyproject.toml') }}`

## 4. GitHub Actions 示例

```yaml
- name: Setup Python
  uses: actions/setup-python@v5
  with:
    python-version: "3.13"
    cache: "pip"

- name: Cache pdm and uv
  uses: actions/cache@v4
  with:
    path: |
      ~/.cache/pdm
      ~/.cache/uv
    key: deps-${{ runner.os }}-py313-${{ hashFiles('pdm.lock', 'uv.lock', 'pyproject.toml') }}
    restore-keys: |
      deps-${{ runner.os }}-py313-

- name: Install tools
  run: |
    python -m pip install --upgrade pip
    python -m pip install -U pdm uv

- name: Sync dependencies (preferred)
  run: |
    uv sync --frozen
```

## 5. 推荐实践

- 锁文件变化后自动切换新缓存键，不复用旧缓存。
- 周期性清理过期缓存，避免膨胀。
- 对非锁定安装流程（例如仅 `pip install -e '.[dev]'`）保留回退步骤。
- CI 失败时记录是否命中缓存、命中哪个键，便于排查缓存污染。

## 6. 风险与规避

- 风险：锁文件未更新但依赖声明变更，导致缓存与解析结果不一致。
- 规避：将 `pyproject.toml` 也纳入哈希键；PR 审查强制检查锁文件同步。
