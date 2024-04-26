import face_recognition
import cv2
import numpy as np
import os
import time



video_capture = cv2.VideoCapture(0)
# 空列表，用于存储对应的人脸名称 编码
unknown_face_folder=r"C:\Users\nan\Desktop\facecog\unknown"
# 已知人脸文件夹
folder_path=r"C:\Users\nan\Desktop\facecog\i_know"


def loadface(path):
    names = []
    encodings = []
    encoding = []
    for filename in os.listdir(path):
        # 检查是否是jpg格式的图片文件
        if filename.lower().endswith(".jpg"):
            # 构造完整的文件路径
            image_path = os.path.join(path, filename)

            # 加载图片
            image = face_recognition.load_image_file(image_path)

            # 获取图片中所有人脸的编码
            encoding = face_recognition.face_encodings(image)

            # 确保图片中有人脸
            if encoding:
                # 将第一个（也是唯一的）人脸编码添加到列表中
                encodings.append(encoding[0])

                # 从文件名中获取人脸名称，去掉".jpg"
                name = os.path.splitext(filename)[0]
                names.append(name)
    return (encodings,names)


# Initialize some variables
known_face_encodings,known_face_names= loadface(folder_path)
known_unknown_face_encodings,known_unknown_face_names=loadface(unknown_face_folder)


face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Only process every other frame of video to save time
    if process_this_frame:
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        #rgb_small_frame = small_frame[:, :, ::-1]
        rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")
        #print(face_locations)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name, encoding in zip(face_locations, face_names, face_encodings):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        if name == "Unknown":

            #如果能在陌生人中找到 不保存进unknown文件夹，否则保存
            # 裁剪出未知人脸的区域q
            print("Unknown")
            # # 检查这个人脸是否已经存在于未知人脸文件夹中
            matches = face_recognition.compare_faces(known_unknown_face_encodings, encoding,tolerance=0.5)
            print(matches)
            if not any(matches):
                # 报警（未实现）
                print("new")
                # 如果没有找到匹配项，保存这个新的人脸
                timestamp = int(time.time())  # 使用当前时间戳作为文件名
                filename = os.path.join(unknown_face_folder, f"Unknown_face_{timestamp}.jpg")
                face = frame[top:bottom, left:right]
                # 保存未知人脸的图像
                cv2.imwrite(filename, face)
                print(f"Unknown face saved as {filename}")
                known_unknown_face_encodings.append(encoding)
                known_unknown_face_names.append(f"Unknown_face_{timestamp}")

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
