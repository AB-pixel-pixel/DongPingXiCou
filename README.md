# -
东拼西凑组作品
## 目前已经完成主要任务：
剩下的工作是：
### 必做：
1.打卡、检查视频是否看完
2.测试
### 可做：
3.设计神经网络和服务器双线程
4.测试
### 可以但没必要做：
5.优化网络设计、公开服务器
6.测试




## 目前的网络示意图


![示意图](https://user-images.githubusercontent.com/89346035/164224854-263a489c-eb50-4189-8952-6c02338219a9.png)



----服务器搭建----
目前服务器仅供测试

## 主要参考教程：

### 安装flask
教程
https://flask.net.cn/installation.html

### 如何让代码运行
进入DongPingXiCou文件夹

在终端依次输入

export FLASK_APP=upload_image.py

export FLASK_ENV=development

下面这行代码会让你的操作系统监听所有公开的IP，大概的范围是局域网
（连接同一个wifi的设备，一个校区内的校园网我也不知道算不算是同一个wifi，我在宿舍用两台电脑连校园网，他们确实可以互相通讯）

flask run --host=0.0.0.0 

下面这行 仅限于本机内通信

flask run 


### 服务器的搭建主要参考这个
https://flask.net.cn/patterns/fileuploads.html

# 目前以实现功能为主要目的，没有怎么考虑安全性或者前端设计
