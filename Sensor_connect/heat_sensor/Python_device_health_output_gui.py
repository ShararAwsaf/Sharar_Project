from tkinter import *

class gui_output:

    def __init__(self, root):
        self.root = root
        frame = Frame(root, width=300, height=300)
        frame.grid()

        Label(frame, "Condition of the room", bg="black", fg="white")
        pos = 0
        while(True):
            with open("output.txt", mode="r+", encoding="utf-8") as file_obj:
                try:
                    Label(frame,text=file_obj.readline(),row=pos,column = 2)
                    pos += 1
                except:
                    print("Finished displaying file")




root = Tk()
gui = gui_output(root)
root.mainloop()