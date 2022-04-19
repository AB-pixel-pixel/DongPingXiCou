import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import random

UPLOAD_FOLDER = '/home/ab/Project/save' # 图片储存路径
ALLOWED_EXTENSIONS = {'png','jpg','jpeg'} # 输入格式仅限于这三种

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

# 假神经网络
def network_infer():
    random.randint(0,1)

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
        try:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  
        except FileNotFoundError :
            return redirect(url_for('error'))
        finally:
            result = network_infer()
            if result :
                return redirect(url_for('real'))
            else:
                return redirect(url_for('fake'))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/error',methods=['GET','POST'])
def error():
    return f'{app.config["path"]}'

@app.route('/real',method=['GET','POST'])
def real():
    return f'图片为真'

@app.route('/fake',method=['GET','POST'])
def fake():
    return f'图片为假'
