from ultralytics import YOLO
import cv2
predit_model=YOLO(r'C:\Users\linyiwu\Desktop\software_design\src\后端整合\flask-LiteAI-main\myweb-flask\App\fire_smoke_detect_mode\ultralytics\ultralytics\model_onnx\best_3epoch.pt')
# predit_model.predict(source=0,save=True)

from flask import Flask, Response

from ultralytics import YOLO
import cv2
import base64

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
    ret, frame = cap.read()
    if not ret:
        return None
    # 进行模型预测等处理
    pred = predit_model(frame)
    
    # 将图像编码为JPEG格式并转换为base64字符串
    _, buffer = cv2.imencode('.jpg', frame)
    frame_data = base64.b64encode(buffer).decode('utf-8')
    
    return frame_data

if __name__ == "__main__":
    main()
