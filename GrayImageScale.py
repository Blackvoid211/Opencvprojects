import cv2
from tkinter import Tk, filedialog, Button,Label
from tkinter import N,S,E,W
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[('Image Files', '*.png *.jpg *.bmp')])
    if file_path:
        convert_to_grayscale(file_path)

def convert_to_grayscale(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow('gray', gray_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def setup_ui(root):
    root.title("Gray Scale Image Processing")
    root.geometry("400x400")
    root.resizable(width=0, height=0)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    label = Label(root, text="Gray Scale Image Processing",wraplength=250)
    label.grid(column=0, row=0, padx=5, pady=5,sticky=N)

    open_button = Button(root, text="Open", command=open_file)
    open_button.grid(column=0, row=1, padx=5, pady=5,sticky=S+E+W)

if __name__ == '__main__':
    root = Tk()
    setup_ui(root)
    root.mainloop()
