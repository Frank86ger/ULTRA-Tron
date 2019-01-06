from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen
from PyQt5.QtCore import Qt
import sys
import random
from TronBike import TronBike
from GameThread import GameThread
import time
import gameconfig
from BoardBlocks import BoardBlocks

class MainWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        win_x_size, win_y_size, _ = BoardBlocks.load_level2(gameconfig.level_name)
        self.win_x_size = win_x_size#gameconfig.win_x_size + 50
        self.win_y_size = win_y_size#gameconfig.win_y_size + 50
        self.initUI()

        #  Start game thread. Needs to be separatly implemented for no-gui interface.
        self.gameThread = GameThread()

        #  Connect sinals of tron-bike positions in gameThread to slot in MainWindow.
        self.gameThread.bike1_list.connect(self.get_bike1_list)
        self.gameThread.bike2_list.connect(self.get_bike2_list)

        #  Connect signal of powerup information in gameTHread to slot in MainWindow.
        self.gameThread.power_up_list.connect(self.get_power_up_list)

        #  Init list of tron-bike positions and list of power ups.
        self.bike1_list = None
        self.bike2_list = None
        self.power_up_list = []
        self.power_up_colors = {'+X':gameconfig.power_up_color_1, '+velo':gameconfig.power_up_color_2, '-velo, +X':gameconfig.power_up_color_3, '+velo, -X':gameconfig.power_up_color_4}

        #  Start gameThread.
        self.gameThread.start()
        
        
    def initUI(self):
        self.setGeometry(300, 300, self.win_x_size, self.win_y_size)
        self.setWindowTitle('ULTRA-Tron')
        self.show()
    
    # Slot for bike 1 list
    def get_bike1_list(self, bike1_list):
        self.bike1_list = bike1_list
        self.update() #  Update graphics output
    
    # Slot for bike 2 list
    def get_bike2_list(self, bike2_list):
        self.bike2_list = bike2_list
        #self.update() #  Update graphics output

    # Slot for power up list
    def get_power_up_list(self, powerup_list):
        self.power_up_list = powerup_list

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawRectangles(qp)
        qp.end()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_F5:
            self.close()
        if e.key() == Qt.Key_Up:
            self.gameThread.bike_1.set_direction('up')
        if e.key() == Qt.Key_Right:
            self.gameThread.bike_1.set_direction('right')
        if e.key() == Qt.Key_Down:
            self.gameThread.bike_1.set_direction('down')
        if e.key() == Qt.Key_Left:
            self.gameThread.bike_1.set_direction('left')
        if e.key() == Qt.Key_W:
            self.gameThread.bike_2.set_direction('up')
        if e.key() == Qt.Key_D:
            self.gameThread.bike_2.set_direction('right')
        if e.key() == Qt.Key_S:
            self.gameThread.bike_2.set_direction('down')
        if e.key() == Qt.Key_A:
            self.gameThread.bike_2.set_direction('left')

    def drawRectangles(self, qp):

        border_width = 2
        shift_1 = 1
        shift_2 = 2
        pen = QPen(Qt.black, border_width, Qt.SolidLine)
        qp.setPen(pen)
        qp.setBrush(QColor(0,0,0))
        qp.drawLine(25-shift_1,25-shift_1,25-shift_1,self.win_y_size-25+shift_2)
        qp.drawLine(25-shift_1,25-shift_1,self.win_x_size-25+shift_2,25-shift_1)
        qp.drawLine(25-shift_1,self.win_y_size-25+shift_2,self.win_x_size-25+shift_2,self.win_y_size-25+shift_2)
        qp.drawLine(self.win_x_size-25+shift_2,25-shift_1,self.win_x_size-25+shift_2,self.win_y_size-25+shift_2)

        qp.setPen(QColor(255,255,255))

        #  Draw bike 1
        qp.setBrush(QColor(*gameconfig.bike_1_color))
        for dot in self.bike1_list:
            x = dot[0]*10+25
            y = dot[1]*10+25
            qp.drawRect(x, y, 10, 10)

        #  Draw bike 2
        qp.setBrush(QColor(*gameconfig.bike_2_color))
        for dot in self.bike2_list:
            x = dot[0]*10+25
            y = dot[1]*10+25
            qp.drawRect(x, y, 10, 10)

        #  Draw power ups
        for (idx, power_up) in enumerate(self.power_up_list[0]):
            qp.setPen(QColor(*self.power_up_colors[self.power_up_list[1][idx]]))
            qp.setBrush(QColor(*self.power_up_colors[self.power_up_list[1][idx]]))
            powerup_x = power_up[0]*10+25
            powerup_y = power_up[1]*10+25
            qp.drawRect(powerup_x, powerup_y, 10, 10)

        #  Draw blocked blocks
        qp.setPen(QColor(*gameconfig.blocked_blocks_color))
        if len(self.gameThread.blocked_blocks) > 0:
            for block in self.gameThread.blocked_blocks:
                qp.setBrush(QColor(*gameconfig.blocked_blocks_color))
                block_x = block[0]*10+25
                block_y = block[1]*10+25
                qp.drawRect(block_x, block_y, 10, 10)


if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())