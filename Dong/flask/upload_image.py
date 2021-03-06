import os, sys
import random 
from pathlib import Path
from flask import Flask, flash, request, redirect
from werkzeug.utils import secure_filename

# 运行说明：
"""上传文件后用网络处理，然后显示纯文本消息，要再次上传就要重新发送请求（刷新网页）"""


# 路径
"""
注意,
人脸识别模型名称必须为:haarcascade_frontalface_alt2.xml
神经网络模型为IR文件:deepfake_detection_model.xml
"""

current_file_path=Path(os.path.abspath(__file__))
openvino_module_path=current_file_path.parent /'openvino_deploy'  # 模块的路径
save_image_path=current_file_path.parent.parent /'save'
extract_face_model_path = current_file_path.parent \
    / 'openvino_deploy/model/haarcascade_frontalface_alt2.xml' # 人脸识别模型路径
extract_face_model_path=str(extract_face_model_path) # opencv函数要求参数为str类型
model_path = current_file_path.parent \
    / 'openvino_deploy/model/deepfake_detection_model.xml'

# 导入模块函数
# print(openvino_module_path)
openvino_module_path = str(openvino_module_path)
sys.path.append(openvino_module_path)
from network import deepfake_detection_network

ALLOWED_EXTENSIONS = {'png','jpg','jpeg'}  # 接受的文件后缀名
"""
env = os.environ.setdefault('FLASK_ENV','devlop')

app = create_app(env)
manager = Manager(app)"""
app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = save_image_path
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS
    
@app.route('/',methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            app.config["image_path"]=(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  
            # result的取值为1，则图片为真，为0，则图片为假
            result = deepfake_detection_network(model_path = model_path,\
                extract_face_model_path = extract_face_model_path,\
                image_path=app.config["image_path"],\
                    test = 0)
            if os.path.exists(app.config["image_path"]):
                os.remove(app.config["image_path"])
            if result == 1:
                return "real_face"
            elif result == -1:
                return "couldn't find face"
            elif result == 0:
                return "fake_face"

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
