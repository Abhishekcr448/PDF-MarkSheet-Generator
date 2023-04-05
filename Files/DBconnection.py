# Created by Abhishek.A.Khatri

import pymysql


class DBconnect:
    """
    This class is responsible to handle all the 
    communication with the mysql server
    """

    def __init__(self, Host, User, Password) -> None:
        """
        This initialiasation builds the connection 
        between the user and the mysql server
        """
        # __connectionInstance is the instance of the connection with the server
        self.__connectionInstance = pymysql.connect(host=Host,
                                                    user=User,
                                                    password=Password,
                                                    charset="utf8mb4",
                                                    autocommit=True,
                                                    cursorclass=pymysql.cursors.DictCursor)

        # __cursorInsatnce is the instance of it's cursor
        self.__cursorInsatnce = self.__connectionInstance.cursor()

    def getDB(self):
        """
        This function returns a list of all the names 
        of all the existing databases
        """
        # To call all the DB
        self.__cursorInsatnce.execute("SHOW DATABASES;")

        output = []

        # To create a list of all the DB
        for i in (self.__cursorInsatnce.fetchall()):
            for key, value in i.items():
                output.append(value)

        return output

    def getTables(self, DBname):
        """
        This function returns a list of all the names
        of the existing Paper Bundles which are tables
        of the given DB
        """
        # Setting the current working database
        self.__cursorInsatnce.execute("USE "+DBname+";")

        output = []

        # Getting the names of all the tables
        self.__cursorInsatnce.execute("SHOW TABLES;")
        for i in (self.__cursorInsatnce.fetchall()):
            for key, value in i.items():
                output.append(value)

        return output

    def insertValues(self, DBname, TableName, lowPRN, highPRN, totalMarks):
        """
        This function adds many new StudentIDs to the new Table
        """
        def refinePRN(prn):
            """
            A function returns two strings by dividing 
            the given StudenID at the last alphabet
            """
            l = len(prn) - 1

            # if cannot be divided then returs False
            if prn[l].isdigit() == False:
                return False, False

            # finding the last alphabet
            for i in range(1, l+1):
                if prn[l-i].isdigit() == False:
                    return prn[:l-i+1], prn[l-i+1:]

        # To check if the given StudenIDs are digits or not
        newhighPRN = refinePRN(
            highPRN) if highPRN.isdigit() == False else ("", highPRN)
        newlowPRN = refinePRN(
            lowPRN) if lowPRN.isdigit() == False else ("", lowPRN)

        # if the StudenID cannot be divided futher
        if newhighPRN[0] == False or newlowPRN[0] == False:
            raise Exception("No number present at the end of RollNo")

        # Initialy adding the total Marks value in the StudentID itself
        self.__cursorInsatnce.execute(
            "INSERT INTO "+DBname+"."+TableName+" (StudentID, Attendance, ExaminerMarks, ModeratorOneMarks, ModeratorTwoMarks, FinalMarks) VALUES ('TotalMarks:"+str(totalMarks)+"','-','-','-','-','-');")

        # Adding all the StudenIDs in the given Table
        diff = int(newhighPRN[1]) - int(newlowPRN[1]) + 1

        if diff <= 0:
            raise Exception("The order of numbers is in non-increasing order")

        for i in range(diff):
            self.__cursorInsatnce.execute(
                "INSERT INTO "+DBname+"."+TableName+" (StudentID, Attendance, ExaminerMarks, ModeratorOneMarks, ModeratorTwoMarks, FinalMarks) VALUES ('"+newlowPRN[0]+str(int(newlowPRN[1])+i)+"','P','-','-','-','-');")
        self.__connectionInstance.commit()

    def createTb(self, DBname, TableName, lowPRN, highPRN, totalMarks):
        """
        This funtion creates a new table into the given DB,
        to create a new bundle of papers
        """
        # To create new Table
        self.__cursorInsatnce.execute("USE "+DBname+";")
        self.__cursorInsatnce.execute(
            "CREATE TABLE "+TableName + "(UniqueID INT NOT NULL AUTO_INCREMENT, StudentID varchar(20) NOT NULL, Attendance varchar(10) NOT NULL, ExaminerMarks varchar(10) NOT NULL, ModeratorOneMarks varchar(10) NOT NULL, ModeratorTwoMarks varchar(10) NOT NULL, FinalMarks varchar(10) NOT NULL, PRIMARY KEY (UniqueID),UNIQUE INDEX StudentID_UNIQUE (StudentID ASC) VISIBLE);")

        # calling insertValues function to add all Student IDs
        self.insertValues(DBname, TableName, lowPRN, highPRN, totalMarks)

    def createDB(self, DBname, TableName, lowPRN, highPRN, totalMarks):
        """
        This funtion creates a new database to create
        a new set of bundles of papers and then redirects
        to function createTb to create a new bundle of papers
        """
        # To create new DB and a new Table
        self.__cursorInsatnce.execute("CREATE DATABASE "+DBname+";")
        self.createTb(DBname, TableName, lowPRN, highPRN, totalMarks)

    def StudentIDlist(self, DBname, TableName):
        """
        This function returns a list of StudentIDs
        """
        # To fetch all StudentIDs of the given table
        self.__cursorInsatnce.execute("USE "+DBname+";")
        self.__cursorInsatnce.execute(
            "SELECT StudentID FROM "+TableName+" WHERE UniqueID!=1;")

        # To create a list of all StudentIDs
        IDlist = []
        tempdict = self.__cursorInsatnce.fetchall()
        for i in tempdict:
            for j, rollNo in i.items():
                IDlist.append(rollNo)

        def sortingFunc():
            try:
                int(IDlist[0])
                IDlist.sort(key=lambda x: int(x))

            except Exception:

                numInd = len(IDlist[0])-1
                while numInd != 0:
                    if 48 <= ord(IDlist[0][numInd]) <= 57:
                        numInd -= 1
                    else:
                        break
                IDlist.sort(key=lambda x: int(x[numInd+1:]))

        sortingFunc()

        return IDlist

    def getData(self, DBname, TableName, StudentID, MarksType):
        """
        This function returns the data of the given
        column and row
        """
        # To fetch the data of the given StudentID and column name
        self.__cursorInsatnce.execute("USE "+DBname+";")
        self.__cursorInsatnce.execute(
            "SELECT "+MarksType+" FROM "+TableName + " WHERE StudentID='"+StudentID+"';")
        return self.__cursorInsatnce.fetchall()[0][str(MarksType)]

    def updateValues(self, DBname, TableName, StudentID, valuesList):
        """
        This function updates the given value in the given row
        of the given table
        """
        self.__cursorInsatnce.execute("USE "+DBname+";")
        self.__cursorInsatnce.execute(
            "SELECT UniqueID FROM "+TableName+" WHERE StudentID='"+StudentID+"';")
        uniqueID = self.__cursorInsatnce.fetchall()[0]["UniqueID"]

        # updating value using instance of __cursorInsatnce
        self.__cursorInsatnce.execute(
            "UPDATE "+TableName+" SET Attendance='"+valuesList[0]+"', ExaminerMarks='"+valuesList[1]+"', ModeratorOneMarks='"+valuesList[2]+"', ModeratorTwoMarks='"+valuesList[3]+"', FinalMarks='"+valuesList[4]+"' WHERE UniqueID = "+str(uniqueID)+";")

    def GetAllData(self, DBname, TableName):
        """
        This function returns all the Student Marks 
        data that is stored in the given table
        """
        self.__cursorInsatnce.execute("USE "+DBname+";")
        self.__cursorInsatnce.execute(
            "SELECT * FROM "+TableName+";")

        allData = []

        for row in self.__cursorInsatnce.fetchall():
            tempList = []
            tempList.append(row["StudentID"])
            tempList.append(row["Attendance"])
            tempList.append(row["ExaminerMarks"])
            tempList.append(row["ModeratorOneMarks"])
            tempList.append(row["ModeratorTwoMarks"])
            tempList.append(row["FinalMarks"])
            allData.append(tempList)

        return allData

    def DropDB(self, DBname):
        """
        This fucntion deletes the given database
        """
        self.__cursorInsatnce.execute("DROP DATABASE "+DBname+";")

    def DropTable(self, DBname, TbName):
        """
        This fucntion deletes the given database
        """
        self.__cursorInsatnce.execute("USE "+DBname+";")
        self.__cursorInsatnce.execute("DROP TABLE "+TbName+";")

    def DeleteRow(self, DBname, TbName, StudentID):
        """
        This function deletes the iven StudentId and it's details
        of the given Bundle
        """
        self.__cursorInsatnce.execute("USE "+DBname+";")
        self.__cursorInsatnce.execute(
            "DELETE FROM "+TbName+" WHERE StudentID='"+StudentID+"';")

    def getColumns(self, DBname, TbName):
        """
        This function returns names of columns of the given DB and Bundle name
        """
        # To fetch names of all the columns
        self.__cursorInsatnce.execute("USE "+DBname+";")
        self.__cursorInsatnce.execute("SHOW COLUMNS FROM "+TbName+";")
        colList = []
        for col in self.__cursorInsatnce.fetchall():
            colList.append(col["Field"])
        return colList

    def quitDB(self):
        """
        This function closes the connection with the mysql
        """
        # to close the connection with the server using instance of __connectionInstance
        self.__connectionInstance.close()


# Testing commands below, Please Ignore...

# t1 = DBconnect("localhost", "root", "abhishek")
# t1.DeleteRow("IT_2022", "B_1", "21b102")
# print(t1.getColumns("IT_2023","B_1"))
# t1.DropTable("a", "a1")
# print(t1.GetAllData("IT_2022", "B_2"))
# t1.updateValues("IT_2022", "B_1", "21b100", ["P", "33", "33", "24.561", "24.561"])
# print(t1.getData("IT_2022", "B_3", "21b100", "ExaminerMarks"))
# print(t1.StudentIDlist("IT_2022", "B_4"))
# t1.createTb("IT_2022", "B_1", "251B100", "251B110", 100)
# print(t1.getDB())
