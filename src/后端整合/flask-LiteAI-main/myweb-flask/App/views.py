import io
from flask import Blueprint, jsonify, request, Flask, send_file, Response, send_from_directory, abort
from .models import *
from flask_jwt_extended import create_access_token
import os, base64
from datetime import datetime
from werkzeug.utils import secure_filename
from App.lpdr.lpdr import lp_img_preprocess, lp_refer, lp_postprocess, lp_generate_result
from App.ppocrv3.ppocrv3 import pp_img_preprocess, pp_refer, pp_postprocess, pp_generate_result
from App.utils import checkface
# from App.fire_smoke_detect_mode.ultralytics.ultralytics.try_predict import generate_frames, gen_frames
# from App.face_recognition_mode.try_4 import loadface
from PIL import Image
from io import BytesIO
import face_recognition
import numpy as np
import winsound
import time
from App.alarm.alarm import alarm_smoke, recognize_person
# from flask_socketio import SocketIO, emit
import cv2

blue = Blueprint('user', __name__)
# socketio = SocketIO(blue)

# 已知人脸文件夹
known_faces_dir = os.path.join(os.getcwd(), 'App', 'faces_db', 'known_faces')
# 未知人脸文件夹
unknown_faces_dir = os.path.join(os.getcwd(), 'App', 'faces_db', 'unknown_faces')

camera = cv2.VideoCapture(0)
streaming_smoke = True
streaming = True

# # 人脸识别参数初始化
# known_face_encodings,known_face_names = loadface(known_faces_dir)
# known_unknown_face_encodings, known_unknown_face_names = loadface(unknown_faces_dir)
# face_locations = []
# face_encodings = []
# face_names = []
# process_this_frame = True


@blue.route('/')
def test():
    return '服务器可用'


@blue.route('/test/', methods=['GET'])
def index():
    return jsonify({
        'code': 0,
        'data': {
            'data': "flask + vue3 成功连通（跨域）！"
        }
    })


@blue.route('/users/loginByFace/', methods=['GET', 'POST'])
def user_loginByFace():
    vue_peopleface = request.form.get('base64str')
    vue_username = checkface(vue_peopleface)
    if vue_username != '':
        filter_user = list(User.query.filter(User.username == vue_username))
        flask_username = filter_user[0].username
        access_token = filter_user[0].access_token
        flask_identity = filter_user[0].identity
        img_filename = flask_username + '.png'
        img_data = open(os.path.join(known_faces_dir, img_filename), "rb").read()
        img_data = base64.b64encode(img_data).decode('utf-8')
        token = access_token
        res = jsonify({
            "success": True,
            "state": 1,
            "message": "登录成功",
            "content": {
                "access_token": token,
                "token_type": "string",
                "img_data": img_data,
                "username": flask_username,
                "identity": flask_identity
            }
        })
        return res
    else:
        res = jsonify({
            'success': False,
            'state': 0,
            'message': '登录失败',
            "content": {
                "access_token": 'null',
                "token_type": "null"
            }
        })
        return res


@blue.route('/users/login/', methods=['GET', 'POST'])
def user_login():
    vue_username = request.form.get('username')
    vue_password = request.form.get('password')

    # 验证用户名和密码
    u = User()
    flask_username = list(User.query.filter(User.username == vue_username))
    flask_password = list(User.query.filter(User.username == vue_username).filter(User.password == vue_password))

    # 用户存在
    if flask_username and flask_password:
        flask_username = flask_username[0].username
        access_token = flask_password[0].access_token
        flask_identity = flask_password[0].identity
        token = access_token
        img_filename = flask_username + '.png'
        if os.path.exists(os.path.join(known_faces_dir, img_filename)):
            img_data = open(os.path.join(known_faces_dir, img_filename), "rb").read()
            img_data = base64.b64encode(img_data).decode('utf-8')
        else:
            img_data = open(os.path.join(known_faces_dir, '101.png'), "rb").read()
            img_data = base64.b64encode(img_data).decode('utf-8')
        res = jsonify({
            "success": True,
            "state": 1,
            "message": "登录成功",
            "content": {
                "access_token": token,
                "token_type": "string",
                "img_data": img_data,
                "username": flask_username,
                "identity": flask_identity
            }
        })
        return res
    else:
        res = jsonify({
            'success': False,
            'state': 0,
            'message': '登录失败，用户名或密码错误',
            "content": {
                "access_token": 'null',
                "token_type": "null"
            }
        })
        return res


