"""Small deterministic benchmark used to reproduce the profiling notes."""

from plagiarism_checker import calculate_similarity


def main() -> None:
    original = "软件工程课程论文查重算法性能测试文本。" * 10000
    plagiarized = "软件工程课程论文查重算法性能改进测试文本。" * 10000
    calculate_similarity(original, plagiarized)


if __name__ == "__main__":
    main()
