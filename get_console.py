# Title: get_console.py
#
# Author: Troy Caro <twc17@pitt.edu>
# Date Modified: 09/17/2018
# Version: 0.0.1
#
# Purpose:
#   Generate HTML5 console for a specific VM

# Imports
import atexit
import OpenSSL
import ssl
import sys
import time

from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
from helper import *


def get_args():
    """Override get_args() from helper.py to add VM name to arguments"""
    parser = build_arg_parser()

    parser.add_argument('-n', '--name',
                        required=True,
                        help='Name of virtual machine to connect to')

    args = parser.parse_args()

    return prompt_for_password(args)


def get_vm(content, name):
    """Get VM from vSphere

    Arguments:
        content Content from vSphere connection
        name Name of virtual machine

    Returns:
        vm VM object
    """
    try:
        name = unicode(name, 'utf-8')
    except TypeError:
        # Need to find a better way to hand type errors for vm names
        pass

    vm = None