@blue.route('/users/addUser/', methods=['GET', 'POST'])
def user_register():
    vue_username = request.form.get('username')
    vue_password = request.form.get('password')
    vue_base64codeImg = request.form.get('base64str')
    vue_identity = request.form.get('identity')
    if request.form.get('identity'):
        vue_identity = '超级管理员'
    else:
        vue_identity = '普通用户'
    u = User()
    flask_username = list(User.query.filter(User.username == vue_username))
    if flask_username:
        res = jsonify({
            'success': False,
            'state': 0,
            'message': '用户已存在',
            "content": {
                "access_token": 'null',
                "token_type": "null"
            }
        })
        return res
    else:
        u.identity = vue_identity
        u.username = vue_username
        u.password = vue_password
        u.identity = vue_identity
        token = create_access_token(identity=vue_username)
        u.access_token = token
        try:
            db.session.add(u)
            db.session.commit()
            res = jsonify({
                "success": True,
                "state": 1,
                "message": "注册成功",
                "content": {
                    "access_token": 'null',
                    "token_type": "null"
                }
            })
            base64_data = vue_base64codeImg.split(',')[1]
            image_bytes = base64.b64decode(base64_data)
            image_io = io.BytesIO(image_bytes)
            image = Image.open(image_io)
            image.save(os.path.join(known_faces_dir, vue_username)+'.png')
            return res
        except Exception as e:
            print(e)
            db.session.rollback()
            db.session.flush()
            res = jsonify({
                'success': False,
                'state': 0,
                'message': '注册失败',
                "content": {
                    "access_token": 'null',
                    "token_type": "null"
                }
            })
            return res


@blue.route('/users/logout/', methods=['POST'])
def user_logout():
    res = jsonify({
        'success': True,
        'state': 1,
        'message': '退出成功',
        "content": {
            "access_token": '不需要返回',
            "token_type": "不需要返回"
        }
    })
    return res


@blue.route('/users/getAll/', methods=['GET'])
def user_getAll():
    now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    arr = []
    for i in range(len(User.query.all())):
        temp = []
        user_id = User.query.all()[i].id
        temp.append(user_id)
        user_identity = User.query.all()[i].identity
        temp.append(user_identity)
        user_username = User.query.all()[i].username
        temp.append(user_username)
        user_password = User.query.all()[i].password
        temp.append(user_password)
        access_token = User.query.all()[i].access_token
        temp.append(access_token)
        arr.append(temp)

    res = []
    for i in range(len(arr)):
        tp = {
            'id': arr[i][0],
            'identity': arr[i][1],
            'username': arr[i][2],
            'password': arr[i][3],
            'token': arr[i][4]
        }
        res.append(tp)

    result = jsonify({
        'code': '000000',
        'data': res,
        'message': '处理成功',
        'time': now_time
    })
    return result


@blue.route('/users/delete/<string:id>', methods=['DELETE'])
def user_del(id):
    u = User.query.get(id)
    now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        db.session.delete(u)
        db.session.commit()
        result = jsonify({
            'code': '000000',
            'data': True,
            'message': '处理成功',
            'time': now_time
        })
        return result
    except Exception as e:
        print(e)
        db.session.rollback()
        db.session.flush()
        result = jsonify({
            'code': '111111',
            'data': False,
            'message': '处理失败',
            'time': now_time
        })
        return result


