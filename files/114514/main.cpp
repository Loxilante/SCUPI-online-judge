#include <iostream>
#include <chrono>
#include <thread>
#include <cstring>
#include <string>

int main(int argc, char *argv[]) {
    // 打印命令行参数
    std::cout << "命令行参数如下：" << std::endl;
    for (int i = 0; i < argc; ++i) {
        std::cout << "参数 " << i << ": " << argv[i] << std::endl;
    }

    // 从标准输入读取内容并打印
    std::cout << "\n请输入内容（输入结束后按Ctrl+D（UNIX）或Ctrl+Z（Windows）结束输入）：" << std::endl;
    std::string line;
    while (std::getline(std::cin, line)) {
        std::cout << line << std::endl;
    }

        //定义运行时间和内存占用
    const int runTimeSeconds = 10;          // 运行时间为10秒
    const size_t memoryUsageMB = 100;       // 内存占用为100MB
    const size_t memoryUsageBytes = memoryUsageMB * 1024 * 1024; // 将MB转换为字节

    // 动态分配内存
    char* memoryBlock = new char[memoryUsageBytes];
    
    // 简单使用内存以避免优化
    std::memset(memoryBlock, 0, memoryUsageBytes);

    // 输出开始信息
    std::cout << "程序开始运行，将持续 " << runTimeSeconds << " 秒，占用大约 " << memoryUsageMB << " MB内存。" << std::endl;

    // 运行指定时间
    std::this_thread::sleep_for(std::chrono::seconds(runTimeSeconds));

    // 释放内存
    delete[] memoryBlock;

    // 输出结束信息
    std::cout << "程序运行结束。" << std::endl;

    return 0;
}

