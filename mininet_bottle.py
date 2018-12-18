#!/usr/bin/python
from gevent import monkey
monkey.patch_all(select=False)

from bottle import Bottle, request, static_file, template
import json
import time

import verify_health

def json_dumps_util(message):
    return json.dumps(message) + '||'

def generate_adj_table(net):
    nodes = ([switch.name for switch in net.switches]) + ([host.name for host in net.hosts])
    table = [[False]*len(nodes) for _ in xrange(len(nodes))]

    # Adjacency
    for link in net.links:
        node1_ind = nodes.index(link.intf1.node.name)
        node2_ind = nodes.index(link.intf2.node.name)
        table[node1_ind][node2_ind] = True
        table[node2_ind][node1_ind] = True

    return {'nodes': nodes, 'table': table}

class MininetVerifyHealth(Bottle):
    def __init__(self, net):
        super(MininetVerifyHealth, self).__init__()
        self.net = net
        self.adj = generate_adj_table(self.net)
        self.route('/<filename:path>', callback=self.send_static)
        self.route('/dashboard', callback=self.view_dashboard)
        self.route('/verify', callback=self.verify_net)

    def send_static(self, filename):
        return static_file(filename, root='static/')

    def view_dashboard(self):
        return template('tpl/dashboard', net=self.net, adj=self.adj)

    def verify_net(self):
        if self.net == None:
            yield json_dumps_util('No Mininet is supplied to MininetBottle.\n')
        else:
            yield json_dumps_util('Disconnected switches (switch to a controller):\n')
            for message in verify_health.checkDisconnectedSwitches(self.net.switches):
                yield json_dumps_util(message)

            yield json_dumps_util('\nMissing links:\n')
            for message in verify_health.checkMissingLinks(self.net.links):
                yield json_dumps_util(message)

            yield json_dumps_util('\nNode Connectivity when Links are Down:\n')
            for message in verify_health.checkAvailableRouteIfLinkDown(self.net, 1, None, 1):
                yield json_dumps_util(message)

            yield json_dumps_util('Done.')
