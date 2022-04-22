from openvino.runtime import Core, PartialShape 
from openvino.offline_transformations import serialize
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import cv2

"""可以独立测试,使用test()函数,测试后,记得删掉 test() 语句"""

# 此处修改文件路径
model_path="model/deepfake_detection_model.xml"
extract_face_model_path="model/haarcascade_frontalface_alt2.xml"
image_path="../../save/true1.jpeg" # 修改此处
test = 0
reshape_model_batch_size = False
enable_caching = False

def extract_face(image_path,extract_face_model_path,test):
    '''提取图像中的一张人脸，输出的数据可以直接放入神经网络'''
    image = cv2.imread(filename=image_path)
    cascade = cv2.CascadeClassifier(extract_face_model_path)
    rects = cascade.detectMultiScale(image, \
        scaleFactor=1.3, minNeighbors=4, minSize=(30, 30),flags=cv2.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:, 2:] += rects[:, :2]
    for x1,y1,x2,y2 in rects:
        # 调整人脸截取的大小。横向为x,纵向为y
        # TODO 就是可以优化这个矩形，例如，将矩形摆正或者之类的
        image_roi = image[y1-15 :y2+30, x1-50 :x2]
    #  展示出人脸
    if test:
        try: 
            plt.imshow(image_roi)
        except ValueError:
            return image # 识别不到人脸，返回原图
    input_image = cv2.resize(image_roi, (224, 224))
    input_image = np.expand_dims(input_image.transpose(2, 0, 1), 0)
    return input_image 

def check_device():
    """检查设备可用情况"""
    if test:
        devices = ie.available_devices
        for device in devices:
            device_name = ie.get_property(device_name=device, name="FULL_DEVICE_NAME")
            print(f"{device}: {device_name}")


def deepfake_detection_network(image_path,model_path,extract_face_model_path,test=0): 
    # init ie
    ie = Core()
    model = ie.read_model(model=model_path)
    # cache model
    """ cache_path = Path("model/model_cache")
    cache_path.mkdir(exist_ok=True)
    config_dict = {"CACHE_DIR": str(cache_path)}"""
    # compile model
    if enable_caching:
        compiled_model = ie.compile_model(model=model,device_name="GPU", config=config_dict)
    else:
        compiled_model = ie.compile_model(model=model,device_name="GPU")
    input_layer = compiled_model.input(0)
    output_layer = compiled_model.output(0)
    # reshape_model_batch_size
    if reshape_model_batch_size: 
        new_shape = PartialShape([1, 3, 224, 224])
        model.reshape({input_layer.any_name: new_shape})
    # check the model infomation
    if test: 
        print(model.input(0).any_name)
        print(f"input precision: {input_layer.element_type}")
        print(f"input shape: {input_layer.shape}")
        print(model.output(0).any_name)
        print(f"output precision: {output_layer.element_type}")
        print(f"output shape: {output_layer.shape}")

    # inference status
    # process image
    while True:
        input_data = extract_face(image_path=image_path,\
                extract_face_model_path=extract_face_model_path,test=test)
        # inference
        try:
            result = list(compiled_model([input_data]).values())[0][0][0]
            print(result)
        except RuntimeError : # 图片为空时，flask会报的错误
            return -1
        except AttributeError : # 图片为空时，单独调试时，报的错
            return "no face"
        if result > 0 :
            result = 1
        else:
            result = 0
        return result #TODO 返回给服务器
            
    

"""以下代码用于将模型从onnx文件转换为IR文件"""
def convert(model_path):
    ie = Core()
    model = ie.read_model(model=model_path)
    serialize(model=model, model_path="model/deepfake_detection_model.xml",\
         weights_path="model/deepfake_detection_model.bin")

def test():
    # check_device()
    # convert(model_path)
    print(deepfake_detection_network(image_path=image_path,\
        model_path=model_path,\
        extract_face_model_path=extract_face_model_path,test=test))
    # next(network(image_path=image_path,model_path=model_path))

test()
