import tkinter
from tkinter import *
import pymysql
import tkinter.ttk
import tkinter.messagebox

# GlobalClass Class is created for All Globalvariables
# that we want to use in diffrent classes

class GlobalClass:
    hostName = None
    user = None
    password = None
    database = None
    connection = None
    @staticmethod
    def showDatainFrame(strQuery,newFrame):
        try:
            myCursor=GlobalClass.connection.cursor()
            rowAffected=myCursor.execute(strQuery)
            if(strQuery.find("select")==-1 and strQuery.find("desc")==-1):
                GlobalClass.connection.commit()
                Label(newFrame, text="Sucess "+str(rowAffected)+" row affected").grid(row=0, column=0)
                return
            elif(rowAffected==0):
                Label(newFrame,text="No Record Found").grid(row=0,column=0)
                return "No Record Found"

            r = 0
            c = 0
            Label(newFrame, text="Total Record= "+str(rowAffected)).grid(row=r, column=c,columnspan=3)
            r+=1
            c=0
            for rowHeader in myCursor.description:
                Label(newFrame, text=rowHeader[0], relief=RIDGE).grid(row=r, column=c, sticky=W + E + N + S)
                c += 1
            r += 1
            for row in myCursor.fetchall():
                c = 0
                for cell in row:
                    # print(cell)
                    # varEntry = StringVar()
                    Label(newFrame,text=cell, relief=RIDGE).grid(row=r, column=c, sticky=W + E + N + S)
                    # Entry(newFrame, textvariable=varEntry, relief=RIDGE).grid(row=r, column=c, sticky=W + E + N + S)
                    # varEntry.set(cell)
                    c += 1
                r+=1
        except Exception as ex:
            tkinter.messagebox.showerror("Exception", ex, parent=DatabaseExplorer.refMaster)


    @staticmethod
    def executeCustomQuery(strQuery,newFrame):

        try:
            if(strQuery=="" or strQuery=="\n"):
                raise Exception("Please Write Query First")
            myCursor=GlobalClass.connection.cursor()
            try:
                myCursor.execute("use " + DatabaseExplorer.selected_DataBase)
            except Exception as ex:
                tkinter.messagebox.showerror("Exception", "Please Select Database", parent=DatabaseExplorer.refMaster)
                return

            # if(strQuery.find("select")!=-1):
            GlobalClass.showDatainFrame(strQuery,newFrame)
                # rowAffected=myCursor.execute(strQuery)

            # GlobalClass.connection.commit()
            DatabaseExplorer.refDatabaseExplorer.createDataBaseTree()
            # return "Sucess: Total Affected:"+str(rowAffected)
        except Exception as ex:
            tkinter.messagebox.showerror("Exception", ex, parent=DatabaseExplorer.refMaster)


    @staticmethod
    def executeDMLQuery(strQuery):
        try:
            myCursor=GlobalClass.connection.cursor()
            myCursor.execute("use " + DatabaseExplorer.selected_DataBase)
            rowAffected=myCursor.execute(strQuery)
            GlobalClass.connection.commit()
            DatabaseExplorer.refDatabaseExplorer.createDataBaseTree()
            return "Sucess: Total Affected:"+str(rowAffected)
        except Exception as ex:
            return ex




    @staticmethod
    def createConnection(host, user, password):
        if (GlobalClass.connection == None):
            GlobalClass.connection = pymysql.connect(host=host, user=user, password=password)
            GlobalClass.hostName = host
            GlobalClass.user = user
            GlobalClass.password = password


# MainForm  is the first form from where we Connect to Server
class MainForm(Frame):
    refMainForm=None
    refMasterWindow=None

    def __init__(self,master=None):
        super().__init__(master)
        self.pack()
        self.createWidget()
        MainForm.refMainForm = self
        MainForm.refMainForm = master
