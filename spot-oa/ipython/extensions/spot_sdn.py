import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.dirname(__file__))))

from plugins.sdn.service.webapp import load_jupyter_server_extension
