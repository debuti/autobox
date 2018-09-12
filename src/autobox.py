#!/usr/bin/env python3
'''
Script for generating .svg finger-jointed boxes
All units are in mm
'''

# Imports
import sys
import os

# Global variables

# Class declarations
class Panel:
  def __init__(self, W, H, thickness, tabs, reverse = False):
    self.W = W;
    self._wtabsize = W / (tabs*2)
    self.H = H;
    self._htabsize = H / (tabs*2)
    self.T = thickness;

    if (reverse):
        offseta = thickness
        offsetb = 0
    else:
        offseta = 0
        offsetb = thickness
        
    self.drillPoints = [];
    self.points = [];
    for i in range(0, tabs):
        self.points.append({"x": i*self._wtabsize*2, "y": offseta})
        self.points.append({"x": i*self._wtabsize*2 + self._wtabsize, "y": offseta})
        self.points.append({"x": i*self._wtabsize*2 + self._wtabsize, "y": offsetb})
        self.points.append({"x": i*self._wtabsize*2 + self._wtabsize*2 , "y": offsetb})

    for i in range(0, tabs):
        self.points.append({"x": W - offseta, "y": i*self._htabsize*2})
        self.points.append({"x": W - offseta, "y": i*self._htabsize*2 + self._htabsize})
        self.points.append({"x": W - offsetb, "y": i*self._htabsize*2 + self._htabsize})
        self.points.append({"x": W - offsetb , "y": i*self._htabsize*2 + self._htabsize*2})
        
    for i in reversed(range(0, tabs)):
        self.points.append({"x": i*self._wtabsize*2 + self._wtabsize*2 , "y": H - offsetb})
        self.points.append({"x": i*self._wtabsize*2 + self._wtabsize, "y": H - offsetb})
        self.points.append({"x": i*self._wtabsize*2 + self._wtabsize, "y": H - offseta})
        self.points.append({"x": i*self._wtabsize*2, "y": H - offseta})

    for i in reversed(range(0, tabs)):
        self.points.append({"x": offsetb , "y": i*self._htabsize*2 + self._htabsize*2})
        self.points.append({"x": offsetb, "y": i*self._htabsize*2 + self._htabsize})
        self.points.append({"x": offseta, "y": i*self._htabsize*2 + self._htabsize})
        self.points.append({"x": offseta, "y": i*self._htabsize*2})
        
    #self.points.append({"x": W, "y": H})
    #self.points.append({"x": 0, "y": H})
    self.points.append({"x": 0, "y": 0})

# Function declarations
def pointsToSvg(front, back, left, right, top, bottom):
    MARGIN = 10;
    STYLE = 'fill:none; stroke:black; stroke-width:1';
    canvash = MARGIN+top.H+MARGIN+front.H+MARGIN+bottom.H
    canvasw = MARGIN+front.W+MARGIN+right.W+MARGIN+back.W+MARGIN+left.W+MARGIN
    
    result = '<?xml version="1.0" encoding="utf-8"?>'+'\n'
    #result += '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">'+'\n'
    result += '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" height="'+str(canvash)+'mm" width="'+str(canvasw)+'mm">'+'\n'
    #result += '<g transform="scale(35.43307)">'+'\n'
    
    result += '<g transform="translate('+str(MARGIN+front.W+MARGIN)+','+str(MARGIN)+')">'+'\n'
    result += '<polyline points="'
    for point in top.points:
        result += str(point["x"])+","+str(point["y"])+" "
    result += '" style="'+STYLE+'"/>'+'\n'
    result += '</g>'+'\n'
    
    result += '<g transform="translate('+str(MARGIN)+','+str(MARGIN+top.H+MARGIN)+')">'+'\n'
    result += '<polyline points="'
    for point in front.points:
        result += str(point["x"])+","+str(point["y"])+" "
    result += '" style="'+STYLE+'"/>'+'\n'
    result += '</g>'+'\n'

    result += '<g transform="translate('+str(MARGIN+front.W+MARGIN)+','+str(MARGIN+top.H+MARGIN)+')">'+'\n'
    result += '<polyline points="'
    for point in right.points:
        result += str(point["x"])+","+str(point["y"])+" "
    result += '" style="'+STYLE+'"/>'+'\n'
    result += '</g>'+'\n'

    result += '<g transform="translate('+str(MARGIN+front.W+MARGIN+right.W+MARGIN)+','+str(MARGIN+top.H+MARGIN)+')">'+'\n'
    result += '<polyline points="'
    for point in back.points:
        result += str(point["x"])+","+str(point["y"])+" "
    result += '" style="'+STYLE+'"/>'+'\n'
    result += '</g>'+'\n'

    result += '<g transform="translate('+str(MARGIN+front.W+MARGIN+right.W+MARGIN+back.W+MARGIN)+','+str(MARGIN+top.H+MARGIN)+')">'+'\n'
    result += '<polyline points="'
    for point in left.points:
        result += str(point["x"])+","+str(point["y"])+" "
    result += '" style="'+STYLE+'"/>'+'\n'
    result += '</g>'+'\n'
    
    result += '<g transform="translate('+str(MARGIN+front.W+MARGIN)+','+str(MARGIN+top.H+MARGIN+front.H+MARGIN)+')">'+'\n'
    result += '<polyline points="'
    for point in top.points:
        result += str(point["x"])+","+str(point["y"])+" "
    result += '" style="'+STYLE+'"/>'+'\n'
    result += '</g>'+'\n'
    
    #result += '</g>'+'\n'
    result += '</svg>'
    return result;
        

def box(H, W, L, thickness = 1, tabs = 4):
    '''
    H, W and L are outer dimms of the requested box
    '''
    panels = {"front" : Panel(W, H, thickness, tabs),
              "side"  : Panel(L, H, thickness, tabs, reverse=True),
              "top"   : Panel(L, W, thickness, tabs)};
    with open('output.svg', 'w+') as f:
        f.write(pointsToSvg(panels["front"],panels["front"],panels["side"],panels["side"],panels["top"],panels["top"]))

def main():
    HEIGHT=30
    WIDTH=80
    LENGTH=150
    THICKNESS = 2
    box(H=HEIGHT, W=WIDTH, L=LENGTH, thickness = THICKNESS)

# Main body
if __name__ == '__main__':
    main()
