---
title: 个人项目
language_tabs:
  - shell: Shell
  - http: HTTP
  - javascript: JavaScript
  - ruby: Ruby
  - python: Python
  - php: PHP
  - java: Java
  - go: Go
toc_footers: []
includes: []
search: true
code_clipboard: true
highlight_theme: darkula
headingLevel: 2
generator: "@tarslib/widdershins v4.0.20"

---

# 个人项目

Base URLs:

# Authentication

- HTTP Authentication, scheme: bearer

# SCUPIOJ/用户系统

## POST 01 登录

POST /login/

登陆页面的操作，返回refresh和access token，role和first_name，同时设置6个cookie：first_name（用户中文名），role（用户角色，可能为student，teacher或administrator sessionid和username（学号），access，refresh

> Body Parameters

```json
{
  "username": "2022141520159",
  "password": "123456"
}
```

### Params

|Name|Location|Type|Required|Title|Description|
|---|---|---|---|---|---|
|body|body|object| no ||none|
|» username|body|string| yes | 用户账号|学生学号|
|» password|body|string| yes | 密码|none|

> Response Examples

> 成功

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxMDU1NjgxMSwiaWF0IjoxNzA2NDA5NjExLCJqdGkiOiIwY2I2ZDA5OTFlOGE0NzA0OGNiZDViYWM1YTVlMDY0YSIsInVzZXJfaWQiOjR9.83wj2GUt7dgaeopFXQE1-_u5KnCz8xTw-DwZNgGTEYw",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA2NDk2MDExLCJpYXQiOjE3MDY0MDk2MTEsImp0aSI6IjJjYTc1ZjliYmU3MjQxZjFhNGY0OTY4MmNhZjk4MjJlIiwidXNlcl9pZCI6NH0.GUTYn-xf7t3nSHVv0oTYiuuyC2eyYcesuuRsznnC3xc",
  "role": "administrator",
  "first_name": "张三"
}
```

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxMDU1NzAwMywiaWF0IjoxNzA2NDA5ODAzLCJqdGkiOiJiNmUwYTJiMzhiNjY0NjhjOGI1MzQ0MDQyMWUzZDc2YyIsInVzZXJfaWQiOjV9.-QHIlaicMNIMB8-vAe7FYfwxFhMnz3lbnSBeZPP5Ypg",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA2NDk2MjAzLCJpYXQiOjE3MDY0MDk4MDMsImp0aSI6ImM3NTY3OGQwMGVmZDQ3ZWFiNWEyYjUyMmNhMjdiNWIyIiwidXNlcl9pZCI6NX0.Tv5XxZ3deWJQZ4bJ547iTNPnStacphXk1BiqmigUSDk",
  "role": "teacher",
  "first_name": "李四"
}
```

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxMDU1NzAyOCwiaWF0IjoxNzA2NDA5ODI4LCJqdGkiOiJjZjAwNDI4ZjdjYzE0NjVjYTlhZjJjMzUxOGM0MDk3ZiIsInVzZXJfaWQiOjZ9.zq9l3rGu8k7smT8wWg3zeUKNvAe7xdWt4QO_V8H906c",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA2NDk2MjI4LCJpYXQiOjE3MDY0MDk4MjgsImp0aSI6ImI5Y2ZmODdhNjc5NzRmNTNiMzUzZGYzNjRiZDE0OGYxIiwidXNlcl9pZCI6Nn0.Z_iYc9PMKpUi2nYO_n8kIpvc_LBdNzxroXdqmx-suuc",
  "role": "student",
  "first_name": "王五"
}
```

> 没有权限

```json
{
  "error": "Invalid username or password"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|没有权限|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» refresh|string|true|none|refresh token|none|
|» access|string|true|none|access token|none|
|» role|string|true|none|用户角色|none|
|» first_name|string|true|none|用户的中文名|none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» error|string|true|none||none|

## POST 02 注销

POST /logout/

注销接口，运行此接口必须有有效的access token和名为sessionid的cookie（前端不用管这个cookie），注销成功后请前端清除所有cookie和token

### Params

|Name|Location|Type|Required|Title|Description|
|---|---|---|---|---|---|
|sessionid|cookie|string| no ||后端的session对应id，前端不可更改|

> Response Examples

> 删除成功

```json
{
  "success": "Logout successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|删除成功|Inline|

### Responses Data Schema

HTTP Status Code **204**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» success|string|true|none||none|

## POST 03 assess token续期

POST /refresh/

access token如果过期，可使用refresh token申请一个新assess token，如果refresh token也过期了会有编号为500的报错，请重新登录

> Body Parameters

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxMDMwNzA2MSwiaWF0IjoxNzA2MTU5ODYxLCJqdGkiOiI0MGVkNDJmZDU3NGU0ZWI0YjAxMjE5ODc4Zjk4YWI5NiIsInVzZXJfaWQiOjR9.9CgDEVgnJhUJw9cgHlOQBlCefQlGpW83wo5JG0asxhs"
}
```

### Params

|Name|Location|Type|Required|Title|Description|
|---|---|---|---|---|---|
|body|body|object| no ||none|
|» refresh|body|string| yes | refresh token|none|

> Response Examples

> 成功

```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA2NDk3OTI0LCJpYXQiOjE3MDYxNTk4NjEsImp0aSI6IjM0ZTMwODYzODExYTQ2OTI4ODk3Mjg1NjFhOGRlN2M4IiwidXNlcl9pZCI6NH0.ke4LVk54svyeHlFkG5A-3GPxq3duacRBKPmtLhQ3obQ"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» access|string|true|none||none|

# SCUPIOJ/用户系统/账号增删改查

## GET 05 老师管理员获取系统全部用户

GET /home/user/

获取系统全部用户，需要老师或管理员权限，登录状态

> Response Examples

> 成功

```json
[
  {
    "username": "admin",
    "email": "admin@example.com",
    "first_name": "超级管理员"
  },
  {
    "username": "2022141520159",
    "email": "3177267975@qq.com",
    "first_name": "张三"
  },
  {
    "username": "2022141520158",
    "email": "3177267975@qq.com",
    "first_name": "李四"
  },
  {
    "username": "2022141520157",
    "email": "3177267975@qq.com",
    "first_name": "王五"
  }
]
```

> 禁止访问

```json
{
  "error": "You don't have permission to view user"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|禁止访问|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» username|string|true|none||none|
|» email|string|true|none||none|
|» first_name|string|true|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» error|string|true|none||none|

## POST 07 管理员创建用户

POST /home/user/

只有管理员可以创建用户，注意new_user_group字段只能为三个值administrator，teacher，student

> Body Parameters

```json
{
  "new_username": "2022141520161",
  "new_user_password": "123456",
  "new_user_email": "123456@outlook.com",
  "new_user_group": "administrator",
  "new_user_first_name": "新增用户2"
}
```

### Params

|Name|Location|Type|Required|Title|Description|
|---|---|---|---|---|---|
|body|body|object| no ||none|
|» new_username|body|string| yes | 新用户学号|none|
|» new_user_password|body|string| yes | 新用户密码|none|
|» new_user_email|body|string| yes | 新用户邮箱|none|
|» new_user_group|body|string| yes | 新用户role|none|
|» new_user_first_name|body|string| yes | 新用户中文名|none|

> Response Examples

> 成功

```json
{
  "success": "User created successfully"
}
```

> 请求有误

```json
{
  "error": "Invalid username or password"
}
```

> 禁止访问

```json
{
  "error": "You don't have permission to create user"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|请求有误|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|禁止访问|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» success|string|true|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» error|string|true|none||输入的学号与密码不合法或用户已存在|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» error|string|true|none||none|

## DELETE 08 管理员删除用户

DELETE /home/user/

只有管理员可以删除用户

> Body Parameters

```json
{
  "delete_username": "2022141520160"
}
```

### Params

|Name|Location|Type|Required|Title|Description|
|---|---|---|---|---|---|
|body|body|object| no ||none|
|» delete_username|body|string| yes | 删除用户学号|none|

> Response Examples

> 成功

```json
{
  "success": "User deleted successfully"
}
```

> 请求有误

```json
{
  "error": "Invalid username"
}
```

> 禁止访问

```json
{
  "error": "You don't have permission to delete user"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|请求有误|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|禁止访问|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» success|string|true|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» error|string|true|none||用户不存在或已被删除|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» error|string|true|none||无权限|

## GET 04 获取单个用户的信息

GET /home/user/%3Cint:username%3E/

通过<int:username>获取相应username的用户的信息，注意老师和管理员有权访问所有用户的信息，学生只能访问自己的信息

> Response Examples

> 成功

```json
{
  "username": "2022141520157",
  "email": "3177267975@qq.com",
  "first_name": "王五"
}
```

> 禁止访问

```json
{
  "error": "You don't have permission to view user"
}
```

> 记录不存在

```json
{
  "error": "Invalid username"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|禁止访问|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|记录不存在|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» username|string|true|none||none|
|» email|string|true|none||none|
|» first_name|string|true|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» error|string|true|none||只有学生越权访问时出现|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» error|string|true|none||用户不存在|

## PUT 06 修改账号密码

PUT /home/user/%3Cint:username%3E/

修改<int:username>用户的密码，学生和老师只能修改自己的密码，需要输入旧密码和新密码，管理员可以强制修改所有人的密码，需要输入旧密码（可以乱写）和新密码，如果用户是学生，前端在密码修改成功后要删除所有的cookie和token，管理员不用

> Body Parameters

```json
{
  "old_password": "123456",
  "new_password": "123456"
}
```

### Params

|Name|Location|Type|Required|Title|Description|
|---|---|---|---|---|---|
|body|body|object| no ||none|
|» old_password|body|string| yes ||none|
|» new_password|body|string| yes ||none|

> Response Examples

> 成功

```json
{
  "success": "Password updated successfully, now logout if you are not admin."
}
```

> 禁止访问

```json
{
  "error": "You don't have permission to update this user"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|禁止访问|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» success|string|true|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» error|string|true|none||非管理员尝试修改其他人的密码|

# SCUPIOJ/班级系统

## POST 09 管理员创建班级

POST /home/

管理员创建新的课程并初始化课程人员有两个参数，course_name和students_list, student_list是一个列表，存有课程人员的学号。

> Body Parameters

```json
{
  "course_name": "Introduction to JAVA",
  "students_list": [
    "2022141520159",
    "2022141520158",
    "2022141520157"
  ]
}
```

### Params

|Name|Location|Type|Required|Title|Description|
|---|---|---|---|---|---|
|body|body|object| no ||none|
|» course_name|body|string| yes ||none|
|» students_list|body|[string]| yes ||none|

> Response Examples

> 成功

```json
{
  "success": "Course created successfully"
}
```

> 请求有误

```json
{
  "error": "Invalid course name"
}
```

> 禁止访问

```json
{
  "error": "You don't have permission to create course"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|请求有误|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|禁止访问|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» success|string|true|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» error|string|true|none||课程名重复或无效|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» error|string|true|none||无权限|

## DELETE 10 管理员删除班级

DELETE /home/

只有管理员有权利删除班级

> Body Parameters

```json
{
  "course_name": "Introduction to CPP"
}
```

### Params

|Name|Location|Type|Required|Title|Description|
|---|---|---|---|---|---|
|body|body|object| no ||none|
|» course_name|body|string| yes | 删除课程名|none|

> Response Examples

> 成功

```json
{
  "success": "Course deleted successfully"
}
```

> 请求有误

```json
{
  "error": "course name error"
}
```

> 禁止访问

```json
{
  "error": "You don't have permission to delete course"
}
```

> 记录不存在

```json
{
  "error": "Course not found"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|请求有误|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|禁止访问|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|记录不存在|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» success|string|true|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» error|string|true|none||组名不合法或不存在|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» error|string|true|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» error|string|true|none||none|

## GET 13 获取此用户所加入的班级

GET /home/

获取此用户所加入的课程，现今只返回班级名，在日后会新增返回，比如未完成作业数和未读通知数

> Response Examples

> 成功

```json
[
  {
    "course_name": "Introduction to JAVA"
  },
  {
    "course_name": "Introduction to Python"
  }
]
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» course_name|string|true|none||none|

## PUT 11 管理员编辑班级成员

PUT /home/%3Cstr:coursename%3E/member/

编辑<str:coursename>课程的班级成员，只有管理员可以编辑班级成员，参数与创建班级相同，请注意students_list里装的是班级所有成员的学号，上传后后端会根据students_list与之前的成员对比进行增减

> Body Parameters

```json
{
  "course_name": "Introduction to JAVA",
  "students_list": [
    "2022141520159",
    "2022141520158"
  ]
}
```

### Params

|Name|Location|Type|Required|Title|Description|
|---|---|---|---|---|---|
|body|body|object| no ||none|
|» course_name|body|string| yes ||none|
|» students_list|body|[string]| yes ||none|

> Response Examples

> 成功

```json
{
  "success": "Course update successfully"
}
```

> 请求有误

```json
{
  "error": "Invalid course not exist"
}
```

> 禁止访问

```json
{
  "error": "You don't have permission to edit course"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|请求有误|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|禁止访问|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» success|string|true|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» error|string|true|none||组名不存在或组名不合法|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» error|string|true|none||none|

## GET 12 获取班级中的成员

GET /home/%3Cstr:coursename%3E/member/

获取名为<str:coursename>课程中所有的成员

> Response Examples

> 成功

```json
[
  {
    "username": "2022141520158",
    "first_name": "李四"
  },
  {
    "username": "2022141520157",
    "first_name": "王五"
  },
  {
    "username": "2022141520159",
    "first_name": "张三"
  }
]
```

> 禁止访问

```json
{
  "error": "You don't have permission to visit this course"
}
```

> 记录不存在

```json
{
  "error": "course not exist"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|禁止访问|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|记录不存在|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» username|string|true|none||none|
|» first_name|string|true|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» error|string|true|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» error|string|true|none||none|

# SCUPIOJ/信息系统操作

## POST 创建新信息

POST /message/

创建新的信件，并返回是否创建成功的信息。在创建信息时只能选择向某些群组发送或向某些用户发送两种之一receiver和receive_group只能二选一

> Body Parameters

```json
" {\r\n    \"level\":\"urgent\",\r\n    \"title\":\"测试信息\",\r\n    \"content\":\"正文内容\",\r\n    \"receive_group\":[\"administrator\"]\r\n  }\r\n  或\r\n  {\r\n    \"level\":\"urgent\",\r\n    \"title\":\"测试信息\",\r\n    \"content\":\"正文内容\",\r\n    \"receiver\":[\"2022141520159\"]\r\n  }\r\n"
```

### Params

|Name|Location|Type|Required|Title|Description|
|---|---|---|---|---|---|
|body|body|object| no ||none|
|» level|body|string| yes | 信息等级|仅可选ordinary或urgent|
|» title|body|string| yes | 信息标题|none|
|» content|body|string| yes | 正文内容|none|
|» receiver|body|[string]¦null| no | 收信人|收信人与收信小组选其一|
|» receive_group|body|[string]¦null| no | 收信小组|none|

> Response Examples

> 成功

```json
{
  "success": "Create message successfully"
}
```

> 请求有误

```json
{
  "error": "message save error"
}
```

```json
{
  "error": "receiver save error"
}
```

```json
{
  "error": "receive_group save error"
}
```

> 收信对象不存在

```json
{
  "error": "user not exist"
}
```

```json
{
  "error": "group not exist"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|请求有误|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|收信对象不存在|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» *anonymous*|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» *anonymous*|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» *anonymous*|string|false|none||none|

## PUT 修改已读状态

PUT /message/

将已读状态设置为‘已读’

> Body Parameters

```json
{
  "message_id": "123456"
}
```

### Params

|Name|Location|Type|Required|Title|Description|
|---|---|---|---|---|---|
|body|body|object| no ||none|
|» message_id|body|integer| yes ||none|

> Response Examples

> 成功

```json
{
  "success": "change is_read to True"
}
```

> 记录不存在

```json
{
  "error": "message not exist"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|记录不存在|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» *anonymous*|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» *anonymous*|string|false|none||none|

## DELETE 删除信息

DELETE /message/

删除信息，返回是否删除成功的信息

> Body Parameters

```json
{
  "message_id": "114514"
}
```

### Params

|Name|Location|Type|Required|Title|Description|
|---|---|---|---|---|---|
|body|body|object| no ||none|
|» message_id|body|integer| yes | 信息的id|none|

> Response Examples

> 成功

```json
{
  "success": "Delete message successfully"
}
```

> 没有权限

```json
{
  "error": "You do not have permission to delete this message"
}
```

> 记录不存在

```json
{
  "error": "message not found"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|没有权限|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|记录不存在|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» *anonymous*|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» *anonymous*|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» *anonymous*|string|false|none||none|

## GET 获取用户发送信息

GET /message/0/

获取以当前用户为发件人的信息

> Body Parameters

```json
{}
```

### Params

|Name|Location|Type|Required|Title|Description|
|---|---|---|---|---|---|
|body|body|object| no ||none|

> Response Examples

> 成功

```json
[
  {
    "sender": "张三",
    "level": "urgent",
    "title": "kfc",
    "content": "222",
    "sent_time": "2024-02-06T08:16:53.661Z",
    "id": 43
  },
  {
    "sender": "张三",
    "level": "urgent",
    "title": "kfc",
    "content": "222",
    "sent_time": "2024-02-06T08:16:24.579Z",
    "id": 42
  },
  {
    "sender": "张三",
    "level": "urgent",
    "title": "kfc",
    "content": "222",
    "sent_time": "2024-02-06T08:16:16.739Z",
    "id": 41
  },
  {
    "sender": "张三",
    "level": "urgent",
    "title": "kfc",
    "content": "222",
    "sent_time": "2024-02-06T08:15:45.537Z",
    "id": 40
  },
  {
    "sender": "张三",
    "level": "urgent",
    "title": "kfc",
    "content": "222",
    "sent_time": "2024-02-06T08:15:18.970Z",
    "id": 39
  }
]
```

> 没有权限(未登录)

```json
{
  "error": "invalid user,please login or register"
}
```

> 找不到已接收信件

```json
{
  "error": "can not find received message"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|没有权限(未登录)|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|找不到已接收信件|Inline|

### Responses Data Schema

HTTP Status Code **200**

*返回一个list，元素是字典*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» sender|string|true|none|发件人|none|
|» level|string|true|none|信息等级|none|
|» title|string|true|none|信息标题|none|
|» sent_time|string|true|none|发送时间|none|
|» id|string|true|none|信息的id|none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»|string|true|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»|string|true|none||none|

## GET 获取用户接收信息

GET /message/1/

获取以当前用户为收件人的信息

> Body Parameters

```json
{}
```

### Params

|Name|Location|Type|Required|Title|Description|
|---|---|---|---|---|---|
|body|body|object| no ||none|

> Response Examples

> 成功

```json
[
  {
    "sender": "张三",
    "level": "urgent",
    "title": "kfc",
    "content": "222",
    "sent_time": "2024-02-06T08:16:53.661Z",
    "id": 43,
    "is_read": false
  },
  {
    "sender": "张三",
    "level": "urgent",
    "title": "kfc",
    "content": "222",
    "sent_time": "2024-02-06T08:16:24.579Z",
    "id": 42,
    "is_read": false
  },
  {
    "sender": "张三",
    "level": "urgent",
    "title": "kfc",
    "content": "222",
    "sent_time": "2024-02-06T08:16:16.739Z",
    "id": 41,
    "is_read": false
  },
  {
    "sender": "张三",
    "level": "urgent",
    "title": "kfc",
    "content": "222",
    "sent_time": "2024-02-06T08:15:45.537Z",
    "id": 40,
    "is_read": false
  },
  {
    "sender": "张三",
    "level": "urgent",
    "title": "kfc",
    "content": "222",
    "sent_time": "2024-02-06T08:15:18.970Z",
    "id": 39,
    "is_read": false
  }
]
```

> 没有权限(未登录)

```json
{
  "error": "invalid user,please login or register"
}
```

> 找不到已接收信件

```json
{
  "error": "can not find received message"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|没有权限(未登录)|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|找不到已接收信件|Inline|

### Responses Data Schema

HTTP Status Code **200**

*返回一个list，元素是字典*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» sender|string|true|none|发件人|none|
|» level|string|true|none|信息等级|none|
|» title|string|true|none|信息标题|none|
|» sent_time|string|true|none|发送时间|none|
|» id|string|true|none|信息的id|none|
|» is_read|boolean|true|none|是否已读|none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»|string|true|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»|string|true|none||none|

# SCUPIOJ/作业操作

## GET 获取课程中布置的作业

GET /home/%3Cstr:coursename%3E/

获取<str:coursename>课程中布置的作业

> Response Examples

> 成功

```json
[
  {
    "name": "实验作业2",
    "description": "A basic assignment on Django models4",
    "created_time": "2024-01-30T21:44:44.845760+08:00",
    "due_date": "2024-01-30T20:00:00+08:00",
    "allow_ai": true
  },
  {
    "name": "实验作业3",
    "description": "A basic assignment on Django models4",
    "created_time": "2024-01-30T21:44:50.122416+08:00",
    "due_date": "2024-01-30T20:00:00+08:00",
    "allow_ai": true
  },
  {
    "name": "实验作业1",
    "description": "A basic assignment on Django models4",
    "created_time": "2024-01-30T21:44:35.579331+08:00",
    "due_date": "2024-01-30T20:00:00+08:00",
    "allow_ai": true
  }
]
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» name|string|true|none|作业的名称|none|
|» description|string|true|none|作业的描述|none|
|» created_time|string|true|none|作业的布置时间|none|
|» due_date|string|true|none|作业的截止时间|none|
|» allow_ai|boolean|true|none|是否主动AI批改|none|

## POST 布置作业

POST /home/%3Cstr:coursename%3E/

在<str:coursename>课程中布置作业，作业创建后返回创建的作业的信息,只有管理员和老师有权布置作业

> Body Parameters

```json
{
  "name": "实验作业3",
  "description": "A basic assignment on Django models4",
  "due_date": "2024-01-30T12:00:00Z",
  "allow_ai": true
}
```

### Params

|Name|Location|Type|Required|Title|Description|
|---|---|---|---|---|---|
|body|body|object| no ||none|
|» name|body|string| yes | 作业名|none|
|» description|body|string| yes | 作业描述|none|
|» due_date|body|string| yes | 截止时间|none|
|» allow_ai|body|boolean| yes | 是否AI主动批改|none|

> Response Examples

> 成功

```json
{
  "name": "实验作业4",
  "description": "A basic assignment on Django models4",
  "created_time": "2024-01-30T22:29:41.117230+08:00",
  "due_date": "2024-01-30T20:00:00+08:00",
  "allow_ai": true
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|成功|Inline|

### Responses Data Schema

HTTP Status Code **201**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» name|string|true|none|作业名|none|
|» description|string|true|none|作业描述|none|
|» created_time|string|true|none|布置时间|none|
|» due_date|string|true|none|截至时间|none|
|» allow_ai|boolean|true|none|是否主动AI批改|none|

## PUT 更改作业信息

PUT /home/%3Cstr:coursename%3E/

更改<str:coursename>课程中作业的信息，提交的body与创建作业相同，返回值也与创建作业相同，只有管理员和老师有权利更改作业信息

> Body Parameters

```json
{
  "name": "实验作业4",
  "description": "A basic assignment on Django models4",
  "due_date": "2024-01-30T12:00:00Z",
  "allow_ai": true
}
```

### Params

|Name|Location|Type|Required|Title|Description|
|---|---|---|---|---|---|
|body|body|object| no ||none|
|» name|body|string| yes ||none|
|» description|body|string| yes ||none|
|» due_date|body|string| yes ||none|
|» allow_ai|body|boolean| yes ||none|

> Response Examples

> 成功

```json
{
  "name": "实验作业4",
  "description": "A basic assignment on Django models",
  "created_time": "2024-01-30T22:29:41.117230+08:00",
  "due_date": "2024-01-30T20:00:00+08:00",
  "allow_ai": true
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» name|string|true|none||none|
|» description|string|true|none||none|
|» created_time|string|true|none||none|
|» due_date|string|true|none||none|
|» allow_ai|boolean|true|none||none|

## DELETE 删除作业

DELETE /home/%3Cstr:coursename%3E/

删除<str:coursename>课程中的作业，只有老师和管理员有权利删除作业，删除成功为204状态，不会有json返回

> Body Parameters

```json
{
  "name": "string"
}
```

### Params

|Name|Location|Type|Required|Title|Description|
|---|---|---|---|---|---|
|body|body|object| no ||none|
|» name|body|string| yes | 删除作业的名称|none|

> Response Examples

> 204 Response

```json
{}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|删除成功|Inline|

### Responses Data Schema

## GET 获取特定学生的作业总分

GET /127.0.0.1:8000/home/%3Cstr:coursename%3E/%3Cstr:assignmentname%3E/getstuscore/%3Cstr:student%3E/

获取特定<str:student>学生的作业总分

> Response Examples

> 成功

```json
{
  "assignment_id": 1,
  "assignment_name": "实验作业3",
  "score": 0
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» assignment_id|integer|true|none||none|
|» assignment_name|string|true|none||none|
|» score|integer|true|none||none|

## GET 获取设定的作业总分数

GET /127.0.0.1:8000/home/%3Cstr:coursename%3E/%3Cstr:assignmentname%3E/getscore/

获取<str:assignmentname>作业总分数，注意是作业设定的总分，作业答题总分

> Response Examples

> 成功

```json
{
  "sumscore": 100
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» sumscore|integer|true|none||none|

## GET 获取所有学生作业总得分

GET /127.0.0.1:8000/home/%3Cstr:coursename%3E/%3Cstr:assignmentname%3E/getstuscore/all/

获取所有获取/<str:coursename>/<str:assignmentname>/所有学生的总得分

> Response Examples

> 成功

```json
[
  {
    "assignment_id": 2,
    "assignment_name": "实验作业2",
    "username": "2022141520159",
    "first_name": "张三",
    "score": 200
  },
  {
    "assignment_id": 2,
    "assignment_name": "实验作业2",
    "username": "2022141520158",
    "first_name": "李四",
    "score": 0
  },
  {
    "assignment_id": 2,
    "assignment_name": "实验作业2",
    "username": "2022141520157",
    "first_name": "王五",
    "score": 200
  }
]
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» assignment_id|integer|true|none||none|
|» assignment_name|string|true|none||none|
|» username|string|true|none||none|
|» first_name|string|true|none||none|
|» score|integer|true|none||none|

# SCUPIOJ/作业操作/题目操作/增删改查题目

## POST 在作业中新建题目

POST /home/%3Cstr:coursename%3E/%3Cstr:assignmentname%3E/

在<str:coursename>班级，<str:assignmentname>作业中新建题目，body为一个列表，可以同时布置多个题目，题目的图片用其他api处理
参数讲解：
title 题目的标题 必填（创建之后不可修改）
content_problem 题目的具体信息 必填
score 题目的分值 必填
type 题目的类型，有三种可选‘programming’，‘text’，‘choice' 必填
response_limit 学生在此题目尝试的最大次数 可不填，不填则视为无限制
non_programming_answer 在题目不是代码题时题目的答案，必填，后端会根据其中内容进行判分，如果题目是代码题这个字段可以不填，会有其他的接口来处理代码题目的答案

若运行成功直接返回创建的题目

#题目答案规则：non_programming_answer中储存选择题和简答题的答案
答案均由"<-&&->"包裹，比如在多选题中答案为a，c，e，non_programming_answer应填"<-&a&-><-&c&-><-&e&->"
在简答题中如为多空简答题，第一个空的答案为“床前明月光”第二个空的答案为“疑是地上霜”，则non_programming_answer应填"<-&床前明月光&-><-&疑是地上霜&->"注意多空简答题答案一一对应，顺序不能错

> Body Parameters

```json
[
  {
    "title": "Problem 1",
    "content_problem": "Describe the process of normalization in databases.",
    "score": 10,
    "type": "text",
    "response_limit": 500,
    "non_programming_answer": "Normalization is the process of organizing data in a database..."
  },
  {
    "title": "Problem 2",
    "content_problem": "What is the time complexity of a binary search algorithm?",
    "score": 5,
    "type": "choice",
    "response_limit": null,
    "non_programming_answer": "<-&a&->"
  },
  {
    "title": "Problem 3",
    "content_problem": "Write a function to reverse a string.",
    "score": 15,
    "type": "programming",
    "response_limit": null,
    "non_programming_answer": null
  }
]
```

### Params

|Name|Location|Type|Required|Title|Description|
|---|---|---|---|---|---|
|body|body|array[object]| no ||none|

> Response Examples

> 成功

```json
[
  {
    "id": 1,
    "title": "Problem 1",
    "content_problem": "Describe the process of normalization in databases.",
    "score": 10,
    "type": "text",
    "response_limit": 500,
    "non_programming_answer": "Normalization is the process of organizing data in a database..."
  },
  {
    "id": 2,
    "title": "Problem 2",
    "content_problem": "What is the time complexity of a binary search algorithm?",
    "score": 5,
    "type": "choice",
    "response_limit": null,
    "non_programming_answer": "<-&a&->"
  },
  {
    "id": 3,
    "title": "Problem 3",
    "content_problem": "Write a function to reverse a string.",
    "score": 15,
    "type": "programming",
    "response_limit": null,
    "non_programming_answer": null
  }
]
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|成功|Inline|

### Responses Data Schema

HTTP Status Code **201**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» id|integer|true|none|数据库中作业id|none|
|» title|string|true|none||none|
|» content_problem|string|true|none||none|
|» score|integer|true|none||none|
|» type|string|true|none||none|
|» response_limit|integer¦null|true|none||none|
|» non_programming_answer|string¦null|true|none||none|

## GET 获取作业中题目

GET /home/%3Cstr:coursename%3E/%3Cstr:assignmentname%3E/

获取在<str:coursename>班级中，<str:assignmentname>作业中的所有题目，现在会显示non_programming_answer，在后续开发中会对此逻辑进行修改，如只有老师与管理员可以看到题目答案，学生要在作业截止后才能看到答案

> Response Examples

> 成功

```json
[
  {
    "id": 14,
    "title": "NEWProblem 1",
    "content_problem": "Describe the process of normalization in databases.",
    "score": 10,
    "type": "text",
    "response_limit": 500,
    "non_programming_answer": "Normalization is the process of organizing data in a database..."
  },
  {
    "id": 15,
    "title": "NEWProblem 2",
    "content_problem": "What is the time complexity of a binary search algorithm?",
    "score": 5,
    "type": "choice",
    "response_limit": null,
    "non_programming_answer": "O(log n)"
  },
  {
    "id": 16,
    "title": "NEWProblem 3",
    "content_problem": "Write a function to reverse a string.ASDFASDFASDFADS",
    "score": 15,
    "type": "programming",
    "response_limit": null,
    "non_programming_answer": null
  }
]
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» id|integer|true|none||none|
|» title|string|true|none||none|
|» content_problem|string|true|none||none|
|» score|integer|true|none||none|
|» type|string|true|none||none|
|» response_limit|integer¦null|true|none||none|
|» non_programming_answer|string¦null|true|none||如果是学生则没有这个字段|

## PUT 修改作业中题目内容

PUT /home/%3Cstr:coursename%3E/%3Cstr:assignmentname%3E/

修改在<str:coursename>班级中，<str:assignmentname>作业中的题目的内容，允许批量修改，只需要将修改之后的题目信息放在list中
注意需含有修改题目的id，id可用get获得，返回修改后题目的信息

> Body Parameters

```json
[
  {
    "id": 14,
    "title": "NEWProblem 1",
    "content_problem": "Describe the process of normalization in databases.",
    "score": 10,
    "type": "text",
    "response_limit": 500,
    "non_programming_answer": "Normalization is the process of organizing data in a database..."
  },
  {
    "id": 15,
    "title": "NEWProblem 2",
    "content_problem": "What is the time complexity of a binary search algorithm?",
    "score": 5,
    "type": "choice",
    "response_limit": null,
    "non_programming_answer": "O(log n)"
  },
  {
    "id": 16,
    "title": "NEWProblem 3",
    "content_problem": "Write a function to reverse a string.ASDFASDFASDFADS",
    "score": 15,
    "type": "programming",
    "response_limit": null,
    "non_programming_answer": null
  }
]
```

### Params

|Name|Location|Type|Required|Title|Description|
|---|---|---|---|---|---|
|body|body|array[object]| no ||none|

> Response Examples

> 成功

```json
[
  {
    "id": 14,
    "title": "NEWProblem 1",
    "content_problem": "Describe the process of normalization in databases.",
    "score": 10,
    "type": "text",
    "response_limit": 500,
    "non_programming_answer": "Normalization is the process of organizing data in a database..."
  },
  {
    "id": 15,
    "title": "NEWProblem 2",
    "content_problem": "What is the time complexity of a binary search algorithm?",
    "score": 5,
    "type": "choice",
    "response_limit": null,
    "non_programming_answer": "O(log n)"
  },
  {
    "id": 16,
    "title": "NEWProblem 3",
    "content_problem": "Write a function to reverse a string.ASDFASDFASDFADS",
    "score": 15,
    "type": "programming",
    "response_limit": null,
    "non_programming_answer": null
  }
]
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» id|integer|true|none||none|
|» title|string|true|none||none|
|» content_problem|string|true|none||none|
|» score|integer|true|none||none|
|» type|string|true|none||none|
|» response_limit|integer¦null|true|none||none|
|» non_programming_answer|string¦null|true|none||none|

## DELETE 删除作业中题目

DELETE /home/%3Cstr:coursename%3E/%3Cstr:assignmentname%3E/

删除在<str:coursename>班级中，<str:assignmentname>作业中的题目，支持批量删除题目

> Body Parameters

```json
{
  "delete_id": [
    11,
    12,
    13
  ]
}
```

### Params

|Name|Location|Type|Required|Title|Description|
|---|---|---|---|---|---|
|body|body|object| no ||none|
|» delete_id|body|[integer]| yes ||none|

> Response Examples

> 204 Response

```json
{}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|删除成功|Inline|

### Responses Data Schema

## GET 获取作业中所有题目得分

GET /127.0.0.1:8000/home/%3Cstr:coursename%3E/%3Cstr:assignmentname%3E/getscore/%3Cstr:student%3E/

获取/<str:student>/在<str:assignmentname>作业中做题所得到的分数，返回一个列表，包含作业中所有题目的得分

> Response Examples

> 成功

```json
[
  {
    "problem_id": 1,
    "title": "Problem 1",
    "score": 100
  },
  {
    "problem_id": 2,
    "title": "Problem 2",
    "score": 5
  },
  {
    "problem_id": 3,
    "title": "Problem 3",
    "score": 0
  }
]
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» problem_id|integer|true|none||none|
|» title|string|true|none||none|
|» score|integer|true|none||none|

# SCUPIOJ/作业操作/题目操作/增删改查题目/增删改查代码答案

## POST 创建代码作业答案

POST /127.0.0.1:8000/home/%3Cstr:coursename%3E/%3Cstr:assignmentname%3E/programming/%3Cint:problem_id%3E/

老师管理员在<str:coursename>课程<str:assignmentname>作业<int:problem_id>题目中新建代码答案，可以批量新建，返回创建的代码答案与相应id
***请前端注意限制判例总分值应等于题目分值***

> Body Parameters

```json
[
  {
    "command_line_arguments": null,
    "standard_input": null,
    "standard_output": "output2",
    "time_limit": 10000,
    "space_limit": 10000,
    "score": 200
  },
  {
    "command_line_arguments": "arg1 arg2 arg3",
    "standard_input": "input1",
    "standard_output": "output1",
    "time_limit": 10000,
    "space_limit": 10000,
    "score": 100
  },
  {
    "command_line_arguments": "arg4 arg5",
    "standard_input": "input2",
    "standard_output": "output3",
    "time_limit": 10000,
    "space_limit": 10000,
    "score": 150
  }
]
```

### Params

|Name|Location|Type|Required|Title|Description|
|---|---|---|---|---|---|
|body|body|array[object]| no ||none|

> Response Examples

> 成功

```json
[
  {
    "id": 1,
    "command_line_arguments": null,
    "standard_input": null,
    "standard_output": "output2",
    "time_limit": 10000,
    "space_limit": 10000,
    "score": 200
  },
  {
    "id": 2,
    "command_line_arguments": "arg1 arg2 arg3",
    "standard_input": "input1",
    "standard_output": "output1",
    "time_limit": 10000,
    "space_limit": 10000,
    "score": 100
  },
  {
    "id": 3,
    "command_line_arguments": "arg4 arg5",
    "standard_input": "input2",
    "standard_output": "output3",
    "time_limit": 10000,
    "space_limit": 10000,
    "score": 150
  }
]
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|成功|Inline|

### Responses Data Schema

HTTP Status Code **201**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» id|integer|true|none||none|
|» command_line_arguments|string¦null|true|none||none|
|» standard_input|string¦null|true|none||none|
|» standard_output|string|true|none||none|
|» time_limit|integer|true|none||none|
|» space_limit|integer|true|none||none|
|» score|integer|true|none||none|

## DELETE 删除代码答案

DELETE /127.0.0.1:8000/home/%3Cstr:coursename%3E/%3Cstr:assignmentname%3E/programming/%3Cint:problem_id%3E/

老师管理员删除<str:coursename>课程<str:assignmentname>作业<int:problem_id>问题的代码答案，注意如果要删除的代码答案不属于这个题目会删除失败

> Body Parameters

```json
{
  "delete_id": [
    1,
    2,
    3
  ]
}
```

### Params

|Name|Location|Type|Required|Title|Description|
|---|---|---|---|---|---|
|body|body|object| no ||none|
|» delete_id|body|[integer]| yes ||要删除代码答案的id|

> Response Examples

> 204 Response

```json
{}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|删除成功|Inline|

### Responses Data Schema

## GET 获取代码答案

GET /127.0.0.1:8000/home/%3Cstr:coursename%3E/%3Cstr:assignmentname%3E/programming/%3Cint:problem_id%3E/

老师管理员获取<str:coursename>/<str:assignmentname>/<int:problem_id>/题目的代码答案

> Response Examples

> 成功

```json
[
  {
    "id": 6,
    "command_line_arguments": "arg4 arg5",
    "standard_input": "input2",
    "standard_output": "output3",
    "time_limit": 10000,
    "space_limit": 10000,
    "score": 150
  },
  {
    "id": 5,
    "command_line_arguments": "arg1 arg2 arg3",
    "standard_input": "input1",
    "standard_output": "output1",
    "time_limit": 10000,
    "space_limit": 10000,
    "score": 100
  },
  {
    "id": 4,
    "command_line_arguments": null,
    "standard_input": null,
    "standard_output": "output2",
    "time_limit": 10000,
    "space_limit": 10000,
    "score": 200
  }
]
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» id|integer|true|none||none|
|» command_line_arguments|string¦null|true|none||none|
|» standard_input|string¦null|true|none||none|
|» standard_output|string|true|none||none|
|» time_limit|integer|true|none||none|
|» space_limit|integer|true|none||none|
|» score|integer|true|none||none|

## PUT 修改代码答案

PUT /127.0.0.1:8000/home/%3Cstr:coursename%3E/%3Cstr:assignmentname%3E/programming/%3Cint:problem_id%3E/

老师管理员修改<str:coursename>/<str:assignmentname>/<int:problem_id>/中代码答案，可以批量修改，返回修改后的结果

> Body Parameters

```json
[
  {
    "id": 6,
    "command_line_arguments": "arg4 arg5",
    "standard_input": "input2",
    "standard_output": "output3",
    "time_limit": 10000,
    "space_limit": 10000,
    "score": 150
  },
  {
    "id": 5,
    "command_line_arguments": "arg1 arg2 arg3",
    "standard_input": "input1",
    "standard_output": "output1",
    "time_limit": 10000,
    "space_limit": 10000,
    "score": 100
  },
  {
    "id": 4,
    "command_line_arguments": null,
    "standard_input": null,
    "standard_output": "output2",
    "time_limit": 10000,
    "space_limit": 10000,
    "score": 200
  }
]
```

### Params

|Name|Location|Type|Required|Title|Description|
|---|---|---|---|---|---|
|body|body|array[object]| no ||none|

> Response Examples

> 成功

```json
[
  {
    "id": 6,
    "command_line_arguments": "arg4 arg5",
    "standard_input": "input2",
    "standard_output": "output3",
    "time_limit": 10000,
    "space_limit": 10000,
    "score": 150
  },
  {
    "id": 5,
    "command_line_arguments": "arg1 arg2 arg3",
    "standard_input": "input1",
    "standard_output": "output1",
    "time_limit": 10000,
    "space_limit": 10000,
    "score": 100
  },
  {
    "id": 4,
    "command_line_arguments": null,
    "standard_input": null,
    "standard_output": "output2",
    "time_limit": 10000,
    "space_limit": 10000,
    "score": 200
  }
]
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» id|integer|true|none||none|
|» command_line_arguments|string¦null|true|none||none|
|» standard_input|string¦null|true|none||none|
|» standard_output|string|true|none||none|
|» time_limit|integer|true|none||none|
|» space_limit|integer|true|none||none|
|» score|integer|true|none||none|

# SCUPIOJ/作业操作/题目操作/回答题目与人工判题操作

## POST 回答题目

POST /home/%3Cstr:coursename%3E/%3Cstr:assignmentname%3E/submit/

作答<str:assignmentname>作业中相应id的作业，body含有两个字段，分别是'id'和'content_answer'，id是作答题目的id可以从get中获得，content_answer是作答的信息
### 题目作答规则
答案均由"*<-&&->*"包裹
* 选择题作答规则，以多选a，c，e为例
 content_answer应填"***<-&a&-><-&c&-><-&e&->***"
 得到返回值id和题目的得分如：
`
{
    "id": 2,
    "score": 5
}
`
* 简答题题作答规则，以多选a，b，c为例，第一个空的答案为“床前明月光”第二个空的答案为“疑是地上霜”
 content_answer应填"***<-&床前明月光&-><-&疑是地上霜&->***"
 得到返回值score和comment一般为null（在ai判题开发之前）
 `{
    "id": 1,
    "score": null,
    "comment": null
 }`
* 代码题的作答规则比较特殊，但是每个部分都由数个"*<-&&->*"包裹
 具体来说，comment分为两个部分，语言选择块和代码块
  * 语言选择块由content_answer中**第一个**"*<-&&->*"构成，比如选择cpp则填"*<-&cpp&->*"，选java则为"*<-&java&->*"（现在只开发了cpp）
  * 代码块紧跟在语言选择快之后，由于要实现多文件判题，每个代码块分为两个"*<-&&->*"，第一个中填写文件名，第二中填写相应文件中代码内容，代码块个数没有限制
举一个具体的例子要提交三个文件：
```cpp
//main.cpp
#include<iostream>
#include "header.h"
using namespace std;
int main(){
    function();
    cout<<"Hello World!"<<endl;
    return 0;
}
```  

```cpp
//function.cpp
#include<iostream>
#include"header.h"
using namespace std;
void function(){
    int a;
    cin >> a;
    cout << a << endl;
}
```  

```cpp
//header.h
void function();
```
我们的body需要这样填写：
```json
{
    "id":4,
    "content_answer":"<-&cpp&-><-&main.cpp&-><-&#include<iostream>\n#include \"header.h\"\nusing namespace std;\nint main(){\nfunction();\ncout<<\"Hello World!\"<<endl;\nreturn 0;\n}&-><-&function.cpp&-><-&#include<iostream>\n#include\"header.h\"\nusing namespace std;\nvoid function(){\nint a;\ncin >> a;\ncout << a << endl;\n}&-><-&header.h&-><-&void function();&->"
}
```
得到的返回值：
```json
{
    "id": 4,
    "score": 200,
    "comment": "50 ms 200 KB Output true\n50 ms 200 KB Output true\n"
}
```

> Body Parameters

```json
{
  "id": 1,
  "content_answer": "<-&a&->"
}
```

### Params

|Name|Location|Type|Required|Title|Description|
|---|---|---|---|---|---|
|body|body|object| no ||none|
|» id|body|integer| yes ||none|
|» content_answer|body|string| yes ||每种题型的作答方式不同，具体已经在上方说明|

> Response Examples

> 代码题成功

```json
{
  "id": 4,
  "score": 200,
  "comment": "50 ms 200 KB Output true\n50 ms 200 KB Output true\n"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|代码题成功|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» id|integer|true|none||none|
|» score|integer|true|none||none|
|» comment|string|true|none||none|

## GET 查询特定学生在某题目的全部提交记录

GET /127.0.0.1:8000/home/%3Cstr:coursename%3E/%3Cstr:assignmentname%3E/%3Cint:problem_id%3E/%3Cstr:student%3E/

查询<str:student>（学号）学生在<int:problem_id>题目中的全部回答，如果没有回答返回404, 返回的内容中有一个user_id这与数据库有关前端可以忽略
学生只能查看自己的提交记录，若试图访问其他人的记录则报错403
老师和管理员可以查看所有人的提交记录

> Response Examples

> 成功

```json
[
  {
    "id": 18,
    "user_id": 4,
    "problem_id": 4,
    "submit_time": "2024-02-11T10:48:04.502520Z",
    "content_answer": "<-&cpp&-><-&main.cpp&-><-&#include<iostream>\n#include \"header.h\"\nusing namespace std;\nint main(){\nfunction();\ncout<<\"Hello World!\"<<endl;\nreturn 0;\n}&-><-&function.cpp&-><-&#include<iostream>\n#include\"header.h\"\nusing namespace std;\nvoid function(){\nint a;\ncin >> a;\ncout << a << endl;\n}&-><-&header.h&-><-&void function();&->",
    "score": 200,
    "comment": "50 ms 200 KB Output true\n50 ms 196 KB Output true\n"
  },
  {
    "id": 19,
    "user_id": 4,
    "problem_id": 4,
    "submit_time": "2024-02-11T12:11:59.131085Z",
    "content_answer": "<-&cpp&-><-&main.cpp&-><-&#include<iostream>\n#include \"header.h\"\nusing namespace std;\nint main(){\nfunction();\ncout<<\"Hello World!\"<<endl;\nreturn 0;\n}&-><-&function.cpp&-><-&#include<iostream>\n#include\"header.h\"\nusing namespace std;\nvoid function(){\nint a;\ncin >> a;\ncout << a << endl;\n}&-><-&header.h&-><-&void function();&->",
    "score": 200,
    "comment": "50 ms 196 KB Output true\n50 ms 200 KB Output true\n"
  },
  {
    "id": 20,
    "user_id": 4,
    "problem_id": 4,
    "submit_time": "2024-02-11T12:26:48.094436Z",
    "content_answer": "<-&cpp&-><-&main.cpp&-><-&#include<iostream>\n#include \"header.h\"\nusing namespace std;\nint main(){\nfunction();\ncout<<\"Hello World!\"<<endl;\nreturn 0;\n}&-><-&function.cpp&-><-&#include<iostream>\n#include\"header.h\"\nusing namespace std;\nvoid function(){\nint a;\ncin >> a;\ncout << a << endl;\n}&-><-&header.h&-><-&void function();&->",
    "score": 200,
    "comment": "50 ms 196 KB Output true\n50 ms 196 KB Output true\n"
  }
]
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» id|integer|true|none||none|
|» user_id|integer|true|none||none|
|» problem_id|integer|true|none||none|
|» submit_time|string|true|none||none|
|» content_answer|string|true|none||none|
|» score|integer|true|none||none|
|» comment|string|true|none||none|

## GET 查看全班成员在特定题目的最新提交记录

GET /127.0.0.1:8000/home/%3Cstr:coursename%3E/%3Cstr:assignmentname%3E/%3Cint:problem_id%3E/all/

老师管理员查询<str:coursename>班级<str:assignmentname>作业<int:problem_id>题目全班成员的最新（最后一次提交）答题记录
返回值中包含班级所有成员的最新答题记录，如果没有提交，除了username和first_name其他字段都为null
若简答题没有批改comment和score也会是null。选择题comment也为null

> Response Examples

> 200 Response

```json
[
  {
    "id": 0,
    "problem_id": 0,
    "submit_time": "string",
    "content_answer": "string",
    "score": 0,
    "comment": "string",
    "username": "string",
    "first_name": "string"
  }
]
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» id|integer¦null|true|none||none|
|» problem_id|integer¦null|true|none||none|
|» submit_time|string¦null|true|none||none|
|» content_answer|string¦null|true|none||none|
|» score|integer¦null|true|none||none|
|» comment|string¦null|true|none||none|
|» username|string|true|none||none|
|» first_name|string|true|none||none|

## PUT 为题目评分

PUT /127.0.0.1:8000/home/%3Cstr:coursename%3E/%3Cstr:assignmentname%3E/%3Cint:problem_id%3E/

老师管理员为/<str:coursename>/<str:assignmentname>/<int:problem_id>/学生提交的答案评分
注意对于score字段，前端请限制分数的最大值，布置题目时的分数可从“获取作业中题目”的get方法获取

> Body Parameters

```json
{
  "submission_id": "16",
  "score": 10,
  "comment": "good job"
}
```

### Params

|Name|Location|Type|Required|Title|Description|
|---|---|---|---|---|---|
|body|body|object| no ||none|
|» submission_id|body|string| yes ||none|
|» score|body|integer| yes ||none|
|» comment|body|string| yes ||none|

> Response Examples

> 成功

```json
{
  "success": "score and comment updated"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» success|string|true|none||none|

## DELETE 删除答题记录

DELETE /127.0.0.1:8000/home/%3Cstr:coursename%3E/%3Cstr:assignmentname%3E/%3Cint:problem_id%3E/

老师管理员删除特定的答题记录，可批量删除，成功204

> Body Parameters

```json
{
  "delete_id": [
    3,
    4,
    5,
    6,
    7,
    8
  ]
}
```

### Params

|Name|Location|Type|Required|Title|Description|
|---|---|---|---|---|---|
|body|body|object| no ||none|
|» delete_id|body|[integer]| yes ||none|

> Response Examples

> 204 Response

```json
{}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|删除成功|Inline|

### Responses Data Schema

# Data Schema

<h2 id="tocS_Tag">Tag</h2>

<a id="schematag"></a>
<a id="schema_Tag"></a>
<a id="tocStag"></a>
<a id="tocstag"></a>

```json
{
  "id": 1,
  "name": "string"
}

```

### Attribute

|Name|Type|Required|Restrictions|Title|Description|
|---|---|---|---|---|---|
|id|integer(int64)|false|none||标签ID编号|
|name|string|false|none||标签名称|

<h2 id="tocS_Category">Category</h2>

<a id="schemacategory"></a>
<a id="schema_Category"></a>
<a id="tocScategory"></a>
<a id="tocscategory"></a>

```json
{
  "id": 1,
  "name": "string"
}

```

### Attribute

|Name|Type|Required|Restrictions|Title|Description|
|---|---|---|---|---|---|
|id|integer(int64)|false|none||分组ID编号|
|name|string|false|none||分组名称|

<h2 id="tocS_Pet">Pet</h2>

<a id="schemapet"></a>
<a id="schema_Pet"></a>
<a id="tocSpet"></a>
<a id="tocspet"></a>

```json
{
  "id": 1,
  "category": {
    "id": 1,
    "name": "string"
  },
  "name": "doggie",
  "photoUrls": [
    "string"
  ],
  "tags": [
    {
      "id": 1,
      "name": "string"
    }
  ],
  "status": "available"
}

```

### Attribute

|Name|Type|Required|Restrictions|Title|Description|
|---|---|---|---|---|---|
|id|integer(int64)|true|none||宠物ID编号|
|category|[Category](#schemacategory)|true|none||分组|
|name|string|true|none||名称|
|photoUrls|[string]|true|none||照片URL|
|tags|[[Tag](#schematag)]|true|none||标签|
|status|string|true|none||宠物销售状态|

#### Enum

|Name|Value|
|---|---|
|status|available|
|status|pending|
|status|sold|

