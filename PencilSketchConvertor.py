import cv2
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk

images={"original": None, "sketch": None}
def open_file():
    filepath = filedialog.askopenfilename()
    if not filepath:
        return
    img=cv2.imread(filepath)
    display_image(img,original=True)
    sketch_img= convert_to_sketch(img)
    display_image(sketch_img,original=False)

def convert_to_sketch(img):
    gray_img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inverted_img=cv2.bitwise_not(gray_img)
    blurred_img=cv2.GaussianBlur(inverted_img, (21,21), sigmaX=0, sigmaY=0)
    inverted_blur_img=cv2.bitwise_not(blurred_img)
    sketch_img=cv2.divide(gray_img, inverted_blur_img, scale=256)
    return sketch_img

def display_image(img,original):
    img_rgb=cv2.cvtColor(img, cv2.COLOR_BGR2RGB) if original else img
    img_pil=Image.fromarray(img_rgb)
    img_tk=ImageTk.PhotoImage(image=img_pil)
    if original:
        images["original"]= img_pil
        original_image_label.config(image=img_tk)
        original_image_label.image = img_tk
    else:
        images["sketch"]= img_pil

        sketch_image_label.config(image=img_tk)
        sketch_image_label.image = img_tk

        label=original_image_label if original else sketch_image_label


def save_sketch():
    if images["sketch"] is None:
        messagebox.showerror("Error", "No image to save")
        return
    sketch_filepath=filedialog.asksaveasfilename(defaultextension=".png", filetypes=(("PNG Files", "*.png"),))
    if not sketch_filepath:
        return

    images["sketch"].save(sketch_filepath,"PNG")
    messagebox.showinfo("Sketch Saved", "Sketch saved to {}".format(sketch_filepath))

app = tk.Tk()
app.title("Pencil Sketch Convertor")

frame = tk.Frame(app)
frame.pack(padx=10, pady=10)

original_image_label = tk.Label(frame)
original_image_label.grid(row=0, column=0, padx=5, pady=5)
sketch_image_label = tk.Label(frame)
sketch_image_label.grid(row=0, column=1, padx=5, pady=5)

btn_frame = tk.Frame(app)
btn_frame.pack(pady=10)

open_button = tk.Button(btn_frame, text="Open", command=open_file)
open_button.grid(row=0, column=0, padx=5)

save_button = tk.Button(btn_frame, text="Save", command=save_sketch)
save_button.grid(row=0, column=1, padx=5)

app.mainloop()


