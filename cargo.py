from customtkinter import *
from PIL import Image
from CTkTable import CTkTable
import database

my_db = database.connect_db()

app = CTk()
app.geometry("1280x720")
app.title("MEF Cargo System")
app.resizable(False,False) 

colors = ["#03045e", "#023e8a", "#0077b6", "#0096c7", "#00b4d8", "#48cae4", "#90e0ef", "#ade8f4", "#caf0f8"]


def customerLogin():
    loginframe = CTkFrame(master=mainFrame2, fg_color="#A8DADC",  width=720, height=480, corner_radius=25)
    loginframe.place(relx=0.5,rely=0.5,anchor="center")

    userImgData = Image.open("images/username.png")
    userImg = CTkImage(light_image=userImgData, dark_image=userImgData, size=(32, 32))
    userImgLabel = CTkLabel(master=loginframe, image=userImg, text="")
    userImgLabel.place(relx=0.32,rely=0.45,anchor="center")

    passImgData = Image.open("images/password.png")
    passImg = CTkImage(light_image=passImgData, dark_image=passImgData, size=(32, 32))
    passImgLabel = CTkLabel(master=loginframe, image=passImg, text="")
    passImgLabel.place(relx=0.32,rely=0.55,anchor="center")


    customerText = CTkLabel(master=loginframe,text="Customer Login",font=("Poppins", 30),text_color="#f4a261",bg_color="#A8DADC")
    customerText.place(relx=0.5,rely=0.3,anchor="center")

    customerID = CTkEntry(master=loginframe, fg_color="#457B9D", font=("Poppins", 14), text_color="#fff",placeholder_text="Customer ID",placeholder_text_color="#fff",bg_color="#A8DADC",height=30,width=200)
    customerID.place(relx=0.5,rely=0.45,anchor="center")

    customerPassw = CTkEntry(master=loginframe, fg_color="#457B9D", font=("Poppins", 14), text_color="#fff",placeholder_text="Password",placeholder_text_color="#fff",bg_color="#A8DADC",height=30,width=200)
    customerPassw.place(relx=0.5,rely=0.55,anchor="center")

    def goBack():
        loginframe.destroy()
    
    def logIn():
        if (customerID.get() != "" and customerPassw.get() != ""):
            newFrame = CTkFrame(master=app, fg_color="#ccd5ae",  width=1280, height=720, corner_radius=0)
            newFrame.place(relx=0.5,rely=0.5,anchor="center")

            tableFrame1 = CTkFrame(master=newFrame, fg_color="transparent",  width=700, height=10, corner_radius=0)
            tableFrame1.place(relx=0.5,rely=0.25,anchor="center")

            tableFrame2 = CTkFrame(master=newFrame, fg_color="transparent",  width=700, height=300, corner_radius=0)
            tableFrame2 = CTkScrollableFrame(master=newFrame, fg_color="transparent",  width=720, height=100, corner_radius=0) 
            tableFrame2.place(relx=0.5,rely=0.57,anchor="center")

            table1Data,table2Data = database.get_cargo_history(int(customerID.get()),my_db)        
            
            database.convert_table(table1Data)
            database.convert_table(table2Data)

            header1 = ["CustomerID","Full Name","Phone Number","Address"]
            table1Data.insert(0,header1)

            header2 = ["CargoNo","Status","Type","Weight","SenderID","ReceiverID","CourierID"]
            table2Data.insert(0,header2)  

            table1 = CTkTable(master=tableFrame1, values=table1Data, colors=["#457B9D","#457B9D"], header_color="#f77f00", hover_color="#1D3557",font=("Poppins", 14))
            table1.edit_row(0, text_color="#FDFCDC", hover_color="#f77f00")
            table1.pack(expand=True)

            table2 = CTkTable(master=tableFrame2, values=table2Data, colors=["#457B9D","#457B9D"], header_color="#a7c957", hover_color="#1D3557",font=("Poppins", 14))
            table2.edit_row(0, text_color="#FDFCDC", hover_color="#a7c957")
            table2.pack(expand=True)

            infoText = CTkLabel(master=newFrame,text="Customer Profile: " + str(table1Data[1][1]),font=("Poppins", 50),text_color="black")
            infoText.place(relx=0.5,rely=0.1,anchor="center")

            infoText2 = CTkLabel(master=newFrame,text="Cargo History",font=("Poppins", 30),text_color="black")
            infoText2.place(relx=0.5,rely=0.38,anchor="center")

            def checkBill():

                newBillFrame = CTkFrame(master=newFrame, fg_color="#ccd5ae",  width=1280, height=720, corner_radius=0)
                newBillFrame.place(relx=0.5,rely=0.5,anchor="center")

                billFrame = CTkFrame(master=newBillFrame, fg_color="#A8DADC",  width=720, height=480, corner_radius=25)
                billFrame.place(relx=0.5,rely=0.5,anchor="center")

                cargoIDinput = CTkEntry(master=billFrame, fg_color="#457B9D", font=("Poppins", 14), text_color="#fff",placeholder_text="CargoID",placeholder_text_color="#fff",height=30,width=200)
                cargoIDinput.place(relx=0.5,rely=0.45,anchor="center")

                infoText = CTkLabel(master=billFrame,text="Check Your Bill",font=("Poppins", 45),text_color="black")
                infoText.place(relx=0.5,rely=0.3,anchor="center")

                def showBill():
                    tableFrame = CTkFrame(master=billFrame, fg_color="transparent",  width=700, height=100, corner_radius=0)
                    tableFrame.place(relx=0.5,rely=0.75,anchor="center")

                    table_data = database.get_cargo_bill(cargoIDinput.get(),my_db)
                    database.convert_table(table_data)

                    header = ["BillID","Bill Date","Price","CargoID","SenderID"]
                    table_data.insert(0,header)  
                    
                    billTable = CTkTable(master=tableFrame, values=table_data, colors=["#457B9D","#457B9D"], header_color="#9a031e", hover_color="#1D3557",font=("Poppins", 14))
                    billTable.edit_row(0, text_color="#FDFCDC", hover_color="#9a031e")
                    billTable.pack(expand=True)



                checkBtn = CTkButton(master=billFrame, text="Check", fg_color="#00B4D8", font=("Poppins", 14), text_color="#fff", hover_color="#0096C7",command=showBill)
                checkBtn.place(relx=0.5,rely=0.55,anchor="center")

                def goBack():
                    newBillFrame.destroy()

                backBtn = CTkButton(master=billFrame, text="Back", fg_color="#E63946", font=("Poppins", 14), text_color="#fff", hover_color="#d00000",bg_color="#A8DADC",border_color="black",command=goBack)
                backBtn.place(relx=0.13,rely=0.95,anchor="center")

            billIDbtn = CTkButton(master=newFrame, text="Check Cargo Bill", fg_color="#ffb700", font=("Poppins", 14), text_color="#fff", hover_color="#ffaa00",command=checkBill)
            billIDbtn.place(relx=0.84,rely=0.8,anchor="center")

            def goBack():
                newFrame.destroy()
            
            goBackBtn = CTkButton(master=newFrame, text="Back", fg_color="#E63946", font=("Poppins", 14), text_color="#fff", hover_color="#d00000",border_color="black",command=goBack)
            goBackBtn.place(relx=0.15,rely=0.8,anchor="center")



    submitBtn = CTkButton(master=loginframe, text="Login", fg_color="#00B4D8", font=("Poppins", 14), text_color="#fff", hover_color="#0096C7",bg_color="#A8DADC",border_color="black",command=logIn)
    submitBtn.place(relx=0.5,rely=0.65,anchor="center")

    backBtn = CTkButton(master=loginframe, text="Back", fg_color="#E63946", font=("Poppins", 14), text_color="#fff", hover_color="#d00000",bg_color="#A8DADC",border_color="black",command=goBack)
    backBtn.place(relx=0.13,rely=0.95,anchor="center")



