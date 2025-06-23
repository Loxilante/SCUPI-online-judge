# Problem List界面
## 功能描述：
显示作业中的题目，老师和管理员可以删除作业，为老师和管理员提供通向Add Problems和Edit Problems与Course Homework Records的入口
1. 页面上方需要显示作业的信息（从19号api获取），包括
   - name
   - description
   - created_time
   - due_date
   - allow_ai
   - sum_score
   - score_get
2. 题目需要显示的信息（从24号api获取）
   - title
   - score
   - type
   - response_limit (在界面中可以写作attempts limit)
   - score_get

**注意**
>如果题目的type为programming，需要为老师和管理员提供通向*Programming problem answer cases*（代码题判例）页面的入口
## api调用
- 学生：19，24
- 老师和管理员：19，24，26
  