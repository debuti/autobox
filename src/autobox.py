#!/usr/bin/env python3
'''
Script for generating .svg finger-jointed boxes
All units are in mm
'''

##TODO:
## - Fix when user requests 0 tabs
## - Fix document dimms when printed

# Imports
import sys
import os
from flask import Flask #pip3 install Flask
from flask import flash, redirect, render_template, request, session, abort, Response, send_from_directory

# Global variables
app = Flask(__name__)


# Class declarations
class Panel:
  def __init__(self, W, H, thickness, tabs, reverse = False, clearance = 0):
    self.W = W;
    self._wtabsize = W / (tabs*2) if (tabs>0) else W
    self.H = H;
    self._htabsize = H / (tabs*2) if (tabs>0) else H
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
        self.points.append({"x": i*self._wtabsize*2 + (offseta if i == 0 else 0) + ((-clearance if reverse else clearance) if i != 0 else 0),
                            "y": offseta})
        if (offseta != 0 and i!=0): self.drillPoints.append(self.points[-1])
        self.points.append({"x": i*self._wtabsize*2 + self._wtabsize + (clearance if reverse else -clearance),
                            "y": offseta})
        if (offseta != 0): self.drillPoints.append(self.points[-1])
        self.points.append({"x": i*self._wtabsize*2 + self._wtabsize + (clearance if reverse else -clearance), 
                            "y": offsetb})
        if (offsetb != 0): self.drillPoints.append(self.points[-1])
        self.points.append({"x": i*self._wtabsize*2 + self._wtabsize*2 - (offseta if i == tabs-1 else 0) + ((-clearance if reverse else clearance) if i != tabs-1 else 0), 
                            "y": offsetb})
        if (offsetb != 0 and i!=tabs-1): self.drillPoints.append(self.points[-1])

    for i in range(0, tabs):
        self.points.append({"x": W - offseta, 
                            "y": i*self._htabsize*2 + (offsetb if i == 0 else 0) + ((-clearance if reverse else clearance) if i != 0 else 0)})
        if (offseta != 0 and i!=0): self.drillPoints.append(self.points[-1])
        self.points.append({"x": W - offseta, 
                            "y": i*self._htabsize*2 + self._htabsize + (clearance if reverse else -clearance)})
        if (offseta != 0): self.drillPoints.append(self.points[-1])
        self.points.append({"x": W - offsetb, 
                            "y": i*self._htabsize*2 + self._htabsize + (clearance if reverse else -clearance)})
        if (offsetb != 0): self.drillPoints.append(self.points[-1])
        self.points.append({"x": W - offsetb , 
                            "y": i*self._htabsize*2 + self._htabsize*2 - (offsetb if i == tabs-1 else 0) + ((-clearance if reverse else clearance) if i != tabs-1 else 0)})
        if (offsetb != 0 and i!=tabs-1): self.drillPoints.append(self.points[-1])
        
    for i in reversed(range(0, tabs)):
        self.points.append({"x": i*self._wtabsize*2 + self._wtabsize*2 - (offsetb if i == tabs-1 else 0) + ((-clearance if reverse else clearance) if i != tabs-1 else 0), 
                            "y": H - offsetb})
        if (offsetb != 0 and i!=tabs-1): self.drillPoints.append(self.points[-1])
        self.points.append({"x": i*self._wtabsize*2 + self._wtabsize + (clearance if reverse else -clearance), 
                            "y": H - offsetb})
        if (offsetb != 0): self.drillPoints.append(self.points[-1])
        self.points.append({"x": i*self._wtabsize*2 + self._wtabsize + (clearance if reverse else -clearance), 
                            "y": H - offseta})
        if (offseta != 0): self.drillPoints.append(self.points[-1])
        self.points.append({"x": i*self._wtabsize*2 + (offsetb if i == 0 else 0) + ((-clearance if reverse else clearance) if i != 0 else 0),
                            "y": H - offseta})
        if (offseta != 0 and i!=0): self.drillPoints.append(self.points[-1])

    for i in reversed(range(0, tabs)):
        self.points.append({"x": offsetb, 
                            "y": i*self._htabsize*2 + self._htabsize*2 - (offseta if i == tabs-1  else 0) + ((-clearance if reverse else clearance) if i != tabs-1 else 0)})
        if (offsetb != 0 and i!=tabs-1): self.drillPoints.append(self.points[-1])
        self.points.append({"x": offsetb, 
                            "y": i*self._htabsize*2 + self._htabsize + (clearance if reverse else -clearance)})
        if (offsetb != 0): self.drillPoints.append(self.points[-1])
        self.points.append({"x": offseta, 
                            "y": i*self._htabsize*2 + self._htabsize + (clearance if reverse else -clearance)})
        if (offseta != 0): self.drillPoints.append(self.points[-1])
        self.points.append({"x": offseta, 
                            "y": i*self._htabsize*2 + (offseta if i == 0  else 0) + ((-clearance if reverse else clearance) if i != 0 else 0)})
        if (offseta != 0 and i != 0): self.drillPoints.append(self.points[-1])
        

