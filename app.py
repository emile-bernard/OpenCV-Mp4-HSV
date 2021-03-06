import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import colors
from mpl_toolkits.mplot3d import Axes3D
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

        self.button = tk.Button(self.parent, text="Get histogram", fg="blue", command=self.drawHSVHHistogram)
        self.button.pack(anchor=tk.CENTER)

        self.updateFrame()

    def updateFrame(self):
        isFrameRead, frame = self.defaultVideoCapture.getFrame(self.BRIGHT_RGB)
        if isFrameRead:
            self.webcamCanvasPhoto = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.webcamCanvas.createImage(0, 0, self.webcamCanvasPhoto, tk.NW)
            self.updateMask(frame)
        self.parent.after(self.UPDATE_DELAY, self.updateFrame)

    def drawHSVHHistogram(self):
        isFrameRead, frame = self.defaultVideoCapture.getFrame(self.BRIGHT_RGB)

        pixelColors = frame.reshape((np.shape(frame)[0]*np.shape(frame)[1], 3))
        norm = colors.Normalize(vmin=-1.,vmax=1.)
        norm.autoscale(pixelColors)
        pixelColors = norm(pixelColors).tolist()
        hsvFrame = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        h, s, v = cv2.split(hsvFrame)
        fig = plt.figure()

        axis = fig.add_subplot(1, 1, 1, projection = "3d")
        axis.scatter(h.flatten(), s.flatten(), v.flatten(), facecolors = pixelColors, marker = ".")
        axis.set_xlabel("Hue")
        axis.set_ylabel("Saturation")
        axis.set_zlabel("Value")

        plt.show()

    def updateMask(self, frame):
        isMaskFrameRead, maskFrame = self.defaultVideoCapture.getFrame(self.BRIGHT_HSV)

        lowHue = self.lowHueSlider.getValue()
        highHue = self.highHueSlider.getValue()
        lowSaturation = self.lowSaturationSlider.getValue()
        highSaturation = self.highSaturationSlider.getValue()
        lowValue = self.lowValueSlider.getValue()
        highValue = self.highValueSlider.getValue()

        lower_hsv = np.array([lowHue, lowSaturation, lowValue])
        higher_hsv = np.array([highHue, highSaturation, highValue])

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_hsv, higher_hsv)

        frame = cv2.bitwise_and(frame, frame, mask = mask)

        #contour features
        self.drawContours(frame)

        self.maskCanvasPhoto = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
        self.maskCanvas.createImage(0, 0, self.maskCanvasPhoto, tk.NW)

    def drawContours(self, frame):
        grayImg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        retValue, threshImg = cv2.threshold(grayImg, 91, 255, cv2.THRESH_BINARY)
        contours =  cv2.findContours(threshImg,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]
        for c in contours:
            cv2.drawContours(frame, [c], 0, (255,0,0), 2)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("OpenCV Webcam HSV")
    root.resizable(0, 0)
    App(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
