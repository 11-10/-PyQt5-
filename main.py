import os
import shutil
import sys

from PyQt5.QtCore import Qt, QRect,QStringListModel
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout,QComboBox,QListView
from qt_material import apply_stylesheet
from config import *


class PaintLabel(QLabel):
    x0 = 0
    y0 = 0
    x1 = img_width
    y1 = img_height
    mode = "lock"  # right/left/top/bottom/lock/new

    # 鼠标点击事件
    def mousePressEvent(self, event):

        if (self.x0 - 5) <= event.x() <= (self.x0 + 5):
            self.mode = 'left'
        elif (self.x1 - 5) <= event.x() <= (self.x1 + 5):
            self.mode = 'right'
        elif (self.y0 - 5) <= event.y() <= (self.y0 + 5):
            self.mode = 'top'
        elif (self.y1 - 5) <= event.y() <= (self.y1 + 5):
            self.mode = 'bottom'
        else:
            self.x0 = event.x()
            self.y0 = event.y()
            self.mode = 'new'

    # 鼠标释放事件
    def mouseReleaseEvent(self, event):
        self.mode = 'lock'

    # 鼠标移动事件
    def mouseMoveEvent(self, event):
        self.setMouseTracking(True)
        if ((self.x0 - 5) <= event.x() <= (self.x0 + 5)) or ((self.x1 - 5) <= event.x() <= (self.x1 + 5)):
            self.setCursor(Qt.SizeHorCursor)
        elif (self.y0 - 5) <= event.y() <= (self.y0 + 5) or (self.y1 - 5) <= event.y() <= (self.y1 + 5):
            self.setCursor(Qt.SizeVerCursor)
        else:
            self.setCursor(Qt.ArrowCursor)
        if self.mode == 'new':
            self.x1 = event.x()
            self.y1 = event.y()
            self.update()
        elif self.mode == 'right':
            self.x1 = event.x()
            self.update()
        elif self.mode == 'left':
            self.x0 = event.x()
            self.update()
        elif self.mode == 'top':
            self.y0 = event.y()
            self.update()
        elif self.mode == 'bottom':
            self.y1 = event.y()
            self.update()

    def get_position(self):
        return self.x0, self.y0, self.x1, self.y1

    def reset_position(self):
        self.x0 = 0
        self.y0 = 0
        self.x1 = img_width
        self.y1 = img_height

    # 绘制事件
    def paintEvent(self, event):
        super().paintEvent(event)
        rect = QRect(self.x0, self.y0, abs(self.x1 - self.x0), abs(self.y1 - self.y0))
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        painter.drawRect(rect)


