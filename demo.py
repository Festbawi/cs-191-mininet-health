#!/usr/bin/python
from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController
from mininet.topo import MinimalTopo
from mininet.topolib import TreeTopo, TorusTopo

from mininet_bottle import MininetVerifyHealth

topo = MinimalTopo()

net = Mininet( topo=topo, switch=OVSSwitch, controller=[RemoteController], autoSetMacs=True )
net.start()

net.waitConnected()

mininetBottle = MininetVerifyHealth( net )
mininetBottle.run( host='0.0.0.0', port='8080', server='gevent' )

net.stop()