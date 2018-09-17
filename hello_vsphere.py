#!/usr/bin/env python
# Title: hello_vsphere.py
#
# Author: Troy Caro <twc17@pitt.edu>
# Date Modified: 09/17/2018
# Version: 0.0.1
#
# Purpose:
#   This is a simple program to connect to a vSphere host and print a
#   'hello world' message.

# Imports
import argparse
import getpass
import atexit

from pyVim import connect
from pyVmomi import vmodl


def get_args():
    """Get command line arguments from the user."""
    parser = argparse.ArgumentParser(
            description='Standard arguments for talking to vSphere server')

    # -h is reserved for 'help', so we will use -s for the host
    parser.add_argument('-s', '--host',
                        required=True,
                        action='store',
                        help='vSphere server to connect to')

    # -p is being used for 'password', so we will use -o for host port
    parser.add_argument('-o', '--port',
                        type=int,
                        default=443,
                        action='store',
                        help='Port to connect on. Default: 443')

    parser.add_argument('-u', '--user',
                        required=True,
                        action='store',
                        help='Username to use when connecting to vSphere host')

    parser.add_argument('-p', '--password',
                        required=False,
                        action='store',
                        help='Password to use when connecting to vSphere host')

    args = parser.parse_args()

    if not args.password:
        args.password = getpass.getpass(
                prompt='Enter password for host %s and user %s: ' %
                (args.host, args.user))

    return args


def main():
    """Simple program to test connectivity to vSphere host"""

    args = get_args()

    try:
        service_instance = connect.SmartConnect(host=args.host,
                                                user=args.user,
                                                pwd=args.password,
                                                port=int(args.port))

        atexit.register(connect.Disconnect, service_instance)

        print("\nHello World!\n")
        print("If you got here, you have authenticated to vSphere successfully!")
        session_id = service_instance.content.sessionManager.currentSession.key
        print("Current session id: {}".format(session_id))

    except vmodl.MethodFault as error:
        print("Caught vmodl fault: " + error.msg)
        return -1

    return 0


# Start the program
if __name__ == "__main__":
    main()
