import sys
from PySide6 import QtWidgets, QtSql
import wufoo_db
import get_wufuu_info


class StartWindow(QtWidgets.QWidget):
    def __init__(self, filename: str, db_filename: str):
        super().__init__()
        self.entry_filename = filename
        self.db_filename = db_filename
        self.setup_start_window()
        self.w = None

    def setup_start_window(self):
        self.setWindowTitle("Wufoo start box")
        start_layout = QtWidgets.QVBoxLayout()
        update_data_button = QtWidgets.QPushButton("Update")
        view_entries_button = QtWidgets.QPushButton("View")
        start_layout.addWidget(update_data_button)
        start_layout.addWidget(view_entries_button)
        view_entries_button.clicked.connect(self.view_entries)
        update_data_button.clicked.connect(self.update_data)
        self.setLayout(start_layout)
        self.show()

    def view_entries(self):
        self.w = MyWindow(self.entry_filename)
        self.close()

    def update_data(self):
        call_api = get_wufuu_info.get_form_info()
        get_wufuu_info.save_response_as_file(call_api, self.entry_filename)
        wufoo_db.configure_db(self.db_filename, self.entry_filename)


class MyWindow(QtWidgets.QWidget):
    def __init__(self, filename: str):
        super().__init__()

        self.filename = filename
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName(filename)
        self.db.open()

        # configure gui model from db
        self.model = QtSql.QSqlTableModel(self, db=self.db)
        self.model.setTable("entries")
        self.model.select()
        self.table_view = QtWidgets.QTableView()
        self.table_view.setModel(self.model)

        # configure the form
        self.entry_title_label = QtWidgets.QLineEdit()
        self.entry_fname_label = QtWidgets.QLineEdit()
        self.entry_lname_label = QtWidgets.QLineEdit()
        self.entry_org_label = QtWidgets.QLineEdit()
        self.entry_email_label = QtWidgets.QLineEdit()
        self.entry_org_site_label = QtWidgets.QLineEdit()
        self.entry_phone_label = QtWidgets.QLineEdit()
        self.entry_proj_owner_label = QtWidgets.QLineEdit()

        # checkbox 1
        self.proj_checkbox = QtWidgets.QCheckBox("project")
        self.guest_checkbox = QtWidgets.QCheckBox("guest")
        self.site_visit_checkbox = QtWidgets.QCheckBox("site vist")
        self.job_shadow_checkbox = QtWidgets.QCheckBox("job shadow")
        self.internship_checkbox = QtWidgets.QCheckBox("internship")
        self.career_checkbox = QtWidgets.QCheckBox("Career Panel")
        self.networking_checkbox = QtWidgets.QCheckBox("networking")
        # checkbox 2
        self.summer_checkbox = QtWidgets.QCheckBox("Summer 2022")
        self.fall_checkbox = QtWidgets.QCheckBox("Fall 2022")
        self.spring_checkbox = QtWidgets.QCheckBox("Spring 2023")
        self.summer2_checkbox = QtWidgets.QCheckBox("Summer 2023")

        self.cw = None

        self.setup_window()

    def setup_window(self):
        self.setWindowTitle("Wufoo Form Viewer")
        list_widget = QtWidgets.QListWidget()
        main_layout = QtWidgets.QHBoxLayout()
        main_layout.addWidget(list_widget, 1)
        view_entry = self.build_view_entry()
        main_widget = QtWidgets.QWidget()
        main_widget.setLayout(view_entry)
        main_layout.addWidget(main_widget, 2)

        num_of_entries = self.model.rowCount()
        column_data = []
        for column in range(num_of_entries):
            column_index = self.model.index(column, 0)
            column_data.append(self.model.data(column_index))

        # check the data you have is the one *think* it should be
        for i in range(len(column_data)):
            list_widget.addItem(str(column_data[i]))

        list_widget.itemClicked.connect(self.update_entry)
        self.setLayout(main_layout)
        self.show()

    def build_view_entry(self) -> QtWidgets.QLayout:
        view_entry_layout = QtWidgets.QVBoxLayout()
        # top of form layout
        top_layout = QtWidgets.QFormLayout()
        # middle of form layout
        checkbox_set_one_layout = QtWidgets.QVBoxLayout()
        # bottom of form layout
        checkbox_set_two_layout = QtWidgets.QVBoxLayout()

        title_label = QtWidgets.QLabel("Title")
        f_name_label = QtWidgets.QLabel("First")
        l_name_label = QtWidgets.QLabel("Last")
        org_label = QtWidgets.QLabel("Org Name")
        email_label = QtWidgets.QLabel("Email")
        org_site_label = QtWidgets.QLabel("Org Site")
        phone_label = QtWidgets.QLabel("Phone")
        proj_owner_label = QtWidgets.QLabel("Project Owner")

        top_layout.addRow(title_label, self.entry_title_label)
        top_layout.addRow(f_name_label, self.entry_fname_label)
        top_layout.addRow(l_name_label, self.entry_lname_label)
        top_layout.addRow(org_label, self.entry_org_label)
        top_layout.addRow(email_label, self.entry_email_label)
        top_layout.addRow(org_site_label, self.entry_org_site_label)
        top_layout.addRow(phone_label, self.entry_phone_label)
        top_layout.addRow(proj_owner_label, self.entry_proj_owner_label)

        checkbox_set_one_layout.addWidget(self.proj_checkbox)
        checkbox_set_one_layout.addWidget(self.guest_checkbox)
        checkbox_set_one_layout.addWidget(self.site_visit_checkbox)
        checkbox_set_one_layout.addWidget(self.job_shadow_checkbox)
        checkbox_set_one_layout.addWidget(self.internship_checkbox)
        checkbox_set_one_layout.addWidget(self.career_checkbox)
        checkbox_set_one_layout.addWidget(self.networking_checkbox)

        checkbox_set_two_layout.addWidget(self.summer_checkbox)
        checkbox_set_two_layout.addWidget(self.spring_checkbox)
        checkbox_set_two_layout.addWidget(self.fall_checkbox)
        checkbox_set_two_layout.addWidget(self.summer2_checkbox)
        claim_project = QtWidgets.QPushButton("Claim a Project")
        claim_project.clicked.connect(self.claim_project_entry)
        checkbox_set_two_layout.addWidget(claim_project)

        view_entry_layout.addLayout(top_layout)
        view_entry_layout.addLayout(checkbox_set_one_layout)
        view_entry_layout.addLayout(checkbox_set_two_layout)
        return view_entry_layout

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
        proj_owner = row_data[22]

        self.entry_title_label.setText(entry_title)
        self.entry_fname_label.setText(entry_fname)
        self.entry_lname_label.setText(entry_lname)
        self.entry_org_label.setText(entry_orgname)
        self.entry_email_label.setText(entry_email)
        self.entry_org_site_label.setText(entry_orgsite)
        self.entry_phone_label.setText(entry_phone)
        self.entry_proj_owner_label.setText(proj_owner)
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

    def claim_project_entry(self):
        self.cw = ClaimGui(self.filename)


