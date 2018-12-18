# Mininet Health
Mininet Health is a project done in Python for CMSC 191 (Software Defined Networks). Developed by Femo Bayani and Sean Pineda.

## Pre-requisites
1. [Bottle](https://bottlepy.org)
```python
pip install bottle
```
2. [gevent](http://www.gevent.org/)
```shell
sudo apt-get python-gevent
```

## Usage
There is an example usage included in [demo.py](demo.py)
```python
topo = MinimalTopo()

net = Mininet( topo=topo, switch=OVSSwitch, controller=[RemoteController], autoSetMacs=True )
net.start()

net.waitConnected()

mininetBottle = MininetVerifyHealth( net )
mininetBottle.run( host='0.0.0.0', port='8080', server='gevent' )

net.stop()
```

Then, just execute the script:
```shell
sudo python demo.py
```