def adminLogin():

    loginframe = CTkFrame(master=mainFrame2, fg_color="#A8DADC",  width=720, height=480, corner_radius=25)
    loginframe.place(relx=0.5,rely=0.5,anchor="center")

    userImgData = Image.open("images/username.png")
    userImg = CTkImage(light_image=userImgData, dark_image=userImgData, size=(32, 32))
    userImgLabel = CTkLabel(master=loginframe, image=userImg, text="")
    userImgLabel.place(relx=0.32,rely=0.45,anchor="center")

    passImgData = Image.open("images/password.png")
    passImg = CTkImage(light_image=passImgData, dark_image=passImgData, size=(32, 32))
    passImgLabel = CTkLabel(master=loginframe, image=passImg, text="")
    passImgLabel.place(relx=0.32,rely=0.55,anchor="center")

    AdminText = CTkLabel(master=loginframe,text="Admin Login",font=("Poppins", 30),text_color="#f4a261",bg_color="#A8DADC")
    AdminText.place(relx=0.5,rely=0.3,anchor="center")

    AdminUsername = CTkEntry(master=loginframe, fg_color="#457B9D", font=("Poppins", 14), text_color="#fff",placeholder_text="Username",placeholder_text_color="#fff",bg_color="#A8DADC",height=30,width=200)
    AdminUsername.place(relx=0.5,rely=0.45,anchor="center")

    AdminPassw = CTkEntry(master=loginframe, fg_color="#457B9D", font=("Poppins", 14), text_color="#fff",placeholder_text="Password",placeholder_text_color="#fff",bg_color="#A8DADC",height=30,width=200)
    AdminPassw.place(relx=0.5,rely=0.55,anchor="center")

    def goBack():
        loginframe.destroy()
    
    def openAdminPage():
        newFrame = CTkFrame(master=app, fg_color="transparent",  width=1280, height=720, corner_radius=0)
        newFrame.place(relx=0.5,rely=0.5,anchor="center")

        buttonsFrame = CTkFrame(master=newFrame, fg_color="#ffb703",  width=400, height=720, corner_radius=0)
        buttonsFrame.place(relx=0.15,rely=0.5,anchor="center")

        rightFrame = CTkFrame(master=newFrame, fg_color="#8ecae6",  width=895, height=900, corner_radius=0)
        rightFrame.place(relx=0.655,rely=0.4,anchor="center")

        adminSystemText = CTkLabel(master=buttonsFrame,text="Admin System",font=("Poppins", 40),text_color="black")
        adminSystemText.place(relx=0.5,rely=0.1,anchor="center")

        def addEmployeePanel():
            empPanel1 = CTkFrame(master=rightFrame, fg_color="#7678ed",  width=900, height=400, corner_radius=0)
            empPanel1.place(relx=0.49,rely=0.36,anchor="center")

            empPanel2 = CTkFrame(master=rightFrame, fg_color="#b8c0ff",  width=900, height=400, corner_radius=0)
            empPanel2.place(relx=0.49,rely=0.8,anchor="center")

            tableFrame = CTkScrollableFrame(master=empPanel1, fg_color="transparent",  width=600, height=225, corner_radius=0)
            tableFrame.place(relx=0.51,rely=0.65,anchor="center")

            addEmpText = CTkLabel(master=empPanel2,text="Add Employee",font=("Poppins", 30),text_color="black")
            addEmpText.place(relx=0.5,rely=0.15,anchor="center")

            tableData = database.get_admin_employee_info(my_db)
            database.convert_table(tableData)
            header = ["ID","Full Name","DC No","Branch No"]
            tableData.insert(0,header)

            empTable = CTkTable(master=tableFrame, values=tableData, colors=["#457B9D","#457B9D"], header_color="#06d6a0", hover_color="#1D3557",font=("Poppins", 14))
            empTable.edit_row(0, text_color="#FDFCDC", hover_color="#06d6a0")
            empTable.pack(expand=True)

            empListText = CTkLabel(master=empPanel1,text="Employee List",font=("Poppins", 40),text_color="black")
            empListText.place(relx=0.51,rely=0.25,anchor="center")

            idEntry = CTkEntry(master=empPanel2, fg_color="#457B9D", font=("Poppins", 14), text_color="#fff",placeholder_text="ID",placeholder_text_color="#fff",height=30,width=200)
            idEntry.place(relx=0.35,rely=0.3,anchor="center")

            fullNameEntry = CTkEntry(master=empPanel2, fg_color="#457B9D", font=("Poppins", 14), text_color="#fff",placeholder_text="Full Name",placeholder_text_color="#fff",height=30,width=200)
            fullNameEntry.place(relx=0.65,rely=0.3,anchor="center")

            dcNoEntry = CTkEntry(master=empPanel2, fg_color="#457B9D", font=("Poppins", 14), text_color="#fff",placeholder_text="DC No",placeholder_text_color="#fff",height=30,width=200)
            dcNoEntry.place(relx=0.35,rely=0.5,anchor="center")

            branchNoEntry = CTkEntry(master=empPanel2, fg_color="#457B9D", font=("Poppins", 14), text_color="#fff",placeholder_text="Branch No",placeholder_text_color="#fff",height=30,width=200)
            branchNoEntry.place(relx=0.65,rely=0.5,anchor="center")

            def addDCEmp():
                database.add_dc_employee(idEntry.get(),fullNameEntry.get(),dcNoEntry.get(),my_db)

            def addBStaff():
                database.add_branch_staff(idEntry.get(),fullNameEntry.get(),branchNoEntry.get(),my_db)
            
            def addBCourier():
                database.add_branch_courier(idEntry.get(),fullNameEntry.get(),branchNoEntry.get(),my_db)

            addDCSBtn = CTkButton(master=empPanel2, text="Add DC Staff", fg_color="#e85d04", font=("Poppins", 14), text_color="#fff", hover_color="#dc2f02",command=addDCEmp)
            addDCSBtn.place(relx=0.15,rely=0.81,anchor="center")

            addBranchStaffBtn = CTkButton(master=empPanel2, text="Add Branch Staff", fg_color="#e85d04", font=("Poppins", 14), text_color="#fff", hover_color="#dc2f02",command=addBStaff)
            addBranchStaffBtn.place(relx=0.4,rely=0.81,anchor="center")

            addBranchCBtn = CTkButton(master=empPanel2, text="Add Branch Courier", fg_color="#e85d04", font=("Poppins", 14), text_color="#fff", hover_color="#dc2f02",command=addBCourier)
            addBranchCBtn.place(relx=0.65,rely=0.81,anchor="center")


            def goBack():
                empPanel1.destroy()
                empPanel2.destroy()

            backBtn = CTkButton(master=empPanel2, text="Back", fg_color="#E63946", font=("Poppins", 14), text_color="#fff", hover_color="#d00000",command=goBack)
            backBtn.place(relx=0.87,rely=0.81,anchor="center")



        def addCustomerPanel():

            cusPanel1 = CTkFrame(master=rightFrame, fg_color="#7678ed",  width=900, height=400, corner_radius=0)
            cusPanel1.place(relx=0.49,rely=0.36,anchor="center")

            cusPanel2 = CTkFrame(master=rightFrame, fg_color="#b8c0ff",  width=900, height=400, corner_radius=0)
            cusPanel2.place(relx=0.49,rely=0.8,anchor="center")

            tableFrame = CTkScrollableFrame(master=cusPanel1, fg_color="transparent",  width=600, height=150, corner_radius=0)
            tableFrame.place(relx=0.51,rely=0.65,anchor="center")

            cusListText = CTkLabel(master=cusPanel1,text="Customer List",font=("Poppins", 40),text_color="black")
            cusListText.place(relx=0.51,rely=0.25,anchor="center")

            tableData = database.get_admin_customer_info(my_db)
            database.convert_table(tableData)

            header = ["ID","Full Name","Phone Number","Address"]
            tableData.insert(0,header)


            cusTable = CTkTable(master=tableFrame, values=tableData, colors=["#457B9D","#457B9D"], header_color="#f35b04", hover_color="#1D3557",font=("Poppins", 14))
            cusTable.edit_row(0, text_color="#FDFCDC", hover_color="#f35b04")
            cusTable.pack(expand=True)

            idEntry = CTkEntry(master=cusPanel2, fg_color="#457B9D", font=("Poppins", 14), text_color="#fff",placeholder_text="ID",placeholder_text_color="#fff",height=30,width=200)
            idEntry.place(relx=0.35,rely=0.3,anchor="center")

            fullNameEntry = CTkEntry(master=cusPanel2, fg_color="#457B9D", font=("Poppins", 14), text_color="#fff",placeholder_text="Full Name",placeholder_text_color="#fff",height=30,width=200)
            fullNameEntry.place(relx=0.65,rely=0.3,anchor="center")

            phoneNoEntry = CTkEntry(master=cusPanel2, fg_color="#457B9D", font=("Poppins", 14), text_color="#fff",placeholder_text="Phone Number",placeholder_text_color="#fff",height=30,width=200)
            phoneNoEntry.place(relx=0.35,rely=0.5,anchor="center")

            addrEntry = CTkEntry(master=cusPanel2, fg_color="#457B9D", font=("Poppins", 14), text_color="#fff",placeholder_text="Address",placeholder_text_color="#fff",height=30,width=200)
            addrEntry.place(relx=0.65,rely=0.5,anchor="center")

            addCusText = CTkLabel(master=cusPanel2,text="Add Customer",font=("Poppins", 30),text_color="black")
            addCusText.place(relx=0.5,rely=0.15,anchor="center")

            def addCustomer():
                database.add_customer(idEntry.get(),fullNameEntry.get(),phoneNoEntry.get(),addrEntry.get(),my_db)

            addCusBtn = CTkButton(master=cusPanel2, text="Add Customer", fg_color="#e85d04", font=("Poppins", 14), text_color="#fff", hover_color="#dc2f02",command=addCustomer)
            addCusBtn.place(relx=0.5,rely=0.81,anchor="center")

            def goBack():
                cusPanel1.destroy()
                cusPanel2.destroy()

            backBtn = CTkButton(master=cusPanel2, text="Back", fg_color="#E63946", font=("Poppins", 14), text_color="#fff", hover_color="#d00000",command=goBack)
            backBtn.place(relx=0.87,rely=0.81,anchor="center")

        def addBranchPanel():
            bPanel1 = CTkFrame(master=rightFrame, fg_color="#7678ed",  width=900, height=400, corner_radius=0)
            bPanel1.place(relx=0.49,rely=0.36,anchor="center")

            bPanel2 = CTkFrame(master=rightFrame, fg_color="#b8c0ff",  width=900, height=400, corner_radius=0)
            bPanel2.place(relx=0.49,rely=0.8,anchor="center")

            branchListText = CTkLabel(master=bPanel1,text="Branch List",font=("Poppins", 40),text_color="black")
            branchListText.place(relx=0.51,rely=0.25,anchor="center")

            tableFrame = CTkScrollableFrame(master=bPanel1, fg_color="transparent",  width=600, height=225, corner_radius=0)
            tableFrame.place(relx=0.51,rely=0.65,anchor="center")

            tableData = database.get_branch_info(my_db)
            database.convert_table(tableData)

            header = ["Branch No","City","District","DC No"]
            tableData.insert(0,header)

            branchTable = CTkTable(master=tableFrame, values=tableData, colors=["#457B9D","#457B9D"], header_color="#52b788", hover_color="#1D3557",font=("Poppins", 14))
            branchTable.edit_row(0, text_color="#FDFCDC", hover_color="#52b788")
            branchTable.pack(expand=True)

            branchNoEntry = CTkEntry(master=bPanel2, fg_color="#457B9D", font=("Poppins", 14), text_color="#fff",placeholder_text="Branch No",placeholder_text_color="#fff",height=30,width=200)
            branchNoEntry.place(relx=0.35,rely=0.3,anchor="center")

            cityEntry = CTkEntry(master=bPanel2, fg_color="#457B9D", font=("Poppins", 14), text_color="#fff",placeholder_text="City",placeholder_text_color="#fff",height=30,width=200)
            cityEntry.place(relx=0.65,rely=0.3,anchor="center")

            districtEntry = CTkEntry(master=bPanel2, fg_color="#457B9D", font=("Poppins", 14), text_color="#fff",placeholder_text="District",placeholder_text_color="#fff",height=30,width=200)
            districtEntry.place(relx=0.35,rely=0.5,anchor="center")

            dcNOEntry = CTkEntry(master=bPanel2, fg_color="#457B9D", font=("Poppins", 14), text_color="#fff",placeholder_text="DC No",placeholder_text_color="#fff",height=30,width=200)
            dcNOEntry.place(relx=0.65,rely=0.5,anchor="center")

            addBranchText = CTkLabel(master=bPanel2,text="Add Branch",font=("Poppins", 30),text_color="black")
            addBranchText.place(relx=0.5,rely=0.15,anchor="center")

            def addBranch():
                database.add_branch(branchNoEntry.get(),cityEntry.get(),districtEntry.get(),dcNOEntry.get(),my_db)

            addBranchBtn = CTkButton(master=bPanel2, text="Add Branch", fg_color="#e85d04", font=("Poppins", 14), text_color="#fff", hover_color="#dc2f02",command=addBranch)
            addBranchBtn.place(relx=0.5,rely=0.81,anchor="center")

            def goBack():
                bPanel1.destroy()
                bPanel2.destroy()

            backBtn = CTkButton(master=bPanel2, text="Back", fg_color="#E63946", font=("Poppins", 14), text_color="#fff", hover_color="#d00000",command=goBack)
            backBtn.place(relx=0.87,rely=0.81,anchor="center")

        def addDCPanel():
            dcPanel1 = CTkFrame(master=rightFrame, fg_color="#7678ed",  width=900, height=400, corner_radius=0)
            dcPanel1.place(relx=0.49,rely=0.36,anchor="center")

            dcPanel2 = CTkFrame(master=rightFrame, fg_color="#b8c0ff",  width=900, height=400, corner_radius=0)
            dcPanel2.place(relx=0.49,rely=0.8,anchor="center")

            tableFrame = CTkScrollableFrame(master=dcPanel1, fg_color="transparent",  width=300, height=175, corner_radius=0)
            tableFrame.place(relx=0.51,rely=0.65,anchor="center")

            dcListText = CTkLabel(master=dcPanel1,text="Distribution Center List",font=("Poppins", 40),text_color="black")
            dcListText.place(relx=0.51,rely=0.25,anchor="center")

            tableData = database.get_dist_center_info(my_db)
            database.convert_table(tableData)

            header = ["DC No","DC Name"]
            tableData.insert(0,header)

            dcTable = CTkTable(master=tableFrame, values=tableData, colors=["#457B9D","#457B9D"], header_color="#72ddf7", hover_color="#1D3557",font=("Poppins", 14))
            dcTable.edit_row(0, text_color="#FDFCDC", hover_color="#72ddf7")
            dcTable.pack(expand=True)

            dcNOEntry = CTkEntry(master=dcPanel2, fg_color="#457B9D", font=("Poppins", 14), text_color="#fff",placeholder_text="DC No",placeholder_text_color="#fff",height=30,width=200)
            dcNOEntry.place(relx=0.5,rely=0.35,anchor="center")

            dcNameEntry = CTkEntry(master=dcPanel2, fg_color="#457B9D", font=("Poppins", 14), text_color="#fff",placeholder_text="DC Name",placeholder_text_color="#fff",height=30,width=200)
            dcNameEntry.place(relx=0.5,rely=0.5,anchor="center")

            addCusText = CTkLabel(master=dcPanel2,text="Add Distribution Center",font=("Poppins", 30),text_color="black")
            addCusText.place(relx=0.5,rely=0.15,anchor="center")

            def addDC():
                database.add_dist_center(dcNOEntry.get(),dcNameEntry.get(),my_db)

            addCusBtn = CTkButton(master=dcPanel2, text="Add Distribution Center", fg_color="#e85d04", font=("Poppins", 14), text_color="#fff", hover_color="#dc2f02",command=addDC)
            addCusBtn.place(relx=0.5,rely=0.81,anchor="center")



            def goBack():
                dcPanel1.destroy()
                dcPanel2.destroy()

            backBtn = CTkButton(master=dcPanel2, text="Back", fg_color="#E63946", font=("Poppins", 14), text_color="#fff", hover_color="#d00000",command=goBack)
            backBtn.place(relx=0.87,rely=0.81,anchor="center")
        

        empImgData = Image.open("images/empList.png")
        empImg = CTkImage(light_image=empImgData, dark_image=empImgData, size=(48, 48))
        empImgLabel = CTkLabel(master=buttonsFrame, image=empImg, text="")
        empImgLabel.place(relx=0.75,rely=0.24,anchor="center")

        cusImgData = Image.open("images/customerList.png")
        cusImg = CTkImage(light_image=cusImgData, dark_image=cusImgData, size=(48, 48))
        cusImgLabel = CTkLabel(master=buttonsFrame, image=cusImg, text="")
        cusImgLabel.place(relx=0.76,rely=0.4,anchor="center")

        branchImgData = Image.open("images/branchList.png")
        branchImg = CTkImage(light_image=branchImgData, dark_image=branchImgData, size=(48, 48))
        branchImgLabel = CTkLabel(master=buttonsFrame, image=branchImg, text="")
        branchImgLabel.place(relx=0.76,rely=0.55,anchor="center")

        dcCenterImgData = Image.open("images/dcList.png")
        dcCenterImg = CTkImage(light_image=dcCenterImgData, dark_image=dcCenterImgData, size=(48, 48))
        dcCenterImgLabel = CTkLabel(master=buttonsFrame, image=dcCenterImg, text="")
        dcCenterImgLabel.place(relx=0.8,rely=0.69,anchor="center")

        empBtn = CTkButton(master=buttonsFrame, text="List Employees", fg_color="#023e8a", font=("Poppins", 14), text_color="#fff", hover_color="#03045e",command=addEmployeePanel)
        empBtn.place(relx=0.5,rely=0.25,anchor="center")

        customerBtn = CTkButton(master=buttonsFrame, text="List Customers", fg_color="#023e8a", font=("Poppins", 14), text_color="#fff", hover_color="#03045e",command=addCustomerPanel)
        customerBtn.place(relx=0.5,rely=0.4,anchor="center")

        branchBtn = CTkButton(master=buttonsFrame, text="List Branches", fg_color="#023e8a", font=("Poppins", 14), text_color="#fff", hover_color="#03045e",command=addBranchPanel)
        branchBtn.place(relx=0.5,rely=0.55,anchor="center")

        dcBtn = CTkButton(master=buttonsFrame, text="List Distribution Centers", fg_color="#023e8a", font=("Poppins", 14), text_color="#fff", hover_color="#03045e",command=addDCPanel)
        dcBtn.place(relx=0.5,rely=0.70,anchor="center")


        def goBack():
            newFrame.destroy()
        
        backBtn = CTkButton(master=buttonsFrame, text="Back", fg_color="#E63946", font=("Poppins", 14), text_color="#fff", hover_color="#d00000",command=goBack)
        backBtn.place(relx=0.5,rely=0.95,anchor="center")
        

    
    submitBtn = CTkButton(master=loginframe, text="Login", fg_color="#00B4D8", font=("Poppins", 14), text_color="#fff", hover_color="#0096C7",bg_color="#A8DADC",border_color="black",command=openAdminPage)
    submitBtn.place(relx=0.5,rely=0.65,anchor="center")

    backBtn = CTkButton(master=loginframe, text="Back", fg_color="#E63946", font=("Poppins", 14), text_color="#fff", hover_color="#d00000",bg_color="#A8DADC",border_color="black",command=goBack)
    backBtn.place(relx=0.13,rely=0.95,anchor="center")