@blue.route('/users/getFaceById/<string:id>', methods=['POST'])
def user_get_face(id):
    u = User.query.get(id)
    now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    img_data = ''
    if u:
        img_filename = u.username + '.png'
        if os.path.exists(os.path.join(known_faces_dir, img_filename)):
            img_data = open(os.path.join(known_faces_dir, img_filename), "rb").read()
            img_data = base64.b64encode(img_data).decode('utf-8')
            res = jsonify({
                'code': '000000',
                'data': True,
                'message': img_data,
                'time': now_time
            })
            return res
    img_data = open(os.path.join(known_faces_dir, '101.png'), "rb").read()
    img_data = base64.b64encode(img_data).decode('utf-8')
    res = jsonify({
        'code': '111111',
        'data': False,
        'message': img_data,
        'time': now_time
    })
    return res


@blue.route('/users/upload/', methods=['GET', 'POST'])
def user_upload():
    rec_ = []
    if request.method == 'POST':
        file = request.files.get('file')
        if file is not None:
            filename = secure_filename(file.filename)
            data = request.form.get('data')
            img_path = 'src/后端整合/flask-LiteAI-main/myweb-flask/App/static/img/resource/' + str(data) + '/' + filename
            file.save(img_path)
            infer_result = 'src/后端整合/flask-LiteAI-main/myweb-flask/App/static/img/dest/' + str(
                data) + '/result_' + filename
            if data == 'lpdr':
                try:
                    img = open(img_path, 'rb').read()
                    pre_img, ratio_h, ratio_w, src_h, src_w = lp_img_preprocess(img)
                    prob = lp_refer(pre_img)
                    post_result = lp_postprocess(prob, ratio_h, ratio_w, src_h, src_w)
                    rec_res = lp_generate_result(img_path, post_result, infer_result)
                    for i in range(len(rec_res)):
                        rec_.append(rec_res[i][0])
                    img_data = open(infer_result, "rb").read()
                    img_data = base64.b64encode(img_data).decode('utf-8')
                    res = jsonify({
                        "success": True,
                        "state": 1,
                        "message": "推理成功",
                        "content": {
                            "img_data": img_data,
                            'rec_result': rec_
                        }
                    })
                    return res
                except:
                    res = jsonify({
                        "success": False,
                        "state": 0,
                        "message": "图片中有效目标为零",
                        "content": {
                            "img_data": 'null',
                        }
                    })
                    return res
            if data == 'ppocrv3':
                try:
                    img = open(img_path, 'rb').read()
                    pre_img, ratio_h, ratio_w, src_h, src_w = pp_img_preprocess(img)
                    prob = pp_refer(pre_img)
                    post_result = pp_postprocess(prob, ratio_h, ratio_w, src_h, src_w)
                    rec_res = pp_generate_result(img_path, post_result, infer_result)
                    for i in range(len(rec_res)):
                        rec_.append(rec_res[i][0])
                    img_data = open(infer_result, "rb").read()
                    img_data = base64.b64encode(img_data).decode('utf-8')
                    res = jsonify({
                        "success": True,
                        "state": 1,
                        "message": "推理成功",
                        "content": {
                            "img_data": img_data,
                            'rec_result': rec_
                        }
                    })
                    return res
                except:
                    res = jsonify({
                        "success": False,
                        "state": 0,
                        "message": "图片中有效目标为零",
                        "content": {
                            "img_data": 'null',
                        }
                    })
                    return res
        else:
            res = jsonify({
                "success": False,
                "state": 0,
                "message": "后端接收不到图片",
                "content": {
                    "img_data": 'null',
                }
            })
            return res
    else:
        res = jsonify({
            "success": False,
            "state": 0,
            "message": "请求方法应为POST",
            "content": {
                "img_data": 'null',
            }
        })
        return res


# def generate_frames_1():
#     while True:
#         data = generate_frames()
#         # Save the image locally (optional)


