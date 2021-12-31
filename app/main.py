from PyQt5.QtWidgets import QApplication, QStackedLayout, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtGui import QPalette
from PyQt5.QtCore import Qt
from podman import PodmanClient
import sys

class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Podman GUI")
        #layout = QVBoxLayout()
        self.setLayout(layout)
        #self.title = 'PyQt5 button - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 300
        self.height = 300
        self.initGUI()

    def initGUI(self):


       # palette = QPalette()
        #palette.setColor(QPalette.ButtonText, Qt.red)
        #app.setPalette(palette)

        self.setLayout(QVBoxLayout())

        self.stackedLayout = QStackedLayout()

        self.page1 = QWidget()

        home = QPushButton('Home', self)
        home.clicked.connect(self.home_on_click)
        imgs = QPushButton('List Images', self)
        imgs.clicked.connect(self.img_on_click)
        ctrs = QPushButton('List Containers')
        ctrs.clicked.connect(self.ctr_on_click)
        pods = QPushButton('List Pods')
        pods.clicked.connect(self.pod_on_click)

        self.page1Layout = QVBoxLayout()
        self.page1Layout.addWidget(home, alignment= Qt.AlignTop)
        self.page1Layout.addWidget(imgs)
        self.page1Layout.addWidget(ctrs)
        self.page1Layout.addWidget(pods)
        self.page1.setLayout(self.page1Layout)

        self.stackedLayout.addWidget(self.page1)

        self.page2 = QWidget()
        self.page2Layout = QVBoxLayout()
        self.page2Layout.addWidget(home, alignment= Qt.AlignTop)
        self.stackedLayout.addWidget(self.page2)

        self.page3 = QWidget()
        self.page3Layout = QVBoxLayout()
        self.page3Layout.addWidget(home, alignment= Qt.AlignTop)
        self.stackedLayout.addWidget(self.page3)

        self.page4 = QWidget()
        self.page4Layout = QVBoxLayout()
        self.page4Layout.addWidget(home, alignment= Qt.AlignTop)
        self.stackedLayout.addWidget(self.page4)


        layout.addLayout(self.stackedLayout)

      #  self.setGeometry(300, 300, 700, 700)
       # self.setLayout(layout)
        #self.show()

    def img_on_click(self):
        self.stackedLayout.setCurrentIndex(1)
        print('here')
        uri = "unix:///run/user/1000/podman/podman.sock"
        with PodmanClient(base_url=uri) as client:
            for image in client.images.list():
                self.page2Layout.addWidget(QLabel('Image ID:  '+image.id))
                self.page2.setLayout(self.page2Layout)
                #self.setLayout(layout)

    def ctr_on_click(self):
        self.stackedLayout.setCurrentIndex(2)
        print('here')
        uri = "unix:///run/user/1000/podman/podman.sock"
        with PodmanClient(base_url=uri) as client:
            for container in client.containers.list():
                self.page3Layout.addWidget(QLabel('Container ID:  '+container.id))
                self.page3.setLayout(self.page3Layout)
              #  self.setLayout(layout)

    def pod_on_click(self):
        self.stackedLayout.setCurrentIndex(3)
        uri = "unix:///run/user/1000/podman/podman.sock"
        with PodmanClient(base_url=uri) as client:
            for pod in client.pods.list():
                self.page4Layout.addWidget(QLabel('Container ID:  '+pod.id))
                self.page4.setLayout(self.page4Layout)


    def home_on_click(self):
        self.stackedLayout.setCurrentIndex(0)


if __name__ == '__main__':
    print('here')
    layout = QVBoxLayout()
    app = QApplication(sys.argv)
    #window = QWidget()
    window = Window()
    print('here')
    window.show()
    sys.exit(app.exec_())