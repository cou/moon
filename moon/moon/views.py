# coding: utf8
from pyramid.view import view_config
from pyramid.response import Response
from moon.libs import validation

import logging,os
log = logging.getLogger(__name__)
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from numpy.random import randn
import matplotlib.font_manager as fm 
import csv

@view_config(route_name='graph', renderer='templates/graph.pt')
def graph(request):
    graph_type = ['binary', 'Blues', 'BuGn', 'BuPu', 'gist_yarg',
        'GnBu', 'Greens', 'Greys', 'Oranges', 'OrRd',
        'PuBu', 'PuBuGn', 'PuRd', 'Purples', 'RdPu',
        'Reds', 'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd'
        'afmhot', 'autumn', 'bone', 'cool', 'copper',
        'gist_gray', 'gist_heat', 'gray', 'hot', 'pink',
        'spring', 'summer', 'winter'
        'BrBG', 'bwr', 'coolwarm', 'PiYG', 'PRGn', 'PuOr',
        'RdBu', 'RdGy', 'RdYlBu', 'RdYlGn', 'seismic'
        'Accent', 'Dark2', 'hsv', 'Paired', 'Pastel1',
        'Pastel2', 'Set1', 'Set2', 'Set3', 'spectral'
        'gist_earth', 'gist_ncar', 'gist_rainbow',
        'gist_stern', 'jet', 'brg', 'CMRmap', 'cubehelix',
        'gnuplot', 'gnuplot2', 'ocean', 'rainbow',
        'terrain', 'flag', 'prism']
    return {'project': 'moon','graph_type':graph_type}

@view_config(route_name='generate', renderer="templates/image.pt")
def generate(request):
    schema = validation.ValidateGraphGenerateForm()
    try:
        form = schema.to_python(request.params)
    except validation.Invalid,e:
        log.exception("")
        res = json.dumps({"res":"ng","error":e.msg})
        return Response(res)
    title = form["title"]
    gtype = form["graph_type"]
    graph_height = form["graph_height"]
    graph_width = form["graph_width"]
    canvas_height = form["canvas_height"]
    canvas_width = form["canvas_width"]
    minv = form["minv"]
    maxv = form["maxv"]
    splitnum = form["splitnum"]
    
    try:
        log.info("--start-- graph_generate")
        cur_path = os.path.dirname(__file__)
        if "file" not in request.POST:
            path = "/static/pyramid.png"
            return {"path":path}
        filename = request.POST["file"].filename
        input_file = request.POST["file"].file
        # Make plot with vertical (default) colorbar
        fig, ax = plt.subplots(figsize=(canvas_width, canvas_height),dpi=10)

        csvfile = csv.reader(input_file)
        #data = [map(float,d) for d in csvfile]
        data = []
        for i in csvfile:
            row = []
            for j in i:
                for width in range(graph_width):
                    v = float(j)
                    if v >=1200:
                        log.debug("@"*20)
                        log.debug(v)
                    v = minv if minv and minv>v else v
                    v = maxv if maxv and maxv<v else v
                    row.append(v)
            for height in range(graph_height):
                data.append(row)
        cax = ax.imshow(data, interpolation='nearest', cmap=cm.__getattribute__(gtype))
        prop = fm.FontProperties(fname=cur_path+'/static/font/ipag.ttf')
        ax.set_title(title, fontproperties=prop)
        
        # Add colorbar, make sure to specify tick locations to match desired ticklabels
        
        # グラフ表示用のデータ生成
        _min = min([j for i in data for j in i ])
        _max = max([j for i in data for j in i])
        _ave = (_min+_max)/2.0
        log.debug("min = %d"%_min)
        log.debug("max = %d"%_max)
        log.debug("ave = %d"%_ave)
        ticks = [_min]+[_min+d*(_max-_min)/float(splitnum) for d in range(1,splitnum)]+[_max]
        cbar = fig.colorbar(cax, ticks=ticks)
        cbar.ax.set_yticklabels(['%.3f'%t for t in ticks])# vertically oriented colorbar
        path = "/static/images/graph.png"
        fig.savefig(cur_path+path)
        log.info("--end-- graph_generate")
    except:
        log.exception("")
        path = "/static/pyramid.png"
    return {"path":path}
