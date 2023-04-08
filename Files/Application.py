# Created by Abhishek.A.Khatri

import sys
import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as TkFont
from Files.DBconnection import DBconnect
from abc import ABC, abstractmethod
from Files.CreatPDF import GeneratePDF
import threading


class GUIstructure(ABC, tk.Tk):
    """
    This Class is an abstract class that defines
    the structure of the GUI of the aaplication
    """

    @abstractmethod
    def __init__(self) -> None:
        ABC.__init__(self)
        tk.Tk.__init__(self)

        # Binding the "WM_DELETE_WINDOW" protocol to the window
        # to call the close_window function on clicking 'x' button
        self.protocol("WM_DELETE_WINDOW", self.close_window)

        # Defining initial size
        self.minsize(750, 450)
        self.maxsize(750, 450)

        # Setting Title
        self.title("PDF MarkSheet Generator")

        # Create the background image and info-button image
        self.background_image = tk.PhotoImage(file="resources/bg2.png")
        self.InfoImg = tk.PhotoImage(file="resources/infoIcon.png")

        # Setting basic text font size
        self.font1 = TkFont.Font(family="MS Serif", size=18)
        self.font2 = TkFont.Font(family="MS Serif", size=16)
        self.font3 = TkFont.Font(family="MS Serif", size=13)

        # Loading pre-defines server details
        self.HostList = []
        self.UserList = []

        # To get the list of previously used DB names and Tables
        f1 = open("resources/ServerAdd.txt", "r")
        for i in f1.readlines():
            templist = (i.replace("\n", "")).split(',')
            self.HostList.append(templist[0])
            self.UserList.append(templist[1])
        f1.close()

        # Seting DB instances
        self.totalMarks = 100
        self.passingMarks = 30
        self.table = ""
        self._UserInstance = "A temporary String for DB object"
        self.DBname = "A temporary String for DB name"
        self.TbName = "A temporary String for Table name"
        self.canvas5 = ""
        self.DBtext = ""
        self.Tbtext = ""
        self.totalMarkstext = ""
        self.passingMarkstext = ""

    def close_window(self):
        """
        A function that distroyes any running process before closing the window
        """
        # Terminate any background threads or processes
        # Destroy the tkinter window
        self.destroy()
        # Forcefully terminate the script
        sys.exit()


class StartUp(GUIstructure):
    """
    This class creates the first page 
    that requests the server details
    """

    def __init__(self) -> None:
        super().__init__()

        self.startup = tk.Frame(self)

        # Creating Page1 Canvas
        canvas0 = tk.Canvas(self.startup, width=750, height=450, bg="black")
        canvas0.pack(fill="both", expand=True)

        # Calling the background image
        canvas0.create_image(80, 386, image=self.background_image, anchor="nw")

        # Text, Entry and combobox to get the server details from user
        canvas0.create_text(360, 20, text="Enter the Sever details",
                            fill="white", font=self.font1)
        canvas0.create_text(250, 80, text="Host:",
                            fill="white", font=self.font1)
        canvas0.create_text(250, 140, text="User:",
                            fill="white", font=self.font1)
        canvas0.create_text(250, 200, text="Password:",
                            fill="white", font=self.font1)
        c0_1_var = tk.StringVar()
        HostEntry = ttk.Combobox(
            self.startup, textvariable=c0_1_var, values=self.HostList)
        canvas0.create_window(410, 80, window=HostEntry)
        c0_2_var = tk.StringVar()
        UserEntry = ttk.Combobox(
            self.startup, textvariable=c0_2_var, values=self.UserList)
        canvas0.create_window(410, 140, window=UserEntry)
        e0_1_var = tk.StringVar()
        PassEntry = tk.Entry(self.startup, textvariable=e0_1_var, show="*")
        canvas0.create_window(410, 200, window=PassEntry)

        def errorMSG():
            """
            This function creates a error msg when error in connecting to the database
            """
            messagebox.showerror("Error", "Incorrect Host , User or Password")

        def connectToDB():
            """
            Connecting to DB and 
            changing frame from StartUp to frame1
            """

            # To connect to the DB
            try:
                self._UserInstance = DBconnect(
                    HostEntry.get(), UserEntry.get(), PassEntry.get())

            except Exception as e:
                errorMSG()
                return

            # To extract all fields of the existing DB
            self.DBchoosen.config(values=self._UserInstance.getDB())

            # Saving the server details
            f1 = open("resources/ServerAdd.txt", "a")
            if HostEntry.get() not in self.HostList and UserEntry.get() not in self.UserList:
                f1.write(HostEntry.get()+","+UserEntry.get()+"\n")
            f1.close()

            # Clearing the entry field and combobox
            HostEntry.set("")
            UserEntry.set("")
            PassEntry.delete(0, tk.END)

            # To shift to feild and bundle selection page
            self.show_frame1()

        # Add a Next Button
        b0 = tk.Button(self.startup, text="Next", command=connectToDB)
        canvas0.create_window(360, 300, window=b0)

        def show_password():
            """
            This function shows/hides the contents of the PassEntry on the button click
            """
            if PassEntry.cget('show') == '':
                PassEntry.config(show="*")
            else:
                PassEntry.config(show="")

        # Button to show/hide password text
        self.eyeImg = tk.PhotoImage(file="resources/eye.png")
        showHideB1 = tk.Button(
            self.startup, image=self.eyeImg, command=show_password)
        canvas0.create_window(530, 200, window=showHideB1)

        # Info button
        infoBtn = tk.Button(self.startup, image=self.InfoImg,
                            command=lambda: messagebox.showinfo("Login", "Enter your mysql HostID, Username and Password"))
        canvas0.create_window(715, 30, window=infoBtn)

        # Show the first frame
        self.startup.pack()


