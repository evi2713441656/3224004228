# 代码质量检查记录

使用 Ruff 0.16.7 对所有 Python 源文件执行静态检查和格式检查：

```text
ruff check main.py plagiarism_checker.py tests profile_benchmark.py
All checks passed!

ruff format --check main.py plagiarism_checker.py tests profile_benchmark.py
5 files already formatted
```

同时执行了：

```text
python -m compileall -q .
```

编译检查通过，项目无第三方运行时依赖。
