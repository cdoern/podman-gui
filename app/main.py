from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QApplication, QLineEdit, QStackedLayout, QComboBox, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QPalette
from PyQt5.QtCore import Qt
import podman
import sys

lists = []
pageLayouts = []
pages = []


client = podman.PodmanClient()

class Window(QWidget):
    print("** Check Service Available")
    if client.ping():
        print("Service active")
    else:
        print(f"No service found @ {client.base_url}")

    lists.append(client.images.list())
    lists.append(client.containers.list())
    lists.append(client.pods.list())
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Podman GUI")
        self.setLayout(layout)
        self.left = 10
        self.top = 10
        self.initGUI()

    def initGUI(self):
            #palette = QPalette()
            #palette.setColor(QPalette.ButtonText, Qt.red)
            #app.setPalette(palette)

            #self.textbox = QLineEdit()

        self.setLayout(QVBoxLayout())
        self.stackedLayout = QStackedLayout()

        imgs = QPushButton('List Images', self)
        ctrs = QPushButton('List Containers', self)
        pods = QPushButton('List Pods', self)
        ctrCreate = QPushButton('Create a Container', self)
        podCreate = QPushButton('Create a Pod', self)


        self.page1 = QWidget()
        self.page1Layout = QVBoxLayout()
        self.page1Layout.setSpacing(0)
        self.page1Layout.addWidget(imgs)
        self.page1Layout.addWidget(ctrs)
        self.page1Layout.addWidget(pods)
        self.page1Layout.addWidget(ctrCreate)
        self.page1Layout.addWidget(podCreate)
        self.page1Layout.addStretch(1)
        pageLayouts.append(self.page1Layout)
        pages.append(self.page1)
        self.page1.setLayout(self.page1Layout)
        self.page1.setStyleSheet(open('stylesheet.css').read())
        self.stackedLayout.addWidget(self.page1)

        self.page2 = QWidget()
        self.page2Layout = QVBoxLayout()
        self.stackedLayout.addWidget(self.page2)
        pageLayouts.append(self.page2Layout)
        pages.append(self.page2)

        self.page3 = QWidget()
        self.page3Layout = QVBoxLayout()
     
        self.stackedLayout.addWidget(self.page3)
        pageLayouts.append(self.page3Layout)
        pages.append(self.page3)

        self.page4 = QWidget()
        self.page4Layout = QVBoxLayout()
        self.stackedLayout.addWidget(self.page4)
        pageLayouts.append(self.page4Layout)
        pages.append(self.page4)

        self.page5 = QWidget()
        self.page5Layout = QVBoxLayout()
        self.stackedLayout.addWidget(self.page5)
        pageLayouts.append(self.page5Layout)
        pages.append(self.page5)

        self.page6 = QWidget()
        self.page6Layout = QVBoxLayout()
        self.stackedLayout.addWidget(self.page6)
        pageLayouts.append(self.page6Layout)
        pages.append(self.page6)

        
        imgs.clicked.connect(lambda: self.list_on_click(0, 1))
        ctrs.clicked.connect(lambda: self.list_on_click(1, 2))
        pods.clicked.connect(lambda: self.list_on_click(2, 3))
        ctrCreate.clicked.connect(lambda: self.create_on_click(4))
        podCreate.clicked.connect(lambda: self.create_on_click(5))
 

        self.resize(600, 600)

        layout.addLayout(self.stackedLayout)

    def list_on_click(self, val, ind):
        self.stackedLayout.setCurrentIndex(ind)
        #pages[ind].setRowCount(len(lists[val]))
        pageLayouts[ind] = QVBoxLayout()
        home = QPushButton('Home', self)
        home.clicked.connect(self.home_on_click)
        pageLayouts[ind].addWidget(home, alignment= Qt.AlignTop)
        table = QTableWidget(pages[ind])
        table.setRowCount(len(lists[val]))
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(('Name', 'ID'))
        for i in range(0, len(lists[val])):
            print(str((lists[val])[i]))
            if ind == 1:
                value = str((lists[val])[i])
                table.setItem(i, 0, QTableWidgetItem(value[value.index(' '):value.index('>')]))
            else:
                value = lists[val][i].name
                table.setItem(i, 0, QTableWidgetItem(value))
            table.setItem(i, 1, QTableWidgetItem(lists[val][i].id))

        #for value in lists[val]:    
        #pageLayouts[ind].addWidget(Q('ID:  '+value.id))
        #pageLayouts[ind].addStretch(1)
        #pages[ind].setLayout(pageLayouts[ind])
        table.resizeColumnsToContents()
        table.resizeRowsToContents()
        pageLayouts[ind].addWidget(table)
        pageLayouts[ind].addStretch(1)
        pages[ind].setLayout(pageLayouts[ind])
        pages[ind].setStyleSheet(open('stylesheet.css').read())

    def create(self, ind, name):
        print(name,ind)
        if ind == 4:
            obj = client.containers.create(name)
        else:
            obj = client.pods.create(name)
        print(obj.id)
        pageLayouts[ind].addWidget(QLabel("Created with ID "+obj.id))
        pageLayouts[ind].addStretch(1)
        pages[ind].setLayout(pageLayouts[ind])
            
    def get_data(self, ind, newBox):
        if ind == 4:
            return newBox.currentText()
        return newBox.text()


    def create_on_click(self, ind):
        self.stackedLayout.setCurrentIndex(ind)
        home = QPushButton('Home', self)
        home.clicked.connect(self.home_on_click)
        pageLayouts[ind].addWidget(home, alignment= Qt.AlignTop)
        self.newPageLayout= QHBoxLayout()
        if ind == 4: # container create
            newBox = QComboBox(pages[ind])
            for value in lists[0]:
                newBox.addItem(value.id)
        else: # pod create 
            newBox = QLineEdit(pages[ind])
        submit = QPushButton('Create', self)
        self.newPageLayout.addWidget(newBox)
        self.newPageLayout.addWidget(submit)
        pageLayouts[ind].addLayout(self.newPageLayout)
        pageLayouts[ind].addStretch(1)
        pages[ind].setLayout(pageLayouts[ind])
        pages[ind].setStyleSheet(open('stylesheet.css').read())
        submit.clicked.connect(lambda: self.create(ind, self.get_data(ind, newBox)))
        #newBox.activated[str].connect(self.create)

    def home_on_click(self):
        self.stackedLayout.setCurrentIndex(0)


if __name__ == '__main__':
    layout = QVBoxLayout()
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())