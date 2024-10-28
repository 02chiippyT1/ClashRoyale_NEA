import tkinter as tk
import GameMenu_tkinter
from PIL import ImageTk, Image


class MapPicker(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        window_frame = tk.Frame(self, width=1400, height=1000)
        window_frame.pack()

        # self.root = tk.Tk()
        # self.root.resizable(width=False, height=False)
        # self.img_path = "./background.png"
        # self.image = tk.PhotoImage(master=parent, file=self.img_path)
        # self.label_image = tk.Label(tk.Frame, image=self.image)
        # self.label_image.pack(side=tk.TOP)
        # self.image = tk.PhotoImage(Image.open(self.img_path))
        # self.root.mainloop()
        button1 = tk.Button(window_frame, text="BACK TO HOME", command=lambda: controller.show_frame(GameMenu_tkinter.GameMenu))
        button1.pack()

        # background_frame = tk.Frame(window_frame)
        # background_frame.place(x=0, y=0)

        img = tk.PhotoImage(master=parent, file='background.png')
        img_lbl = tk.Label(window_frame, image=img)
        img_lbl.image = img
        img_lbl.pack()

# MapPicker