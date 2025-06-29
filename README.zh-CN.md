# SCUPI-ONLINE-JUDGE-SYSTEM

版本号：2.1.3

**[中文更新日志](./CHANGELOG.zh-CN.md)**

---

## 一. 项目描述

### 项目背景

四川大学匹兹堡学院计算机科学与技术专业自2022年成立以来尚未拥有适合计算机科学专业课程使用的OJ系统，虽然绝大多数课程选择使用Black board 作为作业的线上提交门户，但Black board总体上是为传统文字作业所设计的 ，对于计算机编程类作业的支持并不理想。特别是在算法和数据结构、编程语言学习、计算机系统基础等课程中，学生需要一个能够即时反馈编程作业结果和性能的平台。由此计算机专业课，的作业部分产生了一些问题，如TA判分随意性大等。 因此，四川大学匹兹堡学院计算机科学与技术专业迫切需要一个专门的在线评测系统（Online Judge，简称OJ），以更好地支持编程教学和实践，帮助学生检验和提升编程能力。在与老师和学生进行充分讨论，了解各方需求后，本项目应运而生。

### 主要功能

1.0.0版本基本实现了基于课程为单位的作业的增删改查功能，支持的题目类型有选择题（支持多选），简答题，编程题，其中编程题支持同目录下多文件代码功能的判题，现今支持cpp和java语言，编程题判例设置支持设置命令行参数，标准输入，时间内存限制，符合编程语言课，数据结构与算法等课程的使用要求。简答题在1.0.0版本只支持人工批改评分。

2.0.0版本后，平台接入了动态化AI辅助评测系统，可以对编程题的代码风格、代码实现进行智能化打分。平台完善了一套完整的API Token管理系统，并设计了AI评测模板，支持多平台AI（如ChatGPT、Deepseek、Gemini等主流生成式AI）

### 特别致谢

本项目的推进与实现，离不开多位 SCUPI 学长的宝贵贡献和辛勤付出。他们在项目的关键模块设计、代码架构搭建及技术文档编写等核心环节中倾注了大量心血。

在此，向以下主要贡献者表示最诚挚的感谢 (排名不分先后):

- **[@Linziyang666](https://www.google.com/search?q=https://github.com/Linziyang666)**
- **[@cysgynn](https://www.google.com/search?q=https://github.com/cysgynn)**
- **[@s1050775697](https://www.google.com/search?q=https://github.com/s1050775697)**

他们的努力为项目的成功奠定了坚实的基础。

以下是 SCUPI-online-judge 的旧版本仓库：

- **前端原仓库:** [LinZiyang666/SCUPIOJ-Front-End](https://github.com/LinZiyang666/SCUPIOJ-Front-End)
- **后端原仓库:** [LinZiyang666/SCUPI-online-judge-system](https://github.com/LinZiyang666/SCUPI-online-judge-system)

## 二. 技术栈

### 前端技术栈

项目开发：Vue3，TypeScript，Naive UI，Vue Router，Pinia，Axios，Vite，pnpm

### 后端技术栈

项目开发：Django，Django-rest-framework，JWT，Docker，简单的Cpp多线程，shell，Celery（用于定时/异步脚本，守护进程）

部署与维护：Apache/Nginx，uwsgi，Mysql（不用学习详细的SQL，懂得基础的数据库知识，会使用phpmyadmin）

## 三. 开发环境搭建（基于Windows本机环境）

1. [官网下载并安装WampServer](https://www.wampserver.com/en/)可参考[bilibili视频](https://www.bilibili.com/video/BV1gJ411x7WT/?spm_id_from=333.337.search-card.all.click&vd_source=3ea11c6471f4ecd3b36df28586aea0fa)

2. 初始化 Mysql root 密码，可参考以上视频。

3. ```shell
   git clone https://github.com/Loxilante/SCUPI-online-judge.git
   cd .\SCUPI-online-judge\
   pip install -r requirements.txt
   ```

   如果`mysqlclient`安装失败，请手动安装：
   
   ```
   pip install mysqlclient
   ```
   
4. (由实际情况决定)

   * 请设置scupioj/setting.py 中数据库用户名称，密码与使用的数据库

   * ```shell
     python3 ./manage.py makemigrations; 
     python3 ./manage.py migrate;
     python3 ./manage.py init_site
     ```

5. [安装docker](https://www.docker.com/products/docker-desktop/)并启动

6. 安装WSL，以Ubuntu作为发行版，windows家庭版与专业版安装方式有区别，请根据自身系统版本上网查找

7. 在WSL中进入SCUPI-online-judge-system/docker/

   分别运行：

   - ```shell
     cd cpp_sandbox && bash ./initialize.sh 
     ```

   - ```shell 
     cd java_sandbox && bash ./initialize.sh
     ```
     
   - ```shell
     cd ai_sandbox && bash ./initialize.sh
     ```

   若因网络原因安装失败请重试```bash ./initialize.sh```

## 四. 架构描述

本项目采取前后端分离式架构，前后端通过api交流。

### 前端架构

#### Soybean Admin

### 后端架构

### MVT（Model-View-Template）

- **Model（模型）**：负责处理应用程序的数据逻辑。它直接管理数据、逻辑和规则。可以理解为数据库（不只是数据库，但可以当数据库理解）得益于Django ORM，我们只用设计数据库的结构，具体设计在Django每个app的model.py中。

- **View（视图）**：负责显示数据（模型）给用户。一个模型可以有多个视图。位于每个Django app的view.py中，在本项目中，view通过restful api与前端沟通。

- **Template（模板）**： 负责渲染用户界面，即呈现数据给用户。（本项目前后端分离，这里不用考虑）

  

### 数据库设计

具体用到的数据库结构如下：![database](./backend/media/images/database.png)

2.0.0版本新增的数据库结构如下：![database2](./backend/media/images/database2.png)
