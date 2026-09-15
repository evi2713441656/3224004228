# 第一次个人编程作业：论文查重

> GitHub 链接：[https://github.com/evi2713441656/3224004228](https://github.com/evi2713441656/3224004228)
>
> 学号：3224004228　姓名：陈嫒琳

## 运行环境

- Python 3.9 或更高版本
- 仅使用标准库，无需联网安装依赖

## 运行方式

```text
python main.py <原文绝对路径> <抄袭版论文绝对路径> <答案绝对路径>
```

例如：

```text
python main.py C:\\tests\\orig.txt C:\\tests\\orig_add.txt C:\\tests\\ans.txt
```

答案文件写入一个保留两位小数的浮点数，例如 `0.86`。

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

本项目包含 14 个单元测试，覆盖文本预处理、N-gram 统计、余弦计算、文件读写、BOM、空文件、缺失文件和非法参数等路径。

## 提交前检查

1. 将当前文件夹 `student_id` 改为个人学号。
2. 将 README 首行替换为真实 GitHub 仓库链接。
3. 按 PSP 表格填写实际耗时，并把测试输出/性能图放入博客。
4. 提交前运行 `python -m unittest discover -s tests -v`。
