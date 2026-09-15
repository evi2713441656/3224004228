# PSP2.1 个人软件过程记录

学号：3224004228　姓名：陈嫒琳

以下“预估”应在编码前记录；“实际”在完成后根据个人时间记录填写。表中实际耗时是本次实现过程的记录，提交博客前请按自己的真实记录校正。

| 阶段 | 工作内容 | 预估耗时（分钟） | 实际耗时（分钟） |
|---|---|---:|---:|
| Planning | 计划与任务拆分 | 20 | 10 |
| Development / Analysis | 需求分析、算法约定确认 | 45 | 35 |
| Development / Design Spec | 生成设计文档 | 30 | 25 |
| Development / Design Review | 设计复审 | 15 | 10 |
| Development / Coding Standard | 确定 Python 命名、异常和格式规范 | 15 | 10 |
| Development / Design | 模块与接口设计 | 30 | 25 |
| Development / Coding | 编写核心算法、CLI 和文件接口 | 120 | 90 |
| Development / Code Review | 代码复审与边界检查 | 30 | 20 |
| Development / Test | 编写并运行单元测试 | 75 | 55 |
| Reporting / Test Report | 整理测试报告 | 20 | 15 |
| Reporting / Size Measurement | 统计文件规模 | 10 | 5 |
| Reporting / Postmortem | 事后总结与改进计划 | 20 | 15 |
| **合计** |  | **430** | **315** |

## 事后总结

本次实现将“预处理、向量化、相似度计算、文件编排”拆成独立函数，使单元测试可以直接覆盖计算模块。后续改进方向是增加可配置的 n-gram 大小，并使用更大规模文本进行基准测试。