def empLogin():
    loginframe = CTkFrame(master=mainFrame2, fg_color="#A8DADC",  width=720, height=480, corner_radius=25)
    loginframe.place(relx=0.5,rely=0.5,anchor="center")

    userImgData = Image.open("images/username.png")
    userImg = CTkImage(light_image=userImgData, dark_image=userImgData, size=(32, 32))
    userImgLabel = CTkLabel(master=loginframe, image=userImg, text="")
    userImgLabel.place(relx=0.32,rely=0.45,anchor="center")

    passImgData = Image.open("images/password.png")
    passImg = CTkImage(light_image=passImgData, dark_image=passImgData, size=(32, 32))
    passImgLabel = CTkLabel(master=loginframe, image=passImg, text="")
    passImgLabel.place(relx=0.32,rely=0.55,anchor="center")

    EmpText = CTkLabel(master=loginframe,text="Employee Login",font=("Poppins", 30),text_color="#f4a261",bg_color="#A8DADC")
    EmpText.place(relx=0.5,rely=0.3,anchor="center")

    EmpUsername = CTkEntry(master=loginframe, fg_color="#457B9D", font=("Poppins", 14), text_color="#fff",placeholder_text="Username",placeholder_text_color="#fff",bg_color="#A8DADC",height=30,width=200)
    EmpUsername.place(relx=0.5,rely=0.45,anchor="center")

    EmpPassw = CTkEntry(master=loginframe, fg_color="#457B9D", font=("Poppins", 14), text_color="#fff",placeholder_text="Password",placeholder_text_color="#fff",bg_color="#A8DADC",height=30,width=200)
    EmpPassw.place(relx=0.5,rely=0.55,anchor="center")

    def goBack():
        loginframe.destroy()

    def openEmpPage():
        newFrame = CTkFrame(master=app, fg_color="transparent",  width=1280, height=720, corner_radius=0)
        newFrame.place(relx=0.5,rely=0.5,anchor="center")

        buttonsFrame = CTkFrame(master=newFrame, fg_color="#A8DADC",  width=400, height=720, corner_radius=0)
        buttonsFrame.place(relx=0.15,rely=0.5,anchor="center")

        rightFrame = CTkFrame(master=newFrame, fg_color="#ccd5ae",  width=895, height=900, corner_radius=0)
        rightFrame.place(relx=0.655,rely=0.4,anchor="center")

        empSystemText = CTkLabel(master=buttonsFrame,text="Employee System",font=("Poppins", 40),text_color="black")
        empSystemText.place(relx=0.5,rely=0.1,anchor="center")

        addCargoImgData = Image.open("images/addCargo.png")
        addCargoImg = CTkImage(light_image=addCargoImgData, dark_image=addCargoImgData, size=(48, 48))
        addCargoImgLabel = CTkLabel(master=buttonsFrame, image=addCargoImg, text="")
        addCargoImgLabel.place(relx=0.75,rely=0.24,anchor="center")

        updateLogImgData = Image.open("images/log.png")
        updateLogImg = CTkImage(light_image=updateLogImgData, dark_image=updateLogImgData, size=(48, 48))
        updateLogImgLabel = CTkLabel(master=buttonsFrame, image=updateLogImg, text="")
        updateLogImgLabel.place(relx=0.76,rely=0.4,anchor="center")

        addCustomerImgData = Image.open("images/addCustomer.png")
        addCustomerImg = CTkImage(light_image=addCustomerImgData, dark_image=addCustomerImgData, size=(48, 48))
        addCustomerImgLabel = CTkLabel(master=buttonsFrame, image=addCustomerImg, text="")
        addCustomerImgLabel.place(relx=0.76,rely=0.55,anchor="center")

        addBillImgData = Image.open("images/bill.png")
        addBillImg = CTkImage(light_image=addBillImgData, dark_image=addBillImgData, size=(48, 48))
        addBillImgLabel = CTkLabel(master=buttonsFrame, image=addBillImg, text="")
        addBillImgLabel.place(relx=0.76,rely=0.69,anchor="center")

        def goBack():
            newFrame.destroy()
        
        def openAddCargo():
            addCargoFrame = CTkFrame(master=rightFrame, fg_color="transparent",  width=895, height=900, corner_radius=0)
            addCargoFrame.place(relx=0.5,rely=0.5,anchor="center")

            addCargoPanel = CTkFrame(master=addCargoFrame, fg_color="#e9edc9",  width=600, height=600, corner_radius=25)
            addCargoPanel.place(relx=0.5,rely=0.55,anchor="center")

            enterCargoText = CTkLabel(master=addCargoFrame,text="Enter Cargo Details",font=("Poppins", 40),text_color="black",bg_color="#e9edc9")
            enterCargoText.place(relx=0.5,rely=0.35,anchor="center")

            cargoNoEntry = CTkEntry(master=addCargoFrame, fg_color="#457B9D", font=("Poppins", 14), text_color="#fff",placeholder_text="CargoNo",placeholder_text_color="#fff",height=30,width=200,bg_color="#e9edc9")
            cargoNoEntry.place(relx=0.5,rely=0.47,anchor="center")

            typeEntry = CTkEntry(master=addCargoFrame, fg_color="#457B9D", font=("Poppins", 14), text_color="#fff",placeholder_text="Type",placeholder_text_color="#fff",height=30,width=200,bg_color="#e9edc9")
            typeEntry.place(relx=0.5,rely=0.53,anchor="center")

            weightEntry = CTkEntry(master=addCargoFrame, fg_color="#457B9D", font=("Poppins", 14), text_color="#fff",placeholder_text="Weight",placeholder_text_color="#fff",height=30,width=200,bg_color="#e9edc9")
            weightEntry.place(relx=0.5,rely=0.59,anchor="center")

            senderIDEntry = CTkEntry(master=addCargoFrame, fg_color="#457B9D", font=("Poppins", 14), text_color="#fff",placeholder_text="Sender ID",placeholder_text_color="#fff",height=30,width=200,bg_color="#e9edc9")
            senderIDEntry.place(relx=0.5,rely=0.65,anchor="center")

            recIDEntry = CTkEntry(master=addCargoFrame, fg_color="#457B9D", font=("Poppins", 14), text_color="#fff",placeholder_text="Receiver ID",placeholder_text_color="#fff",height=30,width=200,bg_color="#e9edc9")
            recIDEntry.place(relx=0.5,rely=0.71,anchor="center")

            empIDEntry = CTkEntry(master=addCargoFrame, fg_color="#457B9D", font=("Poppins", 14), text_color="#fff",placeholder_text="Employee ID",placeholder_text_color="#fff",height=30,width=200,bg_color="#e9edc9")
            empIDEntry.place(relx=0.5,rely=0.77,anchor="center")

            def goBack():
                addCargoFrame.destroy()

            def insertToTable():
                database.add_cargo(cargoNoEntry.get(),typeEntry.get(),weightEntry.get(),recIDEntry.get(),senderIDEntry.get(),empIDEntry.get(),my_db)
            
            addBtn = CTkButton(master=addCargoFrame, text="Add", fg_color="#00B4D8", font=("Poppins", 14), text_color="#fff", hover_color="#0096C7",bg_color="#e9edc9",command=insertToTable)
            addBtn.place(relx=0.5,rely=0.83,anchor="center")

            backBtn = CTkButton(master=addCargoFrame, text="Back", fg_color="#E63946", font=("Poppins", 14), text_color="#fff", hover_color="#d00000",command=goBack)
            backBtn.place(relx=0.5,rely=0.95,anchor="center")



        def updateLog():
            updateLogFrame = CTkFrame(master=rightFrame, fg_color="transparent",  width=895, height=900, corner_radius=0)
            updateLogFrame.place(relx=0.5,rely=0.5,anchor="center")

            updateLogPanel = CTkFrame(master=updateLogFrame, fg_color="#e9edc9",  width=600, height=600, corner_radius=25)
            updateLogPanel.place(relx=0.5,rely=0.55,anchor="center")

            updateLogText = CTkLabel(master=updateLogFrame,text="Enter Log Details",font=("Poppins", 40),text_color="black",bg_color="#e9edc9")
            updateLogText.place(relx=0.5,rely=0.35,anchor="center")

            actionBox = CTkComboBox(master=updateLogFrame,fg_color="#457B9D",values=["Action","Branch Received","In Transport","In Distribution","Delivered"],font=("Poppins", 14),text_color="#fff",height=30,width=200,bg_color="#e9edc9",dropdown_fg_color="#457B9D",dropdown_font=("Poppins", 14))
            actionBox.place(relx=0.5,rely=0.5,anchor="center")


            cargoIDEntry = CTkEntry(master=updateLogFrame, fg_color="#457B9D", font=("Poppins", 14), text_color="#fff",placeholder_text="Cargo ID",placeholder_text_color="#fff",height=30,width=200,bg_color="#e9edc9")
            cargoIDEntry.place(relx=0.5,rely=0.6,anchor="center")

            empIDEntry = CTkEntry(master=updateLogFrame, fg_color="#457B9D", font=("Poppins", 14), text_color="#fff",placeholder_text="Employee ID",placeholder_text_color="#fff",height=30,width=200,bg_color="#e9edc9")
            empIDEntry.place(relx=0.5,rely=0.7,anchor="center")

            def addLog():
                database.add_log(actionBox.get(),cargoIDEntry.get(),empIDEntry.get(),my_db)

            updateBtn = CTkButton(master=updateLogFrame, text="Update", fg_color="#00B4D8", font=("Poppins", 14), text_color="#fff", hover_color="#0096C7",bg_color="#e9edc9",border_color="black",command=addLog)
            updateBtn.place(relx=0.5,rely=0.8,anchor="center")


            def goBack():
                updateLogFrame.destroy()


            backBtn = CTkButton(master=updateLogFrame, text="Back", fg_color="#E63946", font=("Poppins", 14), text_color="#fff", hover_color="#d00000",command=goBack)
            backBtn.place(relx=0.5,rely=0.95,anchor="center")

        def addCustomer():
            addCustomerFrame = CTkFrame(master=rightFrame, fg_color="transparent",  width=895, height=900, corner_radius=0)
            addCustomerFrame.place(relx=0.5,rely=0.5,anchor="center")

            addCustomerPanel = CTkFrame(master=addCustomerFrame, fg_color="#e9edc9",  width=600, height=600, corner_radius=25)
            addCustomerPanel.place(relx=0.5,rely=0.55,anchor="center")
            
            cusDetailsText = CTkLabel(master=addCustomerFrame,text="Enter Customer Details",font=("Poppins", 40),text_color="black",bg_color="#e9edc9")
            cusDetailsText.place(relx=0.5,rely=0.35,anchor="center")

            customerIDEntry = CTkEntry(master=addCustomerFrame, fg_color="#457B9D", font=("Poppins", 14), text_color="#fff",placeholder_text="Customer ID",placeholder_text_color="#fff",height=30,width=200,bg_color="#e9edc9")
            customerIDEntry.place(relx=0.5,rely=0.45,anchor="center")

            nameEntry = CTkEntry(master=addCustomerFrame, fg_color="#457B9D", font=("Poppins", 14), text_color="#fff",placeholder_text="Name",placeholder_text_color="#fff",height=30,width=200,bg_color="#e9edc9")
            nameEntry.place(relx=0.5,rely=0.55,anchor="center")

            phoneEntry = CTkEntry(master=addCustomerFrame, fg_color="#457B9D", font=("Poppins", 14), text_color="#fff",placeholder_text="Phone Number",placeholder_text_color="#fff",height=30,width=200,bg_color="#e9edc9")
            phoneEntry.place(relx=0.5,rely=0.65,anchor="center")

            cusAddEntry = CTkEntry(master=addCustomerFrame, fg_color="#457B9D", font=("Poppins", 14), text_color="#fff",placeholder_text="Customer Address",placeholder_text_color="#fff",height=30,width=200,bg_color="#e9edc9")
            cusAddEntry.place(relx=0.5,rely=0.75,anchor="center")

            def addCustomerDetails():
                database.add_customer(customerIDEntry.get(),nameEntry.get(),phoneEntry.get(),cusAddEntry.get(),my_db) 

            addBtn = CTkButton(master=addCustomerFrame, text="Add", fg_color="#00B4D8", font=("Poppins", 14), text_color="#fff", hover_color="#0096C7",bg_color="#e9edc9",command=addCustomerDetails)
            addBtn.place(relx=0.5,rely=0.83,anchor="center")

            def goBack():
                addCustomerFrame.destroy()

            backBtn = CTkButton(master=addCustomerFrame, text="Back", fg_color="#E63946", font=("Poppins", 14), text_color="#fff", hover_color="#d00000",command=goBack)
            backBtn.place(relx=0.5,rely=0.95,anchor="center")


        def addBill():
            addBillFrame = CTkFrame(master=rightFrame, fg_color="transparent",  width=895, height=900, corner_radius=0)
            addBillFrame.place(relx=0.5,rely=0.5,anchor="center")

            addBillPanel = CTkFrame(master=addBillFrame, fg_color="#e9edc9",  width=600, height=600, corner_radius=25)
            addBillPanel.place(relx=0.5,rely=0.55,anchor="center")

            billDetailsText = CTkLabel(master=addBillFrame,text="Enter Bill Details",font=("Poppins", 40),text_color="black",bg_color="#e9edc9")
            billDetailsText.place(relx=0.5,rely=0.35,anchor="center")

            priceEntry = CTkEntry(master=addBillFrame, fg_color="#457B9D", font=("Poppins", 14), text_color="#fff",placeholder_text="Price",placeholder_text_color="#fff",height=30,width=200,bg_color="#e9edc9")
            priceEntry.place(relx=0.5,rely=0.45,anchor="center")

            cargoIDEntry = CTkEntry(master=addBillFrame, fg_color="#457B9D", font=("Poppins", 14), text_color="#fff",placeholder_text="Cargo ID",placeholder_text_color="#fff",height=30,width=200,bg_color="#e9edc9")
            cargoIDEntry.place(relx=0.5,rely=0.55,anchor="center")

            senderIDEntry = CTkEntry(master=addBillFrame, fg_color="#457B9D", font=("Poppins", 14), text_color="#fff",placeholder_text="Sender ID",placeholder_text_color="#fff",height=30,width=200,bg_color="#e9edc9")
            senderIDEntry.place(relx=0.5,rely=0.65,anchor="center")

            def addBillDetails():
                database.add_bill(priceEntry.get(),cargoIDEntry.get(),senderIDEntry.get(),my_db)

            addBtn = CTkButton(master=addBillFrame, text="Add", fg_color="#00B4D8", font=("Poppins", 14), text_color="#fff", hover_color="#0096C7",bg_color="#e9edc9",command=addBillDetails)
            addBtn.place(relx=0.5,rely=0.83,anchor="center")


            def goBack():
                addBillFrame.destroy()

            backBtn = CTkButton(master=addBillFrame, text="Back", fg_color="#E63946", font=("Poppins", 14), text_color="#fff", hover_color="#d00000",command=goBack)
            backBtn.place(relx=0.5,rely=0.95,anchor="center")



        addCargoBtn = CTkButton(master=buttonsFrame, text="Add Cargo", fg_color="#ffb703", font=("Poppins", 14), text_color="#fff", hover_color="#fb8500",command=openAddCargo)
        addCargoBtn.place(relx=0.5,rely=0.25,anchor="center")

        updateLogBtn = CTkButton(master=buttonsFrame, text="Update Log", fg_color="#ffb703", font=("Poppins", 14), text_color="#fff", hover_color="#fb8500",command=updateLog)
        updateLogBtn.place(relx=0.5,rely=0.4,anchor="center")

        addCustomerBtn = CTkButton(master=buttonsFrame, text="Add Customer", fg_color="#ffb703", font=("Poppins", 14), text_color="#fff", hover_color="#fb8500",command=addCustomer)
        addCustomerBtn.place(relx=0.5,rely=0.55,anchor="center")

        addBillBtn = CTkButton(master=buttonsFrame, text="Add Bill", fg_color="#ffb703", font=("Poppins", 14), text_color="#fff", hover_color="#fb8500",command=addBill)
        addBillBtn.place(relx=0.5,rely=0.70,anchor="center")

        backBtn = CTkButton(master=buttonsFrame, text="Back", fg_color="#E63946", font=("Poppins", 14), text_color="#fff", hover_color="#d00000",command=goBack)
        backBtn.place(relx=0.5,rely=0.95,anchor="center")


    submitBtn = CTkButton(master=loginframe, text="Login", fg_color="#00B4D8", font=("Poppins", 14), text_color="#fff", hover_color="#0096C7",bg_color="#A8DADC",border_color="black",command=openEmpPage)
    submitBtn.place(relx=0.5,rely=0.65,anchor="center")

    backBtn = CTkButton(master=loginframe, text="Back", fg_color="#E63946", font=("Poppins", 14), text_color="#fff", hover_color="#d00000",bg_color="#A8DADC",border_color="black",command=goBack)
    backBtn.place(relx=0.13,rely=0.95,anchor="center")


