import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QListWidget, QListWidgetItem, QFrame, QPushButton)
from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtGui import QFont

class InfiniteTimePicker(QWidget):
    def __init__(self):
        super().__init__()
        self.hour_list = None
        self.minute_list = None
        self.second_list = None
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('无限循环时间选择器')
        self.setGeometry(300, 300, 400, 300)
        
        # 主布局
        main_layout = QHBoxLayout()
        
        # 创建时分秒选择器
        self.hour_picker, self.hour_list = self.create_time_picker(0, 23, "时")
        self.minute_picker, self.minute_list = self.create_time_picker(0, 59, "分")
        self.second_picker, self.second_list = self.create_time_picker(0, 59, "秒")
        
        # 添加到主布局
        main_layout.addWidget(self.hour_picker)
        main_layout.addWidget(self.minute_picker)
        main_layout.addWidget(self.second_picker)
        
        # 当前时间显示
        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setFont(QFont("Arial", 16))
        
        # 获取当前时间并设置初始值
        current_time = QTime.currentTime()
        self.set_time(current_time.hour(), current_time.minute(), current_time.second())
        
        # 主窗口布局
        layout = QVBoxLayout()
        layout.addLayout(main_layout)
        layout.addWidget(self.time_label)
        
        self.setLayout(layout)
        
    def create_time_picker(self, min_val, max_val, label_text):
        """创建时间选择器组件"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Box)
        frame.setLineWidth(1)
        
        layout = QVBoxLayout()
        
        # 标题标签
        label = QLabel(label_text)
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Arial", 12, QFont.Bold))
        
        # 列表控件
        list_widget = QListWidget()
        list_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        list_widget.setFixedSize(80, 150)
        
        # 填充数据 - 创建足够的项目来实现平滑循环
        num_extra = 10  # 额外的项目数量
        total_items = (max_val - min_val + 1) + 2 * num_extra
        
        # 添加前置项目（用于循环）
        for i in range(max_val - num_extra + 1, max_val + 1):
            item = QListWidgetItem(f"{i:02d}")
            item.setTextAlignment(Qt.AlignCenter)
            list_widget.addItem(item)
        
        # 添加主要项目
        for i in range(min_val, max_val + 1):
            item = QListWidgetItem(f"{i:02d}")
            item.setTextAlignment(Qt.AlignCenter)
            list_widget.addItem(item)
        
        # 添加后置项目（用于循环）
        for i in range(min_val, min_val + num_extra):
            item = QListWidgetItem(f"{i:02d}")
            item.setTextAlignment(Qt.AlignCenter)
            list_widget.addItem(item)
        
        # 设置初始位置（在主要项目区域）
        list_widget.setCurrentRow(num_extra)
        
        # 连接信号
        list_widget.currentRowChanged.connect(
            lambda row, lw=list_widget, min=min_val, max=max_val, extra=num_extra: 
            self.on_selection_changed(row, lw, min, max, extra)
        )
        
        layout.addWidget(label)
        layout.addWidget(list_widget)
        frame.setLayout(layout)
        
        return frame, list_widget
    
    def on_selection_changed(self, row, list_widget, min_val, max_val, num_extra):
        """处理选择变化，实现无限循环"""
        total_items = list_widget.count()
        main_range = max_val - min_val + 1
        
        # 如果滚动到前置区域，跳转到对应的主要区域
        if row < num_extra:
            target_row = row + main_range
            list_widget.blockSignals(True)  # 阻塞信号避免递归调用
            list_widget.setCurrentRow(target_row)
            list_widget.blockSignals(False)
        
        # 如果滚动到后置区域，跳转到对应的主要区域
        elif row >= num_extra + main_range:
            target_row = row - main_range
            list_widget.blockSignals(True)  # 阻塞信号避免递归调用
            list_widget.setCurrentRow(target_row)
            list_widget.blockSignals(False)
        
        self.update_display()
    
    def set_time(self, hour, minute, second):
        """设置当前时间"""
        # 确保在有效范围内
        hour = max(0, min(23, hour))
        minute = max(0, min(59, minute))
        second = max(0, min(59, second))
        
        # 设置当前行（加上偏移量）
        if self.hour_list:
            self.hour_list.setCurrentRow(hour + 10)  # 10是前置项目数量
        
        if self.minute_list:
            self.minute_list.setCurrentRow(minute + 10)
        
        if self.second_list:
            self.second_list.setCurrentRow(second + 10)
        
        self.update_display()
    
    def get_time(self):
        """获取当前选择的时间"""
        try:
            hour = 0
            minute = 0
            second = 0
            
            if self.hour_list and self.hour_list.currentItem():
                current_row = self.hour_list.currentRow()
                hour = (current_row - 10) % 24  # 10是前置项目数量
            
            if self.minute_list and self.minute_list.currentItem():
                current_row = self.minute_list.currentRow()
                minute = (current_row - 10) % 60
            
            if self.second_list and self.second_list.currentItem():
                current_row = self.second_list.currentRow()
                second = (current_row - 10) % 60
            
            return hour, minute, second
            
        except Exception as e:
            print(f"获取时间错误: {e}")
            return 0, 0, 0
    
    def update_display(self):
        """更新显示的时间"""
        try:
            hour, minute, second = self.get_time()
            self.time_label.setText(f"{hour:02d}:{minute:02d}:{second:02d}")
        except Exception as e:
            print(f"更新显示错误: {e}")

class EnhancedTimePicker(QWidget):
    """增强版时间选择器，带有确认按钮和更多功能"""
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('增强版时间选择器')
        self.setGeometry(300, 300, 450, 400)
        
        layout = QVBoxLayout()
        
        # 创建时间选择器
        self.time_picker = InfiniteTimePicker()
        
        # 确认按钮
        confirm_btn = QPushButton('确认选择')
        confirm_btn.clicked.connect(self.on_confirm)
        
        # 当前选择显示
        self.selected_label = QLabel('尚未选择')
        self.selected_label.setAlignment(Qt.AlignCenter)
        self.selected_label.setFont(QFont("Arial", 14))
        
        layout.addWidget(self.time_picker)
        layout.addWidget(confirm_btn)
        layout.addWidget(self.selected_label)
        
        self.setLayout(layout)
    
    def on_confirm(self):
        """确认选择"""
        try:
            hour, minute, second = self.time_picker.get_time()
            self.selected_label.setText(f"选择的时间: {hour:02d}:{minute:02d}:{second:02d}")
        except Exception as e:
            print(f"确认选择错误: {e}")
            self.selected_label.setText("选择失败")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # 使用基础版本
    picker = InfiniteTimePicker()
    
    # 使用增强版本
    # picker = EnhancedTimePicker()
    
    picker.show()
    sys.exit(app.exec_())