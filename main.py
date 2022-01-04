# main.py
# Initializes up an interactive Podman GUI
# currently has the ability to list containers, images and pods
# as well as create containers and pods
# github repo at https://github.com/cdoern/podman-gui

from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import QGridLayout, QTabWidget, QFrame, QTableWidget, QTableWidgetItem, QApplication, QLineEdit, QStackedLayout, QComboBox, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
from PyQt5.QtGui import QColor, QFont, QPalette, QPixmap
from PyQt5.QtCore import QSize, Qt
import podman
import sys
import urllib.parse
import os
import copy

lists = [] # stores the respective function calls to podman lists
pageLayouts = [] # stores the different page layouts
pages = [] # stores the pages that contain different layouts
tables = [] # used to store the tables for each page
currentUrl = '' # used to change socket location
createOutputs = [] # used to display all create IDs

# these hold the absolute dirs for images and files necessary for the project

bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
logoPath = os.path.abspath(os.path.join(bundle_dir, 'podman.png'))
stylePath = os.path.abspath(os.path.join(bundle_dir, 'stylesheet.qss'))
activePath = os.path.abspath(os.path.join(bundle_dir, 'active.png'))
inactivePath = os.path.abspath(os.path.join(bundle_dir, 'inactive.png'))
downPath = os.path.abspath(os.path.join(bundle_dir, 'down.png'))



client = podman.PodmanClient()