def noLogin():
    
    loginframe = CTkFrame(master=mainFrame2, fg_color="#A8DADC",  width=720, height=480, corner_radius=25)
    loginframe.place(relx=0.5,rely=0.5,anchor="center")

    cIDImgData = Image.open("images/cargoID.png")
    cIDImg = CTkImage(light_image=cIDImgData, dark_image=cIDImgData, size=(64, 64))
    cIDImgLabel = CTkLabel(master=loginframe, image=cIDImg, text="")
    cIDImgLabel.place(relx=0.32,rely=0.45,anchor="center")

    noLoginText = CTkLabel(master=loginframe,text="Track your cargo without login",font=("Poppins", 30),text_color="#f4a261",bg_color="#A8DADC")
    noLoginText.place(relx=0.5,rely=0.3,anchor="center")

    cargoID = CTkEntry(master=loginframe, fg_color="#457B9D", font=("Poppins", 14), text_color="#fff",placeholder_text="CargoID",placeholder_text_color="#fff",bg_color="#A8DADC",height=30,width=200)
    cargoID.place(relx=0.5,rely=0.45,anchor="center")

    
    def goBack():
        loginframe.destroy()

    def track():


        if (cargoID.get() != ""):
            newFrame = CTkFrame(master=app, fg_color="#ccd5ae",  width=1280, height=720, corner_radius=0)
            newFrame.place(relx=0.5,rely=0.5,anchor="center")
            sideFrame = CTkFrame(master=newFrame, fg_color="#A8DADC",  width=400, height=720, corner_radius=0)
            sideFrame.place(relx=0.15,rely=0.5,anchor="center")

            

            rightFrame = CTkFrame(master=newFrame, fg_color="transparent",  width=895, height=900, corner_radius=0)
            rightFrame.place(relx=0.655,rely=0.4,anchor="center")

            statusLabel = CTkLabel(master=sideFrame,text="Your Cargo Status",font=("Poppins", 30),text_color="black",bg_color="#A8DADC")
            statusLabel.place(relx=0.5,rely=0.1,anchor="center")

            #"Branch Received", "In Transport", "In Distribution", "Delivered"

            bReceivedText = CTkLabel(master=sideFrame,text="Branch Received -",font=("Poppins", 17),text_color="#2b2d42",bg_color="#A8DADC")
            bReceivedText.place(relx=0.25,rely=0.71,anchor="center")

            inTransportText = CTkLabel(master=sideFrame,text="- In Transport",font=("Poppins", 17),text_color="#2b2d42",bg_color="#A8DADC")
            inTransportText.place(relx=0.7,rely=0.55,anchor="center")

            inDistText = CTkLabel(master=sideFrame,text="In Distribution -",font=("Poppins", 17),text_color="#2b2d42",bg_color="#A8DADC")
            inDistText.place(relx=0.27,rely=0.38,anchor="center")

            deliveredText = CTkLabel(master=sideFrame,text="- Delivered",font=("Poppins", 17),text_color="#2b2d42",bg_color="#A8DADC")
            deliveredText.place(relx=0.67,rely=0.27,anchor="center")

            infoText = CTkLabel(master=newFrame,text="Your Cargo Info",font=("Poppins", 50),text_color="black")
            infoText.place(relx=0.65,rely=0.1,anchor="center")

        

            trackProgressBar = CTkProgressBar(master=newFrame,orientation="vertical",width=35,height=350,bg_color="#A8DADC",border_width=5,border_color="black",progress_color="#ffb703")
            trackProgressBar.place(relx=0.15,rely=0.5,anchor="center")

            tableFrame = CTkScrollableFrame(master=rightFrame, fg_color="transparent",  width=900, height=300, corner_radius=0)
            tableFrame.place(relx=0.5,rely=0.55,anchor="center")
            
            tableFrame2 = CTkScrollableFrame(master=rightFrame, fg_color="transparent",  width=900, height=300, corner_radius=0)
            tableFrame2.place(relx=0.5,rely=0.65,anchor="center")

            table1Data, table2Data = database.cargo_tracking(cargoID.get(),my_db)            
            
            database.convert_table(table1Data)
            database.convert_table(table2Data)

            header1 = ["CargoNo","Status","Type","Weight","SenderName","SenderAddress","ReceiverName","RecAddress"]
            table1Data.insert(0,header1)

            header2 = ["LogNo","Date and Time","Action","District","DC Name"]
            table2Data.insert(0,header2)

            table1 = CTkTable(master=tableFrame, values=table1Data, colors=["#457B9D","#457B9D"], header_color="#bc6c25", hover_color="#1D3557",font=("Poppins", 14))
            table1.edit_row(0, text_color="#FDFCDC", hover_color="#bc6c25")
            table1.pack(expand=True)
        
            

            table2 = CTkTable(master=tableFrame2, values=table2Data, colors=["#457B9D","#457B9D"], header_color="#023047", hover_color="#1D3557",font=("Poppins", 14))
            table2.edit_row(0, text_color="#FDFCDC", hover_color="#023047")
            table2.pack(expand=True)

            if (table1Data[1][1] == "Delivered"):
                trackProgressBar.set(1)

            elif (table1Data[1][1] == "In Distribution"):
                trackProgressBar.set(0.75)

            elif (table1Data[1][1] == "In Transport"):
                trackProgressBar.set(0.35)
            
            elif (table1Data[1][1] == "Branch Received"):
                trackProgressBar.set(0)


            def goBack():
                newFrame.destroy()
            

            backBtn = CTkButton(master=newFrame, text="Back", fg_color="#E63946", font=("Poppins", 14), text_color="#fff", hover_color="#d00000",border_color="black",bg_color="#A8DADC",command=goBack)
            backBtn.place(relx=0.15,rely=0.85,anchor="center")
        else:
            pass


        

    trackbtn = CTkButton(master=loginframe, text="Track", fg_color="#00B4D8", font=("Poppins", 14), text_color="#fff", hover_color="#0096C7",bg_color="#A8DADC",border_color="black",command=track)
    trackbtn.place(relx=0.5,rely=0.55,anchor="center")   
    
    backBtn = CTkButton(master=loginframe, text="Back", fg_color="#E63946", font=("Poppins", 14), text_color="#fff", hover_color="#d00000",bg_color="#A8DADC",border_color="black",command=goBack)
    backBtn.place(relx=0.13,rely=0.95,anchor="center")

