import sys
from PySide6 import QtWidgets, QtGui, QtSql


class Color(QtWidgets.QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(color))
        self.setPalette(palette)


class MyGui(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wufoo Form Viewer")
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('my_form_db.sqlite')
        self.db.open()
        self.model = QtSql.QSqlTableModel(self, db=self.db)
        self.model.setTable("entries")
        self.model.select()
        self.table_view = QtWidgets.QTableView()
        self.table_view.setModel(self.model)

        tabs = QtWidgets.QTabWidget()
        tabs.setTabPosition(QtWidgets.QTabWidget.North)
        tabs.setMovable(True)
        tabs.setDocumentMode(True)

        tabs.addTab(self.table_view, "View Database")
        tabs.addTab(Color("blue"), "blue")
        self.setCentralWidget(tabs)


def run_gui():
    app = QtWidgets.QApplication(sys.argv)
    window = MyGui()
    window.resize(200, 100)
    window.setStyleSheet("""
        background-color: #262626;
        color: #FFFFFF;
        font-family: Arial;
        font-size: 18px;
        """)
    window.show()
    app.exec()


run_gui()
