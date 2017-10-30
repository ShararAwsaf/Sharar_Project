from tkinter import *

class gui_layout:

    #calss var
    count = 0
    frame = None
    num_0 = 0
    num_1 = 0
    num_2 = 0
    num_3 = 0
    num_4 = 0
    bt = ""


    def __init__(self,root):

        #frame
        self.root = root
        topFrame = Frame(root,width=300,height=300)
        topFrame.grid()


        #title
        Label(topFrame,text = "WELCOME TO DEVICE HEALTH",bg="black",fg="white").grid(row = 0)

        #create labels for the left frame
        label0 = Label(topFrame, text="Number of people in room : ", bg="white", fg="black")
        label1 = Label(topFrame,text="Number of phones in room : ",bg="white",fg="black")
        label2 = Label(topFrame,text="Number of computers in room : ",bg="white",fg="black")
        label3 = Label(topFrame,text="Number of tvs in room : ",bg="white",fg="black")
        label4 = Label(topFrame,text="Number of other appliances in room : ",bg="white",fg="black")
        label5 = Label(topFrame, text="Breath Test (Y/N) : ", bg="white", fg="black")

        label0.grid(row=1, column=0, sticky=W)
        label1.grid(row=2,column=0,sticky=W)
        label2.grid(row=3,column=0,sticky=W)
        label3.grid(row=4,column=0,sticky=W)
        label4.grid(row=5,column=0,sticky=W)
        label5.grid(row=6, column=0, sticky=W)

        # placing the entrys
        self.entry_0 = Entry(topFrame)
        self.entry_1 = Entry(topFrame)
        self.entry_2 = Entry(topFrame)
        self.entry_3 = Entry(topFrame)
        self.entry_4 = Entry(topFrame)
        self.entry_5 = Entry(topFrame)

        self.entry_0.grid(row=1, column=1)
        self.entry_1.grid(row=2, column=1)
        self.entry_2.grid(row=3, column=1)
        self.entry_3.grid(row=4, column=1)
        self.entry_4.grid(row=5, column=1)
        self.entry_5.grid(row=6, column=1)

        # submit
        self.subBtn = Button(topFrame,text="Submit",command = self.submit)
        self.subBtn.grid(row = 7,column = 0)


    def submit(self):
        self.num_0 = self.entry_0.get()
        self.num_1 = self.entry_1.get()
        self.num_2 = self.entry_2.get()
        self.num_3 = self.entry_3.get()
        self.num_4 = self.entry_4.get()

        if self.entry_5.get() =="Y" or self.entry_5.get() =="y":
            self.bt = "Y"
        else:
            self.bt = "N"
        file_str = str(self.num_0) +","+str(self.num_1) +","+str(self.num_2) +","+ str(self.num_3) +","+ str(self.num_4) +","+ str(self.bt)

        f = open("data.txt","w+")
        f.write(file_str)
        f.close()
        self.root.quit()



def main():
    root = Tk()  # constructor window
    gui = gui_layout(root)
    root.mainloop() # keeps widows in place forever till x hit
main()