import cv2
import tkinter as tk
from tkinter import ttk

class LivegrayscaleFilter:
    def __init__(self, root):
        self.root= root
        self.root.title("Livegrayscale Filter")
        self.run_filter=False
        self.setup_ui()
        self.cap = cv2.VideoCapture(0)

    def setup_ui(self):
        self.start_button=ttk.Button(self.root,text="Start",command=self.start_filter)
        self.start_button.pack(pady=10)

        self.stop_button=ttk.Button(self.root,text="Stop",command=self.stop_filter)
        self.stop_button.pack(pady=10)

    def start_filter(self):
        self.run_filter=True
        self.procces_frames()

    def stop_filter(self):
        self.run_filter=False
        cv2.destroyAllWindows()

    def procces_frames(self):
        if not self.run_filter:
            return
        ret, frame = self.cap.read()
        if ret:
            grey_frame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow("Livegrayscale Filter", grey_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):  
                self.stop_filter()

        self.root.after(10, self.procces_frames)
    def on_closing(self):
        self.run_filter=False
        if self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()
        self.root.destroy()

if __name__=="__main__":
    root=tk.Tk()
    app=LivegrayscaleFilter(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
