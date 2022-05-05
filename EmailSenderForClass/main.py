from fileinput import close, filename
from sys import argv
from PyQt5.uic import *
from PyQt5 import *
from numpy import False_
from pyqt5_tools import *
from PyQt5.QtWidgets import *
import csv
import re
import smtplib
import imghdr
from email.message import EmailMessage

EMAIL_ADDRESS = "randomusersomewhere@gmail.com"
EMAIL_PASSWORD = "@newways"

def selectFile():
    fname = QFileDialog.getOpenFileNames(start, "open file", "." , "CSV ONLY (*.csv)")
    fname = fname[0]
    with open("inputstart\inputs.csv","w", newline="") as FILE:
        writer = csv.writer(FILE)
        writer.writerow(fname)

def selectFile1():
    fname = QFileDialog.getOpenFileName(start, "open file", "." , "CSV ONLY (*.csv)")
    fname = fname[0]
    with open("inputstart\inputs.csv","w", newline="") as FILE:
        writer = csv.writer(FILE)
        writer.writerow([fname])

def selected():
    selectFile()
    fname = []
    with open("inputstart\inputs.csv","r") as FILE:
        reader = csv.reader(FILE)
        for line in reader:
            fname = line
    answer = 0
    if (len(fname) != 0) :
        answer = 1
    with open("verify.csv","w",newline="") as FILE:
        writer = csv.writer(FILE)
        writer.writerow([answer])
    
def fetch_students(ch):
    students = []
    with open(ch,"r")as FILE:
        reader = csv.DictReader(FILE)
        for student in reader:
            students.append(student)
    return students




def edited():
    selectFile1()
    fname = []
    with open("inputstart\inputs.csv","r") as FILE:
        reader = csv.reader(FILE)
        for line in reader:
            fname = line
    answer = 0
    if (len(fname) != 0) :
        start.close()
        edit.show()
    


def created():
    start.close()
    make.show()

def verifyemail(ch,students):
    test = True
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not(re.fullmatch(regex, ch)):
        test = False
    for student in students:
        if student["adress"] == ch:
            test = False
    return test

def verifyemail1(ch,students):
    test = True
    count = 0
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not(re.fullmatch(regex, ch)):
        test = False
    for student in students:
        if student["adress"] == ch:
            count+=1
    if count == 0 :
        test = False
    return test

def verifyename(ch,students):
    test = True
    spacecount = 0
    check = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm "
    for i in range(len(ch)):
        if ch[i] == " ":
            spacecount+=1
        if not(ch[i] in check):
                test = False
                print(ch[i])
                print("alpha")
    if spacecount != 1 :
        test = False
        print(spacecount)
    for student in students:
        if student["name"] == ch:
            test = False
            print("exist")
    return test

def verifyename1(ch,students):
    test = True
    count = 0
    spacecount = 0
    check = "QWERTYUIOPASDFGHJKLZXCVBNMmnbvcxzlkjhgfdsapoiuytrewq "
    for i in range(len(ch)):
        if ch[i] == " ":
            spacecount+=1
        if not(ch[i] in check):
                test = False
    if spacecount != 1 :
        test = False
    for student in students:
        if student["name"] == ch:
            count+=1
    if count == 0 :
        test = False
    return test

def addstudents():
    error = ""
    cstudent = {}
    header = ["name","adress"]
    students = []
    with open("tmpstudents.csv","r") as FILE :
        studentss = csv.DictReader(FILE)
        for student in studentss :
            students.append(student)
    print(len(students))
    if (len(students) == 0):
        with open("tmpstudents.csv","w", newline="") as FILE :
            print("made it")
            writer = csv.DictWriter(FILE, fieldnames=header)
            writer.writeheader()
            cstudent["name"] = make.name.text()
            cstudent["adress"] = make.adress.text()
            if (verifyemail(cstudent["adress"],students) == False):
                error = "Email Not Appropriate"  
            elif(verifyename(cstudent["name"],students) == False):
                error = "Name Not Aprropriate"
            if (error == ""):
                writer.writerow(cstudent)
            else:
                errors.errorlab.setText(error)
                errors.show()
                error=""
    else :
        with open("tmpstudents.csv","w", newline="") as FILE :
            print("made it")
            writer = csv.DictWriter(FILE, fieldnames=header)
            writer.writeheader()
            cstudent["name"] = make.name.text()
            cstudent["adress"] = make.adress.text()
            print(cstudent["name"])
            if (verifyemail(cstudent["adress"],students) == False):
                error = "Email Not Appropriate"
                
            elif(verifyename(cstudent["name"],students) == False):
                error = "Name Not Aprropriate"
            if (error == ""):
                writer.writerow(cstudent)
                for i in range(len(students)):
                    writer.writerow(students[i])
            else:
                for i in range(len(students)):
                    writer.writerow(students[i])
                errors.errorlab.setText(error)
                errors.show()
                error=""


def quitte():
    errors.close()

