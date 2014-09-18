# coding: utf8
from pyramid.view import view_config
from pyramid.response import Response,FileResponse
from moon.libs import validation

import logging,os
log = logging.getLogger(__name__)
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.font_manager as fm
import csv
import StringIO

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

@view_config(route_name='generate')
def generate(request):
    schema = validation.ValidateGraphGenerateForm()
    try:
        form = schema.to_python(request.params)
    except validation.Invalid,e:
        log.exception("")
        return Response(e.msg)
    title = form["title"]
    filename = form["file"].filename
    input_file = form["file"].file
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
        data = []
        #log.debug(input_file)
        csvfile = csv.reader(input_file)
        for i in csvfile:
            row = []
            for j in i:
                for width in range(graph_width):
                    v = float(j)
                    v = minv if minv and minv>v else v
                    v = maxv if maxv and maxv<v else v
                    row.append(v)
            for height in range(graph_height):
                data.append(row)
        fig, ax = plt.subplots(figsize=(canvas_width, canvas_height),dpi=10)
        cax = ax.imshow(data, interpolation='nearest', cmap=cm.__getattribute__(gtype))
        cur_path = os.path.dirname(__file__)
        prop = fm.FontProperties(fname=cur_path+'/static/fonts/ipag.ttf')
        ax.set_title(title, fontproperties=prop)
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

        imgdata = StringIO.StringIO()
        fig.savefig(imgdata,format='png')
        imgdata.seek(0)
        log.info("--end-- graph_generate")
    except Exception,e:
        log.exception("")
        return Response("%s"%e)
    return Response(imgdata.read(),content_type="image/png")
