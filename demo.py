import cv2
from ultralytics import YOLO
import time

def main():
    model = YOLO('runs/detect/train8/weights/best.pt')
    
    # 尝试不同的摄像头索引和后端
    backends = [
        (0, cv2.CAP_DSHOW),  # Windows首选
        (0, cv2.CAP_ANY),    # 通用
        (0, cv2.CAP_V4L2)    # Linux
    ]
    
    cap = None
    for camera_index, backend in backends:
        cap = cv2.VideoCapture(camera_index, backend)
        if cap.isOpened():
            print(f"成功打开摄像头，使用后端: {backend}")
            break
        else:
            print(f"尝试索引 {camera_index} 和后端 {backend} 失败")
    
    if not cap or not cap.isOpened():
        print("所有尝试均失败，可能原因：")
        print("1. 摄像头未连接或损坏")
        print("2. 驱动程序未安装（新摄像头需安装驱动）")
        print("3. 权限问题（特别是Linux/macOS）")
        return
    
    # 设置摄像头参数
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    print("实时检测中，按Q键退出...")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("获取帧失败，尝试重新初始化摄像头...")
            cap.release()
            time.sleep(1)
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            if not cap.isOpened():
                print("重新初始化失败，退出程序")
                break
            continue
        
        # YOLO检测
        results = model(frame, imgsz=640)
        annotated_frame = results[0].plot()
        
        cv2.imshow('工具检测', annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()