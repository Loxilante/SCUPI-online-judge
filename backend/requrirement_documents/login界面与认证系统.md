# login page：
## 功能描述：
登录页面，处理用户账号的登录
## login page 使用的api：1


# 认证系统：
用户通过1号接口登录，登录之后后端会给前端设置6个cookie（详见api文档），其中包含access token与refresh token
access token的持续时间为5 min，refresh token的持续时间为1 day
如果access token过期且refresh token没有过期的情况下可用refresh token从3号接口申请一个access token，若refresh token过期则需要重新登录。
整个网站除了1号与3号api在请求时都需要access token。
## 认证系统所使用的api：1，2，3