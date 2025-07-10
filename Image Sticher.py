import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image

# Global list to store image paths
image_paths = []

def open_file():
    files = filedialog.askopenfilenames(title="Select files")
    if len(files) < 2:
        messagebox.showerror("Error", "Please select at least 2 files")
        return

    # Debugging: Print the selected file paths
    print("Selected files:", files)

    # Clear previous image paths
    image_paths.clear()

    for file in files:
        image_paths.append(file)
    messagebox.showinfo("Success", f"{len(files)} files selected")

def stitch_images():
    if len(image_paths) < 2:
        messagebox.showerror("Error", "Please select at least 2 images")
        return

    images = []
    for path in image_paths:
        # Debugging: Print the file path to ensure it's correct
        print(f"Reading image from: {path}")

        image = cv2.imread(path)
        if image is None:
            messagebox.showerror("Error", f"Image not found: {path}")
            return
        images.append(image)

    stitcher = cv2.Stitcher_create()
    status, pano = stitcher.stitch(images)
    if status != cv2.Stitcher_OK:
        messagebox.showerror("Error", "Stitching failed")
        return

    display_image(pano)
    messagebox.showinfo("Success", "Image stitched successfully")

def display_image(cv2_img):
    cv2_img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(cv2_img_rgb)
    imgtk = ImageTk.PhotoImage(image=pil_img)
    panel.configure(image=imgtk)
    panel.image = imgtk

root = tk.Tk()
root.title("Image Stitcher")

open_button = tk.Button(root, text="Open Images", command=open_file)
stitch_button = tk.Button(root, text="Stitch Images", command=stitch_images)
panel = tk.Label(root)

open_button.pack(pady=10)
stitch_button.pack(pady=10)
panel.pack(pady=10)

root.mainloop()