# class Widget defines and initializes a Qwidget containing a stacked layout each of which contains multiple sub layouts
class Window(QWidget): 
    def __init__(self):
        super().__init__()
        self.setFixedHeight(400)
        self.ping_client()
        self.setWindowTitle("Podman GUI")
        self.setLayout(layout)
        pal = self.palette()
        pal.setColor(QPalette.Window, QColor(146, 7, 181))
        self.setPalette(pal)
        self.left = 10
        self.top = 10
        self.initGUI()

    def initGUI(self):
        global currentUrl
        self.setLayout(layout)
        self.stackedLayout = QStackedLayout()

        # Home Screen Buttons
        imgs = QPushButton('List Images', self)
        ctrs = QPushButton('List Containers', self)
        pods = QPushButton('List Pods', self)
        ctrCreate = QPushButton('Create a Container', self)
        podCreate = QPushButton('Create a Pod', self)

        # tables for listing images, containers, pods
        tableImg = QTableWidget()
        tableImg.setUpdatesEnabled(True)

        tableCtr = QTableWidget()
        tableCtr.setUpdatesEnabled(True)

        tablePod = QTableWidget()
        tablePod.setUpdatesEnabled(True)

        tables.append(tableImg)
        tables.append(tableCtr)
        tables.append(tablePod)

        createCtr = QTableWidget()
        createCtr.setUpdatesEnabled(True)

        createPod = QTableWidget()
        createPod.setUpdatesEnabled(True)

        createCtr.setColumnCount(2)
        createPod.setColumnCount(2)
        createCtr.setHorizontalHeaderLabels(('Name', 'ID'))
        createPod.setHorizontalHeaderLabels(('Name', 'ID'))
        createCtr.setRowCount(1)
        createPod.setRowCount(1)

        tables.append(createCtr)
        tables.append(createPod)

        self.page1 = QWidget() # setup page 1 (home)
        self.page1Layout = QVBoxLayout()
        self.page1LayoutSub = QGridLayout() # we use a grid layout so we can place things side by side on the home screen
        self.page1LayoutSub.setHorizontalSpacing(50)
        self.page1LayoutButtons = QVBoxLayout()
        self.page1LayoutButtons.addWidget(imgs) # add buttons to thheir own box layout
        self.page1LayoutButtons.addWidget(ctrs)
        self.page1LayoutButtons.addWidget(pods)
        self.page1LayoutButtons.addWidget(ctrCreate)
        self.page1LayoutButtons.addWidget(podCreate)
        self.page1.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding,
                                                 QSizePolicy.MinimumExpanding))
        self.page1LayoutSub.addLayout(self.page1LayoutButtons, 0, 0) # add the buttons to the left most grid position
        version_report = client.version()
        self.page1LayoutInfo= QVBoxLayout()
        url = urllib.parse.unquote(client.api.base_url.geturl())
        url = url[url.index("+")+1:]
        podmanGUITitle = QLabel("PodmanGUI")
        podmanGUITitle.setFont(QFont('Arial', 20))
        self.page1LayoutInfo.addWidget(podmanGUITitle)
        # add relative podman info to the page
        socketLabel = QLabel("Unix Socket Location: "+url)
        self.page1LayoutInfo.addWidget(QLabel("Podman API Version: "+version_report["Components"][0]["Details"]["APIVersion"]))
        self.page1LayoutInfo.addWidget(socketLabel)
        currentUrl = url
        # create a status layout so we can modify it when the socket is changed
        status = QHBoxLayout()
        status.setSpacing(2)
        status.addWidget(QLabel("Podman Service Status:"))
        active = QLabel()
        active.setPixmap(QPixmap(inactivePath)) # this is the widget for the green/red circle indicating socket activity
        if client.ping():
           active.setPixmap(QPixmap(activePath))
        status.addWidget(active, alignment=Qt.AlignLeft)
        status.addStretch(1)
        self.page1LayoutInfo.addLayout(status)
        podmanPhoto = QPixmap(logoPath) # widget containing the podman logo
        logo = QLabel()
        logo.setPixmap(podmanPhoto)
        self.page1LayoutInfo.addWidget(logo)
        socketReset = QHBoxLayout()
        socketReset.setSpacing(5)
        newBox = QLineEdit()
        submit = QPushButton('Reset Socket Location', self)
        submit.clicked.connect(lambda: self.reset_socket(newBox.text(), socketLabel)) # when the reset socket button is clicked, call the function to save the new data (contained in newbox)
        socketReset.addWidget(newBox)
        socketReset.addWidget(submit)
        self.page1LayoutInfo.addLayout(socketReset)
        self.page1LayoutSub.addLayout(self.page1LayoutInfo, 0, 2)
        self.page1LayoutSub.setColumnStretch(1,1)
        self.page1LayoutSub.setVerticalSpacing(0)

        sep = QFrame() # the vertical line on the home screen needs its CSS defined here due to Qt issues
        sep.setStyleSheet("""
            QWidget {
                color: white
            }
        """)
        sep.setFrameShape(QFrame.VLine)
        sep.setLineWidth(3)

        self.page1LayoutSub.addWidget(sep, 0, 1) # add vertical line between the buttons and the podman info
        self.page1Layout.addLayout(self.page1LayoutSub)
        self.page1Layout.addStretch(1)
        pageLayouts.append(self.page1Layout)
        pages.append(self.page1)
        self.page1.setLayout(self.page1Layout)
        self.page1.setStyleSheet(open(stylePath).read())
        self.stackedLayout.addWidget(self.page1)

        self.page2 = QWidget() # list images page
        self.page2Layout = QVBoxLayout()
        self.stackedLayout.addWidget(self.page2)
        pageLayouts.append(self.page2Layout)
        pages.append(self.page2)

        self.page3 = QWidget() # list containers page
        self.page3Layout = QVBoxLayout()
        self.stackedLayout.addWidget(self.page3)
        pageLayouts.append(self.page3Layout)
        pages.append(self.page3)

        self.page4 = QWidget() # list pods page
        self.page4Layout = QVBoxLayout()
        self.stackedLayout.addWidget(self.page4)
        pageLayouts.append(self.page4Layout)
        pages.append(self.page4)

        self.page5 = QWidget() # create ctr page
        self.page5Layout = QVBoxLayout()
        self.page5CreateOutput = QLabel()
        self.stackedLayout.addWidget(self.page5)
        pageLayouts.append(self.page5Layout)
        pages.append(self.page5)
        createOutputs.append(self.page5CreateOutput)

        self.page6 = QWidget() # create pod page
        self.page6Layout = QVBoxLayout()
        self.page6CreateOutput = QLabel()
        self.stackedLayout.addWidget(self.page6)
        pageLayouts.append(self.page6Layout)
        pages.append(self.page6)
        createOutputs.append(self.page6CreateOutput)

        # connect the buttons to all of their functions, pass proper index
        imgs.clicked.connect(lambda: self.list_on_click(0, 1))
        ctrs.clicked.connect(lambda: self.list_on_click(1, 2))
        pods.clicked.connect(lambda: self.list_on_click(2, 3))
        ctrCreate.clicked.connect(lambda: self.create_on_click(4))
        podCreate.clicked.connect(lambda: self.create_on_click(5))
        

        layout.addLayout(self.stackedLayout)

    # list_on_click takes two indexes, defining which page to modify (img, ctr, pod) and uses this info
    # to list either the current running containers, pulled images, or created pods
    def list_on_click(self, val, ind):
        client = podman.PodmanClient(base_url=currentUrl) # make sure url is correct
        self.define_lists(client)
        self.stackedLayout.setCurrentIndex(ind)
        pageLayouts[ind].removeWidget(tables[val])
        pageLayouts[ind] = QVBoxLayout()
        home = QPushButton('Home')
        home.clicked.connect(self.home_on_click) # add home button to the page
        pageLayouts[ind].addWidget(home, alignment= Qt.AlignTop)  
        out = lists[val]() # get the list of either images, ctrs, or pods
        tables[val].clear() # retreive the proper table and clear it from our last usage
        tables[val].setRowCount(len(out))
        tables[val].setColumnCount(2)
        tables[val].setHorizontalHeaderLabels(('Name', 'ID'))
        for i in range(0, len(out)):
            if ind == 1: # listing images, we need to parse the output in a different way
                value = str((out)[i])
                tables[val].setItem(i, 0, QTableWidgetItem(value[value.index(' '):value.index('>')]))
            else: # else ctrs or pods, get the name
                value = out[i].name
                tables[val].setItem(i, 0, QTableWidgetItem(value))
            tables[val].setItem(i, 1, QTableWidgetItem(out[i].id)) # second column contains the ids
        tables[val].resizeColumnsToContents()
        tables[val].resizeRowsToContents()
        tables[val].update()
        pageLayouts[ind].addWidget(tables[val])
        pageLayouts[ind].addStretch(1)
        pages[ind].setLayout(pageLayouts[ind])
        pages[ind].setStyleSheet(open(stylePath).read()) # setStylesheet reads out .qss file for each page

    # create is a helper function for create_on_click, executing the actual podman function
    # this takes an index and a name and either creates a pod or a ctr with this name
    def create(self, ind, name):
        if ind == 4:
            obj = client.containers.create(name)
        else:
            obj = client.pods.create(name)
        print(obj.id)

        value = obj.name # now we add the container we created to the proper table
        tables[ind-1].setItem(tables[ind-1].rowCount()-1, 0, QTableWidgetItem(value))
        tables[ind-1].setItem(tables[ind-1].rowCount()-1, 1, QTableWidgetItem(obj.id)) # second column contains the ids
        tables[ind-1].resizeColumnsToContents()
        tables[ind-1].resizeRowsToContents()
        tables[ind-1].update()
        tables[ind-1].setRowCount(tables[ind-1].rowCount() + 1)
        pageLayouts[ind].addWidget(tables[ind-1])
        pageLayouts[ind].addStretch(1)
        pageLayouts[ind].setStretch(2, 30) # make sure table does not move with the stretch

 
        pages[ind].setLayout(pageLayouts[ind])
  
    # get_data gets the current text from either the ctr create drop down or the pod create text box         
    def get_data(self, ind, newBox):
        if ind == 4:
            return newBox.currentText()
        return newBox.text()

    # create_on_click is the function called when a user presses the "create a container" or "create a pod button"
    # this sets up each page and populates the data
    def create_on_click(self, ind):
        client = podman.PodmanClient(base_url=currentUrl)
        self.define_lists(client) # get img lists
        self.stackedLayout.setCurrentIndex(ind)
        pageLayouts[ind] = QVBoxLayout()
        home = QPushButton('Home', self)
        home.clicked.connect(self.home_on_click)
        pageLayouts[ind].addWidget(home, alignment= Qt.AlignTop)
        self.newPageLayout= QHBoxLayout()
        imgs = lists[0]()
        if ind == 4: # container create
            newBox = QComboBox(pages[ind])
            for value in imgs:
                newBox.addItem(value.id)
        else: # pod create 
            newBox = QLineEdit(pages[ind])
        submit = QPushButton('Create', self)
        self.newPageLayout.addWidget(newBox) # text or drop down box (img list or place to input pod name)
        self.newPageLayout.addWidget(submit)
        pageLayouts[ind].addLayout(self.newPageLayout)
        pageLayouts[ind].addStretch(1)
        pages[ind].setLayout(pageLayouts[ind])
        pages[ind].setStyleSheet(open(stylePath).read())
        submit.clicked.connect(lambda: self.create(ind, self.get_data(ind, newBox)))  # connect the create button to the actual create function

    # home_on_click returns the user to the home screen when clicked
    def home_on_click(self):
        self.stackedLayout.setCurrentIndex(0)

    # ping_client is how we test if the podman socket is up and running
    def ping_client(self):
        print("** Check Service Available")
        if client.ping():
            print("Service active")
        else:
            print(f"No service found @ {client.base_url}")

    # define_lists populates the image, containers, and pods list
    def define_lists(self, client):
        lists.clear
        lists.append(client.images.list)
        lists.append(client.containers.list)
        lists.append(client.pods.list)

    # delete_widgets is a helper function to fully clear out a Qt page
    def delete_widgets(self, ind):
        while pageLayouts[ind].count():
            child = pageLayouts[ind].takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    # reset_socket is the function used to change the socket global variable
    def reset_socket(self, newUrl, oldLabel):
        global currentUrl
        currentUrl = newUrl
        self.page1LayoutInfo.replaceWidget(oldLabel, QLabel("Unix Socket Location: "+newUrl))


if __name__ == '__main__':
    layout = QVBoxLayout()
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())