from __future__ import print_function

import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../"))
import lib

def handler(event, context):
    return lib.update_note(event, context)