class ClaimGui(QtWidgets.QWidget):
    def __init__(self, db_filename: str):
        super().__init__()
        self.pw = None
        self.db_filename = db_filename
        self.entry_id = QtWidgets.QLineEdit()
        self.entry_fname_label = QtWidgets.QLineEdit()
        self.entry_lname_label = QtWidgets.QLineEdit()
        self.entry_title_label = QtWidgets.QLineEdit()
        self.entry_email_label = QtWidgets.QLineEdit()
        self.entry_department_label = QtWidgets.QLineEdit()
        self.setup_claim_gui()

    def setup_claim_gui(self):
        self.setWindowTitle("Claim Project")
        claim_layout = QtWidgets.QFormLayout()

        entry_id = QtWidgets.QLabel("Entry ID")
        f_name_label = QtWidgets.QLabel("First")
        l_name_label = QtWidgets.QLabel("Last")
        title_label = QtWidgets.QLabel("Title")
        email_label = QtWidgets.QLabel("Email")
        department_label = QtWidgets.QLabel("Department Name")
        submit_button = QtWidgets.QPushButton("submit")

        claim_layout.addRow(entry_id, self.entry_id)
        claim_layout.addRow(f_name_label, self.entry_fname_label)
        claim_layout.addRow(l_name_label, self.entry_lname_label)
        claim_layout.addRow(title_label, self.entry_title_label)
        claim_layout.addRow(email_label, self.entry_email_label)
        claim_layout.addRow(department_label, self.entry_department_label)
        claim_layout.addWidget(submit_button)
        submit_button.clicked.connect(self.submit_claim)
        self.setLayout(claim_layout)
        self.show()

    def submit_claim(self):
        data = []
        entry_id = self.entry_id.text()
        fname = self.entry_fname_label.text()
        lname = self.entry_lname_label.text()
        title = self.entry_title_label.text()
        email = self.entry_email_label.text()
        department = self.entry_department_label.text()
        data.append(entry_id)
        data.append(fname)
        data.append(lname)
        data.append(title)
        data.append(email)
        data.append(department)
        wufoo_db.format_claim(self.db_filename, data)
        self.pw = PopUp()
        self.close()


class PopUp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Submitted")
        pop_layout = QtWidgets.QVBoxLayout()
        QBtn = QtWidgets.QPushButton("Project Claimed")
        QBtn.clicked.connect(self.popup_clicked)
        pop_layout.addWidget(QBtn)
        self.setLayout(pop_layout)
        self.show()

    def popup_clicked(self):
        self.close()


def run_gui(filename: str, entry_filename: str):
    app = QtWidgets.QApplication()
    window = StartWindow(filename, entry_filename)
    window.show()
    app.exec()
    sys.exit()
