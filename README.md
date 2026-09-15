# 第一次个人编程作业：论文查重

> GitHub 链接：[https://github.com/evi2713441656/3224004228](https://github.com/evi2713441656/3224004228)
>
> 学号：3224004228　姓名：陈嫒琳

## 运行环境

- Python 3.9 或更高版本
- 仅使用标准库，无需联网安装依赖

## 运行方式（提交评测用）

```text
python main.py <原文绝对路径> <抄袭版论文绝对路径> <答案绝对路径>
```

例如：

```text
python main.py C:\\tests\\orig.txt C:\\tests\\orig_add.txt C:\\tests\\ans.txt
```

答案文件写入一个保留两位小数的浮点数，例如 `0.86`。

`main.py` 是严格原始输入版本：不会识别、删除或替换 HTML 标签，输入文件中的 HTML 会按普通字符参与计算。这是提交老师评测时应使用的入口。

如果本地下载到的是 GitHub 网页而不是纯文本文件，可以使用可选的 `main_clean.py` 检查网页中嵌入的正文：

```text
python main_clean.py <原文绝对路径> <抄袭版绝对路径> <答案绝对路径>
```

该版本只用于本地诊断，不替换 `main.py`，也不会修改原始测试文件。

## 算法约定

程序先删除所有空白字符，再对文本生成重叠的字符级 3-gram，并统计每个 3-gram 的出现次数。两个词频向量的余弦值作为重复率：

```text
similarity = dot(original, plagiarized) /
             (norm(original) * norm(plagiarized))
```

这一实现对中文不依赖分词库，能够保持线性扫描复杂度，适合评测环境。空文档、缺失文件和非法参数会返回错误信息并以非 0 状态码退出。

## 测试

在项目目录执行：

```text
python -m unittest discover -s tests -v
```

本项目包含 20 个单元测试，覆盖文本预处理、N-gram 统计、余弦计算、文件读写、BOM、空文件、缺失文件、非法参数以及两个入口版本等路径。

实际测试压缩包的核对情况见 [TEST_DATA_AUDIT.md](TEST_DATA_AUDIT.md)，完整提交前检查见 [SUBMISSION_AUDIT.md](SUBMISSION_AUDIT.md)。

## 提交前检查

1. 将当前文件夹 `student_id` 改为个人学号。
2. 将 README 首行替换为真实 GitHub 仓库链接。
3. 按 PSP 表格填写实际耗时，并把测试输出/性能图放入博客。
4. 提交前运行 `python -m unittest discover -s tests -v`。