#Method of Main Form
    def createWidget(self):
        self.lblHostName=Label(self,text="Host Name")
        self.lblHostName.grid(row=1,column=0,sticky=W)
        self.varHostName=StringVar()
        self.varHostName.set("localhost")
        self.txtHostName=Entry(self,textvariable=self.varHostName)
        self.txtHostName.grid(row=1,column=1,sticky=W)

        self.lblUser = Label(self, text="User")
        self.lblUser.grid(row=2, column=0,sticky=W)
        self.varUser = StringVar()
        self.varUser.set("root")
        self.txtUser = Entry(self, textvariable=self.varUser)
        self.txtUser.grid(row=2, column=1,sticky=W)

        self.lblPassword = Label(self, text="Password")
        self.lblPassword.grid(row=3, column=0,sticky=W)
        self.varPassword = StringVar()

        self.txtPassword = Entry(self, textvariable=self.varPassword,show='*')
        self.txtPassword.grid(row=3, column=1,sticky=W)

        self.btnConnect=Button(self,text="Connect",command=self.btnConnect_Click)
        self.btnConnect.grid(row=4,column=3)
        self.txtHostName.bind("<Key>",self.txtHostName_Enter)
        self.txtUser.bind("<Key>", self.txtUser_Enter)
        self.txtPassword.bind("<Key>", self.txtPassword_Enter)
#Event of Main Form
    def btnConnect_Click(self):
        try:
            if(self.varHostName.get()==""):
                raise Exception("Enter Host Name")
            if (self.varUser.get() == ""):
                raise Exception("Enter User")
            if (self.varPassword.get() == ""):
                raise Exception("Enter Password")
            GlobalClass.createConnection(self.varHostName.get(),self.varUser.get(),self.varPassword.get())
            # tkinter.messagebox.showinfo("Info", "Sucess")
            newRoot=Tk()
            newRoot.state("z")
            newRoot.iconbitmap("database2.ico")
            frmQuery=DatabaseExplorer(newRoot)
            root.destroy()
        except Exception as ex:
            tkinter.messagebox.showerror("Error",ex)
    def txtHostName_Enter(self,e):
        if(e.keycode==13):
            self.txtUser.focus()
    def txtUser_Enter(self,e):
        if(e.keycode==13):
            self.txtPassword.focus()
    def txtPassword_Enter(self,e):
        if(e.keycode==13):
            self.btnConnect_Click()
