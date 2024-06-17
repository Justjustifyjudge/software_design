'''
Author: lin
Time: 2024年4月22日10:40:22
Description: 实现摄像头的调用，人脸检测和验证的合并
'''
import cv2
from deepface import DeepFace

# 初始化摄像头
cap = cv2.VideoCapture(0)

# 调整摄像头捕捉的图像大小
cap.set(3, 640)  # 宽度
cap.set(4, 480)  # 高度

# 设置用于比对的人脸图像文件夹路径
base_folder = r'C:\Users\linyiwu\Desktop\datasets\face\train'
img2_pathe = r"C:\Users\linyiwu\Desktop\datasets\face\train\0001.jpg"

while True:
    ret, frame = cap.read()

    # 保存摄像头捕捉的图像到临时文件
    temp_face_path = r"C:\Users\linyiwu\Desktop\datasets\face\train\temp_face.jpg"
    cv2.imwrite(temp_face_path, frame)

    # 调用DeepFace进行人脸验证
    try:
        # result = DeepFace.verify(img1_path=temp_face_path, img2_path=img2_path, model_name='GhostFaceNet', enforce_detection=False)
        # Debug
        # result = DeepFace.verify(img1_path=img2_pathe, img2_path=img2_pathe, model_name='DeepFace', enforce_detection=False)
        result = DeepFace.verify(img1_path=r'C:\Users\linyiwu\Desktop\datasets\face\train\temp_face.jpg', img2_path=r"C:\Users\linyiwu\Desktop\datasets\face\train\0001.jpg")

        # 提取验证结果
        verified = result['verified']
        distance = result['distance']

        if verified:
            verified_text = f"Verified: {verified} - distance: {distance:0.4}"
        else:
            verified_text = f"Not Verified - distance: {distance:0.4}"

        cv2.putText(frame, verified_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # 显示图像
        cv2.imshow('Face Verification', frame)
    except:
        cv2.imshow('Face Verification', frame)
        print("No face detected")
    # 按下 'q' 键退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头资源并关闭窗口
cap.release()
cv2.destroyAllWindows()


# from deepface import DeepFace
# import matplotlib.pyplot as plt
# import cv2

# result = DeepFace.verify(img1_path=r"C:\Users\linyiwu\Desktop\datasets\face\train\0001.jpg",
#                           img2_path=r"C:\Users\linyiwu\Desktop\datasets\face\train\0001.jpg",
#                           model_name='VGG-Face')

# fig, axs = plt.subplots(1, 2, figsize=(10, 5))
# axs[0].imshow(plt.imread(r"C:\Users\linyiwu\Desktop\datasets\face\train\0001.jpg"))
# axs[1].imshow(plt.imread(r"C:\Users\linyiwu\Desktop\datasets\face\train\0001.jpg"))
# fig.suptitle(f"Verified: {result['verified']} - distance: {result['distance']:0.4}")
# plt.show()