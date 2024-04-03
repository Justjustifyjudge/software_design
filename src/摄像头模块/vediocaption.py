import cv2

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
    cv2.imwrite('first_frame.jpg', frame)

    while True:
        # 读取一帧图像
        ret, frame = cap.read()

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

if __name__ == "__main__":
    main()
