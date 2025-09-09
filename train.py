from ultralytics import YOLO
import torch.multiprocessing as mp

def main():
    # 加载模型
    model = YOLO('yolo11n.pt')
    
    # 训练参数
    results = model.train(
        data='data.yaml',
        epochs=100,
        batch=16,
        imgsz=640,
        device='0'  # '0' 如果有GPU
    )

if __name__ == '__main__':
    # Windows多进程支持
    mp.freeze_support()
    main()