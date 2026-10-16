import time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import csv
from math import *

def supersplit(text):
    prim=''
    for i in text:
        if i not in '<>=!':
            prim+=i
        else:
            break
    new=text[len(prim):]
    sec=new.strip('<>=!')
    sym=''
    for i in text:
        if i in '<>=!':
            sym+=i
    return([prim,sym,sec])
def csvtodict(filehandle,delimiter):
    data=filehandle.readlines()
    if data==[]:
        return {1:{"":""}}
    elif len(data)==1:
        dict1={}
        dict1.update({1:{}})
        for i in data:
            dict1[1].update({i:""})
        return dict1
    else:
        alldata=[]
        for i in data:
            a=i.strip()
            alldata.append(a)
        for i in alldata:
            if i=="":
                alldata.remove(i)
        parameters=alldata[0]
        parameters=parameters.split(delimiter)
        maindict={}
        innerdict={}
        for i in range(1,len(alldata)):
            alldata[i]=alldata[i].split(delimiter)
            innerdict=zip(parameters,alldata[i])
            maindict.update({i:dict(innerdict)})
        return maindict

class MainTableWindow(QWidget): 
    def __init__(self, dictionary): 
        super().__init__() 
        self.title = 'Data Table'
        self.left = 300
        self.top = 300
        self.width = 800
        self.height = 300

        self.setWindowTitle(self.title) 
        self.setGeometry(self.left, self.top, self.width, self.height) 
        self.setStyleSheet("background-color:#cadee3;""font-size:15px;")

        self.createTable(dictionary) 

        self.layout = QVBoxLayout() 
        self.layout.addWidget(self.tableWidget) 
        self.setLayout(self.layout) 

        self.show() 
    
    def createTable(self, dictionary): 
        self.tableWidget = QTableWidget() 

        self.tableWidget.setRowCount(len(dictionary.keys()) + 1) 
        self.tableWidget.setColumnCount(len(dictionary[1].keys())) 

        refdata = list(dictionary.values())
        parameters = list(refdata[0].keys())
        self.tableWidget.setHorizontalHeaderLabels(parameters)

        rownum = 0
        for i in refdata:
            colnum = 0
            for j in list(i.values()):
                self.tableWidget.setItem(rownum, colnum, QTableWidgetItem(str(j)))
                colnum += 1
            rownum += 1

        self.tableWidget.horizontalHeader().setStretchLastSection(True) 
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 

        
class MasterEditorWindow(QWidget):
    def __init__(self, dictionary,delimiter,location):
        super().__init__()
        self.localtext=location
        self.delim=delimiter
        self.setWindowTitle("Master Editor")
        self.setGeometry(200, 200, 1000, 500)
        self.setStyleSheet("background-color:#ffe600;")

        self.layout = QGridLayout()
        
        self.command_input = QLineEdit(self)
        self.command_input.setPlaceholderText("Enter command...")
        self.command_input.setStyleSheet('font-size:30px;'"background-color:#f2e2b6;")
        self.layout.addWidget(self.command_input,0,0)
        
        self.execute_button = QPushButton("Execute", self)
        self.execute_button.clicked.connect(self.execute_command)
        self.execute_button.setStyleSheet('font-size:30px;'"background-color:#f2d37c;")
        self.layout.addWidget(self.execute_button,0,1)
        
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setStyleSheet("background-color:#cadee3;""font-size:15px;")
        self.layout.addWidget(self.tableWidget,1,0,1,2)
        
        self.save_button = QPushButton("Save as CSV", self)
        self.save_button.clicked.connect(self.save_table_to_csv)
        self.save_button.setStyleSheet('font-size:30px;'"background-color:#f2d37c;")
        self.layout.addWidget(self.save_button,2,0,2,2)
        
        self.setLayout(self.layout)
        self.populate_table(dictionary)
    
    def execute_command(self):
        command = self.command_input.text()
        breaker=self.delim
        if command == "save csv":
            self.save_table_to_csv()
        elif command.startswith('show any where '):
            alldata=command[len('show any where '):]
            alldata=alldata.split(" <or> ")
            fh=open(self.localtext)
            data=list(csv.reader(fh,delimiter=self.delim))
            fh.close()
            for i in data:
                if i==[]:
                    data.remove(i)
            viewer=[]
            for parameter in alldata:
                parameter=parameter.split("=")
                para=data[0]
                target=para.index(parameter[0])
                for i in range(1,len(data)):
                    temp=data[i]
                    if temp[target]==parameter[1]:
                        viewer.append(temp)
            newfile=open("temp.csv", 'w')
            datawrite=csv.writer(newfile,delimiter=self.delim)
            required=[]
            required.append(data[0])
            for i in viewer:
                required.append(i)
            datawrite.writerows(required)
            newfile.close()
            fh=open("temp.csv")
            data=csvtodict(fh,self.delim)
            self.populate_table(data)
        elif command.startswith('show all specific where '):
            alldata=command[len('show all specific where '):]
            parameters=alldata.split(" <and> ")
            headers=[]
            values=[]
            viewer=[]
            for i in parameters:
                a=i.split("=")
                headers.append(a[0])
                values.append(a[1])
            fh=open(self.localtext)
            data=list(csv.reader(fh,delimiter=self.delim))
            fh.close()
            for i in data:
                if i==[]:
                    data.remove(i)
            para=data[0]
            targetparameters=[para.index(i) for i in headers]
            to_be_removed=True
            for i in range(1,len(data)):
                temp=data[i]
                to_be_removed=True
                counter=0
                for j in targetparameters:
                    if temp[j] != values[counter]:
                        to_be_removed=False
                        break
                    counter+=1
                if to_be_removed==True:
                    viewer.append(temp)
            newfile=open("temp.csv", 'w')
            writedata=csv.writer(newfile,delimiter=self.delim)
            required=[]
            required.append(data[0])
            for i in viewer:
                required.append(i)
            writedata.writerows(required)
            newfile.close()
            newfile=open("temp.csv")
            data=csvtodict(newfile,self.delim)
            self.populate_table(data)   
        elif command.startswith('any where '):
            alldata=command[len('any where '):]
            alldata=alldata.split(" <set> ")
            requirements=alldata[0]
            changes=alldata[1]
            requirements=requirements.split(" <or> ")
            headers=[]
            targetvalues=[]
            changes=changes.split(" <and> ")
            for i in changes:
                temp=i.split("=")
                headers.append(temp[0])
                targetvalues.append(temp[1])
            fh=open(self.localtext)
            data=list(csv.reader(fh,delimiter=self.delim))
            fh.close()
            for i in data:
                if i==[]:
                    data.remove(i)
            viewer=[]
            for parameter in requirements:
                parameter=parameter.split("=")
                para=data[0]
                target=para.index(parameter[0])
                for i in range(1,len(data)):
                    temp=data[i]
                    if temp[target]==parameter[1]:
                        viewer.append(i)
            viewer=list(set(viewer))
            fh=open(self.localtext)
            dict1=csvtodict(fh,self.delim)
            for i in dict1:
                if i in viewer:
                    for j in range(len(headers)):
                        dict1[i].update({headers[j]:targetvalues[j]})
            self.populate_table(dict1) 
        elif command.startswith('specific where '):
            alldata=command[len('specific where '):]
            alldata=alldata.split(" <set> ")
            requirements=alldata[0]
            head=[]
            val=[]
            changes=alldata[1]
            print(changes)
            requirements=requirements.split(" <and> ")
            headers=[]
            targetvalues=[]
            changes=changes.split(" <and> ")
            for i in changes:
                temp=i.split("=")
                headers.append(temp[0])
                targetvalues.append(temp[1])
            for i in requirements:
                a=i.split("=")
                head.append(a[0])
                val.append(a[1])
            fh=open(self.localtext)
            data=list(csv.reader(fh,delimiter=self.delim))
            fh.close()
            for i in data:
                if i==[]:
                    data.remove(i)
            to_be_removed=True
            viewer=[]
            print(head,val)
            print(headers,targetvalues)
            para=data[0]
            targetparameters=[para.index(i) for i in head]
            to_be_removed=True
            for i in range(1,len(data)):
                temp=data[i]
                to_be_removed=True
                counter=0
                for j in targetparameters:
                    if temp[j] != val[counter]:
                        to_be_removed=False
                        break
                    counter+=1
                if to_be_removed==True:
                    viewer.append(i)
            fh=open(self.localtext)
            dict1=csvtodict(fh,self.delim)
            for i in dict1:
                if i in viewer:
                    for j in range(len(headers)):
                        dict1[i].update({headers[j]:targetvalues[j]})
            self.populate_table(dict1)
        elif command.startswith('for entry '):
            alldata=command[len('for entry '):]
            alldata=alldata.split(" <set> ")
            position=int(alldata[0])
            changes=alldata[1]
            headers=[]
            targetvalues=[]
            changes=changes.split(" <and> ")
            for i in changes:
                temp=i.split("=")
                headers.append(temp[0])
                targetvalues.append(temp[1])
            fh=open(self.localtext)
            dict1=csvtodict(fh,self.delim)
            for j in range(0,len(headers)):
                dict1[position].update({headers[j]:targetvalues[j]})
            self.populate_table(dict1)
        elif command.startswith("add parameter "):
            arguments=command[len("add parameter "):].split(" <and> ")
            for i in arguments:
                column=i
                fh=open(self.localtext)
                data=csvtodict(fh,self.delim)
                for i in data:
                    data[i].update({column:""})
            self.populate_table(data)
        elif command.startswith('add blank entry where '):
            parameter=command[len('add blank entry where '):]
            parameter=parameter.split("=")
            fh=open(self.localtext)
            data=list(csv.reader(fh,delimiter=self.delim))
            fh.close()
            for i in data:
                if i==[]:
                    data.remove(i)
            position=data[0].index(parameter[0])
            newdata=['' for i in range(len(data[0]))]
            newdata[position]=parameter[1]
            data.append(newdata)
            fh=open("temp.csv", 'w')
            writeobject=csv.writer(fh,delimiter=self.delim)
            writeobject.writerows(data)
            fh.close()
            fh=open("temp.csv")
            data=csvtodict(fh,self.delim)
            self.populate_table(data)
        elif command.startswith("set parameter "):
            parameter=command[len('set parameter '):]
            parameter=parameter.split(" <to> ")
            fh=open(self.localtext)
            data=csvtodict(fh,self.delim)
            newdata={}
            for i in data:
                basedict={}
                newstuff=data[i]
                for j in newstuff:
                    if j==parameter[0]:
                        basedict.update({parameter[1]:newstuff[j]})
                    else:
                        basedict.update({j:newstuff[j]})
                newdata.update({i:basedict})
            self.populate_table(newdata)
        elif command.startswith('compare show any where '):
            alldata=command[len('compare show any where '):]
            alldata=alldata.split(" <or> ")
            fh=open(self.localtext)
            data=list(csv.reader(fh,delimiter=","))
            fh.close()
            for i in data:
                if i==[]:
                    data.remove(i)
            viewer=[]
            for parameter in alldata:
                lineworker="temp[target]"
                ultralineworker="float(temp[target])"
                counter=0
                for i in parameter:
                    if i not in '<>=!':
                        counter+=1
                        pass
                    else:
                        newstuff=(parameter[counter:]).strip('<>=!')
                        checksym=parameter[:parameter.index(newstuff)]
                        keypara=checksym.strip("<>=!")
                        for i in checksym:
                            if i not in '<>=!':
                                checksym=checksym.replace(i,"")
                lineworker+=checksym
                ultralineworker+=checksym
                lineworker+="parameter[1]"
                ultralineworker+="float(parameter[1])"
                parameter=[keypara,newstuff]
                para=data[0]
                target=para.index(parameter[0])
                for i in range(1,len(data)):
                    temp=data[i]
                    try:
                        if eval(ultralineworker)==True:
                            viewer.append(temp) 
                    except:
                        if eval(lineworker)==True:
                            viewer.append(temp)
            viewer.insert(0,data[0])
            fh=open('temp.csv','w')
            writertool=csv.writer(fh,delimiter=self.delim)
            writertool.writerows(viewer)
            fh.close()
            fh=open('temp.csv')
            dict1=csvtodict(fh,self.delim)
            self.populate_table(dict1)
        elif command.startswith('compare show specific where '):
            alldata=command[len('compare show specific where '):]
            alldata=alldata.split('<and>')
            fh=open(self.localtext)
            readfile=list(csv.reader(fh,delimiter=self.delim))
            for parameter in alldata:
                title=readfile.pop(0)
                parameter=supersplit(parameter)
                for i in readfile.copy():
                    targethead=title.index((parameter[0]).strip())  
                    while len(i) < len(title):
                        i.append("")
                    try:
                        new=float(i[targethead])
                        if eval(str(new)+parameter[1]+str(float(parameter[2])))==False:
                            readfile.remove(i)
                    except:
                        new=(i[targethead])
                        if eval("'"+new+"'"+parameter[1]+"'"+(parameter[2])+"'")==False:
                            readfile.remove(i)
                readfile.insert(0,title)
            fh=open('temp.csv','w',newline='')
            writertool=csv.writer(fh,delimiter=self.delim)
            writertool.writerows(readfile)
            fh.close()
            fh=open('temp.csv',newline='')
            dict1=csvtodict(fh,self.delim)
            self.populate_table(dict1)



    

    def save_temp_csv(self):
        with open("temp.csv", "w", newline="") as file:
            writer = csv.writer(file)
            
            headers = [self.tableWidget.horizontalHeaderItem(i).text() if self.tableWidget.horizontalHeaderItem(i) else "Column " + str(i+1) for i in range(self.tableWidget.columnCount())]
            writer.writerow(headers)
            
            for row in range(self.tableWidget.rowCount()):
                row_data = [self.tableWidget.item(row, col).text() if self.tableWidget.item(row, col) else "" 
                            for col in range(self.tableWidget.columnCount())]
                writer.writerow(row_data)
    
    def save_table_to_csv(self):
        timestamp = time.strftime("%d-%m-%Y_%H-%M-%S")
        filename = f"{timestamp}.csv"
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file,delimiter=self.delim)
            
            headers = [self.tableWidget.horizontalHeaderItem(i).text() if self.tableWidget.horizontalHeaderItem(i) else "Column " + str(i+1) for i in range(self.tableWidget.columnCount())]
            writer.writerow(headers)
            
            maintext="File saved successfully as "
            maintext+=filename
            
            QMessageBox.information(self, "Success!",maintext)
            
            
            
            for row in range(self.tableWidget.rowCount()):
                row_data = [self.tableWidget.item(row, col).text() if self.tableWidget.item(row, col) else "" 
                            for col in range(self.tableWidget.columnCount())]
                writer.writerow(row_data)
    
    def populate_table(self, dictionary):
        self.tableWidget.setRowCount(len(dictionary.keys()))
        self.tableWidget.setColumnCount(len(next(iter(dictionary.values())).keys()))
        self.tableWidget.setStyleSheet("background-color:#f0e79c;")

        refdata = list(dictionary.values())
        parameters = list(refdata[0].keys())
        self.tableWidget.setHorizontalHeaderLabels(parameters)

        rownum = 0
        for i in refdata:
            colnum = 0
            for j in list(i.values()):
                self.tableWidget.setItem(rownum, colnum, QTableWidgetItem(str(j)))
                colnum += 1
            rownum += 1

        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(30, 30, 900, 400)
        self.setWindowTitle("DataBase Manager")
        self.setStyleSheet("background-color:#6ff7c1;")
        self.initUI()
        self.delim=","
        
    def submitlocation(self):

        try:
            self.localtext = self.location.text().strip()
            fh=open(self.localtext, 'r')
            data = csvtodict(fh,self.delim)
            self.table_window = MainTableWindow(data)  
            self.table_window.show()
            self.locationerror.setText("")
            fh.close() 
        except Exception as error:
            wrong=str(error)
            self.locationerror.setText(wrong + "\n \n Please try again.") 
            self.locationerror.setWordWrap(True)
            self.locationerror.setStyleSheet("color:red;""font-size:20px;")
        
    def execute(self):
        try:
            command = self.function.text().strip()
            self.localtext = self.location.text().strip()
    
            if command.startswith("change delimiter to "):
                self.executionerror.setText("")
                command = command[len("change delimiter to "):]
                self.delim=command
            elif command.startswith("add entry at position "):
                self.executionerror.setText("")
                command = command[len('add entry at position '):]
                space_index = command.find(" ")  
                position = int(command[:space_index])  
                newdata = command[space_index + 1:] 
                newdata=newdata.split(" <and> ")
                fh=open(self.localtext, 'r')
                data=list(csv.reader(fh,delimiter=self.delim))
                for i in data:
                    if i==[]:
                        data.remove(i)
                newdata.reverse()
                for i in newdata:
                    i=i.split(self.delim)
                    data.insert(position,i)
                fh.close()
                fh=open(self.localtext, 'w')
                writeobject=csv.writer(fh,delimiter=self.delim)
                writeobject.writerows(data)
                fh.close()
            elif command.startswith("add entry at top "):
                self.executionerror.setText("")
                newdata = command[len('add entry at top '):] 
                newdata=newdata.split(" <and> ")
                fh=open(self.localtext, 'r')
                data=list(csv.reader(fh,delimiter=self.delim))
                for i in data:
                    if i==[]:
                        data.remove(i)
                newdata.reverse()
                for i in newdata:
                    i=i.split(self.delim)
                    data.insert(1,i)
                fh.close()
                fh=open(self.localtext, 'w')
                writeobject=csv.writer(fh,delimiter=self.delim)
                writeobject.writerows(data)
                fh.close()
            elif command.startswith("add entry "):
                self.executionerror.setText("")
                newdata = command[len('add entry '):] 
                newdata=newdata.split(" <and> ")
                fh=open(self.localtext, 'r')
                data=list(csv.reader(fh,delimiter=self.delim))
                for i in data:
                    if i==[]:
                        data.remove(i)
                newdata.reverse()
                for i in newdata:
                    i=i.split(self.delim)
                    data.append(i)
                fh.close()
                fh=open(self.localtext, 'w')
                writeobject=csv.writer(fh,delimiter=self.delim)
                writeobject.writerows(data)
                fh.close()
            elif command.startswith('add parameter at position '):
                self.executionerror.setText("")
                parameter=command[len('add parameter at position '):]
                space_index = parameter.find(" ")
                position = int(parameter[:space_index])  
                parameter = parameter[space_index + 1:]
                parameter=parameter.split(" <and> ")
                fh=open(self.localtext)
                data=list(csv.reader(fh,delimiter=self.delim))
                for i in data:
                    if i==[]:
                        data.remove(i)
                fh.close()
                parameter.reverse()
                for i in parameter:
                    data[0].insert(position-1,i)
                for i in range(len(parameter)):
                    for j in range(1,len(data)):
                        data[j].insert(position-1,"")
                fh=open(self.localtext, 'w')
                writeobject=csv.writer(fh,delimiter=self.delim)
                writeobject.writerows(data)
                fh.close()   
            elif command.startswith("add parameter "):
                self.executionerror.setText("")
                parameter=command[len('add parameter '):]
                parameter=parameter.split(" <and> ")
                fh=open(self.localtext)
                data=list(csv.reader(fh,delimiter=self.delim))
                for i in data:
                    if i==[]:
                        data.remove(i)
                fh.close()
                parameter.reverse()
                for i in parameter:
                    data[0].append(i)
                for i in range(len(parameter)):
                    for j in range(1,len(data)):
                        data[j].append("")
                fh=open(self.localtext, 'w')
                writeobject=csv.writer(fh,delimiter=self.delim)
                writeobject.writerows(data)
                fh.close()  
            elif command.startswith('add blank entry where '):
                self.executionerror.setText("")
                parameter=command[len('add blank entry where '):]
                parameter=parameter.split("=")
                fh=open(self.localtext)
                data=list(csv.reader(fh,delimiter=self.delim))
                for i in data:
                    if i==[]:
                        data.remove(i)
                position=data[0].index(parameter[0])
                newdata=['' for i in range(len(data[0]))]
                newdata[position]=parameter[1]
                data.append(newdata)
                fh=open(self.localtext, 'w')
                writeobject=csv.writer(fh,delimiter=self.delim)
                writeobject.writerows(data)
                fh.close() 
            elif command.startswith("remove any where "):
                self.executionerror.setText("")
                alldata=command[len('remove any where '):]
                alldata=alldata.split(" <or> ")
                removals=[]
                for parameter in alldata:
                    parameter=parameter.split("=")
                    fh=open(self.localtext)
                    data=list(csv.reader(fh,delimiter=self.delim))
                    fh.close()
                    para=data[0]
                    target=para.index(parameter[0])
                    for i in data:
                        if i==[]:
                            data.remove(i)
                    for i in range(1,len(data)):
                        new=data[i]
                        if new[target]==parameter[1]:
                            removals.append(new)
                for i in data.copy():
                    if i in removals:
                        data.remove(i)
                fh=open(self.localtext, 'w')
                writeobject=csv.writer(fh,delimiter=self.delim)
                writeobject.writerows(data)
                fh.close() 
                removals=[]
            elif command.startswith("remove all specific where "):
                self.executionerror.setText("")
                alldata=command[len('remove all specific where '):]
                parameters=alldata.split(" <and> ")
                headers=[]
                values=[]
                removals=[]
                for i in parameters:
                    a=i.split("=")
                    headers.append(a[0])
                    values.append(a[1])
                fh=open(self.localtext)
                data=list(csv.reader(fh,delimiter=self.delim))
                fh.close()
                for i in data:
                    if i==[]:
                        data.remove(i)
                para=data[0]
                targetparameters=[para.index(i) for i in headers]
                to_be_removed=True
                for i in range(1,len(data)):
                    temp=data[i]
                    to_be_removed=True
                    counter=0
                    for j in targetparameters:
                        if temp[j] != values[counter]:
                            to_be_removed=False
                            break
                        counter+=1
                    if to_be_removed==True:
                        removals.append(temp)
                for i in data.copy():
                    if i in removals:
                        data.remove(i) 
                fh=open(self.localtext, 'w')
                writercsv=csv.writer(fh,delimiter=self.delim)
                writercsv.writerows(data)
                fh.close()
            elif command.startswith('remove parameter '):
                self.executionerror.setText("")
                alldata=command[len('remove parameter '):]
                alldata=alldata.split(" <and> ")
                fh=open(self.localtext)
                data=list(csv.reader(fh,delimiter=self.delim))
                fh.close()
                for i in data:
                    if i==[]:
                        data.remove(i)
                parameters=data[0]
                locator=[parameters.index(i) for i in alldata]
                main=[]
                for i in parameters:
                    if i in alldata:
                        parameters.remove(i)
                newlists=[]
                for i in range(1,len(data)):
                    temp=data[i]
                    another=[]
                    for j in range(len(temp)):
                        if j in locator:
                            pass
                        else:
                            another.append(temp[j])
                    newlists.append(another)
                main.append(parameters)
                for i in newlists:
                    main.append(i)
                fh=open(self.localtext, 'w')
                writeobject=csv.writer(fh,delimiter=self.delim)
                writeobject.writerows(main)
                fh.close()
            elif command.startswith('remove entry at position '):
                self.executionerror.setText("")
                alldata=command[len('remove entry at position '):]
                position=int(alldata)
                fh=open(self.localtext)
                data=list(csv.reader(fh,delimiter=self.delim))
                fh.close()
                for i in data:
                    if i==[]:
                        data.remove(i)
                data.pop(position)
                fh=open(self.localtext,"w")
                writer=(csv.writer(fh,delimiter=self.delim))
                writer.writerows(data)
                fh.close()
            elif command.startswith("eval "):
                data=command[len('eval '):]
                data=eval(data)
                self.executionerror.setText(str(data)) 
                self.executionerror.setWordWrap(True)
                self.executionerror.setStyleSheet("color:black;""font-size:20px;")
            else:
                self.executionerror.setText("Invalid Function \n \n Please try again.") 
                self.executionerror.setWordWrap(True)
                self.executionerror.setStyleSheet("color:red;""font-size:20px;")
        except Exception as error:
            wrong=str(error)
            self.executionerror.setText(wrong + "\n \n Please try again.") 
            self.executionerror.setWordWrap(True)
            self.executionerror.setStyleSheet("color:red;""font-size:20px;")
        
    def allfunc(self):
        self.function_window = FunctionWindow()  
        self.function_window.show()
    def masterload(self):
        self.executionerror.setText("")
        fh=open(self.location.text().strip())
        data=csvtodict(fh,self.delim)
        self.masterwindow=MasterEditorWindow(data,self.delim,self.location.text().strip())
        self.masterwindow.show()
    def rawload(self):
        self.rawwindow = RawFileMaker(self.delim)
        self.rawwindow.show()
    def credload(self):
        credtext="This project was made for CBSE Board Practicals 2025-26 \n \n "
        credtext+="Made By... \n"
        credtext+="SOUNAK SARKAR \n"
        credtext+="XII-B"
        QMessageBox.information(self, 'Credits',credtext)

    def initUI(self):
        self.delim=","
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.mainlabel = QLabel("My Database Manager", self)
        self.mainlabel.setStyleSheet("font-size:30px")

        self.location = QLineEdit(self)
        self.location.setStyleSheet('font-size:30px;'"background-color:#a9f5d6;")
        self.location.setPlaceholderText("Enter file location...")

        self.locationsubmit = QPushButton("Load", self)
        self.locationsubmit.setStyleSheet('font-size:30px;'"background-color:#00ccff;")
        self.locationsubmit.clicked.connect(self.submitlocation)

        self.locationerror = QLabel(self)
        self.locationerror.setStyleSheet("color:red;")

        self.function = QLineEdit(self)
        self.function.setStyleSheet('font-size:30px;'"background-color:#a9f5d6;")
        self.function.setPlaceholderText("Enter function...")

        self.commander = QPushButton("Execute", self)
        self.commander.setStyleSheet('font-size:30px;'"background-color:#00ccff;")
        self.commander.clicked.connect(self.execute)

        self.executionerror = QLabel(self)
        self.executionerror.setStyleSheet("color:red;")

        self.docu = QPushButton("Show All Functions", self)
        self.docu.setStyleSheet('font-size:30px;'"background-color:#00ccff;")
        self.docu.clicked.connect(self.allfunc)

        self.master = QPushButton("Open Master Editor", self)
        self.master.setStyleSheet('font-size:30px;'"background-color:#00ccff;")
        self.master.clicked.connect(self.masterload)

        self.raw = QPushButton("Open Raw Editor", self)
        self.raw.setStyleSheet('font-size:30px;'"background-color:#00ccff;")
        self.raw.clicked.connect(self.rawload)
        
        self.credits = QPushButton("Credits",self)
        self.credits.setStyleSheet('font-size:30px;'"background-color:#00ccff;")
        self.credits.clicked.connect(self.credload)

        innergrid=QGridLayout()
        inwid=QWidget()
        inwid.setLayout(innergrid)
        innergrid.addWidget(self.docu,0,0)
        innergrid.addWidget(self.master,0,1)
        innergrid.addWidget(self.raw,1,0)
        innergrid.addWidget(self.credits,1,1)

        
        grid = QGridLayout()
        grid.addWidget(self.mainlabel, 0, 0)
        grid.addWidget(self.location, 1, 0)
        grid.addWidget(self.locationsubmit, 1, 1)
        grid.addWidget(self.locationerror,2,0)
        grid.addWidget(self.function,3,0)
        grid.addWidget(self.commander,3,1)
        grid.addWidget(self.executionerror,4,0)
        grid.addWidget(inwid,5,0)

        
        central_widget.setLayout(grid)

