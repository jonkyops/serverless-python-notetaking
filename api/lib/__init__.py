""" Lib """

import sys
import os
import ctypes
import lib.build_response
from lib.hello import get_hello
from lib.notes import create_note
from lib.notes import read_note
from lib.notes import read_all
from lib.notes import update_note
from lib.notes import delete_note
#import lib.notes

LIBS_PATH = "../vendored"

# add vendored folder to sys path
HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(HERE, LIBS_PATH))

# Manually load OS libraries
# ref: https://serverlesscode.com/post/deploy-scikitlearn-on-lamba/

for d, dirs, files in os.walk(LIBS_PATH):
    for f in files:
        if ".so" in f:
            ctypes.cdll.LoadLibrary(os.path.join(d, f))
