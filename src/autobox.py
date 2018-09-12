#!/usr/bin/env python3
'''
Script for generating .svg finger-jointed boxes
All units are in mm
'''

# Imports
import sys
import os
from flask import Flask #pip3 install Flask
from flask import flash, redirect, render_template, request, session, abort, Response, send_from_directory

# Global variables
app = Flask(__name__)


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
        self.points.append({"x": i*self._wtabsize*2 + (offseta if i == 0 else 0),
                            "y": offseta})
        self.points.append({"x": i*self._wtabsize*2 + self._wtabsize,
                            "y": offseta})
        self.points.append({"x": i*self._wtabsize*2 + self._wtabsize, 
                            "y": offsetb})
        self.points.append({"x": i*self._wtabsize*2 + self._wtabsize*2 - (offseta if i == tabs-1 else 0) , 
                            "y": offsetb})

    for i in range(0, tabs):
        self.points.append({"x": W - offseta, 
                            "y": i*self._htabsize*2 + (offsetb if i == 0 else 0)})
        self.points.append({"x": W - offseta, 
                            "y": i*self._htabsize*2 + self._htabsize})
        self.points.append({"x": W - offsetb, 
                            "y": i*self._htabsize*2 + self._htabsize})
        self.points.append({"x": W - offsetb , 
                            "y": i*self._htabsize*2 + self._htabsize*2 - (offsetb if i == tabs-1 else 0)})
        
    for i in reversed(range(0, tabs)):
        self.points.append({"x": i*self._wtabsize*2 + self._wtabsize*2 - (offsetb if i == tabs-1 else 0), 
                            "y": H - offsetb})
        self.points.append({"x": i*self._wtabsize*2 + self._wtabsize, 
                            "y": H - offsetb})
        self.points.append({"x": i*self._wtabsize*2 + self._wtabsize, 
                            "y": H - offseta})
        self.points.append({"x": i*self._wtabsize*2 + (offsetb if i == 0 else 0), 
                            "y": H - offseta})

    for i in reversed(range(0, tabs)):
        self.points.append({"x": offsetb, 
                            "y": i*self._htabsize*2 + self._htabsize*2 - (offseta if i == tabs-1  else 0)})
        self.points.append({"x": offsetb, 
                            "y": i*self._htabsize*2 + self._htabsize})
        self.points.append({"x": offseta, 
                            "y": i*self._htabsize*2 + self._htabsize})
        self.points.append({"x": offseta, 
                            "y": i*self._htabsize*2 + (offseta if i == 0  else 0)})
        
#    self.points.append({"x": 0, "y": 0})

# Function declarations
def pointsToSvg(front, back, left, right, top, bottom):
    MARGIN = 10;
    #SHAPE="polyline";
    SHAPE="polygon";
    STYLE = 'fill:none; stroke:black; stroke-width:1';
    canvash = MARGIN+top.H+MARGIN+front.H+MARGIN+bottom.H
    canvasw = MARGIN+front.W+MARGIN+right.W+MARGIN+back.W+MARGIN+left.W+MARGIN
    
    result = '<?xml version="1.0" encoding="utf-8"?>'+'\n'
    result += '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" height="'+str(canvash)+'mm" width="'+str(canvasw)+'mm">'+'\n'
    #result += '<g transform="scale(35.43307)">'+'\n'
    
    result += '<g transform="translate('+str(MARGIN+front.W+MARGIN)+','+str(MARGIN)+')">'+'\n'
    result += '<'+SHAPE+' points="'
    for point in top.points:
        result += str(point["x"])+","+str(point["y"])+" "
    result += '" style="'+STYLE+'"/>'+'\n'
    result += '</g>'+'\n'
    
    result += '<g transform="translate('+str(MARGIN)+','+str(MARGIN+top.H+MARGIN)+')">'+'\n'
    result += '<'+SHAPE+' points="'
    for point in front.points:
        result += str(point["x"])+","+str(point["y"])+" "
    result += '" style="'+STYLE+'"/>'+'\n'
    result += '</g>'+'\n'

    result += '<g transform="translate('+str(MARGIN+front.W+MARGIN)+','+str(MARGIN+top.H+MARGIN)+')">'+'\n'
    result += '<'+SHAPE+' points="'
    for point in right.points:
        result += str(point["x"])+","+str(point["y"])+" "
    result += '" style="'+STYLE+'"/>'+'\n'
    result += '</g>'+'\n'

    result += '<g transform="translate('+str(MARGIN+front.W+MARGIN+right.W+MARGIN)+','+str(MARGIN+top.H+MARGIN)+')">'+'\n'
    result += '<'+SHAPE+' points="'
    for point in back.points:
        result += str(point["x"])+","+str(point["y"])+" "
    result += '" style="'+STYLE+'"/>'+'\n'
    result += '</g>'+'\n'

    result += '<g transform="translate('+str(MARGIN+front.W+MARGIN+right.W+MARGIN+back.W+MARGIN)+','+str(MARGIN+top.H+MARGIN)+')">'+'\n'
    result += '<'+SHAPE+' points="'
    for point in left.points:
        result += str(point["x"])+","+str(point["y"])+" "
    result += '" style="'+STYLE+'"/>'+'\n'
    result += '</g>'+'\n'
    
    result += '<g transform="translate('+str(MARGIN+front.W+MARGIN)+','+str(MARGIN+top.H+MARGIN+front.H+MARGIN)+')">'+'\n'
    result += '<'+SHAPE+' points="'
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
    return pointsToSvg(panels["front"],panels["front"],panels["side"],panels["side"],panels["top"],panels["top"])

def main():
    HEIGHT=30
    WIDTH=80
    LENGTH=150
    THICKNESS = 2
    with open('output.svg', 'w+') as f:
        f.write(box(H=HEIGHT, W=WIDTH, L=LENGTH, thickness = THICKNESS))

@app.route("/box.svg")
def makebox():
	return Response(box(H = float(request.args.get('H')),
                        W = float(request.args.get('W')),
                        L = float(request.args.get('L')),
                        thickness = (float(request.args.get('T')) if request.args.get('T') else 1.0),
						tabs = (int(request.args.get('tabs')) if request.args.get('tabs') else 4)),
                    mimetype='image/svg+xml')

@app.route("/")
def hello():
    return render_template('form.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Main body
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
    #main()
