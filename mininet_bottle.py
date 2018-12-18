#!/usr/bin/python
from gevent import monkey
monkey.patch_all(select=False)

from bottle import Bottle, request, static_file, template
import json
import time

import verify_health

def jsonDumpUtil(message):
    return json.dumps(message) + '||'

class MininetVerifyHealth(Bottle):
    def __init__(self, net):
        super(MininetVerifyHealth, self).__init__()
        self.net = net
        self.route('/<filename:path>', callback=self.send_static)
        self.route('/dashboard', callback=self.view_dashboard)
        self.route('/verify', callback=self.verify_net)

    def send_static(self, filename):
        return static_file(filename, root='static/')

    def view_dashboard(self):
        return template('tpl/dashboard', details=verify_health.getNetDetails(self.net))

    def verify_net(self):
        if self.net == None:
            yield jsonDumpUtil('No Mininet is supplied to MininetBottle.\n')
        else:
            yield jsonDumpUtil('Disconnected switches (switch to a controller):\n')
            for message in verify_health.checkDisconnectedSwitches(self.net.switches):
                yield jsonDumpUtil(message)

            yield jsonDumpUtil('\nMissing links:\n')
            for message in verify_health.checkMissingLinks(self.net.links):
                yield jsonDumpUtil(message)

            yield jsonDumpUtil('\nNode Connectivity when Links are Down:\n')
            for message in verify_health.checkAvailableRouteIfLinkDown(self.net, 1, None, 1):
                yield jsonDumpUtil(message)