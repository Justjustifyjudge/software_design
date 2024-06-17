import base64
import io
import os.path
import face_recognition
from PIL import Image

current_path = os.getcwd()
test_folder_path = os.path.join(current_path, 'App', 'test_img')
known_faces_dir = os.path.join(os.getcwd(), 'App', 'faces_db', 'known_faces')


def loadface(path):
    names = []
    encodings = []
    encoding = []
    for filename in os.listdir(path):
        if filename.lower().endswith(".png"):
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
                # 从文件名中获取人脸名称，去掉".png"
                name = os.path.splitext(filename)[0]
                names.append(name)
    return encodings,names


# 判断base64格式的图片是否属于已知人像库
def checkface(base64_str):
    folder_name = 'test_img'
    base64_data = base64_str.split(',')[1]
    image_bytes = base64.b64decode(base64_data)
    image_io = io.BytesIO(image_bytes)
    image = Image.open(image_io)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    file_name = 'test.png'
    aim_path = os.path.join(test_folder_path, file_name)
    image.save(aim_path)
    print(aim_path)
    known_face_encodings, known_face_names = loadface(known_faces_dir)
    print(known_face_names)
    unknown_face_encodings, unknown_face_names = loadface(test_folder_path)
    for face_encoding in unknown_face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
        # # If a match was found in known_face_encodings, just use the first one.
        for i in range(len(matches)):
            if matches[i]:
                return known_face_names[i]
    return ''