mainFrame1 = CTkFrame(master=app, fg_color="#e3d5ca",  width=500, height=720, corner_radius=0)
mainFrame1.place(relx=0.19,rely=0.5,anchor="center")

mainFrame2 = CTkFrame(master=app, fg_color="#0096c7",  width=800, height=720, corner_radius=0)
mainFrame2.place(relx=0.69,rely=0.5,anchor="center")

customerLoginbtn = CTkButton(master=mainFrame2 , text="Customer Login", fg_color="#48CAE4", font=("Poppins", 14), text_color="#FDFCDC", hover_color="#023E8A",command=customerLogin)
customerLoginbtn.place(relx=0.50,rely=0.45,anchor="center")

adminLoginbtn = CTkButton(master=mainFrame2, text="Admin Login", fg_color="#48CAE4", font=("Poppins", 14), text_color="#FDFCDC", hover_color="#023E8A",command=adminLogin)
adminLoginbtn.place(relx=0.25,rely=0.45,anchor="center")

empLoginbtn = CTkButton(master=mainFrame2, text="Employee Login", fg_color="#48CAE4", font=("Poppins", 14), text_color="#FDFCDC", hover_color="#023E8A",command=empLogin)
empLoginbtn.place(relx=0.75,rely=0.45,anchor="center")

