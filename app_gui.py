# I need to really redo this portion
import sys
from PySide6 import QtWidgets, QtSql


class MyGui(QtWidgets.QMainWindow):
    def __init__(self, filename: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Wufoo Form Viewer")

        # connect to local db
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName(filename)
        self.db.open()

        # configure gui model from db
        self.model = QtSql.QSqlTableModel(self, db=self.db)
        self.model.setTable("entries")
        self.model.select()
        self.table_view = QtWidgets.QTableView()
        self.table_view.setModel(self.model)

        # make form
        top_layout = QtWidgets.QFormLayout()
        title_label = QtWidgets.QLabel("Title")
        f_name_label = QtWidgets.QLabel("First")
        l_name_label = QtWidgets.QLabel("Last")
        org_label = QtWidgets.QLabel("org name")
        email_label = QtWidgets.QLabel("email")
        org_site_label = QtWidgets.QLabel("org site")
        phone_label = QtWidgets.QLabel("phone")

        self.entry_title_label = QtWidgets.QLineEdit()
        self.entry_fname_label = QtWidgets.QLineEdit()
        self.entry_lname_label = QtWidgets.QLineEdit()
        self.entry_org_label = QtWidgets.QLineEdit()
        self.entry_email_label = QtWidgets.QLineEdit()
        self.entry_org_site_label = QtWidgets.QLineEdit()
        self.entry_phone_label = QtWidgets.QLineEdit()

        top_layout.addRow(title_label, self.entry_title_label)
        top_layout.addRow(f_name_label, self.entry_fname_label)
        top_layout.addRow(l_name_label, self.entry_lname_label)
        top_layout.addRow(org_label, self.entry_org_label)
        top_layout.addRow(email_label, self.entry_email_label)
        top_layout.addRow(org_site_label, self.entry_org_site_label)
        top_layout.addRow(phone_label, self.entry_phone_label)

        # add checkboxes
        checkbox_set_one_layout = QtWidgets.QVBoxLayout()
        self.proj_checkbox = QtWidgets.QCheckBox("project")
        self.guest_checkbox = QtWidgets.QCheckBox("guest")
        self.site_visit_checkbox = QtWidgets.QCheckBox("site vist")
        self.job_shadow_checkbox = QtWidgets.QCheckBox("job shadow")
        self.internship_checkbox = QtWidgets.QCheckBox("internship")
        self.career_checkbox = QtWidgets.QCheckBox("Career Panel")
        self.networking_checkbox = QtWidgets.QCheckBox("networking")
        checkbox_set_one_layout.addWidget(self.proj_checkbox)
        checkbox_set_one_layout.addWidget(self.guest_checkbox)
        checkbox_set_one_layout.addWidget(self.site_visit_checkbox)
        checkbox_set_one_layout.addWidget(self.job_shadow_checkbox)
        checkbox_set_one_layout.addWidget(self.internship_checkbox)
        checkbox_set_one_layout.addWidget(self.career_checkbox)
        checkbox_set_one_layout.addWidget(self.networking_checkbox)

        checkbox_set_two_layout = QtWidgets.QVBoxLayout()
        self.summer_checkbox = QtWidgets.QCheckBox("Summer 2022")
        self.fall_checkbox = QtWidgets.QCheckBox("Fall 2022")
        self.spring_checkbox = QtWidgets.QCheckBox("Spring 2023")
        self.summer2_checkbox = QtWidgets.QCheckBox("Summer 2023")

        checkbox_set_two_layout.addWidget(self.summer_checkbox)
        checkbox_set_two_layout.addWidget(self.spring_checkbox)
        checkbox_set_two_layout.addWidget(self.fall_checkbox)
        checkbox_set_two_layout.addWidget(self.summer2_checkbox)

        full_widget = QtWidgets.QWidget()
        self.view_entry_layout = QtWidgets.QVBoxLayout()
        self.view_entry_layout.addLayout(top_layout)
        self.view_entry_layout.addLayout(checkbox_set_one_layout)
        self.view_entry_layout.addLayout(checkbox_set_two_layout)
        full_widget.setLayout(self.view_entry_layout)

        list_widget = QtWidgets.QListWidget()
        tab_layout = QtWidgets.QHBoxLayout()
        tab_layout.addWidget(list_widget, 1)
        tab_layout.addWidget(full_widget, 2)
        view_entry_list = QtWidgets.QWidget()
        view_entry_list.setLayout(tab_layout)

        tabs = QtWidgets.QTabWidget()
        tabs.setTabPosition(QtWidgets.QTabWidget.North)
        tabs.setMovable(True)
        tabs.setDocumentMode(True)
        tabs.addTab(view_entry_list, "View Entries")
        tabs.addTab(self.table_view, "View Database Table")

        num_of_entries = self.model.rowCount()
        column_data = []
        for column in range(num_of_entries):
            column_index = self.model.index(column, 0)
            column_data.append(self.model.data(column_index))

        # check the data you have is the one *think* it should be
        for i in range(len(column_data)):
            list_widget.addItem(str(column_data[i]))

        list_widget.itemClicked.connect(self.update_entry)
        self.setCentralWidget(tabs)

    def update_entry(self, item):

        # take the entry # and use it to
        # get the row of info from the uploaded db model
        item = item.text()
        num_of_rows = self.model.columnCount()
        row_data = []
        for row in range(num_of_rows):
            row_index = (self.model.index(int(item) - 1, row))
            row_data.append(self.model.data(row_index))

        # take items from data and update the form view
        entry_title = row_data[4]
        entry_fname = row_data[3]
        entry_lname = row_data[2]
        entry_orgname = row_data[5]
        entry_email = row_data[6]
        entry_orgsite = row_data[7]
        entry_phone = row_data[8]

        self.entry_title_label.setText(entry_title)
        self.entry_fname_label.setText(entry_fname)
        self.entry_lname_label.setText(entry_lname)
        self.entry_org_label.setText(entry_orgname)
        self.entry_email_label.setText(entry_email)
        self.entry_org_site_label.setText(entry_orgsite)
        self.entry_phone_label.setText(entry_phone)
        self.update_checkboxes(row_data[9:19])

    def update_checkboxes(self, checkbox_data: list):
        self.proj_checkbox.setChecked(False)
        self.guest_checkbox.setChecked(False)
        self.site_visit_checkbox.setChecked(False)
        self.job_shadow_checkbox.setChecked(False)
        self.internship_checkbox.setChecked(False)
        self.career_checkbox.setChecked(False)
        self.networking_checkbox.setChecked(False)

        self.summer_checkbox.setChecked(False)
        self.fall_checkbox.setChecked(False)
        self.fall_checkbox.setChecked(False)
        self.summer2_checkbox.setChecked(False)

        comparison_data = {'Course Project': 'self.proj_checkbox.setChecked(True)',
                           'Guest Speaker': 'self.guest_checkbox.setChecked(True)',
                           'Site Visit': 'self.site_visit_checkbox.setChecked(True)',
                           'Job Shadow': 'self.job_shadow_checkbox.setChecked(True)',
                           'Internships': 'self.internship_checkbox.setChecked(True)',
                           'Career Panel': 'self.career_checkbox.setChecked(True)',
                           'Networking Event': 'self.networking_checkbox.setChecked(True)',
                           'Summer 2022 (Juner 2022 - August 2022 )':
                               'self.summer_checkbox.setChecked(True)',
                           ' Fall 2022 (September 2022- December 2022)':
                               'self.fall_checkbox.setChecked(True)',
                           ' Spring 2023 (January 2023- April 2023)':
                               'self.spring_checkbox.setChecked(True)'}

        for i in range(len(checkbox_data)):
            if checkbox_data[i] in comparison_data:
                item = comparison_data.get(checkbox_data[i])
                eval(item)


def run_gui(filename: str):
    app = QtWidgets.QApplication()
    window = MyGui(filename)
    window.show()
    with open("styles/style.qss", "r") as f:
        custom_style = f.read()
        app.setStyleSheet(custom_style)
    app.exec()
    sys.exit()