class DatabaseExplorer(Frame):
    refDatabaseExplorer=None
    refMaster=None
    selected_DataBase=None
    selected_Table=None

    def __init__(self, master=None):
        super().__init__(master)
        master.title("DataBase Explorer")
        self.pack(side=LEFT,fill=Y)

        DatabaseExplorer.refDatabaseExplorer=self
        DatabaseExplorer.refMaster=master
        self.createWidget()

    # Method of Database Explorer
    def createWidget(self):
        self.createDatabaseMenu = Menu(self)
        self.createDatabaseMenu.add_command(label="Create New Database", command=self.createDatabaseMenu_Click)
        self.createTableMenu = Menu(self)
        self.createTableMenu.add_command(label="Create New Table", command=self.createTableMenu_Click)

        self.deleteDatabaseMenu = Menu(self)
        self.deleteDatabaseMenu.add_command(label="Delete Database", command=self.deleteDatabaseMenu_Click)
        self.deleteTableMenu = Menu(self)
        self.deleteTableMenu.add_command(label="Open Table", command=self.openTableMenu_Click)
        self.deleteTableMenu.add_command(label="Detete Table", command=self.deleteTableMenu_Click)

        self.treeDataBase = tkinter.ttk.Treeview(self)
        self.treeDataBase.pack(side="left", fill=Y)
        self.treeDataBase.bind("<Button-3>", self.treeDataBase_Button_3)
        self.treeDataBase.bind("<<TreeviewSelect>>", self.treeDataBase_TreeviewSelect)
        self.createDataBaseTree()
        self.topFrame=Frame(self)
        self.topFrame.pack(fill=X)
        self.msg=Label(self.topFrame,text="Selected Database: ")
        self.msg.pack(side='left')
        self.varSelectedDatabase=StringVar()

        self.txtSelectedDatabase=Label(self.topFrame,text="Not Selected")
        self.varSelectedDatabase.set("Not Selected")
        self.txtSelectedDatabase.pack(side='left')
        self.btnExecute = Button(self.topFrame, text="Execute", command=self.btnExecute_Click, padx=10)
        self.btnExecute.pack(side="right")

        self.queryFrame = LabelFrame(self,text="Write query to execute")
        self.queryFrame.pack(fill="both",expand=True)
        self.txtQuery=Text(self.queryFrame,height=10)
        self.txtQuery.pack(fill=X)
        # self.executeFrame=Frame(self,)
        # self.executeFrame.pack()

        self.resultFrame = Frame(self)
        self.resultFrame.pack(fill=X)
    def btnExecute_Click(self):
        try:
            strQuery=self.txtQuery.get(1.0,END)
            for element in self.resultFrame.grid_slaves():
                element.destroy()

            GlobalClass.executeCustomQuery(strQuery,self.resultFrame)
        except Exception as ex:
            tkinter.messagebox.showerror("Exception", ex, parent=DatabaseExplorer.refMaster)




    def deleteAllElementTree(self):
        for i in self.treeDataBase.get_children():
            self.treeDataBase.delete(i)

    def createDataBaseTree(self):
        self.deleteAllElementTree()
        self.treeDataBase.insert("", 0, 'localhost', text="Localhost")
        self.treeDataBase.insert('localhost', 0, 'databases', text="Databases")
        myCursorDB = GlobalClass.connection.cursor()
        strDatabase = "show databases"
        countDataBase = myCursorDB.execute(strDatabase)
        if (countDataBase != 0):
            dbcount = 0
            for row in myCursorDB.fetchall():
                self.treeDataBase.insert('databases', dbcount, 'databases_'+row[0], text=row[0])
                self.treeDataBase.insert('databases_'+row[0], 0, 'tables' + "_" + row[0], text="Tables")
                dbcount += 1
                myCursorTab = GlobalClass.connection.cursor()
                strUseDataBase = "use " + row[0]
                myCursorTab.execute(strUseDataBase)
                strTables = "show tables"
                countTable = myCursorTab.execute(strTables)
                if (countTable != 0):
                    tableCount = 0
                    for rowTable in myCursorTab.fetchall():
                        self.treeDataBase.insert('tables' + "_" + row[0], tableCount, row[0] + "_" + rowTable[0],
                                                 text=rowTable[0])
                        tableCount += 1

    #Event of Database Explorer
    def createDatabaseMenu_Click(self):
        top=Tk()
        CreateDataBase(top)
    def createTableMenu_Click(self):
        top = Tk()
        CreateTable(top)
    def deleteDatabaseMenu_Click(self):
        CreateDataBase.deleteDataBase(DatabaseExplorer.selected_DataBase)
    def deleteTableMenu_Click(self):
        CreateTable.deleteTable()
    def openTableMenu_Click(self):
        frmOpenTable=Tk()
        ShowTables(frmOpenTable,DatabaseExplorer.selected_DataBase,DatabaseExplorer.selected_Table)

    def treeDataBase_TreeviewSelect(self,event):
            # print(self.treeDataBase.selection())
            if (self.treeDataBase.selection()[0].find("databases_") != -1):
                strdb = str(self.treeDataBase.selection()[0]).replace("databases_", "")
                if (strdb != "localhost" and strdb != ""):
                    DatabaseExplorer.selected_DataBase = str(self.treeDataBase.selection()[0]).replace("databases_", "")
                    DatabaseExplorer.refDatabaseExplorer.txtSelectedDatabase[
                        "text"] = DatabaseExplorer.selected_DataBase

    def treeDataBase_Button_3(self, event):
        iid = self.treeDataBase.identify_row(event.y)
        if iid:
            # mouse pointer over item

            # print(self.treeDataBase.parent(iid))
            self.treeDataBase.selection_set(iid)
            # print(self.treeDataBase.selection())
            if (self.treeDataBase.selection()[0].find("databases_") != -1):
                strdb=str(self.treeDataBase.selection()[0]).replace("databases_", "")
                if(strdb!="localhost" and strdb!=""):
                    DatabaseExplorer.selected_DataBase=str(self.treeDataBase.selection()[0]).replace("databases_", "")
                    DatabaseExplorer.refDatabaseExplorer.txtSelectedDatabase["text"]=DatabaseExplorer.selected_DataBase
                    self.deleteDatabaseMenu.post(event.x_root, event.y_root)
            else:
                strdb = str(self.treeDataBase.parent(iid)).replace("databases_", "").replace("tables_", "")
                if (strdb != "localhost" and strdb != ""):
                    DatabaseExplorer.selected_DataBase= str(self.treeDataBase.parent(iid)).replace("databases_", "").replace("tables_", "")
                    DatabaseExplorer.refDatabaseExplorer.txtSelectedDatabase["text"] = DatabaseExplorer.selected_DataBase

            if(self.treeDataBase.selection()[0]=="databases"):
                self.createDatabaseMenu.post(event.x_root, event.y_root)
            elif (self.treeDataBase.selection()[0].find("tables") !=-1 ):
                self.createTableMenu.post(event.x_root, event.y_root)
            elif (self.treeDataBase.selection()[0].find("databases_") != -1):
                pass
            elif (self.treeDataBase.selection()[0].find(DatabaseExplorer.selected_DataBase+"_") != -1):
                DatabaseExplorer.selected_Table = str(self.treeDataBase.selection()[0]).replace(DatabaseExplorer.selected_DataBase+"_", "")
                self.deleteTableMenu.post(event.x_root, event.y_root)