noLoginTrack = CTkButton(master=mainFrame2, text="Track without Login", fg_color="#fcbf49", font=("Poppins", 14), text_color="#FDFCDC", hover_color="#f77f00",command=noLogin)
noLoginTrack.place(relx=0.5,rely=0.6,anchor="center")

logoImgData = Image.open("images/package.png")
logoImg = CTkImage(light_image=logoImgData, dark_image=logoImgData, size=(52, 52))
logoImgLabel = CTkLabel(master=mainFrame1, image=logoImg, text="")
logoImgLabel.place(relx=0.77,rely=0.2,anchor="center")

shipImgData = Image.open("images/shipping.png")
shipImg = CTkImage(light_image=shipImgData, dark_image=shipImgData, size=(256, 256))
shipImgLabel = CTkLabel(master=mainFrame1, image=shipImg, text="")
shipImgLabel.place(relx=0.5,rely=0.6,anchor="center")

adminImgData = Image.open("images/admin.png")
adminImg = CTkImage(light_image=adminImgData, dark_image=adminImgData, size=(32, 32))
adminImgLabel = CTkLabel(master=mainFrame2, image=adminImg, text="")
adminImgLabel.place(relx=0.25,rely=0.4,anchor="center")

empImgData = Image.open("images/employees.png")
empImg = CTkImage(light_image=empImgData, dark_image=empImgData, size=(32, 32))
empImgLabel = CTkLabel(master=mainFrame2, image=empImg, text="")
empImgLabel.place(relx=0.75,rely=0.4,anchor="center")

