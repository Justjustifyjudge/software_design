# from ultralytics import YOLO
# yolo =YOLO("./yolov8n.pt",task="detect")
# result=yolo(source="./ultralytics/assets/zidane.jpg",save=True)
# # result=yolo(source="screen")
# # result=yolo(source=0)


from ultralytics import YOLO
yolo =YOLO("best.pt",task="detect")

result=yolo(source=r'D:\PycharmProjects\2024mathorcup\B题\dataset\test\images\020027.jpg',save=True,save_txt=True)
