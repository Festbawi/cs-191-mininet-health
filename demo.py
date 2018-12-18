#!/usr/bin/python
from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController
from mininet.topo import LinearTopo, SingleSwitchTopo, Topo
from mininet.topolib import TreeTopo, TorusTopo

from mininet_bottle import MininetVerifyHealth

# topo = SingleSwitchTopo( 3 )
topo = TreeTopo( 3, 2 )

net = Mininet( topo=topo, switch=OVSSwitch, controller=[RemoteController], autoSetMacs=True )
net.start()

net.waitConnected()

mininetBottle = MininetVerifyHealth( net )
mininetBottle.run( server='gevent', host='0.0.0.0', port='8080' )

net.stop()