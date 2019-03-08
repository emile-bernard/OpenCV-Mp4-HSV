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

    BRIGHT_RGB = cv2.COLOR_BGR2RGB
    BRIGHT_HSV = cv2.COLOR_BGR2HSV

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.defaultVideoCapture = VideoCapture(0)

        self.webcamCanvas = Canvas(self.parent, self.defaultVideoCapture)
        self.maskCanvas = Canvas(self.parent, self.defaultVideoCapture)

        self.lowHueSlider = Slider(self.parent, "Low Hue", 10, 0, 180)
        self.highHueSlider = Slider(self.parent, "High Hue", 25, 0, 180)
        self.lowSaturationSlider = Slider(self.parent, "Low Saturation", 100, 0, 255)
        self.highSaturationSlider = Slider(self.parent, "High Saturation", 255, 0, 255)
        self.lowValueSlider = Slider(self.parent, "Low Value", 20, 0, 255)
        self.highValueSlider = Slider(self.parent, "High Value", 255, 0, 255)

        self.updateFrame()

    def updateFrame(self):
        isFrameRead, frame = self.defaultVideoCapture.getFrame(self.BRIGHT_RGB)
        if isFrameRead:
            self.webcamCanvasPhoto = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.webcamCanvas.createImage(0, 0, self.webcamCanvasPhoto, tk.NW)

            self.updateMask(frame)
        self.parent.after(self.UPDATE_DELAY, self.updateFrame)

    def updateMask(self, frame):
        isMaskFrameRead, maskFrame = self.defaultVideoCapture.getFrame(self.BRIGHT_HSV)

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

        frame = cv2.bitwise_and(frame, frame, mask = mask)

        # countour features
        # ret, thresh = cv2.threshold(frame, 127, 255, 0)
        # contours, hierarchy = cv2.findContours(thresh, 1, 2)
        #
        # cnt = contours[0]
        #
        # epsilon = 0.1 * cv2.arcLength(cnt, True)
        # approx = cv2.approxPolyDP(cnt, epsilon, True)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(5,5),0)
        ret, thresh_img = cv2.threshold(blur,91,255,cv2.THRESH_BINARY)
        contours =  cv2.findContours(thresh_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[-2]
        for c in contours:
            cv2.drawContours(frame, [c], -1, (0,255,0), 3)




        self.maskCanvasPhoto = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
        self.maskCanvas.createImage(0, 0, self.maskCanvasPhoto, tk.NW)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("OpenCV Webcam HSV")
    root.resizable(0, 0)
    App(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
