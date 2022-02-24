"""
Define commonly re-used paths in a way that's agnostic to the operating system
being used.
"""
import os, socket
from sunnyhills import __path__

DATADIR = os.path.join(os.path.dirname(__path__[0]), 'data')
EPOCHSDIR = os.path.join(os.path.dirname(__path__[0]), 'personal_epochs')
