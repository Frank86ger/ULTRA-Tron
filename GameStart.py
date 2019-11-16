from PyQt5.QtWidgets import QWidget, QApplication, QDockWidget, QMainWindow
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QRect
import sys
from GameThread import GameThread
import gameconfig
from BoardBlocks import BoardBlocks
import pyqtgraph as pg
import numpy as np


class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        win_x_size, win_y_size, _ = BoardBlocks.load_level2(gameconfig.level_name)
        self.win_x_size = win_x_size  # gameconfig.win_x_size + 50
        self.win_y_size = win_y_size  # gameconfig.win_y_size + 50
        self.initUI()

        self.plotwin1 = PlotWindow(self, self.win_x_size, 25, 500-25, int(1.*self.win_y_size/2)-50)
        self.plotwin2 = PlotWindow(self, self.win_x_size, int(1. * self.win_y_size / 2)+25, 500 - 25, int(1.*self.win_y_size/2)-50)

        #  Start game thread. Needs to be separatly implemented for no-gui interface.
        self.gameThread = GameThread()

        #  Connect sinals of tron-bike positions in gameThread to slot in MainWindow.
        self.gameThread.bike1_list.connect(self.get_bike1_list)
        self.gameThread.bike2_list.connect(self.get_bike2_list)
        self.gameThread.reward_list.connect(self.get_reward_list)
        self.gameThread.probs_list.connect(self.get_probs_list)

        #  Connect signal of powerup information in gameTHread to slot in MainWindow.
        self.gameThread.power_up_list.connect(self.get_power_up_list)

        #  Init list of tron-bike positions and list of power ups.
        self.bike1_list = []
        self.bike2_list = []
        self.reward_list = []
        self.probs_list = []
        self.power_up_list = [[]]
        self.power_up_colors = {'+X': gameconfig.power_up_color_1,
                                '+velo': gameconfig.power_up_color_2,
                                '-velo, +X': gameconfig.power_up_color_3,
                                '+velo, -X': gameconfig.power_up_color_4}

        #  Start gameThread.
        self.gameThread.start()

    def initUI(self):
        self.setGeometry(300, 300, self.win_x_size+500, self.win_y_size)
        self.setWindowTitle('ULTRA-Tron')
        self.show()
    
    # Slot for bike 1 list
    def get_bike1_list(self, bike1_list):
        self.bike1_list = bike1_list
        self.update()  # Update graphics output
    
    # Slot for bike 2 list
    def get_bike2_list(self, bike2_list):
        self.bike2_list = bike2_list
        # self.update()  #  Update graphics output

    def get_reward_list(self, reward_list):
        self.reward_list = reward_list
        self.plotwin1.clear()
        self.plotwin1.plot(np.arange(len(reward_list)), reward_list, pen=None, symbol='o')

    def get_probs_list(self, probs_list):
        self.probs_list = probs_list
        self.plotwin2.clear()
        #print(probs_list)
        probs = np.array(probs_list)

        self.plotwin2.plot(np.arange(len(probs_list)), probs[:, 0], pen=None, symbol='+')
        #self.plotwin2.plot(np.arange(len(probs_list)), probs[:, 1], pen=None, symbol='s')
        #self.plotwin2.plot(np.arange(len(probs_list)), probs[:, 2], pen=None, symbol='t')

        self.plotwin2.plot(np.arange(len(probs_list)), probs[:, 3], pen=None, symbol='o')


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
            self.gameThread.save_dqn()
            self.close()
        # Player 1
        if gameconfig.bike1_player == 'human':
            if e.key() == Qt.Key_Up:
                self.gameThread.bike_1.set_direction('up')
            if e.key() == Qt.Key_Right:
                self.gameThread.bike_1.set_direction('right')
            if e.key() == Qt.Key_Down:
                self.gameThread.bike_1.set_direction('down')
            if e.key() == Qt.Key_Left:
                self.gameThread.bike_1.set_direction('left')
        # Player 2
        if gameconfig.bike2_player == 'human':
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
        qp.setBrush(QColor(0, 0, 0))
        qp.drawLine(25-shift_1, 25-shift_1, 25-shift_1, self.win_y_size-25+shift_2)
        qp.drawLine(25-shift_1, 25-shift_1, self.win_x_size-25+shift_2, 25-shift_1)
        qp.drawLine(25-shift_1, self.win_y_size-25+shift_2, self.win_x_size-25+shift_2, self.win_y_size-25+shift_2)
        qp.drawLine(self.win_x_size-25+shift_2, 25-shift_1, self.win_x_size-25+shift_2, self.win_y_size-25+shift_2)

        qp.setPen(QColor(255, 255, 255))

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


#class PlotWindow(QWidget):
class PlotWindow(pg.PlotWidget):
    def __init__(self, parent, x, y, width, height):
        super(PlotWindow, self).__init__(parent)
        self.setGeometry(x, y, width, height)
        self.show()
        #self.plotter =






if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
