# -
东拼西凑组作品


----服务器搭建----
目前服务器仅供测试

## 主要参考教程：

### 安装flask
教程
https://flask.net.cn/installation.html

### 如何让代码运行
首先确保终端的环境中有flask，和openvino。如果没有Openvino可以：
## 没有openvino
用首页的upload_image.py去替代Dong里的upload_image.py

进入Flask文件夹,打开终端依次输入

export FLASK_APP=upload_image.py

export FLASK_ENV=development

下面这行代码会让你的操作系统监听所有公开的IP，大概的范围是局域网
（连接同一个wifi的设备，一个校区内的校园网我也不知道算不算是同一个wifi，我在宿舍用两台电脑连校园网，他们确实可以互相通讯）

flask run --host=0.0.0.0 

下面这行 仅限于本机内通信

flask run 
