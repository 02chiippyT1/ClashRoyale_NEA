import tkinter as tk
from PIL import ImageTk,Image

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(width=False, height=False)
    root.geometry('480x640')

    img_path = "./maps_design_earth_1.png"

    image = ImageTk.PhotoImage(Image.open(img_path))
    label_image=tk.Label(root, image=image)
    label_image.pack(side=tk.TOP)

    root.mainloop()
