#!/usr/bin/env python3
"""
Script for generating .svg finger-jointed boxes
All units are in mm
"""

# Imports
import sys
import os

# Global variables

# Class declarations

# Function declarations
def pointsToSvg(front, back, left, right, top, bottom):
    MARGIN = 10;
    STYLE = 'fill:none; stroke:black; stroke-width:1';
    canvash = MARGIN+top[2]["y"]+MARGIN+front[2]["y"]+MARGIN+bottom[2]["y"]
    canvasw = MARGIN+front[2]["x"]+MARGIN+right[2]["x"]+MARGIN+back[2]["x"]+MARGIN+left[2]["x"]+MARGIN
    
    result = '<?xml version="1.0" encoding="utf-8"?>'+'\n'
    #result += '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">'+'\n'
    result += '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" height="'+str(canvash)+'mm" width="'+str(canvasw)+'mm">'+'\n'
    #result += '<g transform="scale(35.43307)">'+'\n'
    
    result += '<g transform="translate('+str(MARGIN+front[2]["x"]+MARGIN)+','+str(MARGIN)+')">'+'\n'
    result += '<polyline points="'
    for point in top:
        result += str(point["x"])+","+str(point["y"])+" "
    result += '" style="'+STYLE+'"/>'+'\n'
    result += '</g>'+'\n'
    
    result += '<g transform="translate('+str(MARGIN)+','+str(MARGIN+top[2]["y"]+MARGIN)+')">'+'\n'
    result += '<polyline points="'
    for point in front:
        result += str(point["x"])+","+str(point["y"])+" "
    result += '" style="'+STYLE+'"/>'+'\n'
    result += '</g>'+'\n'

    result += '<g transform="translate('+str(MARGIN+front[2]["x"]+MARGIN)+','+str(MARGIN+top[2]["y"]+MARGIN)+')">'+'\n'
    result += '<polyline points="'
    for point in right:
        result += str(point["x"])+","+str(point["y"])+" "
    result += '" style="'+STYLE+'"/>'+'\n'
    result += '</g>'+'\n'

    result += '<g transform="translate('+str(MARGIN+front[2]["x"]+MARGIN+right[2]["x"]+MARGIN)+','+str(MARGIN+top[2]["y"]+MARGIN)+')">'+'\n'
    result += '<polyline points="'
    for point in back:
        result += str(point["x"])+","+str(point["y"])+" "
    result += '" style="'+STYLE+'"/>'+'\n'
    result += '</g>'+'\n'

    result += '<g transform="translate('+str(MARGIN+front[2]["x"]+MARGIN+right[2]["x"]+MARGIN+back[2]["x"]+MARGIN)+','+str(MARGIN+top[2]["y"]+MARGIN)+')">'+'\n'
    result += '<polyline points="'
    for point in left:
        result += str(point["x"])+","+str(point["y"])+" "
    result += '" style="'+STYLE+'"/>'+'\n'
    result += '</g>'+'\n'
    
    result += '<g transform="translate('+str(MARGIN+front[2]["x"]+MARGIN)+','+str(MARGIN+top[2]["y"]+MARGIN+front[2]["y"]+MARGIN)+')">'+'\n'
    result += '<polyline points="'
    for point in top:
        result += str(point["x"])+","+str(point["y"])+" "
    result += '" style="'+STYLE+'"/>'+'\n'
    result += '</g>'+'\n'
    
    #result += '</g>'+'\n'
    result += '</svg>'
    return result;
        
def createPanel(W, H):
    points = [];
    points.append({"x": 0, "y": 0})
    points.append({"x": W, "y": 0})
    points.append({"x": W, "y": H})
    points.append({"x": 0, "y": H})
    points.append({"x": 0, "y": 0})
    return points

def box(H, W, L, thickness = 1):
    panels = [];
    panels.append(createPanel(W, H))
    panels.append(createPanel(L, H))
    panels.append(createPanel(L, W))
    with open('output.svg', 'w+') as f:
        f.write(pointsToSvg(panels[0],panels[0],panels[1],panels[1],panels[2],panels[2]))

def main():
    HEIGHT=30
    WIDTH=80
    LENGTH=150
    box(H=HEIGHT, W=WIDTH, L=LENGTH)

# Main body
if __name__ == '__main__':
    main()
