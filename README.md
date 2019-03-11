# OpenCV-Mp4-HSV
This project contains a basic python script to run opencv-python with an HSV mask applied to a webcam stream. Also, it uses the opencv contours methods to draw contours on the HVS mask.

## Previews
![Preview1](./preview/Preview1.PNG?raw=true "Preview1")
![Preview2](./preview/Preview2.PNG?raw=true "Preview2")

## How it work's

HSV is a color space that attempts to represent colors the way humans perceive it. It stores color information in a cylindrical representation of RGB color points. HSV is useful in computer vision for color segmentation.

![Doc1](./documentation/Doc1.PNG?raw=true "Doc1")

The HSV color space components:

  H – Hue (Dominant Wavelength/Color) [0-180].

  S – Saturation (Purity/shades of the color) [0-255].
  
  V – Value (Brightness/Intensity) [0-255].

In the HSV color space only the Hue (H) channel describes color.

## How to setup
- Install opencv-python
```
$ pip install opencv-python
```

- Install tkinter
```
$ pip install tkinter
```

- Install pillow
```
$ pip install pillow
```

- Install numpy
```
$ pip install numpy
```

- Install matplotlib
```
$ pip install matplotlib
```

## How to run
- Run
```
$ python ./app.py
```

## Links
- [Python Patterns - Github](https://github.com/faif/python-patterns)
- [Python Design Patterns: For Sleek And Fashionable Code](https://www.toptal.com/python/python-design-patterns)
- [Python Tkinter](https://www.javatpoint.com/python-tkinter)
- [Python Opencv show video in tkinter window](https://solarianprogrammer.com/2018/04/21/python-opencv-show-video-tkinter-window/)
- [Tkinter layout management](https://www.python-course.eu/tkinter_layout_management.php)
- [Python gui tkinter](https://www.geeksforgeeks.org/python-gui-tkinter/)
- [Color spaces in opencv](https://www.learnopencv.com/color-spaces-in-opencv-cpp-python/)
- [HSV color picker](https://alloyui.com/examples/color-picker/hsv)
