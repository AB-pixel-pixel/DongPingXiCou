from openvino.runtime import Core, PartialShape 
from openvino.offline_transformations import serialize
from pathlib import Path
import numpy as np
import cv2

"""
这份代码在设置好模型路径之后，运行得到的结果是：
{<ConstOutput: names[output] shape{1,1} type: f32>: array([[-2.247045]], dtype=float32)}
这个数据类型我不懂，然后输出的好像是array这一列里面的东西，我不知道怎么弄出来
然后就是，我输入的是错误的图片，然后得到的是负数，所以，负数代表假脸，对吗？
"""

model_path="model/deepfake_detection_model.xml"

test = 1
reshape_model_batch_size = 0
enable_caching = True


def check_device():
    if test:
        devices = ie.available_devices
        for device in devices:
            device_name = ie.get_property(device_name=device, name="FULL_DEVICE_NAME")
            print(f"{device}: {device_name}")


def network(model_path="model/deepfake_detection_model.xml"):
    # init ie
    ie = Core()
    model = ie.read_model(model=model_path)
    # cache model
    cache_path = Path("model/model_cache")
    cache_path.mkdir(exist_ok=True)
    config_dict = {"CACHE_DIR": str(cache_path)}
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
        image_filename = "../../save/test.jpg"
        image = cv2.imread(image_filename)
        N, C, H, W = input_layer.shape
        resized_image = cv2.resize(src = image, dsize=(W,H))
        input_data = np.expand_dims(np.transpose(resized_image, (2, 0, 1)), 0).astype(np.float32)
        if test: 
            print("image.shape:",image.shape)
            print("input_data.shape:",input_data.shape)

        compiled_model = ie.compile_model(model=model,device_name="GPU", config=config_dict)
        # inference
        yield compiled_model([input_data])

            
    

"""以下代码用于将模型从onnx文件转换为IR文件"""
def convert(model_path):
    model = ie.read_model(model=model_path)
    serialize(model=model, model_path="model/deepfake_detection_model.xml", weights_path="model/deepfake_detection_model.bin")

def main():
    ie = Core()
    # check_device()
    # convert(model_path)
    network_infer = next(network(model_path))
    print(network_infer)

main()
