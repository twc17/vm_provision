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

from pyVim.connect import SmartConnect, SmartConnectNoSSL, Disconnect
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
    vm = None

    container = content.viewManager.CreateContainerView(
            content.rootFolder, [vim.VirtualMachine], True)

    for c in container.view:
        if c.name == name:
            vm = c
            break

    return vm


def main():
    """Generate HTML5 console for a specific VM"""

    args = get_args()

    try:
        if args.disable_ssl_verification:
            service_instance = SmartConnectNoSSL(host=args.host,
                                                 user=args.user,
                                                 pwd=args.password,
                                                 port=int(args.port))
        else:
            service_instance = SmartConnect(host=args.host,
                                            user=args.user,
                                            pwd=args.password,
                                            port=int(args.port))

    except Exception as e:
        print("Could not connect to vSphere host")
        print(repr(e))
        sys.exit(1)

    atexit.register(Disconnect, service_instance)

    content = service_instance.RetrieveContent()

    vm = get_vm(content, args.name)
    vm_moid = vm._moId

    vcenter_data = content.setting
    vcenter_settings = vcenter_data.setting
    console_port = '7331'

    for item in vcenter_settings:
        key = getattr(item, 'key')
        if key == 'VirtualCenter.FQDN':
            vcenter_fqdn = getattr(item, 'value')

    session_manager = content.sessionManager
    session = session_manager.AcquireCloneTicket()

    vc_cert = ssl.get_server_certificate((args.host, int(args.port)))
    vc_pem = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM,
                                             vc_cert)
    vc_fingerprint = vc_pem.digest('sha1')

    print("\nOpen the following URL in your browser to access the"
          + " remote console.\n")
    print("You have 60 seconds to open the URL, or the session"
          + " will be terminted.\n")
    print("http://" + args.host + ":" + console_port + "/console/?vmId="
          + str(vm_moid) + "&vmName=" + args.name + "&host=" + vcenter_fqdn
          + "&sessionTicket=" + session + "&thumbprint="
          + vc_fingerprint.decode('utf-8'))
    print("\nWaiting 60 seconds, then exit")
    time.sleep(60)


# Run program
if __name__ == "__main__":
    main()
