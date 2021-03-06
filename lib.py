import math
import random 

import numpy as np
from PIL import Image, ImageDraw


class kandinskyShape:
  def __init__(self):
          self.shape = "circle"
          self.color = "red"
          self.x     = 0.5
          self.y     = 0.5
          self.size  = 0.5
  
  def __str__(self):  
      return "%s %s %3.1f (%4.2f, %4.2f)"%(self.color, self.shape, self.size, self.x, self.y)
      #return self.color + " " +  self.shape + " (" + \
      #       str(self.size) + "," + str(self.x) + "," + str(self.y) + ")"

class SimpleUniverse:
   kandinsky_colors = ['red','yellow', 'blue']
   kandinsky_shapes = ['square', 'circle', 'triangle']

class ExtendedUniverse:
   # still have to add drawing functions below 
   kandinsky_colors = ['red', 'yellow', 'blue', "green", "orange"]
   kandinsky_shapes = ['square', 'circle', 'triangle', "star"]


def square (d,cx,cy,s,f):
        s = 0.7 * s
        d.rectangle(((cx-s/2, cy-s/2), (cx+s/2, cy+s/2)), fill=f)

def circle (d,cx,cy,s,f):
        # correct the size to  the same area as an square
        s = 0.7 * s * 4 / math.pi 
        d.ellipse(((cx-s/2, cy-s/2), (cx+s/2, cy+s/2)), fill=f)

def triangle (d,cx,cy,s,f):
        r = math.radians(30)
        # correct the size to  the same area as an square
        s = 0.7 * s * 3 * math.sqrt(3) / 4
        dx = s * math.cos (r) / 2
        dy = s * math.sin (r) / 2
        d.polygon([(cx,cy-s/2), (cx+dx, cy+dy), (cx-dx,cy+dy)], fill = f)

def triangle2 (d,cx,cy,s,f):        
        # correct the size to  the same area as an square
        s = s * 0.9
        corners = 3

        points = list()
        for e in range(corners):
          r = math.radians(360/corners*e)
          dx = s * math.cos (r) / 2
          dy = s * math.sin (r) / 2
          p =  (cx+dx , cy+dy)
          points.append(p)

        d.polygon(p, fill = f)

def star (d,cx,cy,s,f):        
        corners = 5
        points = list()
        for e in range(corners):
          r = math.radians(360/corners*e)
          dx = s * math.cos (r) / 2
          dy = s * math.sin (r) / 2
          p =  (cx+dx , cy+dy)
          points.append(p)

          r = math.radians(360/corners*e+360/corners/2)
          dx = s * math.cos (r) / 5
          dy = s * math.sin (r) / 5                    
          p =  (cx+dx , cy+dy)
          points.append(p)

        d.polygon(points, fill = f)       


def kandinskyFigureAsImage (shapes, width=220, subsampling = 2):
  image = Image.new("RGB", (subsampling*width,subsampling*width), (width,width,width))
  d = ImageDraw.Draw(image)
  w = subsampling * width

  for s in shapes:
      globals()[s.shape]( d, w*s.x, w*s.y, w*s.size, s.color)
  if subsampling>1:
    image.thumbnail( (width,width), Image.ANTIALIAS)

  return image

def overlaps(shapes, width=64):
  image = Image.new("L", (width,width), 0)
  sumarray = np.array(image)
  d = ImageDraw.Draw(image)
  w = width

  for s in shapes:
    image      = Image.new("L", (width,width), 0)
    d = ImageDraw.Draw(image)
    globals()[s.shape]( d, w*s.x, w*s.y, w*s.size, 10)
    sumarray = sumarray + np.array(image)

  sumimage = Image.fromarray (sumarray)
  return sumimage.getextrema ()[1] > 10

def _randomobject(colors, shapes, minsize = 0.1, maxsize = 0.5):
    o = kandinskyShape()
    o.color = random.choice (colors)
    o.shape = random.choice (shapes)
    o.size  = minsize +  (maxsize-minsize) * random.random ()
    o.x     = o.size/2 + random.random () * (1-o.size )
    o.y     = o.size/2 + random.random () * (1-o.size )
    return o
    
def RandomFigure(render_size=(200, 200), obj_size=(.1, .6), obj_count=(2, 15), colors=['red', 'green'], shapes='circle', overlap_render_size=128):
    kf = []
    kftemp = []
    n = random.randint (obj_count[0],obj_count[1])    

    minsize = 0.1
    if n == 3: minsize = 0.2
    if n == 2: minsize = 0.3
    if n == 1: minsize = 0.4
    
    maxsize = 0.6
    if n == 5: maxsize = 0.4
    if n == 6: maxsize = 0.3
    if n == 7: maxsize = 0.2
    if n > 7: maxsize = 0.15
    #    m = n-7
    #    maxsize = 0.2 - m * (0.2)/70.0 

    if maxsize < 0.001: maxsize =  0.001
    if minsize > maxsize: minsize =  maxsize

    # print (n, minsize, maxsize)
    i = 0
    maxtry= 20
    while i<n:
        kftemp = kf
        t = 0
        o = _randomobject(colors, shapes, minsize, maxsize)
        kftemp = kf[:]
        kftemp.append (o)
        while overlaps(kftemp, width=overlap_render_size) and (t < maxtry):
            o = _randomobject(colors, shapes, minsize, maxsize)
            kftemp = kf[:]
            kftemp.append (o)
            t = t + 1
        if (t < maxtry):
            kf = kftemp[:]
            i = i + 1
        else: 
            maxsize = maxsize*0.95
            minsize = minsize*0.95
    return kf

class Figure:
    def __init__(self):        
        self.f = RandomFigure(
            obj_count=(2, 15), 
            colors=['red','yellow', 'blue'],
            shapes=['circle'])

    def render(self):
        return kandinskyFigureAsImage(self.f)

    def save(self, path):
        return kandinskyFigureAsImage(self.f).save(path)

import matplotlib.pyplot as plt
def plot_history(history, ):
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')
    plt.show()

    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')
    plt.show()

def plot_history_categorical(history):
    def plot_metric(m, readable):
        plt.plot(history[m])
        plt.plot(history['val_%s'%m])
        plt.title('Model %s'%readable)
        plt.ylabel(readable)
        plt.xlabel('Epoch')
        plt.legend(['Train', 'Validation'], loc='upper left')
        plt.show()
    
    plot_metric('categorical_accuracy', 'Accuracy')
    plot_metric('loss', 'Loss')
