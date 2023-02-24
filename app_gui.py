import sys
from PySide6 import QtWidgets, QtSql


class MyGui(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Wufoo Form Viewer")
        # connect to local db
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('my_form_db.sqlite')
        self.db.open()

        # configure gui model from db
        self.model = QtSql.QSqlTableModel(self, db=self.db)
        self.model.setTable("entries")
        self.model.select()
        self.table_view = QtWidgets.QTableView()
        self.table_view.setModel(self.model)
        self.vertical_header = self.table_view.verticalHeader()

        # make form
        top_layout = QtWidgets.QFormLayout()
        title_label = QtWidgets.QLabel("Title")
        f_name_label = QtWidgets.QLabel("First")
        l_name_label = QtWidgets.QLabel("Last")
        org_label = QtWidgets.QLabel("org name")
        email_label = QtWidgets.QLabel("email")
        org_site_label = QtWidgets.QLabel("org site")
        phone_label = QtWidgets.QLabel("phone")

        top_layout.addRow(title_label, QtWidgets.QLineEdit())
        top_layout.addRow(f_name_label, QtWidgets.QLineEdit())
        top_layout.addRow(l_name_label, QtWidgets.QLineEdit())
        top_layout.addRow(org_label, QtWidgets.QLineEdit())
        top_layout.addRow(email_label, QtWidgets.QLineEdit())
        top_layout.addRow(org_site_label, QtWidgets.QLineEdit())
        top_layout.addRow(phone_label, QtWidgets.QLineEdit())

        # add checkboxes
        checkbox_set_one_layout = QtWidgets.QVBoxLayout()
        proj_checkbox = QtWidgets.QCheckBox("project")
        guest_checkbox = QtWidgets.QCheckBox("guest")
        site_visit_checkbox = QtWidgets.QCheckBox("site vist")
        job_shadow_checkbox = QtWidgets.QCheckBox("job shadow")
        internship_checkbox = QtWidgets.QCheckBox("internship")
        networking_checkbox = QtWidgets.QCheckBox("networking")

        checkbox_set_one_layout.addWidget(proj_checkbox)
        checkbox_set_one_layout.addWidget(guest_checkbox)
        checkbox_set_one_layout.addWidget(site_visit_checkbox)
        checkbox_set_one_layout.addWidget(job_shadow_checkbox)
        checkbox_set_one_layout.addWidget(internship_checkbox)
        checkbox_set_one_layout.addWidget(networking_checkbox)

        checkbox_set_two_layout = QtWidgets.QVBoxLayout()
        summer_checkbox = QtWidgets.QCheckBox("summer")
        spring_checkbox = QtWidgets.QCheckBox("spring")
        winter_checkbox = QtWidgets.QCheckBox("winter")
        summer2_checkbox = QtWidgets.QCheckBox("summer2")

        checkbox_set_two_layout.addWidget(summer_checkbox)
        checkbox_set_two_layout.addWidget(spring_checkbox)
        checkbox_set_two_layout.addWidget(winter_checkbox)
        checkbox_set_two_layout.addWidget(summer2_checkbox)

        full_widget = QtWidgets.QWidget()
        view_entry_layout = QtWidgets.QVBoxLayout()
        view_entry_layout.addLayout(top_layout)
        view_entry_layout.addLayout(checkbox_set_one_layout)
        view_entry_layout.addLayout(checkbox_set_two_layout)
        full_widget.setLayout(view_entry_layout)
        # configure main widget from table
        list_widget = QtWidgets.QListWidget()
        tab_layout = QtWidgets.QHBoxLayout()
        tab_layout.addWidget(list_widget, 1)
        tab_layout.addWidget(full_widget, 2)
        # tab_layout.addWidget(text_widget, 4)

        view_entry_list = QtWidgets.QWidget()
        view_entry_list.setLayout(tab_layout)

        tabs = QtWidgets.QTabWidget()
        tabs.setTabPosition(QtWidgets.QTabWidget.North)
        tabs.setMovable(True)
        tabs.setDocumentMode(True)

        tabs.addTab(view_entry_list, "View Entries")
        tabs.addTab(self.table_view, "View Database")

        num_of_entries = self.model.rowCount()
        column_data = []
        for column in range(num_of_entries):
            column_index = self.model.index(column, 0)
            column_data.append(self.model.data(column_index))
        # check the data you have is the one *think* it should be
        for i in range(len(column_data)):
            list_widget.addItem(str(column_data[i]))

        self.setCentralWidget(tabs)


def run_gui():
    app = QtWidgets.QApplication()
    window = MyGui()
    window.show()
    with open("styles/style.qss", "r")as f:
        _style = f.read()
        app.setStyleSheet(_style)
    sys.exit(app.exec())


run_gui()
