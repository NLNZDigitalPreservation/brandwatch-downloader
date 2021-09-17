import sys, os, platform
os.environ['CURL_CA_BUNDLE'] = ''
from datetime import datetime, timedelta
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from brandwatch import Brandwatch

# Login Form layer, check if token file not exist or invalid, show this layer
class LoginForm(QFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.gb = QGroupBox(self)
        self.gb.setStyleSheet('QGroupBox {border: 1px solid #D5DBDB; border-radius: 10px;}')
        self.gb.move(130, 140)
        self.gb.resize(460, 280)
        
        self.gbLabel = QLabel('Login', self)
        self.gbLabel.setStyleSheet('QLabel {border: 1px solid #D5DBDB; background-color: #D0D3D4; border-radius: 5px; font-family: Arial, sans-serif; font-size: 12pt; font-style: italic;}')
        self.gbLabel.setAlignment(Qt.AlignCenter)
        self.gbLabel.setAutoFillBackground(True)
        self.gbLabel.move(320, 125)
        self.gbLabel.resize(80, 36)

        # Display error/status message
        self.msg = QLabel(self)
        self.msg.setStyleSheet('color: #CB4335;')
        self.msg.setText('')
        self.msg.setAlignment(Qt.AlignCenter)
        self.msg.move(200, 165)
        self.msg.resize(320, 28)

        # Token input area
        self.tokenLabel = QLabel('Token', self)
        self.tokenLabel.setStyleSheet("font-family: Arial, sans-serif; font-size: 12pt;")
        self.tokenLabel.move(160, 200)
        self.tokenLabel.resize(90,36)
        self.tokenInput = QLineEdit(self)
        self.tokenInput.setStyleSheet("font-family: Arial, sans-serif; border: 1px solid grey; border-radius: 5px; font-size: 12pt;")
        self.tokenInput.move(250, 200)
        self.tokenInput.resize(320, 36)

        # Username/Password input area
        self.userLabel = QLabel('Username', self)
        self.userLabel.setStyleSheet("font-family: Arial, sans-serif; font-size: 12pt;")
        self.userLabel.move(160, 265)
        self.userLabel.resize(90,36)
        self.userInput = QLineEdit(self)
        self.userInput.setStyleSheet("font-family: Arial, sans-serif; border: 1px solid grey; border-radius: 5px; font-size: 12pt;")
        self.userInput.move(250, 265)
        self.userInput.resize(320, 36)

        self.pwdLabel = QLabel('Password', self)
        self.pwdLabel.setStyleSheet("font-family: Arial, sans-serif; font-size: 12pt;")
        self.pwdLabel.move(160, 310)
        self.pwdLabel.resize(90,36)
        self.pwdInput = QLineEdit(self)
        self.pwdInput.setEchoMode(QLineEdit.Password)
        self.pwdInput.setStyleSheet("font-family: Arial, sans-serif; border: 1px solid grey; border-radius: 5px; font-size: 12pt;")
        self.pwdInput.move(250, 310)
        self.pwdInput.resize(320, 36)

        self.loginBtn = QPushButton(self)
        self.loginBtn.setText('Login')
        self.loginBtn.setStyleSheet("font-family: Arial, sans-serif; font-size: 12pt;")
        self.loginBtn.move(300, 360)
        self.loginBtn.resize(120, 32)

    # Set click action for login button
    def func(self, loginFunc):
        self.loginBtn.clicked.connect(loginFunc)

    def paintEvent(self, event):
        self.seperator = QPainter()
        self.seperator.begin(self)
        self.seperator.setRenderHint(QPainter.Antialiasing)
        self.seperator.setPen(Qt.gray)
        self.seperator.setBrush(Qt.white)
        self.seperator.drawLine(150,250,570,250)
        self.seperator.end()

# Custom list menu 
class SelectList(QListWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.listWidget = QListWidget(self)

    def addItems(self, items):
        self.listWidget.addItems(items)

    def addItem(self, item):
        self.listWidget.addItem(item)

    def getItems(self):
        return [str(self.listWidget.item(x).text()) for x in range(self.listWidget.count())]

    # Set item click action
    def clicked(self, func):
        self.listWidget.itemClicked.connect(func)
    
    # Get size of current list
    def size(self, w, h):
        self.listWidget.resize(w, h)

    # Sort current list with default ASC order
    def sort(self):
        self.listWidget.sortItems()

    # Clear items in list
    def clear(self):
        self.listWidget.clear()

# Download layer, it will show current user, list all projects under the user, choose groups based on project, choose queries based on project/groups, get mentions and download in different format.
class Downloader(QFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.select = {'groups': None, 'queries': None}
        self.dataset = pd.DataFrame([])
        self.icon_file = b'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'
        self.icon_folder = b'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'
        self.savePath = self.convertPath(os.getcwd()+'/dataset.csv')

        # Display current user
        self.userLabel = QLabel(self)
        self.userLabel.setText('Current user: ')
        self.userLabel.move(20, 10)
        self.userLabel.resize(240,28)

        self.projectsLabel = QLabel(self)
        self.projectsLabel.setText('Project Name:')
        self.projectsLabel.move(20, 40)
        self.projectsLabel.resize(120, 36)

        # List all projects
        self.projects = QComboBox(self)
        self.projects.addItems([])
        self.projects.move(140, 40)
        self.projects.resize(240, 36)

        # Fetch group list based on project
        self.getGroupsBtn = QPushButton(self)
        self.getGroupsBtn.setText('Get Groups')
        self.getGroupsBtn.move(400, 40)
        self.getGroupsBtn.resize(120, 36)
        self.getGroupsBtn.setToolTip('Get groups of selected project')

        # Fetch query list based on groups
        self.getQueriesBtn = QPushButton(self)
        self.getQueriesBtn.setText('Get Queries')
        self.getQueriesBtn.move(540, 40)
        self.getQueriesBtn.resize(120, 36)
        self.getQueriesBtn.setToolTip('Get queries of selected groups')
  
        # Groups and selected groups, click item will move to another side, or click button to select/unselect all
        self.groups = SelectList(self)
        self.groups.addItems([])
        self.groups.size(240, 160)
        self.groups.move(20, 85)
        self.groups.resize(240, 160)
        self.groups.clicked(self.setSelectGroupItem)

        self.groupsLabel = QLabel(self)
        self.groupsLabel.setText('Groups')
        self.groupsLabel.move(280, 95)
        self.groupsLabel.resize(120, 30)
        self.groupsLabel.setAlignment(Qt.AlignCenter)

        self.selectAllgroups = QPushButton(self)
        self.selectAllgroups.setText('Select all >>')
        self.selectAllgroups.move(280, 135)
        self.selectAllgroups.resize(120, 30)
        self.selectAllgroups.clicked.connect(self.setSelectAllGroups)
        self.selectAllgroups.setToolTip('Select all groups')

        self.unselectAllgroups = QPushButton(self)
        self.unselectAllgroups.setText('<< Unselect all')
        self.unselectAllgroups.move(280, 185)
        self.unselectAllgroups.resize(120, 30)
        self.unselectAllgroups.clicked.connect(self.setUnselectAllGroups)
        self.unselectAllgroups.setToolTip('Unselect all groups')

        self.select['groups'] = SelectList(self)
        self.select['groups'].addItems([])
        self.select['groups'].size(240, 160)
        self.select['groups'].move(420, 85)
        self.select['groups'].resize(240, 160)
        self.select['groups'].clicked(self.setUnselectGroupItem)

        # Queries and selected queries, click item will move to another side, or click button to select/unselect all
        self.queries = SelectList(self)
        self.queries.addItems([])
        self.queries.size(240, 160)
        self.queries.move(20, 260)
        self.queries.resize(240, 160)
        self.queries.clicked(self.setSelectQueriesItem)

        self.queriesLabel = QLabel(self)
        self.queriesLabel.setText('Queries')
        self.queriesLabel.move(280, 270)
        self.queriesLabel.resize(120, 30)
        self.queriesLabel.setAlignment(Qt.AlignCenter)

        self.selectAllqueries = QPushButton(self)
        self.selectAllqueries.setText('Select all >>')
        self.selectAllqueries.move(280, 310)
        self.selectAllqueries.resize(120, 30)
        self.selectAllqueries.clicked.connect(self.setSelectAllQueries)
        self.selectAllqueries.setToolTip('Select all queries')

        self.unselectAllquries = QPushButton(self)
        self.unselectAllquries.setText('<< Unselect all')
        self.unselectAllquries.move(280, 360)
        self.unselectAllquries.resize(120, 30)
        self.unselectAllquries.clicked.connect(self.setUnselectAllQueries)
        self.unselectAllquries.setToolTip('Unselect all queries')

        self.select['queries'] = SelectList(self)
        self.select['queries'].addItems([])
        self.select['queries'].size(240, 160)
        self.select['queries'].move(420, 260)
        self.select['queries'].resize(240, 160)
        self.select['queries'].clicked(self.setUnselectQueriesItem)

        # Display logs and progress
        self.log_text_box = QPlainTextEdit(self)
        self.log_text_box.setReadOnly(True)
        self.log_text_box.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.log_text_box.move(20, 480)
        self.log_text_box.resize(400, 140)
        self.log_text_box.appendPlainText('')

        # Pre-defined period, 1W, 1M, 3M, 6M, 1Y
        self.p1 = QPushButton(self)
        self.p1.setText('1W')
        self.p1.move(20, 440)
        self.p1.resize(36, 30)
        self.p1.clicked.connect(self.period1W)
        self.p1.setToolTip('Pre defined 1 week')

        self.p2 = QPushButton(self)
        self.p2.setText('1M')
        self.p2.move(56, 440)
        self.p2.resize(36, 30)
        self.p2.clicked.connect(self.period1M)
        self.p2.setToolTip('Pre defined 1 month')

        self.p3 = QPushButton(self)
        self.p3.setText('3M')
        self.p3.move(92, 440)
        self.p3.resize(36, 30)
        self.p3.clicked.connect(self.period3M)
        self.p3.setToolTip('Pre defined 3 months')

        self.p4 = QPushButton(self)
        self.p4.setText('6M')
        self.p4.move(128, 440)
        self.p4.resize(36, 30)
        self.p4.clicked.connect(self.period6M)
        self.p4.setToolTip('Pre defined 6 months')

        self.p5 = QPushButton(self)
        self.p5.setText('1Y')
        self.p5.move(164, 440)
        self.p5.resize(36, 30)
        self.p5.clicked.connect(self.period1Y)
        self.p5.setToolTip('Pre defined 1 year')

        # Select time zone, default is UTC
        self.utcBtn = QRadioButton(self)
        self.utcBtn.setText('UTC')
        self.utcBtn.setChecked(True)
        self.utcBtn.move(230, 440)
        self.utcBtn.resize(60, 30)

        self.nztBtn = QRadioButton(self)
        self.nztBtn.setText('NZT')
        self.nztBtn.move(290, 440)
        self.nztBtn.resize(60, 30)

        self.tzBtnGrp = QButtonGroup(self)
        self.tzBtnGrp.addButton(self.utcBtn, 1)
        self.tzBtnGrp.addButton(self.nztBtn, 2)

        # Set pre-defined time or custom start/end time
        self.startLabel = QLabel(self)
        self.startLabel.setText('Start')
        self.startLabel.setStyleSheet("font-family: Arial, sans-serif; font-size: 10pt;")
        self.startLabel.move(350, 420)
        self.startLabel.resize(80, 20)

        self.startTime = QDateTimeEdit(self)
        self.startTime.setDisplayFormat('yyyy-MM-dd hh:mm')
        self.startTime.setDateTime(datetime.strptime(datetime.utcnow().strftime('%Y-%m-%d %H:00'), '%Y-%m-%d %H:%M') - timedelta(days=7))
        self.startTime.move(350, 440)
        self.startTime.resize(150, 30)

        self.endLabel = QLabel(self)
        self.endLabel.setText('End')
        self.endLabel.setStyleSheet("font-family: Arial, sans-serif; font-size: 10pt;")
        self.endLabel.move(510, 420)
        self.endLabel.resize(80, 20)

        self.endTime = QDateTimeEdit(self)
        self.endTime.setDisplayFormat('yyyy-MM-dd hh:mm')
        self.endTime.setDateTime(datetime.strptime(datetime.utcnow().strftime('%Y-%m-%d %H:00'), '%Y-%m-%d %H:%M'))
        self.endTime.move(510, 440)
        self.endTime.resize(150, 30)

        # Fetch data based on the filter selection, this should be clicked before download button.
        self.fetchBtn = QPushButton(self)
        self.fetchBtn.setText('Fetch Data')
        self.fetchBtn.move(495, 480)
        self.fetchBtn.resize(100, 26)
        self.fetchBtn.setToolTip('Fetch data from Brandwatch')

        # Set download file's format, default is CSV (delimiter with comma)
        self.formatLabel = QLabel(self)
        self.formatLabel.setText('Format')
        self.formatLabel.move(430, 510)
        self.formatLabel.resize(60, 26)

        self.formats = QComboBox(self)
        self.formats.addItems(['CSV (delimiter with comma)', 'CSV (delimiter with pipe)','EXCEL', 'JSON'])
        self.formats.move(495, 510)
        self.formats.resize(165, 26)
        self.formats.currentIndexChanged.connect(self.changeFormat)

        # Set order by attr, this list will only show after data is fetched
        self.orderbyLabel = QLabel(self)
        self.orderbyLabel.setText('OrderBy')
        self.orderbyLabel.move(430, 540)
        self.orderbyLabel.resize(60, 26)

        self.orderby = QComboBox(self)
        self.orderby.addItems([])
        self.orderby.move(495, 540)
        self.orderby.resize(105, 26)

        self.order = QComboBox(self)
        self.order.addItems(['ASC','DESC'])
        self.order.move(600, 540)
        self.order.resize(60, 26)

        # Set save file path, you can click first button to select folder/file, if you select folder, default file name will be appended, you can change it manually. You also can open second button to open destination folder.
        self.saveLabel = QLabel(self)
        self.saveLabel.setText('Save to')
        self.saveLabel.move(430, 565)
        self.saveLabel.resize(60, 26)
        self.saveInput = QLineEdit(self)
        self.saveInput.setStyleSheet("border: 1px solid grey; border-radius: 5px;")
        self.saveInput.textChanged.connect(self.setSavePath)
        self.saveInput.setText(self.savePath)
        self.saveInput.move(495, 568)
        self.saveInput.resize(110, 24)
        self.saveBtn = QPushButton(self)
        self.saveBtn.setIcon(self.iconFromBase64(self.icon_file))
        self.saveBtn.clicked.connect(self.saveSelector)
        self.saveBtn.move(610, 568)
        self.saveBtn.resize(24, 24)
        self.saveBtn.setToolTip('Choose file or folder to save data')
        self.openSaveBtn = QPushButton(self)
        self.openSaveBtn.setIcon(self.iconFromBase64(self.icon_folder))
        self.openSaveBtn.clicked.connect(self.saveOpen)
        self.openSaveBtn.move(636, 568)
        self.openSaveBtn.resize(24, 24)
        self.openSaveBtn.setToolTip('Open destination folder')

        # Save data locally, this can only be used after data fetched.
        self.downloadBtn = QPushButton(self)
        self.downloadBtn.setText('Download')
        self.downloadBtn.move(495, 595)
        self.downloadBtn.resize(100, 26)
        self.downloadBtn.setToolTip('Download data to destination path')

    # Open folder/file selector
    def getOpenFilesAndDirs(self, parent=None, caption='', directory='', filter='', initialFilter='', options=None):
        def updateText():
            selected = []
            for index in view.selectionModel().selectedRows():
                selected.append('{}'.format(index.data()))
            lineEdit.setText(' '.join(selected))

        dialog = QFileDialog(parent, windowTitle=caption)
        dialog.setFileMode(dialog.ExistingFiles)
        if options:
            dialog.setOptions(options)
        dialog.setOption(dialog.DontUseNativeDialog, True)
        if directory:
            dialog.setDirectory(directory)
        if filter:
            dialog.setNameFilter(filter)
            if initialFilter:
                dialog.selectNameFilter(initialFilter)
        dialog.accept = lambda: QDialog.accept(dialog)
        stackedWidget = dialog.findChild(QStackedWidget)
        view = stackedWidget.findChild(QListView)
        view.selectionModel().selectionChanged.connect(updateText)

        lineEdit = dialog.findChild(QLineEdit)
        dialog.directoryEntered.connect(lambda: lineEdit.setText(''))

        dialog.exec_()
        return dialog.selectedFiles()

    # Convert path depends on the platform
    def convertPath(self, originalPath):
        if platform.system() == 'Windows':
            p = originalPath.replace('/','\\')
        else:
            p = originalPath
        return p
    
    # Save path
    def setSavePath(self, text):
        self.savePath = text

    def saveSelector(self):
        self.savePath = self.getOpenFilesAndDirs()
        if len(self.savePath) > 0:
            self.savePath = self.convertPath(self.savePath[0])
            self.changeFormat()

    def saveOpen(self):
        if self.savePath != '':
            if os.path.exists(self.savePath) is not True or os.path.isfile(self.savePath):
                filepath = os.path.dirname(self.savePath)
            else:
                filepath = self.savePath
            if platform.system() == 'Windows':
                os.system(f'start {os.path.realpath(filepath)}')
            else:
                os.system('xdg-open "%s"' % filepath)

    # If the format is changed, the ext can be changed automatically
    def changeFormat(self):
        if os.path.isdir(self.savePath):
            self.savePath = self.savePath + '/dataset'
        pre, ext = os.path.splitext(self.savePath)
        if self.formats.currentText() == 'JSON':
            self.savePath = pre + '.json'
        elif self.formats.currentText() == 'EXCEL':
            self.savePath = pre + '.xlsx'
        else:
            self.savePath = pre + '.csv'
        self.saveInput.setText(self.savePath)
    
    # Set time period actions
    def period1W(self):
        self.startTime.setDateTime(datetime.strptime(self.endTime.text(), '%Y-%m-%d %H:%M') - timedelta(days=7))
    
    def period1M(self):
        self.startTime.setDateTime(datetime.strptime(self.endTime.text(), '%Y-%m-%d %H:%M') - timedelta(days=30))

    def period3M(self):
        self.startTime.setDateTime(datetime.strptime(self.endTime.text(), '%Y-%m-%d %H:%M') - timedelta(days=90))
    
    def period6M(self):
        self.startTime.setDateTime(datetime.strptime(self.endTime.text(), '%Y-%m-%d %H:%M') - timedelta(days=180))

    def period1Y(self):
        self.startTime.setDateTime(datetime.strptime(self.endTime.text(), '%Y-%m-%d %H:%M') - timedelta(days=365))

    # Set username
    def setUsername(self, username):
        self.userLabel.setText('Current user: ' + username)

    # Set button actions
    def setGetGroupsAction(self, func):
        self.getGroupsBtn.clicked.connect(func)

    def setGetQueriesAction(self, func):
        self.getQueriesBtn.clicked.connect(func)

    def setFetchAction(self, func):
        self.fetchBtn.clicked.connect(func)

    def setDownloadAction(self, func):
        self.downloadBtn.clicked.connect(func)

    def setTimezone(self, func):
        self.tzBtnGrp.buttonClicked.connect(func)

    # Set dataset
    def setProjects(self, projects):
        self.projects.clear()
        self.projects.addItems(projects)

    def setGroups(self, groups):
        self.groups.clear()
        self.select['groups'].clear()
        self.groups.addItems(groups)
        self.groups.sort()

    def setOrderby(self, orderby):
        self.orderby.clear()
        self.orderby.addItems(orderby)
    
    def setDataset(self, dataset):
        self.dataset = dataset

    def setSelectAllGroups(self, func):
        groups = self.groups.getItems()
        self.groups.clear()
        self.select['groups'].addItems(groups)
        self.select['groups'].sort()

    def setUnselectAllGroups(self, func):
        groups = self.select['groups'].getItems()
        self.select['groups'].clear()
        self.groups.addItems(groups)
        self.groups.sort()

    def setSelectGroupItem(self, item):
        groups = self.groups.getItems()
        groups.remove(item.text())
        self.select['groups'].addItem(item.text())
        self.select['groups'].sort()
        self.groups.clear()
        self.groups.addItems(groups)
        self.groups.sort()

    def setUnselectGroupItem(self, item):
        groups = self.select['groups'].getItems()
        groups.remove(item.text())
        self.groups.addItem(item.text())
        self.groups.sort()
        self.select['groups'].clear()
        self.select['groups'].addItems(groups)
        self.select['groups'].sort()

    def setQueries(self, queries):
        self.queries.clear()
        self.select['queries'].clear()
        self.queries.addItems(queries)
        self.queries.sort()

    def setSelectAllQueries(self, func):
        queries = self.queries.getItems()
        self.queries.clear()
        self.select['queries'].addItems(queries)
        self.select['queries'].sort()

    def setUnselectAllQueries(self, func):
        queries = self.select['queries'].getItems()
        self.select['queries'].clear()
        self.queries.addItems(queries)
        self.queries.sort()

    def setSelectQueriesItem(self, item):
        queries = self.queries.getItems()
        queries.remove(item.text())
        self.select['queries'].addItem(item.text())
        self.select['queries'].sort()
        self.queries.clear()
        self.queries.addItems(queries)
        self.queries.sort()

    def setUnselectQueriesItem(self, item):
        queries = self.select['queries'].getItems()
        queries.remove(item.text())
        self.queries.addItem(item.text())
        self.queries.sort()
        self.select['queries'].clear()
        self.select['queries'].addItems(queries)
        self.select['queries'].sort()

    # Set icon image from base64
    def iconFromBase64(self, base64):
        pixmap = QPixmap()
        pixmap.loadFromData(QByteArray.fromBase64(base64))
        icon = QIcon(pixmap)
        return icon

# Multi-thread worker object
class Worker(QObject):
    # Set signal to get updates
    finished = pyqtSignal()
    BWObject = pyqtSignal(object)
    results = pyqtSignal(object)
    logger = pyqtSignal(object)

    BW = None

    # Set parameters
    def setProject(self, project):
        self.project = project

    def setGroup(self, group):
        self.group = group

    def setGroups(self, groups):
        self.groups = groups

    def setQuery(self, query):
        self.query = query

    def setQueries(self, queries):
        self.queries = queries

    def setStart(self, start):
        self.start = start
    
    def setEnd(self, end):
        self.end = end

    def setType(self, type):
        self.type = type

    def setBW(self, BW):
        self.BW = BW

    def setToken(self, token):
        self.token = token

    def setUserPwd(self, username, pwd):
        self.username = username
        self.pwd = pwd

    # Run thread
    def run(self):
        # Set default value if Brandwatch object exists, default terminate is False, and set logger
        if self.BW is not None:
            self.BW.terminate(False)
            self.BW.setLogger(self.logger)
        if self.type == 'loginToken':
            try:
                self.BW = Brandwatch(token=self.token, token_path='.brandwatch_token', terminate=False, logger=self.logger)
                self.user = self.BW.getUser()
                if self.user is not None:
                    self.BWObject.emit(self.BW)
                self.results.emit(self.user)
            except:
                self.results.emit(None)
        elif self.type == 'loginUser':
            try:
                self.BW = Brandwatch(username=self.username, password=self.pwd, token_path='.brandwatch_token', terminate=False, logger=self.logger)
                self.user = self.BW.getUser()
                if self.user is not None:
                    self.BWObject.emit(self.BW)
                self.results.emit(self.user)
            except:
                self.results.emit(None)
        elif self.type == 'getProjects':
            try:
                projects = []
                projects = self.BW.getProjects()
                self.results.emit(projects)
            except Exception as e:
                self.logger.emit('Error: ' + str(e))
                self.results.emit([])
        elif self.type == 'getGroups':
            try:
                groups = None
                self.BW.getGroups(str(self.project))
                groups = self.BW.GroupsDF()
                self.results.emit(groups['name'].values)
            except Exception as e:
                self.logger.emit('Error: ' + str(e))
                self.results.emit([])
        elif self.type == 'getQueries':
            try:
                queries = None
                self.BW.getQueries(str(self.project))
                queries = self.BW.QueriesDF()
                if len(queries) > 0:
                    self.results.emit(queries['name'].tolist())
                else:
                    self.results.emit([])
            except Exception as e:
                self.logger.emit('Error: ' + str(e))
                self.results.emit([])
        elif self.type == 'getQueriesByGroup':
            try:
                queries = []
                for group in self.groups:
                    try:
                        self.logger.emit('Fetching queries of group[' + group + '] ...')
                        self.BW.getQueriesByGroup(str(group))
                        query = self.BW.GroupQueriesDF()
                        if len(query) > 0:
                            try:
                                queries = queries + query['name'].tolist()
                                self.logger.emit('Fetched queries of group[' + group + ']')
                            except Exception as e1:
                                self.logger.emit('Error: ' + str(e1))
                                pass
                    except Exception as e2:
                        self.logger.emit('Error: ' + str(e2))
                        pass
                self.results.emit(queries)
            except Exception as e3:
                self.logger.emit('Error: ' + str(e3))
                self.results.emit([])
        elif self.type == 'getMentions':
            try:
                mentions = pd.DataFrame([])
                for query in self.queries:
                    try:
                        self.logger.emit('Fetching mentions of query[' + query + '] ...')
                        self.BW.getMentions(self.project, query, self.start, self.end)
                        self.logger.emit('Converting data ...')
                        mention = self.BW.MentionsDF()
                        if len(mention) > 0:
                            try:
                                if len(mentions) == 0:
                                    mentions = mention
                                else:
                                    mentions.append(mention)
                                self.logger.emit('Fetched mentions of query[' + query + ']')
                            except Exception as e1:
                                self.logger.emit('Error: ' + str(e1))
                                pass
                    except Exception as e2:
                        self.logger.emit('Error: ' + str(e2))
                        pass
                self.results.emit(mentions)
            except Exception as e3:
                self.logger.emit('Error: ' + str(e3))
                self.results.emit(pd.DataFrame([]))
        self.finished.emit()

    def terminate(self):
        self.BW.terminate(True)


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Brandwatch Downloader V1.0')
        self.setFixedWidth(680)
        self.setFixedHeight(640)

        # Check token exists or not
        if os.path.isfile('.brandwatch_token'):
            try:
                f = open('.brandwatch_token','r')
                token = f.read().split('\t')[1]
                f.close()
                self.BW = Brandwatch(token=token, token_path='.brandwatch_token')
            except:
                self.BW = Brandwatch(token_path='.brandwatch_token')
        else:
            self.BW = Brandwatch(token_path='.brandwatch_token')
        
        # Set 60 seconds delay to retry if rate limit reach
        self.BW.set_delay(60)
        
        self.login = LoginForm(self)
        self.downloader = Downloader(self)

        # If user token not exist/expire, show login layer, otherwise show download layer
        self.user = self.BW.getUser()
        self.login.func(self.loginAction)
        if self.user == None:
            self.loginUI()
        else:
            self.downloaderUI()
    
    # Display logs
    def loggerHandler(self, value):
        if value == 'Token is invalid or expired':
            self.loginUI()
        else:
            self.downloader.log_text_box.appendPlainText(value)

    # Update parameters
    def updateBW(self, BW):
        self.BW = BW

    def updateUser(self, user):
        if user == None:
            self.login.msg.setStyleSheet('color: #CB4335;')
            self.login.msg.setText('Invalid token')
            self.login.loginBtn.setEnabled(True)
        else:
            self.user = user
            self.downloaderUI()

    def updateProjects(self, projects):
        self.downloader.setProjects(self.getProjectname(projects))
        self.downloader.setGetGroupsAction(self.getGroupsAction)
        self.downloader.setGetQueriesAction(self.getQueriesAction)
        self.downloader.setFetchAction(self.fetchDataAction)
        self.downloader.setDownloadAction(self.downloadData)
        self.downloader.setTimezone(self.timeConvert)

    def updateGroups(self, groups):
        self.downloader.setGroups(self.remove_duplicates(groups))

    def updateQueries(self, queries):
        self.downloader.setQueries(self.remove_duplicates(queries))

    def updateFetchedData(self, data):
        self.downloader.setOrderby(data.columns.tolist())
        self.downloader.setDataset(data)

    # Save data locally
    def downloadData(self):
        self.downloader.downloadBtn.setEnabled(False)
        self.loggerHandler('Downloading dataset ...')
        self.downloader.changeFormat()
        order = self.downloader.order.currentText()
        format = self.downloader.formats.currentText()
        df = pd.DataFrame([])
        try:
            if order == 'ASC':
                df = self.downloader.dataset.sort_values(by = self.downloader.orderby.currentText(), ascending = True)
            elif order == 'DESC':
                df = self.downloader.dataset.sort_values(by = self.downloader.orderby.currentText(), ascending = False)
            if format == 'JSON':
                df.to_json(self.downloader.savePath, orient = 'records')
            elif format == 'CSV (delimiter with comma)':
                df.to_csv(self.downloader.savePath, sep = ',', index = False)
            elif format == 'CSV (delimiter with pipe)':
                df.to_csv(self.downloader.savePath, sep = '|', index = False)
            elif format == 'EXCEL':
                df.to_excel(self.downloader.savePath, index = False)
        except Exception as e:
            self.loggerHandler('Error: ' + str(e))
            pass
        self.loggerHandler('Downloaded dataset into ' + self.downloader.savePath)
        self.loggerHandler('-------------------------------')
        self.downloader.downloadBtn.setEnabled(True)
    
    # Extract username from BWUser object
    def getUsername(self, user):
        try:
            username = ' '.join(user.__dict__['username'].split('@')[0].split('.'))
        except:
            username = user
        return username

    # Extract project name from BWProject object list
    def getProjectname(self, projects):
        return list(map(lambda x: str(x['name']), projects))

    # Login action, login with token or username/password
    def loginAction(self):
        self.login.msg.setStyleSheet('color: #1E8449;')
        self.loginThread = QThread()
        self.loginWorker = Worker()
        if self.login.tokenInput.text() != None and self.login.tokenInput.text() != '':
            self.login.msg.setText('Verifying token ...')
            self.login.loginBtn.setEnabled(False)             
            self.loginWorker.setType('loginToken')
            self.loginWorker.setToken(self.login.tokenInput.text())
        else:
            self.login.msg.setText('Verifying username/password ...')
            self.login.loginBtn.setEnabled(False) 
            self.loginWorker.setType('loginUser')
            self.loginWorker.setUserPwd(self.login.userInput.text(), self.login.pwdInput.text())
        self.loginWorker.moveToThread(self.loginThread)
        self.loginThread.started.connect(self.loginWorker.run)
        self.loginWorker.finished.connect(self.loginThread.quit)
        self.loginWorker.finished.connect(self.loginWorker.deleteLater)
        self.loginThread.finished.connect(self.loginThread.deleteLater)
        self.loginWorker.BWObject.connect(self.updateBW)
        self.loginWorker.results.connect(self.updateUser)
        self.loginThread.start()

    # Set login layer visible
    def loginUI(self):
        self.login.msg.setText('')
        self.login.setVisible(True)
        self.downloader.setVisible(False)

    # Set download layer visible
    def downloaderUI(self):
        self.downloader.setUsername(self.getUsername(self.user))
        self.login.setVisible(True)
        self.downloader.setVisible(False)

        self.login.msg.setStyleSheet('color: #1E8449;')
        self.login.msg.setText('Verifying user credential ...')
        self.login.loginBtn.setEnabled(False)

        self.downloader.log_text_box.clear()

        self.loggerHandler('Fetching project list ...')
        # Get projects
        self.projectsThread = QThread()
        self.projectsWorker = Worker()
        self.projectsWorker.setBW(self.BW)
        self.projectsWorker.setType('getProjects')
        self.projectsWorker.moveToThread(self.projectsThread)
        self.projectsThread.started.connect(self.projectsWorker.run)
        self.projectsWorker.finished.connect(self.projectsThread.quit)
        self.projectsWorker.finished.connect(self.projectsWorker.deleteLater)
        self.projectsThread.finished.connect(self.projectsThread.deleteLater)
        self.projectsWorker.results.connect(self.updateProjects)
        self.projectsWorker.logger.connect(self.loggerHandler)
        self.projectsThread.start()

        self.downloader.getQueriesBtn.setEnabled(False)
        self.downloader.fetchBtn.setEnabled(False)
        self.downloader.downloadBtn.setEnabled(False)

        self.projectsThread.finished.connect(lambda: self.downloader.setVisible(True))
        self.projectsThread.finished.connect(lambda: self.login.setVisible(False))
        self.projectsThread.finished.connect(lambda: self.login.loginBtn.setEnabled(True))
        self.projectsThread.finished.connect(lambda: self.loggerHandler('Project list fetched'))
        self.projectsThread.finished.connect(lambda: self.loggerHandler('-------------------------------'))

    # Set Get groups button action
    def getGroupsAction(self):
        self.downloader.getGroupsBtn.setEnabled(False)
        self.loggerHandler('Fetching group list by project['+self.downloader.projects.currentText()+']...')
        self.groupsThread = QThread()
        self.groupsWorker = Worker()
        self.groupsWorker.setBW(self.BW)
        self.groupsWorker.setType('getGroups')
        self.groupsWorker.setProject(self.downloader.projects.currentText())
        self.groupsWorker.moveToThread(self.groupsThread)
        self.groupsThread.started.connect(self.groupsWorker.run)
        self.groupsWorker.finished.connect(self.groupsThread.quit)
        self.groupsWorker.finished.connect(self.groupsWorker.deleteLater)
        self.groupsThread.finished.connect(self.groupsThread.deleteLater)
        self.groupsWorker.results.connect(self.updateGroups)
        self.groupsWorker.logger.connect(self.loggerHandler)
        self.groupsThread.start()

        self.groupsThread.finished.connect(lambda: self.loggerHandler('Group list fetched'))
        self.groupsThread.finished.connect(lambda: self.loggerHandler('-------------------------------'))
        self.groupsThread.finished.connect(lambda: self.downloader.getGroupsBtn.setEnabled(True))
        self.groupsThread.finished.connect(lambda: self.downloader.getQueriesBtn.setEnabled(True))
        self.groupsThread.finished.connect(lambda: self.downloader.fetchBtn.setEnabled(False))
        self.groupsThread.finished.connect(lambda: self.downloader.downloadBtn.setEnabled(False))

    # Set Get queries button action
    def getQueriesAction(self):
        self.downloader.getQueriesBtn.setEnabled(False)
        self.queriesThread = QThread()
        self.queriesWorker = Worker()
        self.queriesWorker.setBW(self.BW)
        if len(self.downloader.select['groups'].getItems()) == 0:
            self.queriesWorker.setType('')
        elif len(self.downloader.groups.getItems()) == 0:
            self.loggerHandler('Fetching queries list of project['+self.downloader.projects.currentText()+']...')
            self.queriesWorker.setType('getQueries')
            self.queriesWorker.setProject(self.downloader.projects.currentText())
        else:
            self.loggerHandler('Fetching queries list by selected groups...')
            self.queriesWorker.setType('getQueriesByGroup')
            self.queriesWorker.setGroups(self.downloader.select['groups'].getItems())
        self.queriesWorker.moveToThread(self.queriesThread)
        self.queriesThread.started.connect(self.queriesWorker.run)
        self.queriesWorker.finished.connect(self.queriesThread.quit)
        self.queriesWorker.finished.connect(self.queriesWorker.deleteLater)
        self.queriesThread.finished.connect(self.queriesThread.deleteLater)
        self.queriesWorker.results.connect(self.updateQueries)
        self.queriesWorker.logger.connect(self.loggerHandler)
        self.queriesThread.start()

        self.queriesThread.finished.connect(lambda: self.loggerHandler('Queries list fetched'))
        self.queriesThread.finished.connect(lambda: self.loggerHandler('-------------------------------'))
        self.queriesThread.finished.connect(lambda: self.downloader.getQueriesBtn.setEnabled(True))
        self.queriesThread.finished.connect(lambda: self.downloader.fetchBtn.setEnabled(True))
        self.queriesThread.finished.connect(lambda: self.downloader.downloadBtn.setEnabled(False))

    # Set fetch data button action
    def fetchDataAction(self):
        self.downloader.fetchBtn.setEnabled(False)
        if self.downloader.nztBtn.isChecked():
            start = self.BW.NZT2UTC(self.downloader.startTime.text()+':00')
            end = self.BW.NZT2UTC(self.downloader.endTime.text()+':00')
        elif self.downloader.utcBtn.isChecked():
            start = (self.downloader.startTime.text()+':00').replace(' ', 'T')
            end = (self.downloader.endTime.text()+':00').replace(' ', 'T')
        self.loggerHandler('Fetching mentions ...')
        self.mentionsThread = QThread()
        self.mentionsWorker = Worker()
        self.mentionsWorker.setBW(self.BW)
        self.mentionsWorker.setType('getMentions')
        self.mentionsWorker.setProject(self.downloader.projects.currentText())
        self.mentionsWorker.setQueries(self.downloader.select['queries'].getItems())
        self.mentionsWorker.setStart(start)
        self.mentionsWorker.setEnd(end)
        self.mentionsWorker.moveToThread(self.mentionsThread)
        self.mentionsThread.started.connect(self.mentionsWorker.run)
        self.mentionsWorker.finished.connect(self.mentionsThread.quit)
        self.mentionsWorker.finished.connect(self.mentionsWorker.deleteLater)
        self.mentionsThread.finished.connect(self.mentionsThread.deleteLater)
        self.mentionsWorker.results.connect(self.updateFetchedData)
        self.mentionsWorker.logger.connect(self.loggerHandler)
        self.mentionsThread.start()

        self.mentionsThread.finished.connect(lambda: self.loggerHandler('Mentions fetched'))
        self.mentionsThread.finished.connect(lambda: self.loggerHandler('-------------------------------'))
        self.mentionsThread.finished.connect(lambda: self.downloader.fetchBtn.setEnabled(True))
        self.mentionsThread.finished.connect(lambda: self.downloader.downloadBtn.setEnabled(True))

    # Convert time
    def timeConvert(self, object):
        id = self.downloader.tzBtnGrp.id(object)
        if id == 1:
            self.downloader.startTime.setDateTime(datetime.strptime(self.BW.NZT2UTC(self.downloader.startTime.text()+':00'), '%Y-%m-%dT%H:%M:%S'))
            self.downloader.endTime.setDateTime(datetime.strptime(self.BW.NZT2UTC(self.downloader.endTime.text()+':00'), '%Y-%m-%dT%H:%M:%S'))
        elif id == 2:
            self.downloader.startTime.setDateTime(datetime.strptime(self.BW.UTC2NZT(self.downloader.startTime.text().replace(' ', 'T')+':00'), '%Y-%m-%d %H:%M:%S'))
            self.downloader.endTime.setDateTime(datetime.strptime(self.BW.UTC2NZT(self.downloader.endTime.text().replace(' ', 'T')+':00'), '%Y-%m-%d %H:%M:%S'))

    def remove_duplicates(self, l):
        return list(set(l))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
