from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QLineEdit
import re
import table
import Doctors_table
import Staff_table
import sqlite3



class Ui_Form(object):

    def __init__(self):
        self.IDs = set()
        self.input = ''
        self.count = 0
        self.all_doctors = []
        self.all_doctors_count = {}
        self.list_of_all_avail_doctors = []
        self.list_of_all_doctors = []

    def showDialog(self, title, message, icon):  # message box
        msgBox = QMessageBox()
        var = f'QMessageBox.{icon}'
        msgBox.setIcon(eval(var))
        msgBox.setText(message)
        msgBox.setWindowTitle(title)
        msgBox.setStyleSheet("background:rgb(255,233,236)")
        icons = QtGui.QIcon()
        icons.addPixmap(QtGui.QPixmap(r"icons/logo1.PNG"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        msgBox.setWindowIcon(icons)
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msgBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        msgBox.Help
        return msgBox.exec()

    def func_for_new_data(self):
        hosp = sqlite3.connect('hospital_data.db')
        curs = hosp.cursor()
        curs.execute('Select ID from data')
        rows = curs.fetchall()
        for row in rows:
            self.IDs.add(row[0])
        while True:
            ID, ok = QtWidgets.QInputDialog.getText(Form, "ID", "Enter the ID:")
            if re.match(r'^[0-9]*$', ID) and ID != '':
                if int(ID) not in self.IDs:
                    break
                else:
                    curs.execute(f'Select * from data where ID=="{ID}"')
                    row = curs.fetchone()
                    self.showDialog('ERROR',
                                    f' The ID already exist\n\n First Name    :   {row[1]}\t\t\t\t\t \n Last Name    :   {row[2]} \n Gender          :   {row[3]} \n Age                :   {row[4]} \n Blood Group :   {row[5]} \n Contact No   :   {row[6]} \n Disease          :   {row[7]} \n Doctor          :   {row[8]} \n AdmissionID           : {row[9]} \n DoctorID           :   {row[10]}\n\n',
                                    'Critical')
            elif ok != True:
                break
            else:
                self.showDialog('Error', 'Please enter a valid ID!!!\n It can only contain numbers', 'Critical')
        if ok == True:
            while True:
                name, ok = QtWidgets.QInputDialog.getText(Form, "Name", "Enter Patient First Name:")
                if re.match(r'^[a-zA-Z]*$', name) and name != '':
                    break
                elif ok != True:
                    break
                else:
                    self.showDialog('Error', 'Please enter a valid name!!!', 'Critical')
            if ok == True:
                while True:
                    name1, ok = QtWidgets.QInputDialog.getText(Form, "Name", "Enter Patient Last Name:")
                    if re.match(r'^[a-zA-Z]*$', name1) and name1 != '':
                        break
                    elif ok != True:
                        break
                    else:
                        self.showDialog('Error', 'Please enter a valid name format!!!', 'Warning')
                if ok == True:
                    self.gender = ['Male', 'Female', 'Others']
                    sex, ok = QtWidgets.QInputDialog.getItem(Form, "Open", "Choose A Team", self.gender, 0, False)
                    if ok == True:
                        while True:
                            age, ok = QtWidgets.QInputDialog.getText(Form, "Age", "Enter the Age:")
                            if re.match(r'^[0-9]*$', age) and age != '' and int(age) < 125:
                                break
                            elif ok != True:
                                break
                            else:
                                self.showDialog('Error', 'Please enter a valid age!!!', 'Warning')
                        if ok == True:
                            self.blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
                            blood_grp, ok = QtWidgets.QInputDialog.getItem(Form, "Open", "Choose your Blood Group",
                                                                           self.blood_groups, 0, False)
                            if ok == True:
                                while True:
                                    contact_no, ok = QtWidgets.QInputDialog.getText(Form, "Contact No",
                                                                                    "Enter Contact No:")
                                    if re.match(r'^\d{10}$', contact_no):

                                        break
                                    elif ok != True:
                                        break
                                    else:
                                        self.showDialog('Error', 'Please enter 10 digits number!!!', 'Warning')
                    if ok == True:
                        while True:
                            disease, ok = QtWidgets.QInputDialog.getText(Form, "Disease",
                                                                         "Enter the Disease suffering from:")
                            if re.match(r'^[a-zA-Z]*$', disease) and disease != '':
                                break
                            elif ok != True:
                                break
                            else:
                                self.showDialog('Error', 'Please enter a valid format!!!', 'Warning')
                        if ok == True:
                               self.docid = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
                               DoctorID, ok = QtWidgets.QInputDialog.getItem(Form, "Open",
                                                                             "Choose A Team",
                                                                             self.docid, 0, False)

                        if ok == True:
                               self.addmitionid = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
                               AdmissionID, ok = QtWidgets.QInputDialog.getItem(Form, "Open",
                                                                                "Choose A Team",
                                                                            self.addmitionid, 0, False)
                        if ok == True:
                            hosp = sqlite3.connect('hospital_data.db')
                            curs = hosp.cursor()
                            curs.execute(
                                    f"Insert into data Values('{ID}','{name.strip().title()}','{name1.strip().title()}','{sex}','{age}','{blood_grp}','{contact_no}','{disease.strip().title()}','{DoctorID}','{AdmissionID}');")
                            hosp.commit()
                            self.showDialog('Success', 'Successfully entered the data!!!',
                                                'Information')
                        else:
                            self.showDialog('Failure', 'Sorry Data not entered!!!', 'Information')

    def func_for_read_data(self):
        self.window = QtWidgets.QWidget()
        self.ui = table.Ui_Table()
        self.ui.setupUi(self.window)
        self.window.show()
        self.ui.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        hosp = sqlite3.connect('hospital_data.db')
        curs = hosp.cursor()
        curs.execute('Select * from data')
        rows = curs.fetchall()
        row_val = 0
        for row in rows:
            col = 0
            while col <= 9:
                self.ui.tableWidget.setItem(row_val, col, QtWidgets.QTableWidgetItem(f'{row[col]}'))
                col += 1
            row_val += 1

    def func_for_id_search(self):
        ID, ok = QtWidgets.QInputDialog.getText(Form, "ID", "Enter the ID of the patient to search:")
        try:
            hosp = sqlite3.connect('hospital_data.db')
            curs = hosp.cursor()
            curs.execute(f'Select * from data where ID=="{ID}"')
            row = curs.fetchone()
            self.showDialog('DATA',
                            f' First Name    :   {row[1]}\t\t\t\t\t \n Last Name    :   {row[2]} \n Gender          :   {row[3]} \n Age                :   {row[4]} \n Blood Group :   {row[5]} \n Contact No   :     {row[6]} \n Disease          :   {row[7]} \n AdmissionID           : {row[8]} \n DoctorID           :    {row[9]}\n\n',
                            'Information')
            return ID

        except:
            self.showDialog('ERROR', 'Please enter a valid ID!!!\n No such ID exists', 'Critical')

    def func_for_blood_grp(self):
        self.blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        blood_grp, ok = QtWidgets.QInputDialog.getItem(Form, "Open", "Choose the Blood Group to search",
                                                       self.blood_groups, 0, False)
        try:
            hosp = sqlite3.connect('hospital_data.db')
            curs = hosp.cursor()
            curs.execute(f'Select * from data where [Blood Group]=="{blood_grp}"')
            rows = curs.fetchall()
            if len(rows) != 0 and ok == True:
                self.window = QtWidgets.QWidget()
                self.ui = table.Ui_Table()
                self.ui.setupUi(self.window)
                self.window.show()
                self.ui.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
                row_val = 0
                for row in rows:
                    col = 0
                    while col <= 9:
                        self.ui.tableWidget.setItem(row_val, col, QtWidgets.QTableWidgetItem(f'{row[col]}'))
                        col += 1
                    row_val += 1
            elif ok != True:
                pass
            else:
                self.showDialog('ERROR', 'Sorry no patient with this blood group exists', 'Critical')
        except:
            pass

    def func_for_age_grp(self):
        while True:
            age1, ok = QtWidgets.QInputDialog.getText(Form, "Age", "Enter the lowest range for Age:")
            if ok != True:
                break
            age2, ok = QtWidgets.QInputDialog.getText(Form, "Age", "Enter the maximum range for Age:")
            if re.match(r'^[0-9]*$', age1) and re.match(r'^[0-9]*$', age2) and age1 != '' and age2 != '':
                break
            elif ok != True:
                break
            else:
                self.showDialog('Error', 'Please enter a valid age!!!', 'Critical')
        try:
            hosp = sqlite3.connect('hospital_data.db')
            curs = hosp.cursor()
            curs.execute(f'Select * from data where Age<="{age2}" and Age>="{age1}"')
            rows = curs.fetchall()
            if len(rows) != 0 and ok == True:
                self.window = QtWidgets.QWidget()
                self.ui = table.Ui_Table()
                self.ui.setupUi(self.window)
                self.window.show()
                self.ui.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
                row_val = 0
                for row in rows:
                    col = 0
                    while col <= 9:
                        self.ui.tableWidget.setItem(row_val, col, QtWidgets.QTableWidgetItem(f'{row[col]}'))
                        col += 1
                    row_val += 1
            elif ok != True:
                pass
            else:
                self.showDialog('ERROR', 'Sorry no patient in this Age range exists', 'Critical')
        except:
            pass

    def func_for_patient_gender_grp(self):
        self.gender = ['Male', 'Female', 'Others']
        gender, ok = QtWidgets.QInputDialog.getItem(Form, "Open", "Choose the Gender to search", self.gender, 0, False)
        try:
            hosp = sqlite3.connect('hospital_data.db')
            curs = hosp.cursor()
            curs.execute(f'Select * from data where Gender=="{gender}"')
            rows = curs.fetchall()
            if len(rows) != 0 and ok == True:
                self.window = QtWidgets.QWidget()
                self.ui = table.Ui_Table()
                self.ui.setupUi(self.window)
                self.window.show()
                self.ui.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
                row_val = 0
                for row in rows:
                    col = 0
                    while col <= 9:
                        self.ui.tableWidget.setItem(row_val, col, QtWidgets.QTableWidgetItem(f'{row[col]}'))
                        col += 1
                    row_val += 1
            elif ok != True:
                pass
            else:
                self.showDialog('ERROR', 'Sorry no patient with this gender exists', 'Critical')
        except:
            pass

    def func_for_contact_grp(self):
        while True:
            contact_no, ok = QtWidgets.QInputDialog.getText(Form, "Contact No", "Enter Contact No:")
            if re.match(r'^\d{10}$', contact_no):
                break
            elif ok != True:
                break
            else:
                self.showDialog('Error', 'Please enter 10 digits number!!!', 'Warning')
        if ok == True:
            hosp = sqlite3.connect('hospital_data.db')
            curs = hosp.cursor()
            curs.execute(f'Select * from data where [Contact No]=="{contact_no}"')
            rows = curs.fetchall()
            if len(rows) != 0 and ok == True:
                self.window = QtWidgets.QWidget()
                self.ui = table.Ui_Table()
                self.ui.setupUi(self.window)
                self.window.show()
                self.ui.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
                row_val = 0
                for row in rows:
                    col = 0
                    while col <= 9:
                        self.ui.tableWidget.setItem(row_val, col, QtWidgets.QTableWidgetItem(f'{row[col]}'))
                        col += 1
                    row_val += 1
                return contact_no
            elif ok != True:
                pass
            else:
                self.showDialog('ERROR', 'No Patient with this contact number exists', 'Critical')

    def func_for_disease_grp(self):
        while True:
            disease, ok = QtWidgets.QInputDialog.getText(Form, "Disease", "Enter the Disease you want to search:")
            if re.match(r'^[a-zA-Z]*$', disease) and disease != '':
                break
            elif ok != True:
                break
            else:
                self.showDialog('Error', 'Please enter a valid format!!!', 'Warning')
        if ok == True:
            hosp = sqlite3.connect('hospital_data.db')
            curs = hosp.cursor()
            curs.execute(f'Select * from data where Disease=="{disease.strip().title()}"')
            rows = curs.fetchall()
            if len(rows) != 0 and ok == True:
                self.input = disease
                self.window = QtWidgets.QWidget()
                self.ui = table.Ui_Table()
                self.ui.setupUi(self.window)
                self.window.show()
                self.ui.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
                row_val = 0
                for row in rows:
                    col = 0
                    while col <= 9:
                        self.ui.tableWidget.setItem(row_val, col, QtWidgets.QTableWidgetItem(f'{row[col]}'))
                        col += 1
                    row_val += 1
            elif ok != True:
                pass
            else:
                self.showDialog('ERROR', 'No Patient suffering from such disease', 'Critical')
    def func_for_name(self):
        while True:
            name, ok = QtWidgets.QInputDialog.getText(Form, "Patient", "Enter the name of the Patient:")
            if re.match(r'^[a-zA-Z]*$', name) and name != '':
                break
            elif ok != True:
                break
            else:
                self.showDialog('Error', 'Please enter a valid name!!!', 'Critical')
        if ok == True:
            hosp = sqlite3.connect('hospital_data.db')
            curs = hosp.cursor()
            curs.execute(f'Select * from data where [First Name]=="{name.strip().title()}"')
            rows = curs.fetchall()
            if len(rows) != 0 and ok == True:
                self.window = QtWidgets.QWidget()
                self.ui = table.Ui_Table()
                self.ui.setupUi(self.window)
                self.window.show()
                self.ui.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
                row_val = 0
                for row in rows:
                    col = 0
                    while col <= 9:
                        self.ui.tableWidget.setItem(row_val, col, QtWidgets.QTableWidgetItem(f'{row[col]}'))
                        col += 1
                    row_val += 1
                return name
            elif ok != True:
                pass
            else:
                self.showDialog('ERROR', 'No Patient with such name exists!!!', 'Critical')

    def func_for_del(self):
        try:
            self.columns = ['ID', 'First Name', 'Contact No']
            value, ok = QtWidgets.QInputDialog.getItem(Form, "Open", "Choose the criteria to search", self.columns, 0,
                                                       False)
            if ok == True:
                hosp = sqlite3.connect('hospital_data.db')
                curs = hosp.cursor()
                if value == 'ID':
                    self.var = int(self.func_for_id_search())
                    curs.execute(f'Select * from data where ID=="{self.var}"')
                    rows = curs.fetchone()
                    if len(rows) == 0:
                        self.showDialog('ERROR', 'No such patient exists!!!', 'Critical')
                    else:
                        curs.execute(f'Delete from data where ID=="{self.var}"')
                        ok = self.showDialog('Confirm', 'Are you sure you want to delete!!!', 'Question')
                        if ok == 1024:
                            hosp.commit()
                        else:
                            pass
                elif value == 'First Name':
                    self.var = self.func_for_name()
                    curs.execute(f'Select * from data where [First Name]=="{self.var.strip().title()}"')
                    rows = curs.fetchall()
                    if len(rows) == 1:
                        curs.execute(f'Delete from data where [First Name]=="{self.var.strip().title()}"')
                        ok = self.showDialog('Confirm', 'Are you sure you want to delete!!!', 'Question')
                        if ok == 1024:
                            self.window.close()
                            hosp.commit()
                            self.showDialog('Success', 'Sucessfully Deleted the data', 'Question')
                        else:
                            pass
                    elif len(rows) == 0:
                        self.showDialog('ERROR', 'No such patient exists!!!', 'Critical')
                    else:
                        self.showDialog('Error',
                                        'More than one patient with this name exists!!!\n Please enter any other criteria',
                                        'Critical')
                        self.func_for_del
                elif value == 'Contact No':
                    self.var = self.func_for_contact_grp()
                    curs.execute(f'Select * from data where [Contact No]=="{self.var}"')
                    rows = curs.fetchall()
                    if len(rows) == 1:
                        curs.execute(f'Delete from data where [Contact No]=="{self.var.strip().title()}"')
                        ok = self.showDialog('Confirm', 'Are you sure you want to delete!!!', 'Question')
                        if ok == 1024:
                            self.window.close()
                            hosp.commit()
                            self.showDialog('Success', 'Sucessfully Deleted the data', 'Question')
                        else:
                            pass
                    elif len(rows) == 0:
                        self.showDialog('ERROR', 'No such patient exists!!!', 'Critical')
                    else:
                        self.showDialog('Error',
                                        'More than one patient with this Conatct No exists!!!\n Please enter any other criteria',
                                        'Information')
                        self.func_for_del
                elif value == 'Doctor':
                    self.var = self.func_for_doctor_grp()
                    curs.execute(f'Select * from data where Doctor=="{self.var.strip().title()}"')
                    rows = curs.fetchall()
                    if len(rows) == 1:
                        curs.execute(f'Delete from data where [Contact No]=="{self.var.strip().title()}"')
                        ok = self.showDialog('Confirm',
                                             'Are you sure you want to delete!!!\n One of the patient entry treated by him will also be deleted',
                                             'Warning')
                        if ok == 1024:
                            self.window.close()
                            hosp.commit()
                            self.showDialog('Success', 'Sucessfully Deleted the data', 'Question')
                        else:
                            pass

                    elif len(rows) == 0:
                        self.showDialog('ERROR', 'No such Doctor exists!!!', 'Information')
                    else:
                        ok = self.showDialog('Error',
                                             f'Dr. {self.var.strip().title()} is trating many Patients.\nThis will also delete all the patients entry which are being treated by Dr. {self.var.strip().title()}!!!\n Are you sure you want to continue',
                                             'Warning')
                        curs.execute(f'Delete from data where [Contact No]=="{self.var.strip().title()}"')
                        if ok == True:
                            self.window.close()
                            hosp.commit()
                            self.showDialog('Success', 'Sucessfully Deleted the data', 'Question')
                        else:
                            pass
            else:
                pass
        except:
            pass

    def func_for_log_out(self):
        quit()


    def func_for_modification(self, all_value, value, var):

        hosp = sqlite3.connect('hospital_data.db')
        curs = hosp.cursor()
        curs.execute('Select ID from data')
        rows = curs.fetchall()
        self.IDs.clear()
        for row in rows:
            self.IDs.add(row[0])

        if all_value == 'ID':
            while True:
                ID, ok = QtWidgets.QInputDialog.getText(Form, "ID", "Enter the new ID of the Patient:")
                if ok == True:
                    if re.match(r'^[0-9]*$', ID) and ID != '':
                        if int(ID) not in self.IDs:
                            curs.execute(f'Update data Set [{all_value}]="{int(ID)}" where {value}=="{var}"')
                            ok = self.showDialog('Confirm', 'Are you sure you want to update!!!', 'Question')
                            if ok == 1024:
                                hosp.commit()
                                self.showDialog('SUCCESS', 'Successfully Updated the data', 'Information')
                                break
                            else:
                                break
                        else:
                            curs.execute(f'Select * from data where ID=="{ID}"')
                            row = curs.fetchone()
                            self.showDialog('ERROR',
                                            f' The ID already exist\n\n First Name    :   {row[1]}\t\t\t\t\t \n Last Name    :   {row[2]} \n Gender          :   {row[3]} \n Age                :   {row[4]} \n Blood Group :   {row[5]} \n Contact No   :      {row[6]} \n Disease          :   {row[7]} \n DoctorID           : {row[8]} \n AdmissionID           :   {row[9]}\n\n',
                                            'Critical')
                else:
                    break


        elif all_value == 'Gender':
            self.gender = ['Male', 'Female', 'Others']
            Gender, ok = QtWidgets.QInputDialog.getItem(Form, "Open", "Choose the gender to be updated", self.gender, 0,
                                                     False)
            if ok == True:
                curs.execute(f'Update data Set [{all_value}]="{Gender}" where [{value}]=="{var}"')
                ok = self.showDialog('Confirm', 'Are you sure you want to update!!!', 'Question')
                if ok == 1024:
                    hosp.commit()
                    self.showDialog('SUCCESS', 'Successfully Updated the data', 'Information')
                else:
                    pass
            else:
                pass

        elif all_value == 'Blood Group':
            self.blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
            blood_grp, ok = QtWidgets.QInputDialog.getItem(Form, "UPDATE", "Choose your updated Blood Group",
                                                           self.blood_groups, 0, False)
            if ok == True:
                curs.execute(f'Update data Set [{all_value}]="{blood_grp}" where [{value}]=="{var}"')
                ok = self.showDialog('Confirm', 'Are you sure you want to update!!!', 'Question')
                if ok == 1024:
                    hosp.commit()
                    self.showDialog('SUCCESS', 'Successfully Updated the data', 'Information')
                    self.window.close()
                else:
                    pass
            else:
                pass

        elif all_value == 'Contact No':
            while True:
                contact_no, ok = QtWidgets.QInputDialog.getText(Form, "Contact No", "Enter the new Contact No:")
                if re.match(r'^\d{10}$', contact_no):
                    break
                elif ok != True:
                    break
                else:
                    self.showDialog('Error', 'Please enter 10 digits number!!!', 'Warning')
            if ok == True:
                curs.execute(f'Update data Set [{all_value}]="{contact_no}" where [{value}]=="{var}"')
                ok = self.showDialog('Confirm', 'Are you sure you want to update!!!', 'Question')
                if ok == 1024:
                    hosp.commit()
                    self.showDialog('SUCCESS', 'Successfully Updated the data', 'Information')
                    self.window.close()
                else:
                    pass

        elif all_value == 'Age':
            while True:
                age, ok = QtWidgets.QInputDialog.getText(Form, "Age", "Enter the updated Age:")
                if re.match(r'^[0-9]*$', age) and age != '':
                    break
                elif ok != True:
                    break
                else:
                    self.showDialog('Error', 'Please enter a valid age!!!', 'Warning')
            if ok == True:
                curs.execute(f'Update data Set [{all_value}]="{age}" where [{value}]=="{var}"')
                ok = self.showDialog('Confirm', 'Are you sure you want to update!!!', 'Question')
                if ok == 1024:
                    hosp.commit()
                    self.showDialog('SUCCESS', 'Successfully Updated the data', 'Information')
                    self.window.close()
                else:
                    pass

    def func_for_modify(self):
        try:
            self.all_columns = ['ID',  'Sex', 'Age', 'Blood Group', 'Contact No',
                                'Disease']
            value1, ok = QtWidgets.QInputDialog.getItem(Form, "Open", "Choose the criteria you want to update",
                                                        self.all_columns, 0, False)
            if ok == True:
                self.columns = ['ID']
                value2, ok = QtWidgets.QInputDialog.getItem(Form, "Open", "Choose the criteria to search", self.columns,
                                                            0, False)
                if ok == True:
                    hosp = sqlite3.connect('hospital_data.db')
                    curs = hosp.cursor()

                    if value2 == 'ID':
                        self.var = int(self.func_for_id_search())
                        curs.execute(f'Select * from data where ID=="{self.var}"')
                        rows = curs.fetchone()
                        if len(rows) == 0:
                            self.showDialog('ERROR', 'No such patient exists!!!', 'Critical')
                        else:
                            self.func_for_modification(value1, value2, self.var)

                    elif value2 == 'First Name':
                        self.var = self.func_for_name()
                        curs.execute(f'Select * from data where [First Name]=="{self.var.strip().title()}"')
                        rows = curs.fetchall()
                        if len(rows) == 1:
                            self.func_for_modification(value1, value2, self.var)
                        elif len(rows) == 0:
                            self.showDialog('ERROR', 'No such patient exists!!!', 'Critical')
                        else:
                            self.showDialog('Error',
                                            'More than one patient with this name exists!!!\n Please enter any other criteria',
                                            'Critical')
                            self.window.close()
                            self.func_for_modify
                    elif value2 == 'Contact No':
                        self.var = self.func_for_contact_grp()
                        curs.execute(f'Select * from data where [Contact No]=="{self.var}"')
                        rows = curs.fetchall()
                        if len(rows) == 1:
                            self.func_for_modification(value1, value2, self.var)
                        elif len(rows) == 0:
                            self.showDialog('ERROR', 'No such patient exists!!!', 'Critical')
                        else:
                            self.showDialog('Error',
                                            'More than one patient with this Conatct No exists!!!\n Please enter any other criteria',
                                            'Information')
                            self.window.close()
                            self.func_for_modify
                else:
                    pass
            else:
                pass
        except:
            pass



    def func_for_read_Doctor_data(self):
        self.window = QtWidgets.QWidget()
        self.ui = Doctors_table.Ui_Table()
        self.ui.setupUi(self.window)
        self.window.show()
        self.ui.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        hosp = sqlite3.connect('hospital_data.db')
        curs = hosp.cursor()
        curs.execute('Select * from Doctors')
        rows = curs.fetchall()
        row_val = 0
        for row in rows:
            col = 0
            while col <= 7:
                self.ui.tableWidget.setItem(row_val, col, QtWidgets.QTableWidgetItem(f'{row[col]}'))
                col += 1
            row_val += 1

    def func_for_doctor_id_search(self):
        ID, ok = QtWidgets.QInputDialog.getText(Form, "ID", "Enter the ID of the patient to search:")
        try:
            hosp = sqlite3.connect('hospital_data.db')
            curs = hosp.cursor()
            curs.execute(f'Select * from Doctors where DoctorID=="{ID}"')
            row = curs.fetchone()
            self.showDialog('DATA',
                            f' FirstName    :   {row[1]}\t\t\t\t\t \n LastName    :   {row[2]} \n DateOfBirth          : {row[3]} \n Gender          :   {row[4]} \n PhoneNumber  :   {row[4]} \n Specialty           : {row[5]} \n receptionID          :       {row[6]}\n\n',
                            'Information')
            return ID

        except:
            self.showDialog('ERROR', 'Please enter a valid ID!!!\n No such ID exists', 'Critical')

        # ... (other code remains unchanged)

    def func_for_Staff_id_search(self):
        ID, ok = QtWidgets.QInputDialog.getText(Form, "NurseID", "Enter the ID of the staff to search:")
        try:
            hosp = sqlite3.connect('hospital_data.db')
            curs = hosp.cursor()
            curs.execute(f'Select * from Staff where StaffID=="{ID}"')
            row = curs.fetchone()
            self.showDialog('DATA',
                            f' StaffType    :   {row[1]}\t\t\t\t\t \n Staffname    :   {row[2]} \n ID          : {row[3]}\n\n',
                            'Information' )
            return ID

        except:
            self.showDialog('ERROR', 'Please enter a valid nurse ID!!!\n No such nurse ID exists', 'Critical')



    def func_for_gender_grp(self):
        self.Docgender = ['Male', 'Female', 'Others']
        Docgender, ok = QtWidgets.QInputDialog.getItem(Form, "Open", "Choose the Gender to search", self.Docgender, 0,
                                                       False)
        try:
            hosp = sqlite3.connect('hospital_data.db')
            curs = hosp.cursor()
            curs.execute(f'Select * from Doctors where Gender=="{Docgender}"')
            rows = curs.fetchall()
            if len(rows) != 0 and ok == True:
                self.window = QtWidgets.QWidget()
                self.ui = Doctors_table.Ui_Table()
                self.ui.setupUi(self.window)
                self.window.show()
                self.ui.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
                row_val = 0
                for row in rows:
                    col = 0
                    while col <= 7:
                        self.ui.tableWidget.setItem(row_val, col, QtWidgets.QTableWidgetItem(f'{row[col]}'))
                        col += 1
                    row_val += 1
            elif ok != True:
                pass
            else:
                self.showDialog('ERROR', 'Sorry no doctor with this gender exists', 'Critical')
        except:
            pass

    def func_for_phone_no(self):
        while True:
            DocNumber, ok = QtWidgets.QInputDialog.getText(Form, "PhoneNumber", "Enter PhoneNumber:")
            if re.match(r'^\d{10}$', DocNumber):
                break
            elif ok != True:
                break
            else:
                self.showDialog('Error', 'Please enter 10 digits number!!!', 'Warning')
        if ok == True:
            hosp = sqlite3.connect('hospital_data.db')
            curs = hosp.cursor()
            curs.execute(f'Select * from Doctors where [PhoneNumber]=="{DocNumber}"')
            rows = curs.fetchall()
            if len(rows) != 0 and ok == True:
                self.window = QtWidgets.QWidget()
                self.ui = Doctors_table.Ui_Table()
                self.ui.setupUi(self.window)
                self.window.show()
                self.ui.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
                row_val = 0
                for row in rows:
                    col = 0
                    while col <= 7:
                        self.ui.tableWidget.setItem(row_val, col, QtWidgets.QTableWidgetItem(f'{row[col]}'))
                        col += 1
                    row_val += 1
                return DocNumber
            elif ok != True:
                pass
            else:
                self.showDialog('ERROR', 'No Doctor with this PhoneNumber exists', 'Critical')

    def func_for_doc_name(self):
        while True:
            Docname, ok = QtWidgets.QInputDialog.getText(Form, "nurse", "Enter the name of the Doctor:")
            if re.match(r'^[a-zA-Z]*$', Docname) and Docname != '':
                break
            elif ok != True:
                break
            else:
                self.showDialog('Error', 'Please enter a valid name!!!', 'Critical')
        if ok == True:
            hosp = sqlite3.connect('hospital_data.db')
            curs = hosp.cursor()
            curs.execute(f'Select * from Doctors where [FirstName]=="{Docname.strip().title()}"')
            rows = curs.fetchall()
            if len(rows) != 0 and ok == True:
                self.window = QtWidgets.QWidget()
                self.ui = Doctors_table.Ui_Table()
                self.ui.setupUi(self.window)
                self.window.show()
                self.ui.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
                row_val = 0
                for row in rows:
                    col = 0
                    while col <= 7:
                        self.ui.tableWidget.setItem(row_val, col, QtWidgets.QTableWidgetItem(f'{row[col]}'))
                        col += 1
                    row_val += 1
                return Docname
            elif ok != True:
                pass
            else:
                self.showDialog('ERROR', 'No Doctor with such name exists!!!', 'Critical')

    def func_for_doc_Specialty(self):
        while True:
            Specialtyname, ok = QtWidgets.QInputDialog.getText(Form, "doctor", "Enter the name of the Specialty:")
            if re.match(r'^[a-zA-Z]*$', Specialtyname) and Specialtyname != '':
                break
            elif ok != True:
                break
            else:
                self.showDialog('Error', 'Please enter a valid Specialty name!!!', 'Critical')
        if ok == True:
            hosp = sqlite3.connect('hospital_data.db')
            curs = hosp.cursor()
            curs.execute(f'Select * from Doctors where [Specialty]=="{Specialtyname.strip().title()}"')
            rows = curs.fetchall()
            if len(rows) != 0 and ok == True:
                self.window = QtWidgets.QWidget()
                self.ui = Doctors_table.Ui_Table()
                self.ui.setupUi(self.window)
                self.window.show()
                self.ui.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
                row_val = 0
                for row in rows:
                    col = 0
                    while col <= 7:
                        self.ui.tableWidget.setItem(row_val, col, QtWidgets.QTableWidgetItem(f'{row[col]}'))
                        col += 1
                    row_val += 1
                return Specialtyname
            elif ok != True:
                pass
            else:
                self.showDialog('ERROR', 'No Doctor with such name exists!!!', 'Critical')


    def func_for_read_Staff_data(self):
        self.window = QtWidgets.QWidget()
        self.ui = Staff_table.Ui_Table()
        self.ui.setupUi(self.window)
        self.window.show()
        self.ui.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        hosp = sqlite3.connect('hospital_data.db')
        curs = hosp.cursor()
        curs.execute('Select * from Staff')
        rows = curs.fetchall()
        row_val = 0
        for row in rows:
            col = 0
            while col <= 3:
                self.ui.tableWidget.setItem(row_val, col, QtWidgets.QTableWidgetItem(f'{row[col]}'))
                col += 1
            row_val += 1




    def func_for_Staff_id_search(self):
        ID, ok = QtWidgets.QInputDialog.getText(Form, "NurseID", "Enter the ID of the staff to search:")
        try:
            hosp = sqlite3.connect('hospital_data.db')
            curs = hosp.cursor()
            curs.execute(f'Select * from Staff where StaffID=="{ID}"')
            row = curs.fetchone()
            self.showDialog('DATA',
                            f' StaffType    :   {row[1]}\t\t\t\t\t \n Staffname    :   {row[2]} \n ID          : {row[3]}\n\n',
                            'Information' )
            return ID

        except:
            self.showDialog('ERROR', 'Please enter a valid nurse ID!!!\n No such nurse ID exists', 'Critical')



    # ... (other code remains unchanged)

    def func_for_Staff_type(self):
        self.stafftype = ['Nurse', 'Wardboy']
        stafftype, ok = QtWidgets.QInputDialog.getItem(Form, "Open", "Choose the staff_type to search", self.stafftype, 0, False)
        try:
            hosp = sqlite3.connect('hospital_data.db')
            curs = hosp.cursor()
            curs.execute(f'Select * from Staff  where StaffType=="{stafftype}"')
            rows = curs.fetchall()
            if len(rows) != 0 and ok == True:
                self.window = QtWidgets.QWidget()
                self.ui = Staff_table.Ui_Table()
                self.ui.setupUi(self.window)
                self.window.show()
                self.ui.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
                row_val = 0
                for row in rows:
                    col = 0
                    while col <= 3:
                        self.ui.tableWidget.setItem(row_val, col, QtWidgets.QTableWidgetItem(f'{row[col]}'))
                        col += 1
                    row_val += 1
            elif ok != True:
                pass
            else:
                self.showDialog('ERROR', 'Sorry no staff with this type exists', 'Critical')
        except:
            pass


    def func_for_Staff_name(self):
        while True:
            staffename, ok = QtWidgets.QInputDialog.getText(Form, "staff", "Enter the name of the staff:")
            if re.match(r'^[a-zA-Z]*$', staffename) and staffename != '':
                break
            elif ok != True:
                break
            else:
                self.showDialog('Error', 'Please enter a valid name!!!', 'Critical')
        if ok == True:
            hosp = sqlite3.connect('hospital_data.db')
            curs = hosp.cursor()
            curs.execute(f'Select * from Staff where [Staffname]=="{staffename.strip().title()}"')
            rows = curs.fetchall()
            if len(rows) != 0 and ok == True:
                self.window = QtWidgets.QWidget()
                self.ui = Staff_table.Ui_Table()
                self.ui.setupUi(self.window)
                self.window.show()
                self.ui.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
                row_val = 0
                for row in rows:
                    col = 0
                    while col <= 3:
                        self.ui.tableWidget.setItem(row_val, col, QtWidgets.QTableWidgetItem(f'{row[col]}'))
                        col += 1
                    row_val += 1
                return staffename
            elif ok != True:
                pass
            else:
                self.showDialog('ERROR', 'No staff with such name exists!!!', 'Critical')


    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(844, 525)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(r"icons/logo.PNG"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        Form.setStyleSheet(
            "background:url(icons/username_background.PNG);background-repeat: no-repeat;background-position: center;")
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 3, 7, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 1, 7, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem2, 2, 7, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 0, 2, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.write_patient = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.write_patient.setFont(font)
        self.write_patient.setStyleSheet("background-color:rgb(237, 171, 255)\n")
        self.write_patient.setObjectName("write_patient")
        self.gridLayout.addWidget(self.write_patient, 6, 0, 1, 1)
        self.age = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.age.setFont(font)
        self.age.setStyleSheet("background-color:rgb(237, 171, 255)\n")
        self.age.setObjectName("age")
        self.gridLayout.addWidget(self.age, 2, 0, 1, 1)
        self.sr_no = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.sr_no.setFont(font)
        self.sr_no.setStyleSheet("background-color:rgb(237, 171, 255)\n")
        self.sr_no.setObjectName("sr_no")
        self.gridLayout.addWidget(self.sr_no, 4, 0, 1, 1)
        self.gender = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.gender.setFont(font)
        self.gender.setStyleSheet("background-color:rgb(237, 171, 255)\n")
        self.gender.setObjectName("sex")
        self.gridLayout.addWidget(self.gender, 9, 0, 1, 1)
        self.blood_grp = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.blood_grp.setFont(font)
        self.blood_grp.setStyleSheet("background-color:rgb(237, 171, 255)\n")
        self.blood_grp.setObjectName("blood_grp")
        self.gridLayout.addWidget(self.blood_grp, 7, 0, 1, 1)
        self.contact_no = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.contact_no.setFont(font)
        self.contact_no.setStyleSheet("background-color:rgb(237, 171, 255)\n")
        self.contact_no.setObjectName("contact_no")
        self.gridLayout.addWidget(self.contact_no, 10, 0, 1, 1)
        self.addmitionid = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 0, 1, 1, 1)
        self.read_patient = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.read_patient.setFont(font)
        self.read_patient.setStyleSheet("background-color:rgb(237, 171, 255)\n")
        self.read_patient.setObjectName("read_patient")
        self.gridLayout.addWidget(self.read_patient, 0, 0, 1, 1)
        self.modify_details = QtWidgets.QPushButton(Form)
        self.modify_details.setFont(font)
        self.modify_details.setStyleSheet("background-color:rgb(237, 171, 255)\n")
        self.modify_details.setObjectName("modify_details")
        self.gridLayout.addWidget(self.modify_details, 5, 0, 1, 1)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.del_details = QtWidgets.QPushButton(Form)
        self.del_details.setFont(font)
        self.del_details.setStyleSheet("background-color:rgb(237, 171, 255)\n")
        self.modify_details.setObjectName("del_details")
        self.gridLayout.addWidget(self.del_details, 3, 0, 1, 1)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Name_search = QtWidgets.QPushButton(Form)
        self.Name_search.setFont(font)
        self.Name_search.setStyleSheet("background-color:rgb(237, 171, 255)\n")
        self.Name_search.setObjectName("name_search")
        self.gridLayout.addWidget(self.Name_search, 4, 2, 1, 1)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.disease = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.disease.setFont(font)
        self.disease.setStyleSheet("background-color:rgb(237, 171, 255)\n")
        self.disease.setObjectName("disease")
        self.gridLayout.addWidget(self.disease, 8, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 3, 3, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem5)
        self.label = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color:rgb(255, 93, 93)")
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem6)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 3, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem7, 0, 0, 1, 1)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem8, 0, 6, 1, 1)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem9, 0, 5, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem10)
        self.log_out = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.log_out.setFont(font)
        self.log_out.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.log_out.setStyleSheet("background-color:rgb(255, 137, 250)\n")
        self.log_out.setObjectName("log_out")
        self.horizontalLayout.addWidget(self.log_out)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 7, 1, 1)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem11, 0, 1, 1, 1)
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem12, 0, 4, 1, 1)
        self.Docgender = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Docgender.setFont(font)
        self.Docgender.setStyleSheet("background-color:rgb(237, 171, 255)\n")
        self.Docgender.setObjectName("nursegender")
        self.gridLayout.addWidget(self.Docgender, 2, 2, 1, 1)
        self.DocNumber = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.DocNumber.setFont(font)
        self.DocNumber.setStyleSheet("background-color:rgb(237, 171, 255)\n")
        self.DocNumber.setObjectName("PhoneNumber")
        self.gridLayout.addWidget(self.DocNumber, 5, 2, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(50, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 0, 8, 1, 1)
        self.read_doctor = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.read_doctor.setFont(font)
        self.read_doctor.setStyleSheet("background-color:rgb(237, 171, 255)\n")
        self.read_doctor.setObjectName("read_nurse")
        self.gridLayout.addWidget(self.read_doctor, 0, 2, 1, 1)
        self.name_Search = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.name_Search = QtWidgets.QPushButton(Form)
        self.name_Search.setFont(font)
        self.name_Search.setStyleSheet("background-color:rgb(237, 171, 255)\n")
        self.name_Search.setObjectName("name_search")
        self.gridLayout.addWidget(self.name_Search, 1, 0, 1, 1)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.docID = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.docID.setFont(font)
        self.docID.setStyleSheet("background-color:rgb(237, 171, 255)\n")
        self.docID.setObjectName("docID")
        self.gridLayout.addWidget(self.docID, 1, 2, 1, 1)
        self.Specialtyname = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Specialtyname.setFont(font)
        self.Specialtyname.setStyleSheet("background-color:rgb(237, 171, 255)\n")
        self.Specialtyname.setObjectName("deptID")
        self.gridLayout.addWidget(self.Specialtyname, 3, 2, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 3, 3, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem5)
        self.label = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color:rgb(255, 93, 93)")
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem6)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 3, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(50, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem7, 0, 0, 1, 1)
        spacerItem8 = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem8, 0, 6, 1, 1)
        spacerItem9 = QtWidgets.QSpacerItem(70, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem9, 0, 5, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem10)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 7, 1, 1)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem11, 0, 1, 1, 1)
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem12, 0, 4, 1, 1)
        self.stafftype = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.stafftype.setFont(font)
        self.stafftype.setStyleSheet("background-color:rgb(237, 171, 255)\n")
        self.stafftype.setObjectName("stafftype")
        self.gridLayout.addWidget(self.stafftype, 6, 5, 1, 1)
        self.StaffID = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.StaffID.setFont(font)
        self.StaffID.setStyleSheet("background-color:rgb(237, 171, 255)\n")
        self.StaffID.setObjectName("StaffID")
        self.gridLayout.addWidget(self.StaffID, 2, 5, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 0, 1, 1, 1)
        self.read_staff = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.read_staff.setFont(font)
        self.read_staff.setStyleSheet("background-color:rgb(237, 171, 255)\n")
        self.read_staff.setObjectName("read_nurse")
        self.gridLayout.addWidget(self.read_staff, 0, 5, 1, 1)
        self.staffename = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.staffename = QtWidgets.QPushButton(Form)
        self.staffename.setFont(font)
        self.staffename.setStyleSheet("background-color:rgb(237, 171, 255)\n")
        self.staffename.setObjectName("name_search")
        self.gridLayout.addWidget(self.staffename,4, 5, 1, 1)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 3, 3, 1)
        self.read_doctor.clicked.connect(self.func_for_read_Doctor_data)
        self.docID.clicked.connect(self.func_for_doctor_id_search)
        self.Docgender.clicked.connect(self.func_for_gender_grp)
        self.DocNumber.clicked.connect(self.func_for_phone_no)
        self.Name_search.clicked.connect(self.func_for_doc_name)
        self.Specialtyname.clicked.connect(self.func_for_doc_Specialty)
        self.write_patient.clicked.connect(self.func_for_new_data)
        self.read_patient.clicked.connect(self.func_for_read_data)
        self.sr_no.clicked.connect(self.func_for_id_search)
        self.blood_grp.clicked.connect(self.func_for_blood_grp)
        self.age.clicked.connect(self.func_for_age_grp)
        self.gender.clicked.connect(self.func_for_patient_gender_grp)
        self.contact_no.clicked.connect(self.func_for_contact_grp)
        self.disease.clicked.connect(self.func_for_disease_grp)
        self.log_out.clicked.connect(self.func_for_log_out)
        self.name_Search.clicked.connect(self.func_for_name)
        self.del_details.clicked.connect(self.func_for_del)
        self.modify_details.clicked.connect(self.func_for_modify)
        self.read_staff.clicked.connect(self.func_for_read_Staff_data)
        self.StaffID.clicked.connect(self.func_for_Staff_id_search)
        self.stafftype.clicked.connect(self.func_for_Staff_type)
        self.staffename.clicked.connect(self.func_for_Staff_name)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Welcome"))
        self.write_patient.setText(_translate("Form", "New Patient"))
        self.age.setText(_translate("Form", "Search patient Age"))
        self.sr_no.setText(_translate("Form", " search patient ID "))
        self.gender.setText(_translate("Form", "Search patient Gender"))
        self.blood_grp.setText(_translate("Form", "Blood Group"))
        self.contact_no.setText(_translate("Form", "Search Contact no."))
        self.read_patient.setText(_translate("Form", "Show Patients"))
        self.modify_details.setText(_translate("Form", "Modify Patient Details"))
        self.del_details.setText(_translate("Form", "Delete Patient Details"))
        self.Name_search.setText(_translate("Form", "Search Doctor"))
        self.disease.setText(_translate("Form", "Search Disease"))
        self.label.setText(_translate("Form", "WELCOME TO THE HOSPITAL"))
        self.log_out.setText(_translate("Form", "Log Out"))
        self.docID.setText(_translate("Form", "DocID "))
        self.Docgender.setText(_translate("Form", "Search doctor Gender"))
        self.DocNumber.setText(_translate("Form", "Search doctor PhoneNumber."))
        self.read_doctor.setText(_translate("Form", "Show Doctors"))
        self.name_Search.setText(_translate("Form", "Search patient "))
        self.Specialtyname.setText(_translate("Form", "Search Specialtyname"))
        self.StaffID.setText(_translate("Form", "StaffID "))
        self.stafftype.setText(_translate("Form", "Search Staff type"))
        self.read_staff.setText(_translate("Form", "Show Staff"))
        self.staffename.setText(_translate("Form", "Search Staff"))


import sys

app = QtWidgets.QApplication(sys.argv)
Form = QtWidgets.QWidget()

if __name__ == "__main__":
    ui = Ui_Form()
    Form = QtWidgets.QWidget()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
