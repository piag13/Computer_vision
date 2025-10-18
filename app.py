#!/usr/bin/env python3
import cv2
import threading
import time
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox

CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
WINDOW_TITLE = "Face Anonymizer (Tkinter GUI)"

class FaceAnonymizerApp:
    def __init__(self, root):
        self.root = root
        root.title(WINDOW_TITLE)

        # Haar face detector
        self.detector = cv2.CascadeClassifier(CASCADE_PATH)

        # Mode variable
        self.mode = tk.StringVar(value="BLUR")

        # Sticker image (optional)
        self.sticker_img = None

        # Video variables
        self.cap = None
        self.running = False
        self.video_thread = None
        self.current_frame = None
        self.video_fps = 25

        self.create_widgets()

    def create_widgets(self):
        frm = tk.Frame(self.root)
        frm.pack(side=tk.TOP, fill=tk.X, padx=6, pady=6)

        tk.Button(frm, text="Open Image", command=self.open_image).pack(side=tk.LEFT, padx=4)
        tk.Button(frm, text="Open Video", command=self.open_video).pack(side=tk.LEFT, padx=4)
        tk.Button(frm, text="Start Webcam", command=self.start_webcam).pack(side=tk.LEFT, padx=4)
        tk.Button(frm, text="Stop", command=self.stop_video).pack(side=tk.LEFT, padx=4)
        tk.Button(frm, text="Save Frame", command=self.save_frame).pack(side=tk.LEFT, padx=4)

        tk.Label(frm, text="Mode:").pack(side=tk.LEFT, padx=(12,0))
        modes = ["BLUR", "PIXEL", "STICKER"]
        tk.OptionMenu(frm, self.mode, *modes).pack(side=tk.LEFT, padx=4)

        tk.Button(frm, text="Select Sticker", command=self.select_sticker).pack(side=tk.LEFT, padx=4)

        self.scale = tk.Scale(frm, from_=1, to=50, orient=tk.HORIZONTAL, label="Strength")
        self.scale.set(15)
        self.scale.pack(side=tk.RIGHT, padx=8)

        self.canvas = tk.Label(self.root)
        self.canvas.pack(padx=6, pady=6)

        self.status = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    # ------------------ IO ------------------
    def open_image(self):
        path = filedialog.askopenfilename(title="Select image",
                                          filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
        if not path:
            return
        self.stop_video()
        img = cv2.imread(path)
        if img is None:
            messagebox.showerror("Error", "Cannot open image.")
            return
        self.process_and_show_frame(img)
        self.status.config(text=f"Opened image: {path}")

    def open_video(self):
        path = filedialog.askopenfilename(title="Select video",
                                          filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")])
        if not path:
            return
        self.stop_video()
        self.cap = cv2.VideoCapture(path)
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Cannot open video.")
            return
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        if fps and fps > 1:
            self.video_fps = fps
        self.running = True
        self.video_thread = threading.Thread(target=self.video_loop, daemon=True)
        self.video_thread.start()
        self.status.config(text=f"Playing video: {path}")

    def start_webcam(self):
        self.stop_video()
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Cannot open webcam.")
            return
        self.video_fps = 25
        self.running = True
        self.video_thread = threading.Thread(target=self.video_loop, daemon=True)
        self.video_thread.start()
        self.status.config(text="Webcam started")

    def stop_video(self):
        self.running = False
        if self.cap:
            self.cap.release()
        self.cap = None
        self.status.config(text="Stopped")

    def save_frame(self):
        if self.current_frame is None:
            messagebox.showinfo("Info", "No frame to save.")
            return
        path = filedialog.asksaveasfilename(title="Save frame", defaultextension=".png",
                                            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
        if path:
            cv2.imwrite(path, self.current_frame)
            self.status.config(text=f"Saved to {path}")

    def select_sticker(self):
        path = filedialog.askopenfilename(title="Select sticker (PNG)",
                                          filetypes=[("PNG files", "*.png")])
        if not path:
            return
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        if img is None or img.shape[2] < 4:
            messagebox.showerror("Error", "Sticker must be PNG with transparency.")
            return
        self.sticker_img = img
        self.status.config(text=f"Sticker loaded: {path}")

    # ------------------ Video Loop ------------------
    def video_loop(self):
        try:
            while self.running and self.cap.isOpened():
                ret, frame = self.cap.read()
                if not ret:
                    break
                self.process_and_show_frame(frame)
                time.sleep(1.0 / max(1, self.video_fps))
        finally:
            self.running = False
            if self.cap:
                self.cap.release()
            self.status.config(text="Stopped")

    # ------------------ Processing ------------------
    def process_and_show_frame(self, frame_bgr):
        gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
        faces = self.detector.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))
        out = frame_bgr.copy()
        strength = int(self.scale.get())

        for (x, y, w, h) in faces:
            x1, y1 = max(0, x), max(0, y)
            x2, y2 = min(out.shape[1], x + w), min(out.shape[0], y + h)
            roi = out[y1:y2, x1:x2]

            mode = self.mode.get()
            if mode == "BLUR":
                k = max(1, (strength // 2) * 2 + 1)
                out[y1:y2, x1:x2] = cv2.GaussianBlur(roi, (k, k), 0)
            elif mode == "PIXEL":
                small = cv2.resize(roi, (max(1, w // (strength//3 + 1)), max(1, h // (strength//3 + 1))))
                pixel = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
                out[y1:y2, x1:x2] = pixel
            elif mode == "STICKER" and self.sticker_img is not None:
                sticker = cv2.resize(self.sticker_img, (w, h), interpolation=cv2.INTER_AREA)
                out = self.overlay_png(out, sticker, x1, y1)

        self.current_frame = out.copy()

        # Show on GUI
        img_rgb = cv2.cvtColor(out, cv2.COLOR_BGR2RGB)
        imgtk = ImageTk.PhotoImage(Image.fromarray(img_rgb))
        self.canvas.imgtk = imgtk
        self.canvas.config(image=imgtk)

    def overlay_png(self, bg, fg, x, y):
        """Overlay RGBA sticker on BGR background."""
        h, w = fg.shape[:2]
        if fg.shape[2] < 4:
            return bg
        alpha = fg[:, :, 3] / 255.0
        for c in range(3):
            bg[y:y+h, x:x+w, c] = (1 - alpha) * bg[y:y+h, x:x+w, c] + alpha * fg[:, :, c]
        return bg

    def on_closing(self):
        self.stop_video()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = FaceAnonymizerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
