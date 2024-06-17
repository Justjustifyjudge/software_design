# from ultralytics import YOLO

# model=YOLO(r'C:\Users\Lenovo\Desktop\ultralytics-8.2.0\best.pt',task='detect')

# # model.predict(r'C:\Users\Lenovo\Desktop\ultralytics-8.2.0\1.mp4',save=True,save_txt=True,show=True)

# from PIL import Image
# # from ultralytics import YOLO
 
# # Load a pretrained YOLOv8n model
# model=YOLO(r'C:\Users\Lenovo\Desktop\ultralytics-8.2.0\best.pt',task='detect')
 
# # Run inference
# results = model('test.jpg')  # results list
 
# # Show the results
# for result in results:
#     im_array = result.plot()  # plot a BGR numpy array of predictions
#     im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
#     im.show()  # show image
#     im.save('results.jpg')  # save image

from ultralytics import YOLO
import cv2
# Load a pretrained YOLOv8n model
model=YOLO(r'C:\Users\linyiwu\Desktop\software_design\src\后端整合\flask-LiteAI-main\myweb-flask\App\fire_smoke_detect_mode\ultralytics\ultralytics\model_onnx\best_3epoch.pt',task='detect')

cap = cv2.VideoCapture(0) # 0表示调用摄像头

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break
#     results = model(frame)
#     annotated_frame = results[0].plot()
#     cv2.imshow('YOLOv8', annotated_frame)
#     if cv2.waitKey(1) == ord('q'):  # 按下q退出
#         break
# 遍历视频帧
while cap.isOpened():
    # 从视频中读取一帧
    success, frame = cap.read()

    if success:
        # 在该帧上运行YOLOv8推理q
        results = model(frame,conf=0.4) # 设置置信度阈值，小于0.7的都不显示


        # 在帧上可视化结果
        annotated_frame = results[0].plot()

        # 显示带注释的帧
        cv2.imshow("YOLOv8推理", annotated_frame)

        # 如果按下'q'则中断循环
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        # 输出置信度
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # box.conf 表示置信度
                print(f"置信度: {box.conf}")
    else:
        # 如果视频结束则中断循环
        break

cap.release()
cv2.destroyAllWindows()