class CreateDataBase(Frame):
    refCreateDataBase=None
    refCreateDataBaseMaster=None
    def __init__(self, master=None):
        super().__init__(master)
        CreateDataBase.refCreateDataBaseMaster=master
        master.title("Create Database")
        # master.minsize(300,100)
        self.pack()
        self.createWidget()
        CreateDataBase.refCreateDataBase=self

    def createWidget(self):
        self.lblDatabase=Label(self,text="Database Name")
        self.lblDatabase.grid(row=0,column=0)
        self.varDatabase=StringVar()
        self.txtDatabase=Entry(self,textvariable=self.varDatabase)
        self.txtDatabase.grid(row=0, column=1)
        self.btnDatabase = Button(self, text="Create Database",command=self.btnDatabase_Click)
        self.btnDatabase.grid(row=0, column=2)
    def btnDatabase_Click(self):
        try:
            if (self.varDatabase.get()==""):
                raise Exception("Enter Database Name")
            myCursor=GlobalClass.connection.cursor()
            strCreateDatabaseQuery="create database "+self.varDatabase.get()
            rowAffected=myCursor.execute(strCreateDatabaseQuery)
            GlobalClass.connection.commit()
            tkinter.messagebox.showinfo("Sucess", "Database Created Sucessfully",parent=DatabaseExplorer.refMaster)
            DatabaseExplorer.refDatabaseExplorer.createDataBaseTree()
            CreateDataBase.refCreateDataBaseMaster.destroy()


        except Exception as ex:
            tkinter.messagebox.showerror("Exception",ex,parent=DatabaseExplorer.refMaster)

    @staticmethod
    def deleteDataBase(strDatabaseName):
        if(tkinter.messagebox.askyesno("Warning","Do you want to delete "+DatabaseExplorer.selected_DataBase+" Database",parent=DatabaseExplorer.refMaster)):
            try:
                myCursor=GlobalClass.connection.cursor()
                strCreateDatabaseQuery="drop database "+strDatabaseName
                myCursor.execute(strCreateDatabaseQuery)
                GlobalClass.connection.commit()
                tkinter.messagebox.showinfo("Sucess", "Database Deleted Sucessfully",parent=DatabaseExplorer.refMaster)
                DatabaseExplorer.refDatabaseExplorer.createDataBaseTree()
            except Exception as ex:
                tkinter.messagebox.showerror("Exception",ex,parent=DatabaseExplorer.refMaster)