class Page1(StartUp):
    """
    This class creates widgets to read the Feild and Table name
    """

    def __init__(self) -> None:
        super().__init__()

        self.frame1 = tk.Frame(self)

        # Creating Page1 Canvas
        canvas1 = tk.Canvas(self.frame1, width=750, height=450, bg="black")
        canvas1.pack(fill="both", expand=True)

        # Calling the background image
        canvas1.create_image(80, 386, image=self.background_image, anchor="nw")

        # Text and button for the first combobox
        canvas1.create_text(200, 80, text="Select Field",
                            fill="white", font=self.font1)
        b1 = tk.Button(self.frame1, text="New+", command=self.show_frame2)
        canvas1.create_window(380, 120, window=b1)

        # DB Combobox creation
        DBchoosen_var = tk.StringVar()
        self.DBchoosen = ttk.Combobox(
            self.frame1, width=27, textvariable=DBchoosen_var, state='readonly')
        canvas1.create_window(200, 120, window=self.DBchoosen)

        # Text and button for the second combobox
        canvas1.create_text(200, 170, text="Select Bundle",
                            fill="white", state='hidden', font=self.font1)
        b2 = tk.Button(self.frame1, text="New+", command=self.show_frame3)
        canvas1.create_window(380, 210, window=b2, state='hidden')

        # Table combobox creation
        TbChoosen_var = tk.StringVar()
        self.TbChoosen = ttk.Combobox(
            self.frame1, width=27, textvariable=TbChoosen_var)
        canvas1.create_window(200, 210, window=self.TbChoosen, state='hidden')

        def GotoEditing():
            """
            This function directs to the final editing frame
            """

            # check if the choosen field is a paper bundle
            if self._UserInstance.getColumns(self.DBname, self.TbName) != ['UniqueID', 'StudentID', 'Attendance', 'ExaminerMarks', 'ModeratorOneMarks', 'ModeratorTwoMarks', 'FinalMarks']:
                messagebox.showerror(
                    "Invalid Bundle", "The choosen bundle is not a Paper bundle")
                return

            # To add list of StudentID in the roll number Combobox
            tempList = self._UserInstance.StudentIDlist(
                self.DBname, self.TbName)
            self.RollNo.config(values=tempList)

            # to update the self variables 'DBname', 'TbName', 'totalMarks', 'passingMarks'
            self.DBname = self.DBchoosen.get()
            self.TbName = self.TbChoosen.get()
            tempList = self._UserInstance.getTotalAndPassingMarks(self.DBname, self.TbName)
            self.totalMarks, self.passingMarks = tempList[0], tempList[1]

            # Adding DB name and Bundle name to the preview on frame5
            self.canvas5.itemconfig(self.DBtext, text=self.DBname)
            self.canvas5.itemconfig(self.Tbtext, text=self.TbName)
            self.canvas5.itemconfig(
                self.totalMarkstext, text="Total Marks: "+str(self.totalMarks))
            self.canvas5.itemconfig(
                self.passingMarkstext, text="Passing Marks: "+str(self.passingMarks))

            # To go to frame4
            self.show_frame4()

        # Saving the details and forwarding to entry frame
        b5 = tk.Button(self.frame1, text="Edit", command=GotoEditing)
        canvas1.create_window(270, 300, window=b5, state='hidden')

        def EditButton(event):
            """
            This function makes the Edit button visible 
            and redirects it to the Entry frame
            """

            # Checking if Bundle choosen is not empty
            if self.TbChoosen.get() != "":
                canvas1.itemconfig(8, state='normal')
                canvas1.itemconfig(10, state='normal')
                self.TbName = self.TbChoosen.get()
            else:
                # Until empty, set TbName to empty string
                canvas1.itemconfig(8, state='hidden')
                canvas1.itemconfig(10, state='hidden')
                self.TbName = ""

        def DBtables(event):
            """
            This function makes the second combobox visible after
            a value is selected in the first one, with a list of 
            tables present in that BD
            """

            if self.DBchoosen.get() != "":
                # Getting names of the tables existing in the given DB
                self.DBname = self.DBchoosen.get()
                self.TbChoosen['values'] = self._UserInstance.getTables(
                    self.DBname)
                self.TbChoosen.set('')
                self.TbChoosen['state'] = 'readonly'

                # Making those hidden widgets visible
                canvas1.itemconfig(5, state='normal')
                canvas1.itemconfig(6, state='normal')
                canvas1.itemconfig(7, state='normal')
                canvas1.itemconfig(9, state='normal')

            else:
                self.DBname = ""

                # Making those visible widgets hidden
                canvas1.itemconfig(5, state='hidden')
                canvas1.itemconfig(6, state='hidden')
                canvas1.itemconfig(7, state='hidden')
                canvas1.itemconfig(9, state='hidden')

            # Calling the function EditButton when a value of self.TbChoosen is selected
            self.TbChoosen.bind("<<ComboboxSelected>>", EditButton)

        # Calling the function DBtables when a value of DBchoosen is selected
        self.DBchoosen.bind("<<ComboboxSelected>>", DBtables)

        def DeleteDB():
            """
            This function calls the drop command in DBconnections
            """
            # Warning message before deleting
            tempmsg = messagebox.askyesno(
                "Delete Feild", "Deleting the choosen Feild, do you want to proceed")

            # Droping the schemas and setting DBchoosen and TbChoosen to empty
            if tempmsg == True:
                self._UserInstance.DropDB(self.DBchoosen.get())

                # To clear the combobox DBchoosen
                self.DBchoosen.set('')
                self.TbChoosen.set('')

                # To extract all fields of the existing DB again
                self.DBchoosen.config(values=self._UserInstance.getDB())

                # Making all other visible widgets hidden
                canvas1.itemconfig(5, state='hidden')
                canvas1.itemconfig(6, state='hidden')
                canvas1.itemconfig(7, state='hidden')
                canvas1.itemconfig(9, state='hidden')
                canvas1.itemconfig(8, state='hidden')
                canvas1.itemconfig(10, state='hidden')
            else:
                return

        def DeleteTable():
            """
            This function calls the drop command in DBconnections
            """
            # Warning message before deleting
            tempmsg = messagebox.askyesno(
                "Delete Table", "Deleting the choosen Table, do you want to proceed")

            # Droping the schemas and setting DBchoosen and TbChoosen to empty
            if tempmsg == True:
                self._UserInstance.DropTable(
                    self.DBchoosen.get(), self.TbChoosen.get())

                # To clear the combobox DBchoosen
                self.TbChoosen.set('')

                # To extract all fields of the existing DB again
                self.TbChoosen.config(
                    values=self._UserInstance.getTables(self.DBname))

                # Making all other visible widgets hidden
                canvas1.itemconfig(8, state='hidden')
                canvas1.itemconfig(10, state='hidden')

        # Delete Buttons
        b3 = tk.Button(self.frame1, text="Delete", command=DeleteDB)
        canvas1.create_window(480, 120, window=b3, state='hidden')
        b4 = tk.Button(self.frame1, text="Delete", command=DeleteTable)
        canvas1.create_window(480, 210, window=b4, state='hidden')

        def Logout():
            """
            This fuction calls on logoutButton,
            and discoonects with the connected database
            """
            # Disconnecting to the DB
            self._UserInstance.quitDB()

            # Returning back to startUp page
            self.show_startup()

        # Logout Button
        LogoutButton = tk.Button(self.frame1, text="Logout", command=Logout)
        canvas1.create_window(60, 30, window=LogoutButton)

        # Info button
        infoBtn = tk.Button(self.frame1, image=self.InfoImg,
                            command=lambda: messagebox.showinfo("Select your Paper Bundle", "These are the schemas and tables of your mysql.\nSelect your paper bundle or create one by clicking on 'New+' button"))
        canvas1.create_window(715, 30, window=infoBtn)