class RawFileMaker(QWidget):
    def __init__(self, breaker):
        super().__init__()
        self.setGeometry(100, 100, 600, 600)
        self.setWindowTitle("Raw File Writer")
        self.setStyleSheet("background-color:#94f589;")
        self.delim = breaker
        self.initUI()     

    def breaklines(self):
        self.delim = self.sepr.text().strip()

    def initUI(self):
        self.name = QLineEdit(self)
        self.name.setStyleSheet('font-size:20px;'"background-color:#a9f5d6;")
        self.name.setPlaceholderText("Enter file location/name...")

        self.sepr = QLineEdit(self)
        self.sepr.setStyleSheet('font-size:20px;'"background-color:#a9f5d6;")
        self.sepr.setPlaceholderText("Enter delimiter...")

        self.seperator = QPushButton("Set", self)
        self.seperator.setStyleSheet('font-size:20px;'"background-color:#60f765;")
        self.seperator.clicked.connect(self.breaklines)

        self.dynamictext = QPlainTextEdit(self)
        self.dynamictext.setStyleSheet('font-size:15px;'"background-color:#69f58e;")

        self.savestuff = QPushButton("Save File as CSV", self)
        self.savestuff.setStyleSheet('font-size:20px;'"background-color:#60f765;")
        self.savestuff.clicked.connect(self.filesaver)

        grid = QGridLayout()
        grid.addWidget(self.name, 0, 0, 1, 2)
        grid.addWidget(self.sepr, 1, 0)
        grid.addWidget(self.seperator, 1, 1)
        grid.addWidget(self.dynamictext, 2, 0, 1, 2)
        grid.addWidget(self.savestuff, 3, 0, 1, 2)

        self.setLayout(grid)

    def filesaver(self):
        text = self.dynamictext.toPlainText()
        lines = [line.split(self.delim) for line in text.split("\n")]

        filename = self.name.text().strip()
        if not filename:
            QMessageBox.warning(self, "Error", "Please enter a valid file name!")
            return

        try:
            with open(filename, "w", newline="") as fh:
                writer = csv.writer(fh, delimiter=self.delim)
                writer.writerows(lines)
            QMessageBox.information(self, "Success", f"File saved as {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save file:\n{str(e)}")

class FunctionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("All Functions")
        self.setGeometry(100, 100, 1000, 500) 
        self.setStyleSheet("font-size:15px;")

        layout = QVBoxLayout()

        allfunctions = """
        THIS IS A LIST OF ALL FUNCTIONS..... (Condition : File must be previously existing)
        
        (Note : You can create a new file using Raw File Editor)

        THE MAIN FUNCTIONS...
        (You can make changes to the whole file)

        - change delimiter to <delimiter>:
          To change delimiter (Default is comma (,))
        
        - add entry <lines separated by <and>>:
          To add new entries into the file 
        
        - add entry at top <lines separated by <and>>:
          To add entries into the top tier 
        
        - add entry at position <position> <lines separated by <and>>:
          To add entries at a specific position 
        
        - add parameter <parameters separated by <and>>:
          To add parameters 
        
        - add parameter at position <parameters separated by <and>>:
          To add parameters at a specific position 
        
        - add blank entry where <<parameter>=<value>>:
          To add new entry with only one value filled 
        
        - remove any where <<parameter>=<value> separated by <or>>:
          To remove entries that fulfill any of the given requirements 
        
        - remove all specific where <<parameter>=<value> separated by <and>>:
          To remove entries that fulfill all of the given requirements 
        
        - remove entry at position <position>:
          To remove an entry at a specific position 
        
        - remove parameter <parameters separated by <and>>:
          To remove parameters 
        
        - eval <simple expressions>:
          To evaluate and solve basic mathematics 

        THE MASTER EDITOR FUNCTIONS...
        (You can dynamically edit the table, show specific entries, and also save the new table as a CSV file.)

        - add parameter <parameters seperated by <and>>:
          To add a new parameter (similar to 'add parameter' in main functions)        
        
        - save csv:
          To save the file (You can also use the saving button)
          
        - set parameter <<old parameter> <to> <new parameter>>:
          To change the name of a parameter
          
        - add blank entry where <<parameter>=<value>>:
          To add new entry with only one value filled (similar to 'add blank entry where' in main functions)          
        
        - show any where <<parameter>=<value> separated by <or>>:
          To show entries that fulfill any of the given requirements 
        
        - show all specific where <<parameter>=<value> separated by <and>>:
          To show entries that fulfill all of the given requirements 
        
        - any where <<parameter>=<value> separated by <or>> <set> <<parameter>=<value> separated by <and>>:
          To set and change values of entries that fulfill any of the given requirements 
        
        - specific where <<parameter>=<value> separated by <and>> <set> <<parameter>=<value> separated by <and>>:
          To set and change values of entries that fulfill all of the given requirements 
        
        - for entry <position> <set> <<parameter>=<value> separated by <and>>:
          To set entries at a given position

        - compare show any where <<parameter>__<value> compared with logical operators and sepearted with <or>>:
          To compare and show all entries that follow any of the given conditions

        - compare show specific where <<parameter>__<value> compared with logical operators and sepearted with <and>>:
          To compare and show all entries that fulfill all the necessary comparative conditions
        """

        label = QLabel(allfunctions)
        label.setWordWrap(True)

        container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.addWidget(label)
        container.setLayout(container_layout)

        scrollArea = QScrollArea()
        scrollArea.setWidget(container)
        scrollArea.setWidgetResizable(True)
        scrollArea.setFrameShape(QFrame.NoFrame)

        layout.addWidget(scrollArea)
        self.setLayout(layout)

    
        
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    
if __name__ == "__main__":
    main()