customerImgData = Image.open("images/customer.png")
customerImg = CTkImage(light_image=customerImgData, dark_image=customerImgData, size=(32, 32))
customerImgLabel = CTkLabel(master=mainFrame2, image=customerImg, text="")
customerImgLabel.place(relx=0.5,rely=0.4,anchor="center")

sideLImgData = Image.open("images/sideLogo.png")
sideLImg = CTkImage(light_image=sideLImgData, dark_image=sideLImgData, size=(128, 128))
sideLImgLabel = CTkLabel(master=mainFrame2, image=sideLImg, text="")
sideLImgLabel.place(relx=0.91,rely=0.94,anchor="center")

airplaneImgData = Image.open("images/airplaneLogo.png")
airplaneImg = CTkImage(light_image=airplaneImgData, dark_image=airplaneImgData, size=(128, 128))
airplaneImgLabel = CTkLabel(master=mainFrame2, image=airplaneImg, text="")
airplaneImgLabel.place(relx=0.1,rely=0.08,anchor="center")

shipImgData = Image.open("images/ship.png")
shipImg = CTkImage(light_image=shipImgData, dark_image=shipImgData, size=(128, 128))
shipImgLabel = CTkLabel(master=mainFrame2, image=shipImg, text="")
shipImgLabel.place(relx=0.1,rely=0.94,anchor="center")

trainImgData = Image.open("images/train.png")
trainImg = CTkImage(light_image=trainImgData, dark_image=trainImgData, size=(128, 128))
trainImgLabel = CTkLabel(master=mainFrame2, image=trainImg, text="")
trainImgLabel.place(relx=0.91,rely=0.08,anchor="center")

MefCargo_text = CTkLabel(master=mainFrame1,text="MEF Cargo",font=("Poppins", 45),text_color="Orange",corner_radius=100)
MefCargo_text.place(relx=0.45,rely=0.2,anchor="center")

loginText = CTkLabel(master=mainFrame2,text="Choose Your Login Type",font=("Poppins", 40),text_color="#caf0f8")
loginText.place(relx=0.5,rely=0.28,anchor="center")

orText = CTkLabel(master=mainFrame2,text="-- Or --",font=("Poppins", 25),text_color="#fcbf49")
orText.place(relx=0.5,rely=0.525,anchor="center")

app.mainloop()

