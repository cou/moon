from pyramid.paster import get_app, setup_logging
import os
__here__ = os.path.dirname(os.path.abspath(__file__))
__parent__ = os.path.dirname(__here__)
ini_path = '%s/development.ini'%(__parent__)
setup_logging(ini_path)
application = get_app(ini_path, 'main')