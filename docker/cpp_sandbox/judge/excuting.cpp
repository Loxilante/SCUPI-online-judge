#include <iostream>
#include <string>
#include <chrono>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/resource.h>
#include <signal.h>
#include <fcntl.h>
#include <fstream>
#include <sstream>
#include <vector>
#include <cstdlib>

struct RunResult {
    int status;         // 运行结束状态
    long time;          // 运行时间（毫秒）
    long maxMemory;     // 最大内存使用（KB）
    std::string output; // 输出或报错
};

long getMemoryUsage(pid_t pid) {
    std::string statmPath = "/proc/" + std::to_string(pid) + "/statm";
    std::ifstream statmFile(statmPath);
    if (!statmFile.is_open()) {
        return -1; // 无法打开文件
    }

    long size, resident;
    statmFile >> size >> resident; // 读取总的程序大小和常驻集大小
    statmFile.close();

    // 这里的单位是页面大小，需要转换为KB
    long pageSizeKB = sysconf(_SC_PAGE_SIZE) / 1024; // 获取系统页面大小（以KB为单位）
    long residentSet = resident * pageSizeKB; // 将常驻集大小转换为KB

    return residentSet;
}

RunResult runExe(const std::string& path, const std::string& args, const std::string& input, int maxTime, int maxMemory) {
    RunResult result;
    // 初始化结果
    result.status = 0;
    result.time = 0;
    result.maxMemory = 0;
    result.output = "";

    // 创建管道用于捕获输出和输入
    int outpipefd[2], inpipefd[2];
    pipe(outpipefd); // 用于捕获输出
    pipe(inpipefd);  // 用于发送输入

    // 记录开始时间
    auto startTime = std::chrono::high_resolution_clock::now();

    // 创建子进程运行.exe文件
    pid_t pid = fork();
    if (pid == 0) {
        // 子进程
        dup2(outpipefd[1], STDOUT_FILENO);  // 重定向stdout
        dup2(outpipefd[1], STDERR_FILENO);  // 重定向stderr
        close(outpipefd[0]);               // 关闭读管道

        dup2(inpipefd[0], STDIN_FILENO);    // 重定向stdin
        close(inpipefd[1]);                // 关闭写管道

        // 分割命令行参数
        std::istringstream iss(args);
        std::vector<std::string> tokens;
        std::string token;
        tokens.push_back(path); // 将程序路径作为第一个参数
        while (iss >> token) {
            tokens.push_back(token);
        }

        // 创建参数数组，包括程序路径和所有参数，以nullptr结尾
        std::vector<char*> c_args;
        for (const auto& arg : tokens) {
            c_args.push_back(const_cast<char*>(arg.c_str()));
        }
        c_args.push_back(nullptr); // execvp要求以nullptr结尾

        // 运行程序
        execvp(path.c_str(), c_args.data());
        exit(0);
    } else {
        // 父进程
        close(outpipefd[1]);  // 关闭输出写管道
        close(inpipefd[0]);   // 关闭输入读管道

        // 写入输入数据
        write(inpipefd[1], input.c_str(), input.size());
        close(inpipefd[1]);   // 关闭输入写管道，发送EOF

        // 监控子进程
        int status;
        //struct rusage usage;
        bool killed = false;
        while (true) {
            // 检查进程是否结束
            if (waitpid(pid, &status, WNOHANG) != 0) {
                if (WIFEXITED(status)) {
                    result.status = WEXITSTATUS(status);
                } else if (WIFSIGNALED(status)) {
                    result.status = -1;
                    result.output = "子进程异常终止";
                }
                break;
            }

            // 检查运行时间
            auto currentTime = std::chrono::high_resolution_clock::now();
            auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(currentTime - startTime).count();
            if (duration > maxTime) {
                kill(pid, SIGKILL);
                killed = true;
                result.status = -1; // 运行时间超限
                result.output = "运行时间超过最大限制";
                break;
            }

            // 检查内存使用
            long memoryUsage = getMemoryUsage(pid);
            if (memoryUsage > result.maxMemory) {
                result.maxMemory = memoryUsage; // 记录最大内存使用量
}
            if (memoryUsage > maxMemory) {
                kill(pid, SIGKILL);
                killed = true;
                result.status = -1; // 内存使用超限
                result.output = "内存使用超过最大限制";
                break;
                }

            usleep(50000); // 每50ms检查一次
        }

        if (!killed) {
            // 读取输出
            char buffer[256];
            ssize_t bytes_read;
            while ((bytes_read = read(outpipefd[0], buffer, sizeof(buffer) - 1)) != 0) {
                if (bytes_read == -1) {
                    if (errno == EINTR) {
                        continue;
                    } else {
                        perror("read");
                        break;
                    }
                }
                buffer[bytes_read] = '\0';
                result.output += buffer;
            }
        }

        // 设置返回结果
        result.time = std::chrono::duration_cast<std::chrono::milliseconds>(
            std::chrono::high_resolution_clock::now() - startTime
        ).count();
    }

    return result;
}

int main(int argc, char *argv[]) {
    // 示例：运行一个程序
    RunResult result = runExe(argv[1], argv[2], argv[3], std::atoi(argv[4]), std::atoi(argv[5]));

    // 输出结果
    std::cout << "<-&" << result.status << "&->";
    std::cout << "<-&" << result.time << " ms"  "&->";
    std::cout << "<-&" << result.maxMemory << " KB" <<  "&->";
    std::cout << "<-&" << result.output <<  "&->";

    return 0;
}
