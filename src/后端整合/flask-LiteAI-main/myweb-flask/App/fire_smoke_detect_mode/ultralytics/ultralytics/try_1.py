from ultralytics import YOLO
model=YOLO(r'src\检测模块\ultralytics-8.1.0\ultralytics-8.1.0\model_onnx\best_zhongyi.pt')
model.train(data='C:/Users/linyiwu\\Desktop\\软件工程课程设计\\src\\检测模块\\ultralytics-8.1.0\\ultralytics-8.1.0\\try_1.yaml',epochs=10,batch=16,workers=0)