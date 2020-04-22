# import tkinter
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

class Timer:
    def __init__(self, parent):
        # variable storing time
        self.seconds = 0
        # label displaying time
        self.label1 = tk.Label(parent, text="Pattern detected: ", font="Arial 15")
        self.label = tk.Label(parent, text=" --- ", font="Arial 30", width=10)

        self.button = tk.Button(parent,
                                text="Click to change text below",
                                command=self.changeText)

        self.label1.pack()
        self.label.pack()
        self.button.pack()


    def changeText(self):
        """ change to corresponding text label if events happen"""
        self.label['text'] = "New pattern"     
        self.label.after(500,self.default_label)


    def default_label(self): 
        """ set label to default message when no events happen """
        self.label['text'] = " --- "  


if __name__ == "__main__":
    root = tk.Tk()
    root.title ("Tapping hotkeys") # set window title
    root.geometry('300x200') # set window size
    timer = Timer(root)
    root.mainloop()