# Function declarations

def panelToPath(panel, absx, absy, fliph=False, flipv=False, drillPoints = False):
    ind = '  '+'  '
    result =  ind + '<g transform="translate('+str(absx)+','+str(absy)+')">'+'\n'
    if fliph:
        result += ind + '  '+'<g transform="translate(0,'+str(panel.H)+') scale(1, -1)">'+'\n'
    if flipv:
        result += ind + '  '+'<g transform="translate('+str(panel.W)+',0) scale(-1, 1)">'+'\n'

    result += ind +'  '+'<path d="'
    for idx, point in enumerate(panel.points):
        if idx == 0: 
            result += "M"
        else:
            result += "L"
        result += str(point["x"])+" "+str(point["y"])+" "
    result += 'Z"/>'+'\n'

    if drillPoints:
        result += ind +'  '+'<g>'   +'\n'
        for point in panel.drillPoints:
            result += ind +'  '+'  '+'<circle cx="'+str(point["x"])+'" cy="'+str(point["y"])+'" r="2" stroke="red" fill="transparent" stroke-width="1"/>'+'\n'
        result += ind +'  '+'</g>'+'\n'     

    if fliph:
        result += ind +'  '+'</g>'+'\n'    
    if flipv:
        result += ind +'  '+'</g>'+'\n'    

    result += ind +'</g>'+'\n'
    return result

def pointsToSvg(front, back, left, right, top, bottom, opts):
    MARGIN = 10;

    canvash = MARGIN+top.H+MARGIN+front.H+MARGIN+bottom.H+MARGIN
    canvasw = MARGIN+front.W+MARGIN+right.W+MARGIN+back.W+MARGIN+left.W+MARGIN
    
    result = '<?xml version="1.0" encoding="utf-8"?>'+'\n'
    result = '<!-- Created with autobox (http://autobx.herokuapp.com/) -->'+'\n'

    result += '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="'+str(canvasw)+'" height="'+str(canvash)+'" viewbox="0 0 '+str(int(canvasw))+' '+str(int(canvash))+'">'+'\n'
    result += '  '+'<g fill="none" stroke="black" stroke-width="1">'     

    result += panelToPath(top, MARGIN+front.W+MARGIN, MARGIN, drillPoints = opts["drillPoints"])
    result += panelToPath(front, MARGIN, MARGIN+top.H+MARGIN, flipv=True, drillPoints = opts["drillPoints"])
    result += panelToPath(right, MARGIN+front.W+MARGIN, MARGIN+top.H+MARGIN, drillPoints = opts["drillPoints"])
    result += panelToPath(back, MARGIN+front.W+MARGIN+right.W+MARGIN, MARGIN+top.H+MARGIN, drillPoints = opts["drillPoints"])
    result += panelToPath(left, MARGIN+front.W+MARGIN+right.W+MARGIN+back.W+MARGIN, MARGIN+top.H+MARGIN, flipv=True, drillPoints = opts["drillPoints"])
    result += panelToPath(bottom, MARGIN+front.W+MARGIN, MARGIN+top.H+MARGIN+front.H+MARGIN, fliph=True, drillPoints = opts["drillPoints"])
    
    result += '  '+'</g>'+'\n'
    
    result += '</svg>'
    return result;
        

def box(H, W, L, thickness = 1, tabs = 4, clearance = 0, drillPoints=False):
    '''
    H, W and L are outer dimms of the requested box
    '''
    panels = {"front" : Panel(W, H, thickness, tabs, clearance = clearance),
              "side"  : Panel(L, H, thickness, tabs, reverse=True, clearance = clearance),
              "top"   : Panel(L, W, thickness, tabs, clearance = clearance)};
    return pointsToSvg(panels["front"],panels["front"],panels["side"],panels["side"],panels["top"],panels["top"], opts = {"drillPoints": drillPoints})


@app.route("/box.svg")
def makebox():
	return Response(box(H = float(request.args.get('H')),
                        W = float(request.args.get('W')),
                        L = float(request.args.get('L')),
                        thickness = (float(request.args.get('T')) if request.args.get('T') else 1.0),
						tabs = (int(request.args.get('tabs')) if request.args.get('tabs') else 4),
                        clearance = (float(request.args.get('clearance')) if request.args.get('clearance') else 0.0),
                        drillPoints = (True if request.args.get('gendrill') and request.args.get('gendrill') == "on" else False)
                        ),
                    mimetype='image/svg+xml')

@app.route("/")
def hello():
    return render_template('form.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


def main():
    '''
    When called from cli
    '''
    HEIGHT=30
    WIDTH=80
    LENGTH=150
    THICKNESS = 2
    with open('output.svg', 'w+') as f:
        f.write(box(H=HEIGHT, W=WIDTH, L=LENGTH, thickness = THICKNESS))


# Main body
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
    #main()
