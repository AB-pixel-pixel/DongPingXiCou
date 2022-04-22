'''
import os
import random 
from flask import Flask, flash, request, redirect
from werkzeug.utils import secure_filename

"""上传文件后用网络处理，然后显示纯文本消息，要再次上传就要重新发送请求（刷新网页）"""

UPLOAD_FOLDER = '/home/ab/Desktop/uploads' # 路径
ALLOWED_EXTENSIONS = {'png','jpg','jpeg'}  # 接受的文件后缀名

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

""" 假神经网络 """
def network(): 
    return random.randint(0,1) > 0.5


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
            app.config["path"]=(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  
        if network():
            return "real"
        else:
            return "fake"

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

'''
