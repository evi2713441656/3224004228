# 作业要求逐项审查

| 作业要求 | 当前状态 | 说明 |
|---|---|---|
| GitHub 中建立学号文件夹 | 已完成本地部分 | 目录为 `3224004228`，推送后位于仓库根目录 |
| PSP 预估与实际耗时 | 已准备 | [PSP.md](PSP.md) 已填写；提交博客前按个人真实耗时校正 |
| Python 3 + requirements.txt | 已完成 | 仅使用标准库，入口文件为 `main.py` |
| 代码质量分析并消除警告 | 已完成 | Ruff check、Ruff format、compileall 均通过 |
| 性能分析与改进 | 已完成 | cProfile 基准脚本、分析说明和 `profiling.svg` 已提供 |
| GitHub 过程管理 | 已完成本地部分 | 已有 3 个提交；推送后可在 GitHub 查看 |
| 至少 10 个单元测试 | 已完成 | 20 个测试全部通过 |
| 覆盖率记录 | 已完成 | `COVERAGE.md`，核心模块覆盖率 87.3% |
| 文件输入输出 | 已完成 | `main.py` 读取原始输入内容，写入指定答案文件；不解析 HTML |
| 输出精确到两位小数 | 已完成 | 使用 `f"{similarity:.2f}"` |
| C++/Java 编译发布 | 不适用 | 本项目使用 Python |
| 博客首行放 GitHub 链接 | 待用户完成 | README 已准备链接，但博客正文需用户发布 |
| 博客中的性能/覆盖率截图 | 待用户完成 | 已提供 SVG 图，可插入博客或截图 |
| 按时提交 | 待用户完成 | 需注意老师的 Deadline 扣分规则 |

## 最终检查命令

```text
python -m unittest discover -s tests -v
ruff check main.py plagiarism_checker.py tests profile_benchmark.py
ruff format --check main.py plagiarism_checker.py tests profile_benchmark.py
python -m compileall -q .
```
