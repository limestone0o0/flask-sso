# flask-sso
基本单点登录系统流程的flask实现


### 技术栈：

 1. flask
 2. redis
 3. gevent
 4. json web token(jwt)
 5. jsonp
 6. mysql


### 安装:


  女装python3.5

  pip instrall -r requirements.txt


### 使用：

直接启动flask项目，对接ip，数据库地址等配置


#### login目录

此目录为sso登录的客户端，使用django填写，使用时需要修改回调函数跳转的路由

请求格式：

类型：get

参数：token，回调函数地址


数据库建表需要统一名称（可以自行修改）：

表名：userinfo

用户名：user_name

密码：user_passwd



#### ssologin目录



验证返回代码：

400：验证成功

401：没有token，重新登录

402：用户不存在

403：密码错误

404: sid不存在


#### 压力测试


https://img2018.cnblogs.com/blog/1458446/201911/1458446-20191121215056154-592494899.png
