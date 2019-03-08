import cv2
import numpy as np
import time
import tkinter as tk
import PIL.Image, PIL.ImageTk

from videoCapture import VideoCapture
from canvas import Canvas
from slider import Slider

class App(tk.Frame):
    UPDATE_DELAY = 15

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.defaultVideoCapture = VideoCapture(0)

        self.webcamCanvas = Canvas(self.parent, self.defaultVideoCapture)
        self.maskCanvas = Canvas(self.parent, self.defaultVideoCapture)

        self.lowHueSlider = Slider(self.parent, "Low Hue", 0)
        self.highHueSlider = Slider(self.parent, "High Hue", 226)
        self.lowSaturationSlider = Slider(self.parent, "Low Saturation", 0)
        self.highSaturationSlider = Slider(self.parent, "High Saturation", 245)
        self.lowValueSlider = Slider(self.parent, "Low Value", 162)
        self.highValueSlider = Slider(self.parent, "High Value", 207)

        self.update()

    def update(self):
        brightRGB = cv2.COLOR_BGR2RGB
        brightLAB = cv2.COLOR_BGR2LAB
        brightHSV = cv2.COLOR_BGR2HSV
        brightYCB = cv2.COLOR_BGR2YCrCb

        isFrameRead, frame = self.defaultVideoCapture.getFrame(brightRGB)
        if isFrameRead:
            self.webcamCanvasPhoto = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.webcamCanvas.createImage(0, 0, self.webcamCanvasPhoto, tk.NW)

            isMaskFrameRead, maskFrame = self.defaultVideoCapture.getFrame(brightHSV)

            # get sliders positions
            lowHue = self.lowHueSlider.getValue()
            highHue = self.highHueSlider.getValue()
            lowSaturation = self.lowSaturationSlider.getValue()
            highSaturation = self.highSaturationSlider.getValue()
            lowValue = self.lowValueSlider.getValue()
            highValue = self.highValueSlider.getValue()

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            lower_hsv = np.array([lowHue, lowSaturation, lowValue])
            higher_hsv = np.array([highHue, highSaturation, highValue])
            mask = cv2.inRange(hsv, lower_hsv, higher_hsv)

            frame = cv2.bitwise_and(frame, frame, mask=mask)

            self.maskCanvasPhoto = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.maskCanvas.createImage(0, 0, self.maskCanvasPhoto, tk.NW)
        self.parent.after(self.UPDATE_DELAY, self.update)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("OpenCV Webcam HSV")
    root.resizable(0, 0)
    App(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
