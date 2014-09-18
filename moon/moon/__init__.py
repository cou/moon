# coding: utf8
import sys
reload(sys)
sys.setdefaultencoding("utf8")

from pyramid.config import Configurator

# ウェブヘルパーをテンプレートで使えるようにする
from pyramid.events import BeforeRender
from webhelpers.html import tags
def add_renderer_globals(event):
   event['h'] = tags

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_subscriber(add_renderer_globals, BeforeRender)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=0)
    config.include('pyramid_scss')
    config.add_route('css', '/css/{css_path:.*}.css')
    config.add_view(route_name='css', view='pyramid_scss.controller.get_scss', renderer='scss',request_method='GET')
    config.add_route('graph', '/')
    config.add_route('generate', '/generate')
    config.scan()
    return config.make_wsgi_app()
