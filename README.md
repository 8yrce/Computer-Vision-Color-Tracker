# Color Based Object Detection

![](color-tracker.gif)

## Track any unknown object of interest instantly realtime!
By averaging the color values of regions of an image our program can discern a selected object from the background and track it. This allows us the ability to perform basic computer vision without the need to train a new model for each new object we want to track.

## Why make this project?
While libraries exist with similair object detection functionality, I wanted to challenge myself to create a computer vision system using only what I could create. With the exception of using OpenCV to grab images from the camera and update the display this program is completely independent of any computer vision libraries.

## Requirements: 
- OpenCv=Latest ( Just for grabbing images and updating screen )
- statistics
- time


## How to use:

```
python3 color-tracker.py
```

For best experience try and use solid color, simple and consistently lit objects. As this program is not yet as refined as some big name computer vision libraries.


## What each py file does:
- color-tracker.py: Tracks an object by color using a handmade computer vision system. 

## Build status:
Current Status:
- [] Undergoing changes
- [X] Working