class Main(QWidget):
    gray = False
    image_list = []
    index = 0

    def __init__(self):
        super(Main, self).__init__()
        for root, folder, file_list in os.walk(original_path):
            self.image_list = [os.path.join(root, i) for i in file_list if i.split('.')[-1] in support_type]
        self.img = PaintLabel(self)
        self.img.setFixedSize(img_width, img_height)
        # 设置初始图片
        self.image = QPixmap(self.image_list[0]).scaled(img_width, img_height)
        # print(f'image编号{self.image_list[0]}')
        self.img.setPixmap(self.image)
        # 保存按钮
        self.save = QPushButton('save', self)
        self.save.clicked.connect(self.save_position)
        # 废弃按钮
        self.discard = QPushButton('discard', self)
        self.discard.clicked.connect(self.discard_image)
        # 还原框按钮
        self.reset = QPushButton('reset', self)
        self.reset.clicked.connect(self.reset_position)
        # 侧边栏显示表单
        # self.chooseitem = QPushButton('选择目录', self)
        # self.item.clicked.connect(self.reset_position)
        # 显示文件列表
        self.listView = QListView(self)
        slm = QStringListModel()
        slm.setStringList(self.image_list)
        self.listView.setModel(slm)
        self.listView.clicked.connect(self.list_clicked)
        # 上一张，下一张
        self.above = QPushButton('上一张', self)
        self.above.clicked.connect(self.above_position)
        self.next = QPushButton('下一张', self)
        self.next.clicked.connect(self.next_position)
        # 旋转 平移
        self.rote = QPushButton('旋转', self)
        # self.reset.clicked.connect(self.reset_position)
        self.translate = QPushButton('平移', self)

        # 总布局
        self.main_layout = QHBoxLayout()
        # 侧边栏布局
        self.left_layout = QVBoxLayout()
        # 水平布局
        self.h_layout = QHBoxLayout()
        # 垂直布局 save reset discard
        self.v_layout = QVBoxLayout()
        # 垂直布局 上一张 下一张
        self.v2_layout = QHBoxLayout()
        # 加载组件 图片水平
        self.v2_layout.addWidget(self.above, alignment=Qt.AlignCenter)
        self.v2_layout.addWidget(self.next, alignment=Qt.AlignCenter)

        self.v2_layout.addWidget(self.rote, alignment=Qt.AlignCenter)
        self.v2_layout.addWidget(self.translate, alignment=Qt.AlignCenter)

        # self.left_layout.addWidget(self.chooseitem, alignment=Qt.AlignCenter)
        self.left_layout.addWidget(self.listView)
        # 控件 垂直布局
        self.h_layout.addWidget(self.save, alignment=Qt.AlignCenter)
        self.h_layout.addWidget(self.reset, alignment=Qt.AlignCenter)
        self.h_layout.addWidget(self.discard, alignment=Qt.AlignCenter)
        # self.h_layout.addWidget(self.check, alignment=Qt.AlignCenter)
        # 加载布局
        # 把图片加到垂直布局中
        self.v_layout.addLayout(self.v2_layout)
        self.v_layout.addWidget(self.img, alignment=Qt.AlignCenter)
        self.v_layout.addLayout(self.h_layout)
        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.v_layout)
        self.setLayout(self.main_layout)
        self.setFixedSize(widget_width, widget_height)

    def change_gray(self, state):
        """
        点击复选框调用
        :param state: 复选框状态
        :return:
        """
        self.gray = (state == Qt.Checked)

    def discard_image(self):
        """
                点击保存按钮调用
                :return:
                """
        # 删除当前照片
        shutil.move(self.image_list[self.index],
                    self.image_list[self.index].replace(original_path, backup_path))
        
        # 切换到下一张图片
        self.index += 1
        if self.index < len(self.image_list):
            self.image = QPixmap(self.image_list[self.index]).scaled(img_width, img_height)
            self.img.setPixmap(self.image)
            self.reset_position()
    
    # 上一张
    def above_position(self):
        """
                点击上一张图片显示调用
                :return:
                """
        self.index = self.index - 1
        if self.index > 0:
            self.image = QPixmap(self.image_list[self.index]).scaled(img_width, img_height)
            self.img.setPixmap(self.image)
            self.reset_position()

    # 下一张
    def next_position(self):
        """
                点击下一张图片显示调用
                :return:
                """
        self.index += 1
        if self.index < len(self.image_list) :
            self.image = QPixmap(self.image_list[self.index]).scaled(img_width, img_height)
            self.img.setPixmap(self.image)
            self.reset_position()



    def save_position(self):
        """
        点击保存按钮调用
        :return:
        """
        # 对位置信息进行处理并保存图片
        x0, y0, x1, y1 = self.img.get_position()
        name = result_name_template % (x0, y0, x1, y1)
        self.image.save(os.path.join(results_path, name))
        # shutil.move(self.image_list[self.index],
        #             self.image_list[self.index].replace(original_path, backup_path))

        # 切换到下一张图片
        self.index += 1
        if self.index < len(self.image_list):
            self.image = QPixmap(self.image_list[self.index]).scaled(img_width, img_height)
            self.img.setPixmap(self.image)
            self.reset_position()

    def reset_position(self):
        """
        点击重置按钮调用
        :return:
        """
        self.img.reset_position()
        self.img.repaint()
    def list_clicked(self,qModelIndex):

        print(qModelIndex)
        path = self.image_list[qModelIndex.row()]
        # 控制台，你选择的信息
        
        self.index = self.image_list.index(path)
        self.image = QPixmap(self.image_list[self.index]).scaled(img_width, img_height)
        self.img.setPixmap(self.image)
        print('你选择了：'+self.image_list[qModelIndex.row()])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_teal.xml')
    main = Main()
    main.show()
    sys.exit(app.exec())