from __future__ import print_function

import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../"))
import lib

def handler(event, context):
    return lib.get_hello(event)

    # Use this code if you don't use the http event with the LAMBDA-PROXY integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