class Page2(Page1):
    """
    This class creates widgets to take inputs as Feild name, Bundle name, StudentId range, Total marks and Passing marks
    to create a new Feild using the instance of DBconnect named as self.UserInstance
    """

    def __init__(self) -> None:
        super().__init__()

        self.frame2 = tk.Frame(self)

        # Creating Page1 Canvas
        canvas2 = tk.Canvas(self.frame2, width=750, height=450, bg="black")
        canvas2.pack(fill="both", expand=True)

        # Calling the background image
        canvas2.create_image(80, 386, image=self.background_image, anchor="nw")

        # Adding the Back Button
        back2 = tk.Button(self.frame2, text="Back", command=self.show_frame1)
        canvas2.create_window(40, 30, window=back2)

        # Adding the Field Entry
        canvas2.create_text(200, 80, text="Enter Field Name",
                            fill="white", font=self.font1)
        e2_1_var = tk.StringVar()
        FieldEntry = tk.Entry(self.frame2, textvariable=e2_1_var)
        canvas2.create_window(200, 120, window=FieldEntry)

        # Adding the Bundle entry
        canvas2.create_text(
            200, 170, text="Enter Bundle Name", fill="white", font=self.font1)
        e2_2_var = tk.StringVar()
        BundleEntry = tk.Entry(self.frame2, textvariable=e2_2_var)
        canvas2.create_window(200, 210, window=BundleEntry)

        # Adding the StudentID range Entry
        canvas2.create_text(
            520, 80, text="Add StudentID range", fill="white", font=self.font1)
        canvas2.create_text(420, 130, text="From",
                            fill="white", font=self.font1)
        canvas2.create_text(420, 180, text="To", fill="white", font=self.font1)
        e2_3_var = tk.StringVar()
        RollStart = tk.Entry(self.frame2, textvariable=e2_3_var)
        canvas2.create_window(560, 130, window=RollStart)
        e2_4_var = tk.StringVar()
        RollEnd = tk.Entry(self.frame2, textvariable=e2_4_var)
        canvas2.create_window(560, 180, window=RollEnd)

        # Entry to get the total marks
        canvas2.create_text(
            470, 260, text="Total Marks:", fill="white", font=self.font1)
        e2_5_var = tk.StringVar()
        TotalMarksEntry = tk.Entry(self.frame2, textvariable=e2_5_var, width=4)
        TotalMarksEntry.insert(0, "100")
        canvas2.create_window(580, 260, window=TotalMarksEntry)

        # Entry to get the Passing marks
        canvas2.create_text(
            455, 290, text="Passing Marks:", fill="white", font=self.font1)
        e2_6_var = tk.StringVar()
        PassingMarksEntry = tk.Entry(
            self.frame2, textvariable=e2_6_var, width=4)
        PassingMarksEntry.insert(0, "30")
        canvas2.create_window(580, 290, window=PassingMarksEntry)

        def NoNumErrorMSG(e):
            """
            This function creates a error msg
            """
            messagebox.showerror("Error", e)

        def createnewField():
            """
            This fuction creates a new DB and a new table
            of given values and redirects to frame4
            """
            # To check if any entry is left empty
            if FieldEntry.get() == "" or BundleEntry.get() == "" or RollStart.get() == "" or RollEnd.get() == "" or TotalMarksEntry.get() == "" or PassingMarksEntry.get() == "":
                NoNumErrorMSG("Some Feilds are empty")
                return

            # To check if Field or Bundle names are not mysql keywords
            if FieldEntry.get() == "as" or BundleEntry.get() == "as":
                NoNumErrorMSG("Feild or Table name cannot be 'as'")
                return

            # To check if Fieldname and Bundle Name is not same
            if FieldEntry.get() == BundleEntry.get():
                NoNumErrorMSG("Field name and Bundle name cannot be same")
                return

            # To check if total and passing marks are numerical values
            try:
                self.totalMarks = float(TotalMarksEntry.get())
                self.passingMarks = float(PassingMarksEntry.get())
            except Exception as e:
                NoNumErrorMSG(
                    "Total marks should be a integer of decimal value")
                return

            # Passing Marks cannot be greater than Total Marks
            if float(TotalMarksEntry.get()) < float(PassingMarksEntry.get()):
                NoNumErrorMSG(
                    "Passing Marks cannot be greater than Total Marks")
                return

            # To Create a new Bundle
            try:
                def start_work():
                    self.frame2.config(cursor="watch")
                    t = threading.Thread(target=do_work)
                    t.start()

                def do_work():
                    self._UserInstance.createDB(FieldEntry.get(), BundleEntry.get(),
                                                RollStart.get(), RollEnd.get(), TotalMarksEntry.get(), PassingMarksEntry.get())
                    # Initialising DBname, TbName, totalMarks and passingMarks variables to store the data on this instance
                    self.DBname = FieldEntry.get()
                    self.TbName = BundleEntry.get()
                    self.totalMarks = float(TotalMarksEntry.get())
                    self.passingMarks = float(PassingMarksEntry.get())

                    # To add list of StudentID in the roll number Combobox
                    self.RollNo.config(values=self._UserInstance.StudentIDlist(
                        self.DBname, self.TbName))

                    # Adding DBname, TbName and totalMarks to the preview frame5
                    self.canvas5.itemconfig(self.DBtext, text=self.DBname)
                    self.canvas5.itemconfig(self.Tbtext, text=self.TbName)
                    self.canvas5.itemconfig(
                        self.totalMarkstext, text="Total Marks: "+str(self.totalMarks))
                    self.canvas5.itemconfig(
                        self.passingMarkstext, text="Passing Marks: "+str(self.passingMarks))

                    self.show_frame4()
                    self.frame2.after(0, lambda: self.frame2.config(cursor=""))

                start_work()

            except Exception as e:
                self.frame2.after(0, lambda: self.frame2.config(cursor=""))
                NoNumErrorMSG(e)
                return

        # Saving the details and forwarding to entry frame
        b2 = tk.Button(self.frame2, text="Next",
                       command=createnewField, padx=20, pady=5)
        canvas2.create_window(360, 340, window=b2)

        def goingBack():
            """
            This function is called by the back2 button.
            It clears all the entry boxes and goes to page1
            """
            # Clearing the entry fields before leaving this frame
            FieldEntry.delete(0, tk.END)
            BundleEntry.delete(0, tk.END)
            RollStart.delete(0, tk.END)
            RollEnd.delete(0, tk.END)
            TotalMarksEntry.delete(0, tk.END)
            self.show_frame1()

        # Adding the Back Button
        back2 = tk.Button(self.frame2, text="Back", command=goingBack)
        canvas2.create_window(40, 30, window=back2)

        # Info button
        infoBtn = tk.Button(self.frame2, image=self.InfoImg,
                            command=lambda: messagebox.showinfo("Create new Field", "Add the required details to create a new Field and Bundle."))
        canvas2.create_window(715, 30, window=infoBtn)


