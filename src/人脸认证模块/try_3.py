import cv2
import numpy as np
from deepface import DeepFace

# 初始化摄像头
cap = cv2.VideoCapture(0)

# 调整摄像头捕捉的图像大小
cap.set(3, 640)  # 宽度
cap.set(4, 480)  # 高度

# 加载人脸检测器
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# 加载预先录入的人脸信息
known_face_img = cv2.imread(r"C:\Users\linyiwu\Desktop\datasets\face\train\0002.jpg")
known_face_encoding = DeepFace.represent(known_face_img)

while True:
    ret, frame = cap.read()
    frame = cv2.imread(r"C:\Users\linyiwu\Desktop\datasets\face\train\0002.jpg")
    # 将图像转换为灰度图像
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 在图像中检测人脸
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # 对检测到的人脸进行处理
    for (x, y, w, h) in faces:
        # 在人脸周围绘制矩形
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # 获取人脸图像并提取特征
        face_img = frame[y:y + h, x:x + w]
        current_face_encoding = DeepFace.represent(face_img)

        # 进行人脸识别
        result = DeepFace.verify(known_face_encoding=known_face_encoding, 
                                 current_face_encoding=current_face_encoding)

        # 显示验证结果
        verified_text = "Verified" if result["verified"] else "Not Verified"
        cv2.putText(frame, verified_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # 显示图像
    cv2.imshow('Face Recognition', frame)

    # 按下 'q' 键退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头资源并关闭窗口
cap.release()
cv2.destroyAllWindows()
