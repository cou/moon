from pyramid.view import view_config
from pyramid.response import Response
import logging,os
log = logging.getLogger(__name__)
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
    title = request.params.get("title","")
    try:
        log.info("--start-- graph_generate")
        cur_path = os.path.dirname(__file__)
        log.debug(request.params)
        if "file" not in request.POST:
            path = "/static/pyramid.png"
            return {"path":path}
        filename = request.POST["file"].filename
        input_file = request.POST["file"].file
        gtype = request.params.get("type","binary")
        # Make plot with vertical (default) colorbar
        fig, ax = plt.subplots()
        
        csvfile = csv.reader(input_file)
        data = [map(float,d) for d in csvfile]
        cax = ax.imshow(data, interpolation='nearest', cmap=cm.__getattribute__(gtype))
        prop = fm.FontProperties(fname=cur_path+'/static/font/ipag.ttf')
        ax.set_title(title, fontproperties=prop)
        
        # Add colorbar, make sure to specify tick locations to match desired ticklabels
        cbar = fig.colorbar(cax, ticks=[-1, 0, 1])
        cbar.ax.set_yticklabels(['< -1', '0', '> 1'])# vertically oriented colorbar
        path = "/static/images/graph.png"
        fig.savefig(cur_path+path)
        log.info("--end-- graph_generate")
    except:
        log.exception("")
        path = "/static/pyramid.png"
    return {"path":path}
