# import cv2
# import face_recognition
# import os

# known_faces_folder = r"C:\Users\linyiwu\Desktop\datasets\face\train"


# # 加载已知人脸的图像和名称
# known_face_encodings = []
# known_face_names = []

# # 添加已知人脸
# for filename in os.listdir(known_faces_folder):
#     if filename.endswith(".jpg") or filename.endswith('.png'):
#         #加载图像文件
#         image_path = os.path.join(known_faces_folder, filename)
#         image = face_recognition.load_image_file(image_path)

#         # 获取图像中的人脸特征向量
#         face_encoding = face_recognition.face_encodings(image)[0]

#         # 获取人脸名称
#         name = os.path.splitext(filename)[0]
        
#         # 将人脸特征向量和名称添加到已知人脸列表中
#         known_face_encodings.append(face_encoding)
#         known_face_names.append(name)

# # 打开摄像头
# video_capture = cv2.VideoCapture(0)

# while True:
#     # 读取一帧视频
#     ret, frame = video_capture.read()

#     # 将彩色帧转换为RGB帧（face_recognition库要求输入RGB图像）
#     rgb_frame = frame[:, :, ::-1]

#     # 在图像中查找人脸位置
#     face_locations = face_recognition.face_locations(rgb_frame)
#     face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

#     for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
#         # 对比已知人脸与当前检测到的人脸
#         matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

#         name = "Unknown"

#         # 如果找到了匹配的人脸
#         if True in matches:
#             first_match_index = matches.index(True)
#             name = known_face_names[first_match_index]

#         # 在图像中绘制人脸边界框和姓名
#         cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
#         font = cv2.FONT_HERSHEY_DUPLEX
#         cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

#     # 显示结果
#     cv2.imshow('Video', frame)

#     # 按下q退出循环
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # 关闭摄像头和窗口
# video_capture.release()
# cv2.destroyAllWindows()


import cv2
import face_recognition

# 初始化摄像头
cap = cv2.VideoCapture(0)

# 调整摄像头捕捉的图像大小
cap.set(3, 640)  # 宽度
cap.set(4, 480)  # 高度

# 加载已知人脸图像并提取特征
known_face_img = face_recognition.load_image_file(r"C:\Users\linyiwu\Desktop\datasets\face\train\0002.jpg")
known_face_encoding = face_recognition.face_encodings(known_face_img)[0]

while True:
    ret, frame = cap.read()

    # 将图像转换为 RGB 格式（face_recognition 要求输入为 RGB 格式）
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 在图像中检测人脸
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # 对检测到的人脸进行处理
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # 进行人脸识别
        matches = face_recognition.compare_faces([known_face_encoding], face_encoding)
        name = "Unknown"

        if matches[0]:
            name = "Known Person"

        # 在人脸周围绘制矩形并显示姓名
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    # 显示图像
    cv2.imshow('Face Recognition', frame)

    # 按下 'q' 键退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头资源并关闭窗口
cap.release()
cv2.destroyAllWindows()