class Page3(Page2):
    """
    This class creates widgets to take inputs as Bundle name, StudentId range, Total marks and Passing marks
    to create a new Bundle using the instance of DBconnect named as self.UserInstance
    """

    def __init__(self) -> None:
        super().__init__()

        self.frame3 = tk.Frame(self)

        # Creating Page1 Canvas
        canvas3 = tk.Canvas(self.frame3, width=750, height=450, bg="black")
        canvas3.pack(fill="both", expand=True)

        # Calling the background image
        canvas3.create_image(80, 386, image=self.background_image, anchor="nw")

        def goingBack():
            """
            This function is called by the back2 button.
            It clears all the entry boxes and goes to page1
            """
            # Clearing the entry fields before leaving this frame
            BundleEntry.delete(0, tk.END)
            RollStart.delete(0, tk.END)
            RollEnd.delete(0, tk.END)
            TotalMarksEntry.delete(0, tk.END)
            self.show_frame1()

        # Adding the Back Button
        back3 = tk.Button(self.frame3, text="Back", command=goingBack)
        canvas3.create_window(40, 30, window=back3)

        # Adding the Bundle Entry
        canvas3.create_text(200, 80, text="Enter Bundle Name",
                            fill="white", font=self.font1)
        e3_1_var = tk.StringVar()
        BundleEntry = tk.Entry(self.frame3, textvariable=e3_1_var)
        canvas3.create_window(200, 120, window=BundleEntry)

        # Adding the StudentID range Entry
        canvas3.create_text(
            520, 80, text="Add StudentID range", fill="white", font=self.font1)
        canvas3.create_text(420, 130, text="From",
                            fill="white", font=self.font1)
        canvas3.create_text(420, 180, text="To", fill="white", font=self.font1)
        e3_2_var = tk.StringVar()
        RollStart = tk.Entry(self.frame3, textvariable=e3_2_var)
        canvas3.create_window(560, 130, window=RollStart)
        e3_3_var = tk.StringVar()
        RollEnd = tk.Entry(self.frame3, textvariable=e3_3_var)
        canvas3.create_window(560, 180, window=RollEnd)

        # Entry to get the total marks
        canvas3.create_text(
            470, 260, text="Total Marks:", fill="white", font=self.font1)
        e3_4_var = tk.StringVar()
        TotalMarksEntry = tk.Entry(self.frame3, textvariable=e3_4_var, width=4)
        TotalMarksEntry.insert(0, "100")
        canvas3.create_window(580, 260, window=TotalMarksEntry)

        # Entry to get the Passing marks
        canvas3.create_text(
            455, 290, text="Passing Marks:", fill="white", font=self.font1)
        e3_5_var = tk.StringVar()
        PassingMarksEntry = tk.Entry(
            self.frame3, textvariable=e3_5_var, width=4)
        PassingMarksEntry.insert(0, "30")
        canvas3.create_window(580, 290, window=PassingMarksEntry)

        def NoNumErrorMSG(e):
            """
            This function creates a error msg
            """
            messagebox.showerror("Error", e)

        def createnewTable():
            """
            This fuction creates a new Bundle of given values
            and redirects to frame4
            """

            # To check if any entry is left empty
            if BundleEntry.get() == "" or RollStart.get() == "" or RollEnd.get() == "" or TotalMarksEntry.get() == "" or PassingMarksEntry.get() == "":
                NoNumErrorMSG("Some Feilds are empty")
                return

            # To check if Field or Bundle names are not mysql keywords
            if BundleEntry.get() == "as":
                NoNumErrorMSG("Feild or Table name cannot be 'as'")
                return

            if BundleEntry.get()[0].isdigit() == True:
                NoNumErrorMSG("First letter cannot be numeric")
                return

            # To check if total and passing marks are numerical values
            try:
                self.totalMarks = float(TotalMarksEntry.get())
                self.passingMarks = float(PassingMarksEntry.get())
            except Exception as e:
                NoNumErrorMSG(
                    "Total marks should be a integer of decimal value")
                return

            # Passing Marks cannot be greater than Total Marks
            if float(TotalMarksEntry.get()) < float(PassingMarksEntry.get()):
                NoNumErrorMSG(
                    "Passing Marks cannot be greater than Total Marks")
                return

            # To Create a new Bundle
            try:
                def start_work():
                    self.frame3.config(cursor="watch")
                    t = threading.Thread(target=do_work)
                    t.start()

                def do_work():
                    self._UserInstance.createTb(self.DBname, BundleEntry.get(), RollStart.get(),
                                                RollEnd.get(), TotalMarksEntry.get(), PassingMarksEntry.get())
                    # Initialising TbName, totalMarks and passingMarks variables to store the data on this instance
                    self.TbName = BundleEntry.get()
                    self.totalMarks = TotalMarksEntry.get()
                    self.passingMarks = PassingMarksEntry.get()

                    # To add list of StudentID in the roll number Combobox
                    # Also ignoring the first value cause it's the Total Marks
                    self.RollNo.config(values=self._UserInstance.StudentIDlist(
                        self.DBname, self.TbName))

                    # Adding DBname, TbName and totalMarks to the preview frame5
                    self.canvas5.itemconfig(self.DBtext, text=self.DBname)
                    self.canvas5.itemconfig(self.Tbtext, text=self.TbName)
                    self.canvas5.itemconfig(
                        self.totalMarkstext, text="Total Marks: "+str(self.totalMarks))
                    self.canvas5.itemconfig(
                        self.passingMarkstext, text="Passing Marks: "+str(self.passingMarks))

                    self.show_frame4()
                    self.frame3.after(0, lambda: self.frame3.config(cursor=""))

                start_work()

            except Exception as e:
                self.frame3.after(0, lambda: self.frame3.config(cursor=""))
                NoNumErrorMSG(e)
                return

        # Saving the details and forwarding to entry frame
        b2 = tk.Button(self.frame3, text="Next",
                       command=createnewTable, padx=20, pady=5)
        canvas3.create_window(360, 340, window=b2)

        # Info button
        infoBtn = tk.Button(self.frame3, image=self.InfoImg,
                            command=lambda: messagebox.showinfo("Create new Bundle", "Add the required details to create a new Bundle."))
        canvas3.create_window(715, 30, window=infoBtn)


