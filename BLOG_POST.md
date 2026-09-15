作业GitHub链接：[https://github.com/evi2713441656/3224004228](https://github.com/evi2713441656/3224004228)

# 第一次个人编程作业：论文查重

学号：3224004228  
姓名：陈嫒琳  
课程：软件工程  
班级：计科24级78班  
作业要求：[第一次个人编程作业](https://edu.cnblogs.com/campus/gdgy/Class78-Grade2024-CS/homework/15702)

## 一、项目介绍

本次作业要求实现一个论文查重程序。程序从命令行接收原文绝对路径、抄袭版论文绝对路径和答案文件绝对路径，在答案文件中输出保留两位小数的重复率。

项目使用 Python 3 实现，入口文件为 `main.py`，运行时只使用 Python 标准库，不需要联网或安装第三方依赖。

运行方式：

```text
python main.py <原文绝对路径> <抄袭版论文绝对路径> <答案绝对路径>
```

例如：

```text
python main.py C:\\tests\\orig.txt C:\\tests\\orig_add.txt C:\\tests\\answer.txt
```

## 二、PSP 表格

开发前先对各阶段进行预估，开发完成后补充实际耗时。实际耗时应以自己的过程记录为准。

| PSP 阶段 | 工作内容 | 预估耗时（分钟） | 实际耗时（分钟） |
|---|---|---:|---:|
| Planning | 计划与任务拆分 | 20 | 10 |
| Analysis | 需求分析、算法约定确认 | 45 | 35 |
| Design Spec | 设计文档 | 30 | 25 |
| Design Review | 设计复审 | 15 | 10 |
| Coding Standard | Python 代码规范 | 15 | 10 |
| Design | 模块和接口设计 | 30 | 25 |
| Coding | 编写程序 | 120 | 90 |
| Code Review | 代码复审 | 30 | 20 |
| Test | 单元测试和回归测试 | 75 | 55 |
| Test Report | 测试报告 | 20 | 15 |
| Size Measurement | 工作量统计 | 10 | 5 |
| Postmortem | 事后总结与改进计划 | 20 | 15 |
| **合计** |  | **430** | **315** |

## 三、计算模块接口的设计与实现

### 3.1 代码组织

```text
3224004228/
├── main.py                    # 老师评测入口，严格按原始文件内容计算
├── main_clean.py              # 可选 HTML 正文检查入口
├── plagiarism_checker.py      # 核心算法和异常类
├── github_html_reader.py      # 可选的 GitHub 网页正文提取器
├── tests/
│   └── test_plagiarism_checker.py
├── requirements.txt
├── profile_benchmark.py
├── PSP.md
├── DESIGN.md
├── PROFILING.md
└── COVERAGE.md
```

核心接口如下：

| 函数 | 作用 |
|---|---|
| `normalize_text` | 删除空白字符，保留中文、英文、数字和标点 |
| `build_ngram_frequency` | 使用滑动窗口构造字符级 3-gram 词频向量 |
| `cosine_similarity` | 计算两个稀疏词频向量的余弦相似度 |
| `calculate_similarity` | 完成文本预处理和相似度计算 |
| `calculate_similarity_from_files` | 读取两个 UTF-8 文件后计算相似度 |

### 3.2 算法原理

程序采用字符级 3-gram 和余弦相似度。

例如文本 `今天是星期天` 会被划分为：

```text
今天是、天是星、是星期、星期天
```

统计两个文本中每个 3-gram 的出现次数后，将其看作两个向量：

```text
similarity = dot(A, B) / (norm(A) * norm(B))
```

最终结果范围为 `[0, 1]`，并在写入答案文件时格式化为两位小数。完全相同的非空文本直接返回 `1.00`，不同且没有公共 3-gram 的短文本返回 `0.00`。

### 3.3 主流程

![程序流程图](https://raw.githubusercontent.com/evi2713441656/3224004228/main/flowchart.svg)

处理流程如下：

1. 检查命令行参数数量和内容。
2. 以 UTF-8 读取原文和抄袭版文件。
3. 删除空白字符。
4. 生成字符级 3-gram 词频向量。
5. 计算余弦相似度。
6. 将结果以两位小数写入答案文件。

设两个文本去除空白后的长度为 `n` 和 `m`，N-gram 统计时间复杂度为 `O(n + m)`，空间复杂度为 `O(n + m)`。

## 四、性能分析与改进

使用 Python 标准库 `cProfile` 对基准文本进行性能分析。基准文本原文和抄袭版各约 190,000 个字符，运行结果为约 0.107 秒、408,841 次函数调用。

累计耗时最高的自有函数是 `build_ngram_frequency`，两次调用累计约 0.092 秒，说明主要耗时在构造 N-gram 词频，而不是余弦点积。

优化前的思路是在计算点积时先构造两个向量键的并集；优化后只遍历第一个稀疏向量，并通过 `second.get(key, 0)` 查询另一个向量的频次，避免额外创建并集对象。

![性能分析图](https://raw.githubusercontent.com/evi2713441656/3224004228/main/profiling.svg)

性能分析复现命令：

```text
python -m cProfile -s cumulative profile_benchmark.py
```

## 五、单元测试

项目使用 Python `unittest` 编写了 20 个测试用例，覆盖：

- 空白字符处理；
- 标点保留；
- 重叠 N-gram 统计；
- 文本短于 3 个字符；
- 完全相同文本；
- 部分相同文本；
- 完全不同文本；
- UTF-8 BOM；
- 空文件；
- 文件不存在；
- 非法参数；
- 原始入口和 HTML 检查入口。

运行测试：

```text
python -m unittest discover -s tests -v
```

部分测试代码：

```python
def test_identical_documents_are_one(self) -> None:
    self.assertAlmostEqual(calculate_similarity("abcdef", "abcdef"), 1.0)

def test_empty_original_is_rejected(self) -> None:
    with self.assertRaises(EmptyDocumentError):
        calculate_similarity(" \n", "abcdef")

def test_partial_overlap_is_between_zero_and_one(self) -> None:
    result = calculate_similarity("abcdefghi", "abcdefxyz")
    self.assertGreater(result, 0.0)
    self.assertLess(result, 1.0)
```

测试覆盖率使用 Python `trace` 统计：

| 文件 | 覆盖率 |
|---|---:|
| `main.py` | 81.0% |
| `main_clean.py` | 65.2% |
| `github_html_reader.py` | 100.0% |
| `plagiarism_checker.py` | 87.3% |
| `tests/test_plagiarism_checker.py` | 99.0% |

![测试覆盖率图](https://raw.githubusercontent.com/evi2713441656/3224004228/main/coverage.svg)

## 六、测试文本核对

老师提供的压缩包中，`orig.txt` 和 `orig_0.8_add.txt` 是正常文本；其余 4 个 `.txt` 文件实际是 GitHub 网页 HTML，网页标题指向 `qizong007/111800827` 的文件页面。

因此本项目保留两个入口：

- `main.py`：严格把输入文件原样作为文本处理，不删除 HTML，提交老师评测时使用；
- `main_clean.py`：只用于本地检查误下载的 GitHub HTML 页面，不修改原始测试文件。

从 HTML 页面中提取正文后运行得到：

| 测试文本 | 输出 |
|---|---:|
| `orig_0.8_add.txt` | `0.70` |
| `orig_0.8_del.txt` | `0.71` |
| `orig_0.8_dis_1.txt` | `0.93` |
| `orig_0.8_dis_10.txt` | `0.76` |
| `orig_0.8_dis_15.txt` | `0.41` |

## 七、异常处理

### 7.1 `ArgumentError`

用于处理非法文本类型、非法 N-gram 大小和非法路径类型，避免函数在错误输入下产生难以理解的异常。

测试场景：传入 `ngram_size=0`，程序抛出 `ArgumentError`。

### 7.2 `FileOperationError`

用于处理文件不存在、没有读取权限或文件编码错误，将底层异常转换成清晰的错误信息。

测试场景：读取不存在的 `missing.txt`，程序抛出 `FileOperationError`。

### 7.3 `EmptyDocumentError`

用于处理文件为空或只含空白字符的情况，避免对无意义的零向量计算相似度。

测试场景：原文内容只有空格和换行时，程序抛出 `EmptyDocumentError`。

命令行入口会捕获这些异常并返回非 0 状态码，不会出现未处理异常退出。

## 八、代码质量与 Git 管理

使用 Ruff 进行静态代码检查和格式检查：

```text
ruff check main.py main_clean.py plagiarism_checker.py github_html_reader.py tests profile_benchmark.py
All checks passed!

ruff format --check main.py main_clean.py plagiarism_checker.py github_html_reader.py tests profile_benchmark.py
7 files already formatted
```

同时使用 `python -m compileall -q .` 检查语法，检查通过。

Git 提交记录按照功能划分：

1. `feat: implement paper plagiarism checker`
2. `test: add tests and submission documentation`
3. `chore: ignore generated coverage reports`
4. `docs: complete submission audit and diagrams`
5. `perf: record final profiling benchmark`
6. `feat: add explicit raw and html-aware entry points`

## 九、总结与改进计划

通过这次作业，我完成了从需求分析、算法设计、编码、测试、性能分析到 GitHub 管理的完整流程。最初容易把“文本相似度”和“简单字符串匹配”混为一谈，实际实现后认识到，使用 N-gram 统计和余弦相似度可以同时处理中文文本中的增删改。

本次实现仍有改进空间：第一，可以把 N-gram 长度做成命令行可配置参数；第二，可以增加中文分词或 SimHash 算法进行对比；第三，可以使用更大规模真实论文建立基准数据，进一步分析准确率和内存占用。

## 十、提交说明

代码仓库已经发布到 GitHub：[https://github.com/evi2713441656/3224004228](https://github.com/evi2713441656/3224004228)。博客发布前检查以下事项：

1. 确认本文第一行仍然是 GitHub 链接；
2. 检查姓名、学号和班级信息；
3. 将性能分析图和覆盖率图显示正常；
4. 根据自己的真实开发记录校正 PSP 实际耗时；
5. 使用 `main.py` 作为老师评测入口；
6. 在博客园作业页面提交博客文章链接。
