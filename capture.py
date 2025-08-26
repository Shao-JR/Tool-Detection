import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                            QLabel, QVBoxLayout, QWidget, QFileDialog)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer
import cv2

class CameraApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("摄像头拍照程序")
        self.setGeometry(100, 100, 800, 600)
        
        # 初始化摄像头
        self.cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            print("无法打开摄像头")
            self.close()
        
        # 设置默认保存路径
        self.save_path = os.path.expanduser("datasets/images/train")
        if not os.path.exists(self.save_path):
            self.save_path = os.getcwd()
        
        # 创建UI
        self.init_ui()
        
        # 定时器更新摄像头画面
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # 30ms更新一次
        
    def init_ui(self):
        # 主窗口布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        
        # 摄像头显示区域
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(640, 480)
        layout.addWidget(self.image_label)
        
        # 路径显示
        self.path_label = QLabel(f"保存路径: {self.save_path}")
        layout.addWidget(self.path_label)
        
        # 按钮区域
        btn_layout = QVBoxLayout()
        
        # 选择路径按钮
        self.path_btn = QPushButton("选择保存路径")
        self.path_btn.clicked.connect(self.select_path)
        btn_layout.addWidget(self.path_btn)
        
        # 拍照按钮
        self.capture_btn = QPushButton("拍照")
        self.capture_btn.clicked.connect(self.capture_image)
        btn_layout.addWidget(self.capture_btn)
        
        layout.addLayout(btn_layout)
        central_widget.setLayout(layout)
    
    def select_path(self):
        """选择保存路径"""
        path = QFileDialog.getExistingDirectory(
            self, "选择保存目录", self.save_path,
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        if path:
            self.save_path = path
            self.path_label.setText(f"保存路径: {self.save_path}")
    
    def update_frame(self):
        """更新摄像头画面"""
        ret, frame = self.cap.read()
        if ret:
            # 转换颜色空间 BGR -> RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # 调整大小以适应显示区域
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            q_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            
            # 缩放图像以适应标签大小
            scaled_img = q_img.scaled(
                self.image_label.size(), 
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(QPixmap.fromImage(scaled_img))
    
    def capture_image(self):
        """拍照并保存"""
        ret, frame = self.cap.read()
        if ret:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"photo_{timestamp}.jpg"
            filepath = os.path.join(self.save_path, filename)
            
            # 保存图片
            cv2.imwrite(filepath, frame)
            
            # 显示保存提示
            self.path_label.setText(f"照片已保存到: {filepath}")
    
    def closeEvent(self, event):
        """关闭窗口时释放资源"""
        self.timer.stop()
        self.cap.release()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CameraApp()
    window.show()
    sys.exit(app.exec_())