class Page4(Page3):
    """
    This class creates all the widgets required for the Page 4.
    This is the main page where all the data entry happens
    """

    def __init__(self) -> None:
        super().__init__()

        self.frame4 = tk.Frame(self)

        # Creating Page1 Canvas
        canvas4 = tk.Canvas(self.frame4, width=750, height=450, bg="black")
        canvas4.pack(fill="both", expand=True)

        # Calling the background image
        canvas4.create_image(80, 386, image=self.background_image, anchor="nw")

        # Text, Entry and combobox for adding details and marks
        canvas4.create_text(360, 20, text="Marks Entry",
                            fill="white", font=self.font1)
        canvas4.create_text(220, 65, text="Roll No:",
                            fill="white", font=self.font2)
        canvas4.create_text(196, 120, text="Attendance:",
                            fill="white", font=self.font2, state='hidden')
        canvas4.create_text(165, 180, text="Examiner Marks:",
                            fill="white", font=self.font2, state='hidden')
        canvas4.create_text(130, 240, text="Moderator 1 Marks:",
                            fill="white", font=self.font2, state='hidden')
        canvas4.create_text(130, 300, text="Moderator 2 Marks:",
                            fill="white", font=self.font2, state='hidden')

        StudentID, ExMarks, Mod1Marks, Mod2Marks, FinalMarks, ExaminerPercent, Mod1Percent = "-", "-", "-", "-", "-", "-", "-"

        def UpdateDatabase(StudentID, ExMarks, Mod1Marks, Mod2Marks, FinalMarks):
            """This function calls the updateValues function 
            of class DBconnect and updates the Entered value on runtime"""

            # To store all the values in one list to update it to DB
            DataList = []

            # Checking if the entry is empty before appending the value to the list
            DataList.append("P") if Attendance_var.get(
            ) == True else DataList.append("AB")
            DataList.append(
                "-") if ExMarks == 0 or ExaminerEntry.get() == "" else DataList.append(ExaminerEntry.get())
            DataList.append(
                "-") if Mod1Marks == 0 or ModOneEntry.get() == "" else DataList.append(ModOneEntry.get())
            DataList.append(
                "-") if Mod2Marks == 0 or ModTwoEntry.get() == "" else DataList.append(ModTwoEntry.get())
            DataList.append(
                "-") if FinalMarks == 0 else DataList.append(FinalMarks)

            # print(self.DBname, self.TbName, StudentID, DataList)

            # Will produce an error message if an error occured while updating the data to the DB
            try:
                self._UserInstance.updateValues(
                    self.DBname, self.TbName, StudentID, DataList)
                canvas4.itemconfig(16, text="Synced!", fill="green")
            except Exception:
                canvas4.itemconfig(16, text="Disconnected!", fill="red")

        def handleWidgets(ExMarks, Mod1Marks, Mod2Marks, FinalMarks, ExaminerPercent, Mod1Percent, StudentID):
            """
            This function is resposible for the initialisation 
            of the widgets in this final page
            """

            # To check if the student is present or not
            if Attendance_var.get() == False:
                canvas4.itemconfig(9, state='normal')
                canvas4.itemconfig(5, state='hidden')
                canvas4.itemconfig(6, state='hidden')
                canvas4.itemconfig(7, state='hidden')
                canvas4.itemconfig(10, state='hidden')
                canvas4.itemconfig(11, state='hidden')
                canvas4.itemconfig(12, state='hidden')
                canvas4.itemconfig(13, state='normal', text="Final Marks: AB")
                ExMarks, Mod1Marks, Mod2Marks, FinalMarks = 0, 0, 0, "AB"
                UpdateDatabase(StudentID, ExMarks, Mod1Marks,
                               Mod2Marks, FinalMarks)
            else:
                canvas4.itemconfig(5, state='normal')
                canvas4.itemconfig(4, state='normal')
                canvas4.itemconfig(9, state='normal')
                canvas4.itemconfig(10, state='normal')
                canvas4.itemconfig(13, state='hidden')

                # If there exsist no Examiner Marks, then it will ask to enter some marks
                if ExMarks == 0:
                    FinalMarks = 0
                    canvas4.itemconfig(6, state='hidden')
                    canvas4.itemconfig(11, state='hidden')
                    canvas4.itemconfig(7, state='hidden')
                    canvas4.itemconfig(12, state='hidden')
                    canvas4.itemconfig(
                        13, state='normal', text="Enter Examiner Marks")

                # If Examiner percent are between 75-100 or 30-40, then allowing moderator to add marks
                elif (ExaminerPercent >= 75 and ExaminerPercent <= 100) or (ExaminerPercent >= 30 and ExaminerPercent <= 40):
                    canvas4.itemconfig(6, state='normal')
                    canvas4.itemconfig(11, state='normal')

                    # If moderator 1 is null, then ask to enter moderator 1 marks
                    if Mod1Marks == 0:
                        FinalMarks = 0
                        canvas4.itemconfig(7, state='hidden')
                        canvas4.itemconfig(12, state='hidden')
                        canvas4.itemconfig(
                            13, state='normal', text="Enter Moderator One Marks")

                    # If diff bet'n mod1 and examiner is bet'n 0-5 then Final Marks = Examiner Marks
                    elif (abs(Mod1Percent-ExaminerPercent) >= 0 and abs(Mod1Percent-ExaminerPercent) < 5):
                        canvas4.itemconfig(7, state='hidden')
                        canvas4.itemconfig(12, state='hidden')
                        FinalMarks = ExMarks
                        canvas4.itemconfig(
                            13, state='normal', text="Final Marks: "+str(FinalMarks))
                        UpdateDatabase(StudentID, ExMarks,
                                       Mod1Marks, Mod2Marks, FinalMarks)

                    # If diff bet'n mod1 and examiner is bet'n 5-15 then Final Marks = Moderator 1 Marks
                    elif (abs(Mod1Percent-ExaminerPercent) >= 5 and abs(Mod1Percent-ExaminerPercent) < 15):
                        canvas4.itemconfig(7, state='hidden')
                        canvas4.itemconfig(12, state='hidden')
                        FinalMarks = Mod1Marks
                        canvas4.itemconfig(
                            13, state='normal', text="Final Marks: "+str(FinalMarks))
                        UpdateDatabase(StudentID, ExMarks,
                                       Mod1Marks, Mod2Marks, FinalMarks)

                    # If diff bet'n mod1 and examiner is bet'n 15-25 then Final Marks = average of Examiner Marks and Moderator1
                    elif (abs(Mod1Percent-ExaminerPercent) >= 15 and abs(Mod1Percent-ExaminerPercent) < 25):
                        canvas4.itemconfig(7, state='hidden')
                        canvas4.itemconfig(12, state='hidden')
                        FinalMarks = str((float(ExMarks) + float(Mod2Marks))/2)
                        canvas4.itemconfig(
                            13, state='normal', text="Final Marks: "+str(FinalMarks))
                        UpdateDatabase(StudentID, ExMarks,
                                       Mod1Marks, Mod2Marks, FinalMarks)

                    # If diff bet'n mod1 and examiner is bet'n 25-100 then Final Marks = Moderator 2 Marks
                    elif (abs(Mod1Percent-ExaminerPercent) >= 25 and abs(Mod1Percent-ExaminerPercent) <= 100):
                        canvas4.itemconfig(7, state='normal')
                        canvas4.itemconfig(12, state='normal')

                        # If moderator 2 is null, then ask to enter moderator 2 marks
                        if Mod2Marks == 0:
                            FinalMarks = 0
                            canvas4.itemconfig(
                                13, state='normal', text="Enter Moderator Two Marks")
                        else:
                            canvas4.itemconfig(
                                13, state='normal', text="Final Marks: "+Mod2Marks)
                            FinalMarks = Mod2Marks
                            UpdateDatabase(StudentID, ExMarks,
                                           Mod1Marks, Mod2Marks, FinalMarks)

                else:
                    # If Examiner Marks are in different ranges then, Final Marks = Examiner Marks
                    canvas4.itemconfig(6, state='hidden')
                    canvas4.itemconfig(7, state='hidden')
                    canvas4.itemconfig(11, state='hidden')
                    canvas4.itemconfig(12, state='hidden')
                    FinalMarks = ExMarks
                    canvas4.itemconfig(13, state='normal',
                                       text="Final Marks: "+str(FinalMarks))
                    UpdateDatabase(StudentID, ExMarks, Mod1Marks,
                                   Mod2Marks, FinalMarks)

        def validMarks(marks):
            """
            This function checks if the given input string could be considered as marks
            """
            # If there are more than 1 '.' in the number, then it's a invalid number
            if marks.count('.') > 1:
                return False

            # If a digit is not in the given string then it's not a number
            if any(c not in '0123456789.' for c in marks):
                return False

            try:
                # Finally checking if the number can be converted to float
                float(marks)
                return True
            except ValueError:
                return False

        def updateWidgetsData(*event):
            """This function is responsible to update the 
            data of the widgets given by the user"""

            # Updating variables according to the given input
            StudentID = self.RollNo.get()
            ExMarks = ExaminerEntry.get()
            Mod1Marks = ModOneEntry.get()
            Mod2Marks = ModTwoEntry.get()
            ExaminerPercent, Mod1Percent = 0, 0

            # If the new Examiner marks are not decimal number, then give error
            if (validMarks(ExMarks) != True and ExMarks != ""):
                messagebox.showwarning(
                    "Invalid Marks", "Only decimal values are allowed")
                ExaminerEntry.delete(len(ExaminerEntry.get()) - 1, tk.END)
                return

            # If the new Moderator 1 marks are not decimal number, then give error
            if (validMarks(Mod1Marks) != True and Mod1Marks != ""):
                messagebox.showwarning(
                    "Invalid Marks", "Only decimal values are allowed")
                ModOneEntry.delete(len(ModOneEntry.get()) - 1, tk.END)
                return

            # If the new Moderator 2 marks are not decimal number, then give error
            if (validMarks(Mod2Marks) != True and Mod2Marks != ""):
                messagebox.showwarning(
                    "Invalid Marks", "Only decimal values are allowed")
                ModTwoEntry.delete(len(ModTwoEntry.get()) - 1, tk.END)
                return

            # If Examiner Marks are greater than total marks, then give error
            if ExMarks != "" and float(ExMarks) > float(self.totalMarks):
                messagebox.showwarning(
                    "Invalid Marks", "Examiner Marks cannot be more than Total Marks")
                ExaminerEntry.delete(len(ExaminerEntry.get()) - 1, tk.END)
                return

            # If Moderator 1 Marks are greater than total marks, then give error
            if Mod1Marks != "" and float(Mod1Marks) > float(self.totalMarks):
                messagebox.showwarning(
                    "Invalid Marks", "Moderator 1 Marks cannot be more than Total Marks")
                ModOneEntry.delete(len(ModOneEntry.get()) - 1, tk.END)
                return

            # If Moderator 2 Marks are greater than total marks, then give error
            if Mod2Marks != "" and float(Mod2Marks) > float(self.totalMarks):
                messagebox.showwarning(
                    "Invalid Marks", "Moderator 2 Marks cannot be more than Total Marks")
                ModTwoEntry.delete(len(ModTwoEntry.get()) - 1, tk.END)
                return

            if ExMarks != "":
                # Finding the persentage from exminer marks
                ExaminerPercent = float(ExMarks)*100/float(self.totalMarks)
            else:
                # If Examiner Marks are null then, ExMarks is = 0
                ExMarks = 0

            if Mod1Marks != "":
                # Finding the persentage from Moderator 1 marks
                Mod1Percent = float(Mod1Marks)*100/float(self.totalMarks)
            else:
                # If Moderator 1 Marks are null then, Mod1Marks is = 0
                Mod1Marks = 0

            if Mod2Marks == "":
                # If Moderator 2 Marks are null then, Mod2Marks is = 0
                Mod2Marks = 0

            # To check the visibility of widgets according to the updated values
            handleWidgets(ExMarks, Mod1Marks, Mod2Marks,
                          FinalMarks, ExaminerPercent, Mod1Percent, StudentID)

        def InitialiseWidgetsData(event):
            """This function is responsible to get data of the student by 
            it's StudentID
            """

            # Updataing the variables from the stored DB
            StudentID = self.RollNo.get()
            canvas4.itemconfig(23, state='normal')
            Attendance_var.set(True) if self._UserInstance.getData(
                self.DBname, self.TbName, StudentID, "Attendance") == "P" else Attendance_var.set(False)
            ExMarks = self._UserInstance.getData(
                self.DBname, self.TbName, StudentID, "ExaminerMarks")
            Mod1Marks = self._UserInstance.getData(
                self.DBname, self.TbName, StudentID, "ModeratorOneMarks")
            Mod2Marks = self._UserInstance.getData(
                self.DBname, self.TbName, StudentID, "ModeratorTwoMarks")
            ExaminerPercent, Mod1Percent = 0, 0

            if ExMarks != "-":
                # To show the stored values on the Entry box
                ExaminerEntry.delete(0, tk.END)
                ExaminerEntry.insert(0, str(ExMarks))
                ExaminerPercent = float(ExMarks)*100/self.totalMarks
            else:
                ExMarks = 0
                ExaminerEntry.delete(0, tk.END)

            if Mod1Marks != "-":
                # To show the stored values on the Entry box
                ModOneEntry.delete(0, tk.END)
                ModOneEntry.insert(0, str(Mod1Marks))
                Mod1Percent = float(Mod1Marks)*100/self.totalMarks
            else:
                ModOneEntry.delete(0, tk.END)

            if Mod2Marks != "-":
                # To show the stored values on the Entry box
                ModTwoEntry.delete(0, tk.END)
                ModTwoEntry.insert(0, str(Mod2Marks))
            else:
                ModTwoEntry.delete(0, tk.END)
                Mod2Marks = 0

            # To check the visibility of widgets according to the updated values
            handleWidgets(ExMarks, Mod1Marks, Mod2Marks,
                          FinalMarks, ExaminerPercent, Mod1Percent, StudentID)

        def validate_entry1(text):
            """
            This function checks if the Examiner Marks are not greater than length 5
            """
            def show_tooltip(event):
                """
                This function shows a floating text when hovered over the warningMark1
                """
                canvas4.itemconfig(18, state='normal')
                warningText1.lift()

            def hide_tooltip(event):
                """
                This function hides the floating text when away from the warningMark1
                """
                canvas4.itemconfig(18, state='hidden')

            # Shows a warning text when Examiner Marks more than length 5
            if len(text) > 5:
                canvas4.itemconfig(18, state='hidden')
                canvas4.itemconfig(17, state='normal')
                warningMark1.bind("<Enter>", show_tooltip)
                warningMark1.bind("<Leave>", hide_tooltip)
                return False
            canvas4.itemconfig(17, state='hidden')
            return True

        def validate_entry2(text):
            """
            This function checks if the Moderator 1 Marks are not greater than length 5
            """
            def show_tooltip(event):
                """
                This function shows a floating text when hovered over the warningMark1
                """
                canvas4.itemconfig(20, state='normal')
                warningText1.lift()

            def hide_tooltip(event):
                """
                This function hides the floating text when away from the warningMark1
                """
                canvas4.itemconfig(20, state='hidden')

            # Shows a warning text when Moderator 1 Marks more than length 5
            if len(text) > 5:
                canvas4.itemconfig(20, state='hidden')
                canvas4.itemconfig(19, state='normal')
                warningMark2.bind("<Enter>", show_tooltip)
                warningMark2.bind("<Leave>", hide_tooltip)
                return False
            canvas4.itemconfig(19, state='hidden')
            return True

        def validate_entry3(text):
            """
            This function checks if the Moderator 2 Marks are not greater than length 5
            """
            def show_tooltip(event):
                """
                This function shows a floating text when hovered over the warningMark1
                """
                canvas4.itemconfig(22, state='normal')
                warningText1.lift()

            def hide_tooltip(event):
                """
                This function hides the floating text when away from the warningMark1
                """
                canvas4.itemconfig(22, state='hidden')

            # Shows a warning text when Moderator 2 Marks more than length 5
            if len(text) > 5:
                canvas4.itemconfig(22, state='hidden')
                canvas4.itemconfig(21, state='normal')
                warningMark3.bind("<Enter>", show_tooltip)
                warningMark3.bind("<Leave>", hide_tooltip)
                return False
            canvas4.itemconfig(21, state='hidden')
            return True

        # Initialising Entry Widgets
        RollNo_var = tk.StringVar()
        self.RollNo = ttk.Combobox(
            self.frame4, textvariable=RollNo_var, state='readonly')
        canvas4.create_window(360, 65, window=self.RollNo)
        self.RollNo.bind("<<ComboboxSelected>>", InitialiseWidgetsData)

        Attendance_var = tk.BooleanVar(value=True)
        self.AttendanceCheck = tk.Checkbutton(self.frame4, text="Present",
                                              variable=Attendance_var, padx=50, command=updateWidgetsData)
        canvas4.create_window(
            360, 120, window=self.AttendanceCheck, state='hidden')

        ExaminerEntry_var = tk.StringVar()
        ExaminerEntry = tk.Entry(self.frame4, textvariable=ExaminerEntry_var, validate="key", validatecommand=(
            self.frame4.register(validate_entry1), '%P'))
        canvas4.create_window(360, 180, window=ExaminerEntry, state='hidden')
        ExaminerEntry.bind('<KeyRelease>', updateWidgetsData)

        ModOneEntry_var = tk.StringVar()
        ModOneEntry = tk.Entry(self.frame4, textvariable=ModOneEntry_var, validate="key", validatecommand=(
            self.frame4.register(validate_entry2), '%P'))
        canvas4.create_window(360, 240, window=ModOneEntry, state='hidden')
        ModOneEntry.bind('<KeyRelease>', updateWidgetsData)

        ModTwoEntry_var = tk.StringVar()
        ModTwoEntry = tk.Entry(self.frame4, textvariable=ModTwoEntry_var, validate="key", validatecommand=(
            self.frame4.register(validate_entry3), '%P'))
        canvas4.create_window(360, 300, window=ModTwoEntry, state='hidden')
        ModTwoEntry.bind('<KeyRelease>', updateWidgetsData)

        canvas4.create_text(360, 350, fill="white",
                            font=self.font2)

        def GoToPreview():
            """
            This function redirects to frame5 and completes the pre-requsites for it
            """
            # To empty the table for adding new values
            if len(self.table.get_children()) > 0:
                self.table.delete(*self.table.get_children())

            # Adding all the values of the given bundle into the table
            AllData = self._UserInstance.GetAllData(self.DBname, self.TbName)
            for row in AllData[1:]:
                self.table.insert('', 'end', values=row)
            self.show_frame5()

        PrintButton = tk.Button(
            self.frame4, text="Print", command=GoToPreview)
        canvas4.create_window(560, 350, window=PrintButton)

        def backfunction():
            """
            This function is called by the back button and
            it clears all the data before redirecting to Page1
            """
            self.RollNo.set("")
            ExaminerEntry.delete(0, tk.END)
            ModOneEntry.delete(0, tk.END)
            ModTwoEntry.delete(0, tk.END)
            canvas4.itemconfig(4, state='hidden')
            canvas4.itemconfig(5, state='hidden')
            canvas4.itemconfig(6, state='hidden')
            canvas4.itemconfig(7, state='hidden')
            canvas4.itemconfig(9, state='hidden')
            canvas4.itemconfig(10, state='hidden')
            canvas4.itemconfig(11, state='hidden')
            canvas4.itemconfig(12, state='hidden')
            canvas4.itemconfig(13, state='hidden')
            canvas4.itemconfig(23, state='hidden')

            self.DBchoosen.config(values=self._UserInstance.getDB())
            self.TbChoosen.config(
                values=self._UserInstance.getTables(self.DBname))

            self.show_frame1()

        # Adding the Back Button
        back4 = tk.Button(self.frame4, text="Back", command=backfunction)
        canvas4.create_window(40, 30, window=back4)

        # To create a status (Synced or disconnected)
        canvas4.create_text(630, 30, fill="green", font=self.font3)

        # Warning Mark widget for Examiner Entry
        warningMark1 = tk.Label(self.frame4, text=" ! ")
        warningText1 = ttk.Label(self.frame4, text="Cannot have more than 5 digits", relief="solid",
                                 borderwidth=1, padding=4)
        canvas4.create_window(500, 180, window=warningMark1)
        canvas4.create_window(400, 150, window=warningText1)
        canvas4.itemconfig(17, state='hidden')
        canvas4.itemconfig(18, state='hidden')

        # Warning Mark widget for Moderator 1 Entry
        warningMark2 = tk.Label(self.frame4, text=" ! ")
        warningText2 = ttk.Label(self.frame4, text="Cannot have more than 5 digits", relief="solid",
                                 borderwidth=1, padding=4)
        canvas4.create_window(500, 240, window=warningMark2)
        canvas4.create_window(400, 210, window=warningText2)
        canvas4.itemconfig(19, state='hidden')
        canvas4.itemconfig(20, state='hidden')

        # Warning Mark widget for Moderator 2 Entry
        warningMark3 = tk.Label(self.frame4, text=" ! ")
        warningText3 = ttk.Label(self.frame4, text="Cannot have more than 5 digits", relief="solid",
                                 borderwidth=1, padding=4)
        canvas4.create_window(500, 300, window=warningMark3)
        canvas4.create_window(400, 270, window=warningText3)
        canvas4.itemconfig(21, state='hidden')
        canvas4.itemconfig(22, state='hidden')

        def DeleteStudent():
            """
            This fuction deletes all the information of the give StudentID,
            using the function DeleteRow of class DBconnect
            """
            deletevar = messagebox.askyesno(
                "Delete Student info", "Are you sure, you want to delete this StudentID completly. You cannot undo it!")
            if deletevar:
                # Deleting the StudentID and clearing the entry box
                self._UserInstance.DeleteRow(
                    self.DBname, self.TbName, self.RollNo.get())
                self.RollNo.delete(0, tk.END)

                # To add list of StudentID in the roll number Combobox
                tempList = self._UserInstance.StudentIDlist(
                    self.DBname, self.TbName)
                self.RollNo.config(values=tempList)

                # Making all other widgets hidden
                canvas4.itemconfig(4, state='hidden')
                canvas4.itemconfig(9, state='hidden')
                canvas4.itemconfig(5, state='hidden')
                canvas4.itemconfig(6, state='hidden')
                canvas4.itemconfig(7, state='hidden')
                canvas4.itemconfig(10, state='hidden')
                canvas4.itemconfig(11, state='hidden')
                canvas4.itemconfig(12, state='hidden')
                canvas4.itemconfig(13, state='hidden')
                ExMarks, Mod1Marks, Mod2Marks, FinalMarks = 0, 0, 0, 0

            else:
                return

        # To delete a row
        DeleteButton = tk.Button(
            self.frame4, text="Delete", command=DeleteStudent)
        canvas4.create_window(530, 65, window=DeleteButton, state='hidden')

        # Info button
        infoBtn = tk.Button(self.frame4, image=self.InfoImg,
                            command=lambda: messagebox.showinfo("Update Student details", "Add the details of each student. The marks can be added in the following manner:\n1)If Examiner Marks are between 30-40'%' or 75-100'%' then Moderator 1 marks can be added.\n2)If difference between Examiner Marks and Moderator 1 marks are\n(i)0-5'%' then Final Marks=Examiner Marks\n(i)5-15'%' then Final Marks=Moderator 1 Marks\n(i)15-25'%' then Final Marks=Average of both\n(i)25-100'%' then Final Marks=Moderator 2 Marks"))
        canvas4.create_window(715, 30, window=infoBtn)