def generate_frames():
    global streaming, process_this_frame
    while streaming:
        success, frame = camera.read()
        if not success:
            break

        if process_this_frame:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
                name = "Unknown"
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left), name, encoding in zip(face_locations, face_names, face_encodings):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            if name == "Unknown":
                matches = face_recognition.compare_faces(known_unknown_face_encodings, encoding, tolerance=0.5)
                if not any(matches):
                    recognize_person()
                    timestamp = int(time.time())
                    filename = os.path.join(unknown_face_folder, f"Unknown_face_{timestamp}.jpg")
                    face = frame[top:bottom, left:right]
                    cv2.imwrite(filename, face)
                    known_unknown_face_encodings.append(encoding)
                    known_unknown_face_names.append(f"Unknown_face_{timestamp}")
                else:
                    for match, unknown_name in zip(matches, known_unknown_face_names):
                        if match:
                            print(unknown_name)

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(frame_rgb)
        buffered = BytesIO()
        im.save(buffered, format='JPEG')
        frame = buffered.getvalue()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def generate_frames_1():
    global streaming
    while streaming:
        success, frame = camera.read()
        if not success:
            break
        else:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(frame_rgb)  # 转换为PIL图像
            processed_frame, posibility = gen_frames(im)  # 调用处理函数
            if posibility > 0.95:
                alarm_smoke()
            buffered = BytesIO()
            processed_frame.save(buffered, format='JPEG')
            frame = buffered.getvalue()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@blue.route('/fire_monitor', methods=['GET'])
def fire_monitor():
    return Response(generate_frames_1(), mimetype='multipart/x-mixed-replace; boundary=frame')

@blue.route('/stop_streaming_smoke', methods=['GET'])
def stop_streaming_smoke():
    global streaming_smoke
    streaming_smoke = False
    # camera.release()
    # Debug返回信息
    return 'Stream stopped successfully.'


@blue.route('/start_streaming_smoke')
def start_stream_smoke():
    global streaming_smoke
    if not streaming_smoke:
        # camera.open(0)
        streaming_smoke = True
    # Debug返回信息
    return 'Stream started successfully.'


####################
# @blue.route('/person_monitor', methods=['GET'])
# def person_monitor():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@blue.route('/stop_streaming_person', methods=['GET'])
def stop_streaming_person():
    global streaming
    streaming = False
    return 'Stream stopped successfully.'


@blue.route('/start_streaming_person', methods=['GET'])
def start_stream_person():
    global streaming
    if not streaming:
        streaming = True
    return 'Stream started successfully.'

#########
# 2024年6月11日15:23:38
# 陌生人脸管理相关
image_folder = r'C:\Users\linyiwu\Desktop\datasets\face\unknown'
@blue.route('/api/images', methods=['GET'])
def get_images():
    try:
        files = os.listdir(image_folder)
        images = [file for file in files if file.lower().endswith(('png', 'jpg', 'jpeg', 'gif'))]
        return jsonify(images)
    except Exception as e:
        return str(e), 500

@blue.route('/api/image/unknown/<filename>', methods=['GET'])
def get_image(filename):
    return send_from_directory(image_folder, filename)

@blue.route('/api/images/<filename>', methods=['DELETE'])
def delete_image(filename):
    try:
        file_path = os.path.join(image_folder, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return '', 204
        else:
            return abort(404)
    except Exception as e:
        return str(e), 500

@blue.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(image_folder, filename)

#################
# 家庭成员管理相关
# 2024年6月11日16:13:46
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

family_image_folder = r'C:\Users\linyiwu\Desktop\datasets\face\train'
@blue.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(family_image_folder, filename))
        return jsonify({'message': 'File uploaded successfully'}), 200
    else:
        return jsonify({'error': 'File type not allowed'}), 400

@blue.route('/api/family_images', methods=['GET'])
def get_family_images():
    try:
        files = os.listdir(family_image_folder)
        images = [file for file in files if file.lower().endswith(('png', 'jpg', 'jpeg', 'gif'))]
        return jsonify(images)
    except Exception as e:
        return str(e), 500

@blue.route('/api/image/family/<filename>', methods=['GET'])
def get_family_image(filename):
    return send_from_directory(family_image_folder, filename)

@blue.route('/api/images/<filename>', methods=['DELETE'])
def delete_family_image(filename):
    try:
        file_path = os.path.join(family_image_folder, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return '', 204
        else:
            return abort(404)
    except Exception as e:
        return str(e), 500

@blue.route('/family_images/<filename>')
def serve_family_image(filename):
    return send_from_directory(family_image_folder, filename)