def addstudentedit():
    error1 = ""
    fname = []
    with open("inputstart\inputs.csv","r") as FILE:
        reader = csv.reader(FILE)
        for line in reader:
            fname = line
    students = fetch_students(fname[0])
    name = edit.username.text()
    adress = edit.adress.text()
    if (verifyemail(adress,students) == False):
        error1 = "Email must not contain spaces and just 1 @ and a correcet Domain"
    elif (verifyename(name,students) == False):
        error1 = "The Name Must not exist already or Contain Any Characters beside Alpha and 1 space"
    if (len(error1) != 0 ):
        with open(fname[0],"w", newline="") as FILE:
            header = ["name","adress"]
            writer = csv.DictWriter(FILE, fieldnames=header)
            writer.writeheader()
            for i in range(len(students)):
                writer.writerow(students[i])
        errors.errorlab.setText(error1)
        errors.show()
        error1 = ""
    else:
        with open(fname[0],"w", newline="") as FILE:
            header = ["name","adress"]
            writer = csv.DictWriter(FILE, fieldnames=header)
            writer.writeheader()
            for i in range(len(students)):
                writer.writerow(students[i])
            writer.writerow(
                {
                    "name":name,
                    "adress":adress
                }
            )

def deletestudent():
    error1 = ""
    fname = []
    with open("inputstart\inputs.csv","r") as FILE:
        reader = csv.reader(FILE)
        for line in reader:
            fname = line
    students = fetch_students(fname[0])
    name = edit.username.text()
    adress = edit.adress.text()
    if (verifyemail1(adress,students) == False):
        error1 = "Email must not contain spaces and just 1 @ and a correcet Domain"
    elif (verifyename1(name,students) == False):
        error1 = "The Name Must  exist  and not Contain Any Characters beside Alpha and 1 space"
    exist = 0
    existadress = 0
    pos = -1
    for student in students:
        pos+=1
        if student["name"] == name:
            exist+=1
            break
        elif student["adress"] == adress:
            existadress+=1
            break
    if (exist == 0 and existadress == 0) :
        error1 = "User Doesn't Exist"

    if (len(error1) != 0 ):
        with open(fname[0],"w",newline="") as FILE:
            header = ["name","adress"]
            writer = csv.DictWriter(FILE, fieldnames=header)
            writer.writeheader()
            for i in range(len(students)):
                writer.writerow(students[i])
        errors.errorlab.setText(error1)
        errors.show()
        error1=""
    else:
        del students[pos]
        with open(fname[0],"w",newline="") as FILE:
            header = ["name","adress"]
            writer = csv.DictWriter(FILE, fieldnames=header)
            writer.writeheader()
            for i in range(len(students)):
                writer.writerow(students[i])

def updateEmail():
    error1 = ""
    fname = []
    with open("inputstart\inputs.csv","r") as FILE:
        reader = csv.reader(FILE)
        for line in reader:
            fname = line
    students = fetch_students(fname[0])
    name = edit.username.text()
    adress = edit.adress.text()
    #if (verifyemail1(adress,students) == False):
    #    error1 = "Email must not contain spaces and just 1 @ and a correcet Domain"
    if (verifyename1(name,students) == False):
        error1 = "The Name Must  exist already and not Contain Any Characters beside Alpha and 1 space"
    exist = 0
    pos = -1
    for student in students:
        pos+=1
        if student["name"] == name:
            exist+=1
            break
    if ( exist == 0) :
        error1 = "User Doesn't Exist"

    if (len(error1) != 0 ):
        with open(fname[0],"w",newline="") as FILE:
            header = ["name","adress"]
            writer = csv.DictWriter(FILE, fieldnames=header)
            writer.writeheader()
            for i in range(len(students)):
                writer.writerow(students[i])
        errors.errorlab.setText(error1)
        errors.show()
        error1=""
    else:
        students[pos]["adress"] = adress
        with open(fname[0],"w",newline="") as FILE:
            header = ["name","adress"]
            writer = csv.DictWriter(FILE, fieldnames=header)
            writer.writeheader()
            for i in range(len(students)):
                writer.writerow(students[i])
def updateName():
    error1 = ""
    fname = []
    with open("inputstart\inputs.csv","r") as FILE:
        reader = csv.reader(FILE)
        for line in reader:
            fname = line
    students = fetch_students(fname[0])
    name = edit.username.text()
    adress = edit.adress.text()
    if (verifyemail1(adress,students) == False):
        error1 = "Email must not contain spaces and just 1 @ and a correcet Domain"
    #elif (verifyename(name,students) == False):
    #    error1 = "The Name Must  exist already and not Contain Any Characters beside Alpha and 1 space"
    exist = 0
    pos = -1
    for student in students:
        pos+=1
        if student["adress"] == adress:
            exist+=1
            break
    if ( exist == 0) :
        error1 = "User Doesn't Exist"

    if (len(error1) != 0 ):
        with open(fname[0],"w",newline="") as FILE:
            header = ["name","adress"]
            writer = csv.DictWriter(FILE, fieldnames=header)
            writer.writeheader()
            for i in range(len(students)):
                writer.writerow(students[i])
        errors.errorlab.setText(error1)
        errors.show()
        error1=""
    else:
        students[pos]["name"] = name
        with open(fname[0],"w",newline="") as FILE:
            header = ["name","adress"]
            writer = csv.DictWriter(FILE, fieldnames=header)
            writer.writeheader()
            for i in range(len(students)):
                writer.writerow(students[i])
    

