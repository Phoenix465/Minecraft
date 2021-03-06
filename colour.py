"""
Handler for the Colour

Class
-----
Colour - Handles a RGB/HSV Colour
"""

import colorsys
from errors import *


class Colour:
    """
    This Class handle a Single Colour

    Parameters
    ----------
    r : float
        The Red of RGB or the Hue of HSV (isHSV has to be True)

    g : float
        The Green of RGB or the Saturation of HSV (isHSV has to be True)

    b : float
        The Blue of RGB or the Value of HSV (isHSV has to be True)

    isHSV : bool
        A bool representing whether the values given are HSV

    convertToDecimal : bool
        A bool representing whether the r, b, b values should be divided by 255

    Attributes
    ----------
    _observers : list
        A list containing the functions that are called when the values are updated

    _r : float
        The Hidden Red (In Decimal Form)

    _g : float
        The Hidden Green (In Decimal Form)

    _b : float
        The Hidden Blue (In Decimal Form)

    _h : float
        The Hidden Hue (In Decimal Form)

    _s : float
        The Hidden Saturation (In Decimal Form)

    _v : float
        The Hidden Value (In Decimal Form)
        
    RGBList : list
        A list containing the RGB values
    
    HSVList : list
            A list containing the HSV values

    RGBTuple : float
            A tuple containing the RGB values

    HSVTuple : float
            A tuple containing the HSV values
    """

    def __init__(self, r, g, b, isHSV=False,  convertToDecimal=False):
        if type(r) != int and type(r) != float:
            raise ColourError("R/H Has To Be Of Class int/float")
        if type(g) != int and type(g) != float:
            raise ColourError("G/S Has To Be Of Class int/float")
        if type(b) != int and type(b) != float:
            raise ColourError("B/V Has To Be Of Class int/float")

        if convertToDecimal:
            r /= 255
            g /= 255
            b /= 255

        if r > 1 or r < 0:
            raise ColourError("R/H Has To Be Between 0 & 1")
        if g > 1 or g < 0:
            raise ColourError("G/S Has To Be Between 0 & 1")
        if b > 1 or b < 0:
            raise ColourError("B/V Has To Be Between 0 & 1")

        self._observers = []

        if not isHSV:
            self._r = r
            self._g = g
            self._b = b

            self._h, self._s, self._v = colorsys.rgb_to_hsv(r, g, b)

        else:
            self._h = r
            self._s = g
            self._v = b
            self._r, self._g, self._b = colorsys.hsv_to_rgb(r, g, b)

        self.RGBList = [self.r, self.g, self.b]
        self.HSVList = [self.h, self.s, self.v]
        self.RGBTuple = tuple(self.RGBList)
        self.HSVTuple = tuple(self.HSVList)

        self.bindTo(self.updateRGBList)
        self.bindTo(self.updateRGBTuple)
        self.bindTo(self.updateHSVList)
        self.bindTo(self.updateHSVTuple)

    @property
    def r(self):
        return self._r

    @property
    def g(self):
        return self._g

    @property
    def b(self):
        return self._b

    @property
    def h(self):
        return self._h

    @property
    def s(self):
        return self._s

    @property
    def v(self):
        return self._v
    
    @r.setter
    def r(self, newVal):
        self._r = newVal

        for callback in self._observers:
            #print("Changed")
            callback(self._r)

    @g.setter
    def g(self, newVal):
        self._g = newVal

        for callback in self._observers:
            #print("Changed")
            callback(self._g)
            
    @b.setter
    def b(self, newVal):
        self._b = newVal

        for callback in self._observers:
            #print("Changed")
            callback(self._b)

    @h.setter
    def h(self, newVal):
        self._h = newVal

        for callback in self._observers:
            #print("Changed")
            callback(self._h)
            
    @s.setter
    def s(self, newVal):
        self._s = newVal

        for callback in self._observers:
            #print("Changed")
            callback(self._s)

    @v.setter
    def v(self, newVal):
        self._v = newVal

        for callback in self._observers:
            #print("Changed")
            callback(self._v)

    def bindTo(self, callback):
        # print("Binding")
        self._observers.append(callback)

    def updateRGBList(self):
        self.RGBList = [self.r, self.g, self.b]

    def updateHSVList(self):
        self.HSVList = [self.h, self.s, self.v]

    def updateRGBTuple(self):
        self.RGBTuple = tuple(self.RGBList)

    def updateHSVTuple(self):
        self.HSVTuple = tuple(self.HSVList)