class CreateTable(Frame):
    refCreateTable = None
    refCreateTableMaster=None
    def __init__(self, master=None):
        super().__init__(master)
        master.title("Create Table")
        CreateTable.refCreateTableMaster=master
        self.pack(side='top',fill=BOTH,expand=True)

        self.createWidget()
        CreateTable.refCreateTable = self

    def createWidget(self):
        self.lblDatabase = Label(self, text="Database Name")
        self.lblDatabase.grid(row=0, column=0)
        self.varDatabase = StringVar()
        self.txtDatabase = Entry(self, textvariable=self.varDatabase,state=DISABLED,width=15)
        self.varDatabase.set(DatabaseExplorer.selected_DataBase)
        self.txtDatabase.grid(row=0, column=1)

        self.lblTable = Label(self, text="Table Name")
        self.lblTable.grid(row=1, column=0)
        self.varTable = StringVar()
        self.txtTable = Entry(self, textvariable=self.varTable,width=15)
        self.txtTable.grid(row=1, column=1)

        self.lblColumn = Label(self, text="Column Name")
        self.lblColumn.grid(row=2, column=0)
        self.varColumn = StringVar()
        self.txtColumn = Entry(self, textvariable=self.varColumn,width=15)
        self.txtColumn.grid(row=2, column=1)

        self.lstDataType=["int","varchar"]
        self.lstDefaultSize = [11, 250]
        self.lblDataType = Label(self, text="DataType")
        self.lblDataType.grid(row=2, column=2)
        self.cmbDataType = tkinter.ttk.Combobox(self,width=5)
        self.cmbDataType.grid(row=2, column=3)
        self.cmbDataType["values"]=self.lstDataType
        self.cmbDataType.bind("<<ComboboxSelected>>",self.cmbDataType_Selected)

        self.lblSize = Label(self, text="Size")
        self.lblSize.grid(row=2, column=4)
        self.varsize = IntVar()
        self.txtsize = Entry(self, textvariable=self.varsize,width=4)
        self.txtsize.grid(row=2, column=5)

        self.cmbDataType.set("int")
        self.varsize.set(11)

        self.varAllowNull=IntVar()
        self.chkAllowNull = Checkbutton(self, text="Allow Null",variable=self.varAllowNull)
        self.varAllowNull.set(1)
        self.chkAllowNull.grid(row=2, column=6)

        self.varKey = IntVar()

        self.radPrimaryKey = Radiobutton(self, text="Primary Key", variable=self.varKey, value=1,command=self.radKey_Select)
        self.radPrimaryKey.grid(row=2, column=7)

        self.radUniqueKey=Radiobutton(self,text="Unique Key",variable=self.varKey,value=2,command=self.radKey_Select)
        self.radUniqueKey.grid(row=2,column=8)

        self.radNoKey = Radiobutton(self, text="No Key", variable=self.varKey, value=3,command=self.radKey_Select)
        self.radNoKey.grid(row=2, column=9)
        self.varKey.set(3)
        self.columnNo=0
        self.btnAddColumn = Button(self, text="Add Column", command=self.btnAddColumn_Click)
        self.btnAddColumn.grid(row=2, column=10)

        self.frameColumnDetails=LabelFrame(self,text="Column Details:")
        self.frameColumnDetails.grid(row=3,column=0,columnspan=11)
        self.lstColumnHeader=["Sn","Name","Type","Size","Null","Key","Default","Extra"]#,"Remove"]
        rHeader=0
        cHeader=0
        for header in self.lstColumnHeader:
            Label(self.frameColumnDetails,text=header,width=12).grid(row=rHeader,column=cHeader)
            cHeader+=1

    def radKey_Select(self):
        if(self.varKey.get()==1):
                self.varAllowNull.set(0)
                self.chkAllowNull["state"]=DISABLED
        else:
            self.chkAllowNull["state"] =NORMAL

    def createQueryForColumn(self):
        strMidQuery=""
        rowNo=1
        while(rowNo<=self.columnNo):
            for element in self.lstColumnHeader:
                if (element == "Name"):
                   strMidQuery+= self.frameColumnDetails.grid_slaves(row=rowNo ,column=1)[0]["text"]+" "
                if (element == "Type"):
                    strMidQuery += self.frameColumnDetails.grid_slaves(row=rowNo, column=2)[0]["text"] + "("+str(self.frameColumnDetails.grid_slaves(row=rowNo, column=3)[0]["text"]) + ") "
                if (element == "Key"):
                    key = "No"
                    if (self.frameColumnDetails.grid_slaves(row=rowNo, column=5)[0]["text"] == "Primary Key"):
                        key = "PRIMARY KEY "
                    elif (self.frameColumnDetails.grid_slaves(row=rowNo, column=5)[0]["text"] == "Unique Key"):
                        key = "UNIQUE"
                        if(self.frameColumnDetails.grid_slaves(row=rowNo, column=4)[0]["text"]==0):
                            key = "NOT NULL UNIQUE "
                    else:
                        key = ""
                        if (self.frameColumnDetails.grid_slaves(row=rowNo, column=4)[0]["text"] == 0):
                            key = "NOT NULL "
                    strMidQuery += key
                # else:
                #     if (self.frameColumnDetails.grid_slaves(row=rowNo, column=4)[0]["text"] == "0"):
                #         strMidQuery += "NOT NULL "

            if(rowNo!=self.columnNo):
                strMidQuery+=", "
            rowNo += 1
        return strMidQuery
    def createTableQuery(self):
        try:
            if(self.varTable.get()==""):
                raise Exception("Enter Table Name")
            if(self.varColumn.get()==""):
                raise Exception("Enter Column Name")
            strQueryStart = "create table "+self.varTable.get()+"("
            strQueryMid = ""
            strQueryEnd = ")"
            strQueryMid=self.createQueryForColumn()
            return strQueryStart + strQueryMid + strQueryEnd
        except Exception as ex:
            tkinter.messagebox.showerror("Error",ex,parent=DatabaseExplorer.refMaster)


    def checkColumnName(self):
        rowNo = 1
        while (rowNo <= self.columnNo):
            if(self.frameColumnDetails.grid_slaves(row=rowNo, column=1)[0]["text"]==self.varColumn.get()):
                raise Exception("Column Name already Exists")
            rowNo+=1

    def checkPrimaryKey(self):
        rowNo = 1
        while (rowNo <= self.columnNo):
            if (self.frameColumnDetails.grid_slaves(row=rowNo, column=5)[0]["text"] == "Primary Key"):
                raise Exception("Only One Primary Key Allowed")
            rowNo += 1

    def btnAddColumn_Click(self):

        try:
            self.checkColumnName()

            if(self.varTable.get()==""):
                raise Exception("Enter Table Name")
            if(self.varColumn.get()==""):
                raise Exception("Enter Column Name")

            for element in self.lstColumnHeader:
                if (self.varKey.get() == 1):
                    self.checkPrimaryKey()
                    # key = "Primary Key"
                if(element=="Sn"):
                    Label(self.frameColumnDetails,text=self.columnNo+1).grid(row=self.columnNo+1,column=0)
                elif(element=="Name"):
                    Label(self.frameColumnDetails, text=self.varColumn.get()).grid(row=self.columnNo+1, column=1)
                elif (element == "Type"):
                    Label(self.frameColumnDetails, text=self.cmbDataType.get()).grid(row=self.columnNo+1, column=2)
                elif (element == "Size"):
                    Label(self.frameColumnDetails, text=self.varsize.get()).grid(row=self.columnNo+1, column=3)
                elif (element == "Null"):
                    Label(self.frameColumnDetails, text=self.varAllowNull.get()).grid(row=self.columnNo+1, column=4)
                elif (element == "Key"):
                    key="No"
                    if(self.varKey.get()==1):
                        # self.checkPrimaryKey()
                        key="Primary Key"
                    elif(self.varKey.get()==2):
                        key="Unique Key"
                    elif (self.varKey.get() == 3):
                        key = "No Key"
                    Label(self.frameColumnDetails, text=key).grid(row=self.columnNo+1, column=5)
                elif (element == "Default"):
                    Label(self.frameColumnDetails, text="No Default").grid(row=self.columnNo+1, column=6)
                elif (element == "Extra"):
                    Label(self.frameColumnDetails, text="No Extra").grid(row=self.columnNo+1, column=7)
                # elif (element == "Remove"):
                #     btnRemove=Button(self.frameColumnDetails, text="Remove")
                #     btnRemove.bind("<Button-1>",self.btnRemove_Click)
                #     btnRemove.rowNo=self.columnNo
                #     btnRemove.grid(row=self.columnNo+1, column=8)
            self.columnNo += 1
            if(self.columnNo==1):
                self.btnCreateTable = Button(self, text="CreateTable",command=self.btnCreateTable_Click)
                self.btnCreateTable.grid(row=4, column=0)
                self.lblQuery = Label(self,text=self.createTableQuery())
                self.lblQuery.grid(row=4, column=1,columnspan=7)
            else:
                self.lblQuery["text"]=self.createTableQuery();


        except Exception as ex:
            tkinter.messagebox.showerror("Error",ex,parent=DatabaseExplorer.refMaster)

    @staticmethod
    def deleteTable():
        if (tkinter.messagebox.askyesno("Warning",
                                        "Do you want to delete " + DatabaseExplorer.selected_Table + " Table",
                                        parent=DatabaseExplorer.refMaster)):
            try:
                myCursor = GlobalClass.connection.cursor()
                myCursor.execute("use "+DatabaseExplorer.selected_DataBase)
                strdroptableQuery = "drop table " + DatabaseExplorer.selected_Table
                myCursor.execute(strdroptableQuery)
                GlobalClass.connection.commit()

                tkinter.messagebox.showinfo("Sucess", "Table Deleted Sucessfully", parent=DatabaseExplorer.refMaster)
                DatabaseExplorer.refDatabaseExplorer.createDataBaseTree()
            except Exception as ex:
                tkinter.messagebox.showerror("Exception", ex,parent=DatabaseExplorer.refMaster)
    def btnCreateTable_Click(self):
        strResult=GlobalClass.executeDMLQuery(self.lblQuery["text"])
        tkinter.messagebox.showinfo("Info",strResult,parent=DatabaseExplorer.refMaster)
        CreateTable.refCreateTableMaster.destroy()
    def cmbDataType_Selected(self,event):
        self.varsize.set(self.lstDefaultSize[self.cmbDataType.current()])
    def btnRemove_Click(self,event):
        tkinter.messagebox.showinfo("Info",event.widget.rowNo,parent=DatabaseExplorer.refMaster)

class ShowTables(Frame):
    def __init__(self,master=None,dataBase="Na",table="Na"):
        super().__init__(master)
        self.pack()
        self.createWidget(dataBase,table)
    def createWidget(self,dataBase,table):
        myCursor = GlobalClass.connection.cursor()
        myCursor.execute("use " + DatabaseExplorer.selected_DataBase)
        myCursor.execute("select * from "+table)
        r = 0
        c = 0
        for rowHeader in myCursor.description:
            Label(self, text=rowHeader[0], relief=RIDGE).grid(row=r, column=c,sticky=W+E+N+S)
            c += 1
        r += 1
        for row in myCursor.fetchall():
            c = 0
            for cell in row:
                varEntry=StringVar()
                Entry(self, textvariable=varEntry, relief=RIDGE).grid(row=r, column=c,sticky=W+E+N+S )
                varEntry.set(cell)
                c += 1
            r+=1



root=Tk()
root.minsize(300,200)
# root.maxsize(400,400)
root.title("MySQL Server Management")
root.resizable(0,0)

frmMain=MainForm(root)
root.iconbitmap("database1.ico")
# frmCreateTable=CreateTable(root)
# frame=Frame()

root.mainloop()