def savethefile():
    header = ["name","adress"]
    file = QFileDialog.getSaveFileName(make,"Choose Where to save the file","students.csv","CSV ONLY (*.csv)")
    with open(file[0],"w",newline="") as FILE:
        students = []
        writer = csv.DictWriter(FILE, fieldnames=header)
        writer.writeheader()
        with open("tmpstudents.csv","r") as FILE :
            studentss = csv.DictReader(FILE)
            for student in studentss :
                students.append(student)
        for i in range(len(students)):
            writer.writerow(students[i])
        with open("tmpstudents.csv","w",newline="") as FILE :
            close
            


def send():
    answer = 0
    with open("verify.csv","r") as FILE:
        reader = csv.reader(FILE)
        for line in reader:
            answer = int(line[0])
    if answer == 0 :
        errors.errorlab.setText("File Not Selected")
        errors.show()
    else:
        with open("verify.csv","w",newline="") as FILE:
            writer = csv.writer(FILE)
            writer.writerow([0])
        start.close()
        sendd.show()



def imagedirectory():
    file = fname = QFileDialog.getOpenFileNames(start, "open file", "." , "Photos (*.png; *.jpg ; *.jfif)")
    file = file[0]
    if (len(file) != 0):
        with open("attach\img.csv","w",newline="") as FILE :
            writer = csv.writer(FILE)
            writer.writerow(file)
        

def pdfdirectory():
    file = fname = QFileDialog.getOpenFileNames(start, "open file", "." , "PDF ONLY (*.pdf)")
    file = file[0]
    if (len(file) != 0):
        with open("attach\pdf.csv","w",newline="") as FILE :
            writer = csv.writer(FILE)
            writer.writerow(file)
        

            






def senditdamn():
    filedirectory = []
    image = []
    pdf = []
    with open("Inputstart\inputs.csv","r") as FILE:
        reader = csv.reader(FILE)
        for line in reader:
            filedirectory.append(line)
    students = []
    for i in range(len(filedirectory[0])):
        with open(filedirectory[0][i],"r") as FILE:
            reader = csv.DictReader(FILE)
            for line in reader :
                if not(line["adress"] in students):
                    students.append(line["adress"])
        if (len(students) == 0):
            errors.errorlab.setText("No Emails Found In FIle")
            errors.show()
            return 0


    msg = EmailMessage()
    msg['Subject'] = sendd.subject.text()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = students
    msg.set_content(sendd.content.toPlainText())


    with open("attach\img.csv","r") as FILE:
        reader = csv.reader(FILE)
        for line in reader:
            image = line
    if (len(image) != 0):
        for i in range(len(image)):
            with open(image[i],"rb") as f:
                file_data = f.read()
                file_type = imghdr.what(f.name)
                file_name = f.name

                msg.add_attachment(file_data, maintype="image", subtype=file_type, filename=file_name)
    with open("attach\img.csv","w",newline="") as FILE:
        writer = csv.writer(FILE)
        close


    with open("attach\pdf.csv","r") as FILE:
        reader = csv.reader(FILE)
        for line in reader:
            pdf = line
    if (len(image) != 0):
        for i in range(len(pdf)):
            with open(pdf[i],"rb") as f:
                file_data = f.read()
                file_name = f.name

                msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)
    with open("attach\pdf.csv","w") as FILE:
        writer = csv.writer(FILE)
        close





    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)










app = QApplication(argv)
start = loadUi("GUI\start_screen\start.ui")
make = loadUi("GUI\create_screen\create.ui")
edit = loadUi("GUI\edit_screen\edit.ui")
errors = loadUi("GUI\error_screen\error.ui")
sendd = loadUi("GUI\send_screen\send.ui")
start.show()
fnames = []
start.sf.clicked.connect(selected)
start.ef.clicked.connect(edited)
start.send.clicked.connect(send)
start.cf.clicked.connect(created)
make.add.clicked.connect(addstudents)
errors.quit.clicked.connect(quitte)
edit.addstudent.clicked.connect(addstudentedit)
edit.deletestudent.clicked.connect(deletestudent)
edit.updateemail.clicked.connect(updateEmail)
edit.updatename.clicked.connect(updateName)
make.savefile.clicked.connect(savethefile)
sendd.sendfinal.clicked.connect(senditdamn)
sendd.image.clicked.connect(imagedirectory)
sendd.pdf.clicked.connect(pdfdirectory)



app.exec_()