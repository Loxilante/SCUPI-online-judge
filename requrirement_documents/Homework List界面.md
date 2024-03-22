# Homeword List界面
## 功能描述：
显示班级中的作业，管理员与老师可以删除作业，需要为管理员与老师提供Create Homework，Edit Homework界面的入口
**此页面需要显示班级的名称**（从上一步获取）
显示的作业要分为两个区块，一个为进行中的作业（Homework In Process），一个为已经截止的作业（Homework Past Due）
### 显示作业时需要显示的信息（api文档中的字段）：
1. name
2. created_time
3. due_date (作业截止时间的意思，没有超过截止时间的作业在Homework In Process中显示，超过截止时间的作业在Homework Past Due中显示)
4. sum_score（作业的总分）
5. score_get （用户作业的得分）
## api调用：
- 学生：19
- 老师，管理员：19，22