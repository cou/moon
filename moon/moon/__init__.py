# coding: utf8
import sys
reload(sys)
sys.setdefaultencoding("utf8")

from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=0)
    config.add_route('graph', '/')
    config.add_route('generate', '/generate')
    config.scan()
    return config.make_wsgi_app()
