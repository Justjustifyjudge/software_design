from ultralytics import YOLO
import cv2
predit_model=YOLO(r'C:\Users\linyiwu\Desktop\software_design\src\后端整合\flask-LiteAI-main\myweb-flask\App\fire_smoke_detect_mode\ultralytics\ultralytics\model_onnx\best_3epoch.pt')
# predit_model.predict(source=0,save=True)
from PIL import Image
from flask import Flask, Response

from ultralytics import YOLO
import cv2
import base64

##################################

# Run inference
# results = model('test.jpg') # results list
# Show the results
# for r in results:
    # im_array = r.plot()# plot a BGR numpy array of predictions
    # im = Image.fromarray(im_array[..., ::-1])# RGB PIL image
    # im.show()# show image
    # im.save('results.jpg')# save image
##################################################################

model=YOLO(r'src\后端整合\flask-LiteAI-main\myweb-flask\App\onnxfile\fire_survellance\best2.pt',task='detect')
def main():
    # 打开摄像头
    cap = cv2.VideoCapture(0)

    # 检查摄像头是否成功打开
    if not cap.isOpened():
        print("无法打开摄像头")
        return

    # 读取第一帧图像
    ret, frame = cap.read()

    # 检查是否成功读取图像
    if not ret:
        print("无法读取图像")
        return

    # 保存第一帧图像
    # cv2.imwrite('first_frame.jpg', frame)
    while True:
        # 读取一帧图像
        ret, frame = cap.read()
        pred = predit_model(frame)

        print(pred['bbox'])
        # 检查是否成功读取图像
        if not ret:
            print("无法读取图像")
            break
        

        # 显示图像
        cv2.imshow('Camera', frame)

        # 保存当前帧图像
        cv2.imwrite('current_frame.jpg', frame)

        # 检测键盘按键，如果按下 q 键则退出循环
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 释放摄像头对象
    cap.release()

    # 关闭所有打开的窗口
    cv2.destroyAllWindows()

def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            return None
        # 进行模型预测等处理
        pred = predit_model(frame)
        # bbox = pred['bbox']

        
        # 将图像编码为JPEG格式并转换为base64字符串
        _, buffer = cv2.imencode('.jpg', frame)
        frame_data = base64.b64encode(buffer).decode('utf-8')
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_data.encode() + b'\r\n')

def gen_frames(img):
    results = model(img)
    for r in results:
        im_array = r.plot()# plot a BGR numpy array of predictions
        boxes = r.boxes
        # box=boxes[0].conf
        for box in boxes:
            config = box.conf
        im = Image.fromarray(im_array[..., ::-1])# RGB PIL image
    return im, config


if __name__ == "__main__":
    main()