class Page5(Page4):
    """
    This class creates a preview of the pdf data
    """

    def __init__(self) -> None:
        super().__init__()

        self.frame5 = tk.Frame(self)

        # Creating Page1 Canvas
        self.canvas5 = tk.Canvas(
            self.frame5, width=750, height=450, bg="black")
        self.canvas5.pack(fill="both", expand=True)

        # Calling the background image
        self.canvas5.create_image(
            80, 386, image=self.background_image, anchor="nw")

        # Details
        self.DBtext = self.canvas5.create_text(300, 20, text=str(self.DBname),
                                               fill="white", font=self.font3)
        self.Tbtext = self.canvas5.create_text(200, 60, text=str(self.TbName),
                                               fill="white", font=self.font3)
        self.totalMarkstext = self.canvas5.create_text(600, 40, text="Total Marks: "+str(self.totalMarks),
                                                       fill="white", font=self.font3)
        self.passingMarkstext = self.canvas5.create_text(600, 60, text="Passing Marks: "+str(self.passingMarks),
                                                       fill="white", font=self.font3)

        # add a table to the canvas
        self.table = ttk.Treeview(self.canvas5, columns=(
            'StudentID', 'Attendance', 'Examiner Marks', 'Moderator 1 Marks', 'Moderator 2 Marks', 'Final Marks'))
        self.table.heading('#0')
        self.table.heading('StudentID', text='StudentID')
        self.table.heading('Attendance', text='Attendance')
        self.table.heading('Examiner Marks', text='Examiner')
        self.table.heading('Moderator 1 Marks', text='Moderator 1')
        self.table.heading('Moderator 2 Marks', text='Moderator 2')
        self.table.heading('Final Marks', text='Final')

        self.table.column('#0', width=0, stretch=False)
        self.table.column('StudentID', width=110, anchor='center')
        self.table.column('Attendance', width=110, anchor='center')
        self.table.column('Examiner Marks', width=110, anchor='center')
        self.table.column('Moderator 1 Marks', width=110, anchor='center')
        self.table.column('Moderator 2 Marks', width=110, anchor='center')
        self.table.column('Final Marks', width=110, anchor='center')

        # Adding the Back Button
        back5 = tk.Button(self.frame5, text="Back", command=self.show_frame4)
        self.canvas5.create_window(40, 30, window=back5)

        # Initialinsing the created table on canvas
        self.canvas5.create_window(40, 80, anchor="nw", window=self.table)

        def pdf():
            """
            This function is called by the PdfButton,
            to generate a PDF of the given bundle using GeneratePDF class of file CreatePDF
            """
            try:
                # Adding it to the try block to check if the process of creation of the pdf is completed
                GeneratePDF(self.DBname, self.TbName, str(self.totalMarks), str(self.passingMarks), self._UserInstance.GetAllData(
                    self.DBname, self.TbName)[1:])
                tempmsg = messagebox.askyesno(
                    "PDF Created", "The pdf file of the given Bundle is been created, do u want to Logout?")

                # Checking the acceptance to Logout, if yes and then returns to the startup page
                if tempmsg == True:
                    self._UserInstance.quitDB()
                    self.show_startup()
            except:
                # if exception occured thn return to the previous page
                return

        PdfButton = tk.Button(
            self.frame5, text="PDF", command=pdf)
        self.canvas5.create_window(560, 350, window=PdfButton)

        # Info button
        infoBtn = tk.Button(self.frame5, image=self.InfoImg,
                            command=lambda: messagebox.showinfo("Create PDF", "The below table is a preview of the PDF.\nCreate a PDF of the following table by clicking on 'PDF' button"))
        self.canvas5.create_window(715, 30, window=infoBtn)


