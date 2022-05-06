# -


----服务器----
目前服务器可以满足基本需求

# 如何让代码运行
## 环境
### 安装flask
教程：（其中的虚拟环境可以由anaconda的环境去替代）
https://flask.net.cn/installation.html
### 安装openvino 2022.1 （可选）
### 模型准备 （可选）
所有模型都放在model文件夹中，
包括，
人脸识别的模型（xml文件）
deepfake detection的模型（IR文件）

### 如果没有Openvino可以：
用首页的upload_image.py去替代Dong里的upload_image.py
里面有假模型，可以满足通信测试
### 接下来的步骤都一样

进入Dong/flask文件夹,在文件夹中打开Linux终端依次输入

export FLASK_APP=upload_image.py

export FLASK_ENV=development

下面这行代码会让你的操作系统监听所有公开的IP，大概的范围是局域网
（连接同一个wifi的设备，一个校区内的校园网我也不知道算不算是同一个wifi，我在宿舍用两台电脑连校园网，他们确实可以互相通讯）

flask run --host=0.0.0.0 

下面这行 仅限于本机内通信

flask run 
