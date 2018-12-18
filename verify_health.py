#!/usr/bin/python
import itertools

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import output

def _getLinkNodeNames( link ):
    return '%s-%s' % ( link.intf1.node.name, link.intf2.node.name )

# https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
def _splitIntoChunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i + n]

def _catNetDetails(l, n = 5):
    chunks = list(_splitIntoChunks(l, n))
    return '\n\t'.join(map('\t'.join, chunks))


def getNetDetails( net ):
    output = 'Network details:\n'
    output += 'Controller(s):\n\t%s\n' % _catNetDetails([controller.name for controller in net.controllers])
    output += '\nHost(s):\n\t%s\n' % _catNetDetails([host.name for host in net.hosts])
    output += '\nSwitch(es):\n\t%s\n' % _catNetDetails([switch.name for switch in net.switches])
    output += '\nLink(s):\n\t%s\n\n' % _catNetDetails([_getLinkNodeNames(link) for link in net.links])
    return output

# Based on mininet/net.py's Mininet.ping()
def _ping( net, hosts=None, timeout=None ):
        packets = 0
        lost = 0
        ploss = None
        if not hosts:
            hosts = net.hosts
            yield '*** Ping: testing ping reachability\n'
        for node in hosts:
            yield '%s -> ' % node.name
            for dest in hosts:
                if node != dest:
                    opts = ''
                    if timeout:
                        opts = '-W %s' % timeout
                    if dest.intfs:
                        result = node.cmd( 'ping -c1 %s %s' %
                                           (opts, dest.IP()) )
                        sent, received = net._parsePing( result )
                    else:
                        sent, received = 0, 0
                    packets += sent
                    if received > sent:
                        yield '*** Error: received too many packets'
                        yield '%s' % result
                        node.cmdPrint( 'route' )
                        exit( 1 )
                    lost += sent - received
                    yield ( '%s ' % dest.name ) if received else 'X '
            yield '\n'
        if packets > 0:
            ploss = 100.0 * lost / packets
            received = packets - lost
            yield "*** Results: %i%% dropped (%d/%d received)\n" % ( ploss, received, packets )
        else:
            ploss = 0
            yield "*** Warning: No packets sent\n"
        # yield ploss

def checkDisconnectedSwitches( switches ):
    disconnectedSwitches = []

    for switch in switches:
        if switch.connected() == False:
            disconnectedSwitches.append( switch )

    if len( disconnectedSwitches ) == 0:
        yield 'None\n'
    else:
        yield '%s\n' % ( ', '.join( sw.name for sw in disconnectedSwitches ) )

def checkMissingLinks( links ):
    missingLinks = []
    
    for link in links:
        if link.status == 'MISSING':
            missingLinks.append( link )
    
    if len( missingLinks ) == 0:
        yield 'None\n'
    else:
        yield '%s\n' % ( ', '.join( missingLinks ) )

def _changeLinkStatus( intf, status ):
    result = intf.ifconfig( status )
    if result:
        return 'link status change failed: %s\n' % result
    return ''

def checkAvailableRouteIfLinkDown( net, minCombinations=1, maxCombinations=1, pingTimeout=None ):
    links = net.links
    
    if maxCombinations == None:
        maxCombinations = len( links )
    
    maxCombinations = max( 0, min( maxCombinations, len( links ) ) )

    for link in links:
        yield _changeLinkStatus( link.intf1, 'up' )
        yield _changeLinkStatus( link.intf2, 'up' )
    
    # yield '\n*** Node Connectivity when Links are Down (combinations from %d to %d):' % ( minCombinations, maxCombinations )
    yield '\n* Links down: None\n'
    for message in _ping(net, None, pingTimeout):
        yield message
    
    for combiLength in range(minCombinations, maxCombinations + 1):
        combinations = itertools.combinations( links, combiLength )
        for i, combination in enumerate( combinations ):
            combinationNames = []
            
            # Down links
            for link in combination:
                combinationNames.append( _getLinkNodeNames(link) )
                yield _changeLinkStatus( link.intf1, 'down' )
                yield _changeLinkStatus( link.intf2, 'down' )
        
            # Check if all connections still work
            yield '\n* Links down: %s\n' % ', '.join( combinationNames )
            for message in _ping(net, None, pingTimeout):
                yield message
        
            # Up links for next iteration
            for link in combination:
                yield _changeLinkStatus( link.intf1, 'up' )
                yield _changeLinkStatus( link.intf2, 'up' )