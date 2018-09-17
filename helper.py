# Title: helper.py
#
# Author: Troy Caro <twc17@pitt.edu>
# Date Modified: 09/17/2018
# Version: 0.0.1
#
# Purpose:
#   Simple helper functions for connection to a vSphere host

# Imports
import argparse
import getpass


def build_arg_parser():
    """Builds a standard argument parser with arguments for connection to vSphere

    Arguments:
        -s, --host Hostname or IP address of vSphere server
        -o, --port Optional port number (Default 443)
        -u, --user Username to connect with
        -p, --password Password to use when connecting

    Returns:
        parser as ArgumentParser object
    """
    parser = argparse.ArgumentParser(
        description='Standard Arguments for talking to vCenter')

    parser.add_argument('-s', '--host',
                        required=True,
                        action='store',
                        help='vSphere server to connect to')

    parser.add_argument('-o', '--port',
                        type=int,
                        default=443,
                        action='store',
                        help='Port to connect on (Default: 443)')

    parser.add_argument('-u', '--user',
                        required=True,
                        action='store',
                        help='Username to use when connecting to host')

    parser.add_argument('-p', '--password',
                        required=False,
                        action='store',
                        help='Password to use when connecting to host')

    parser.add_argument('-S', '--disable_ssl_verification',
                        required=False,
                        action='store_true',
                        help='Disable ssl host certificate verification')

    return parser


def prompt_for_password(args):
    """If no password is specified on the command line, prompt for it"""
    if not args.password:
        args.password = getpass.getpass(
                prompt='Enter password for host %s and user %s: ' %
                (args.host, args.user))

    return args


def get_args():
    """Supports the command-line arguments needed to connect to vSphere"""
    parser = build_arg_parser()

    args = parser.parse_args()

    return prompt_for_password(args)


def prompt_y_n_question(question, default="no"):
    """ based on:
        http://code.activestate.com/recipes/577058/
    :param question: Question to ask
    :param default: No
    :return: True/False
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("Invalid default answer: '{}'".format(default))

    while True:
        print(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            print("Please, respond with 'yes' or 'no' or 'y' or 'n'.")
