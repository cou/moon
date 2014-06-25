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

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'moon'}

@view_config(route_name='graph', renderer='templates/graph.pt')
def graph(request):
    return {'project': 'moon'}

@view_config(route_name='generate', renderer="templates/image.pt")
def generate(request):
    title = request.params.get("title","")
    try:
        cur_path = os.path.dirname(__file__)
        filename = request.POST["file"].filename
        input_file = request.POST["file"].file
        
        # Make plot with vertical (default) colorbar
        fig, ax = plt.subplots()
        
        csvfile = csv.reader(input_file)
        data = [map(float,d) for d in csvfile]
        cax = ax.imshow(data, interpolation='nearest', cmap=cm.cool)
        prop = fm.FontProperties(fname=cur_path+'/static/font/ipag.ttf')
        ax.set_title(title, fontproperties=prop)
        
        # Add colorbar, make sure to specify tick locations to match desired ticklabels
        cbar = fig.colorbar(cax, ticks=[-1, 0, 1])
        cbar.ax.set_yticklabels(['< -1', '0', '> 1'])# vertically oriented colorbar
        path = "/static/images/graph.png"
        fig.savefig(cur_path+path)
    except:
        log.exception("")
        path = "/static/pyramid.png"
    return {"path":path}