class App(Page5):
    """
    This class handles the shifting of frames
    """

    def __init__(self):
        super().__init__()

    def show_startup(self):
        """
        Shows the StartUp Page and hides other frames
        """
        self.startup.pack()
        self.frame1.pack_forget()
        self.frame2.pack_forget()
        self.frame3.pack_forget()
        self.frame4.pack_forget()
        self.frame5.pack_forget()

    def show_frame1(self):
        """
        Shows the frame1 Page and hides other frames
        """
        self.startup.pack_forget()
        self.frame1.pack()
        self.frame2.pack_forget()
        self.frame3.pack_forget()
        self.frame4.pack_forget()
        self.frame5.pack_forget()

    def show_frame2(self):
        """
        Shows the frame2 Page and hides other frames
        """
        self.startup.pack_forget()
        self.frame1.pack_forget()
        self.frame2.pack()
        self.frame3.pack_forget()
        self.frame4.pack_forget()
        self.frame5.pack_forget()

    def show_frame3(self):
        """
        Shows the frame3 Page and hides other frames
        """
        self.startup.pack_forget()
        self.frame1.pack_forget()
        self.frame2.pack_forget()
        self.frame3.pack()
        self.frame4.pack_forget()
        self.frame5.pack_forget()

    def show_frame4(self):
        """
        Shows the frame4 Page and hides other frames
        """
        self.startup.pack_forget()
        self.frame1.pack_forget()
        self.frame2.pack_forget()
        self.frame3.pack_forget()
        self.frame4.pack()
        self.frame5.pack_forget()

    def show_frame5(self):
        """
        Shows the frame5 Page and hides other frames
        """
        self.startup.pack_forget()
        self.frame1.pack_forget()
        self.frame2.pack_forget()
        self.frame3.pack_forget()
        self.frame4.pack_forget()
        self.frame5.pack()