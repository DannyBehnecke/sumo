# -*- coding: utf-8 -*-
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2008-2019 German Aerospace Center (DLR) and others.
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html
# SPDX-License-Identifier: EPL-2.0

# @file    __init__.py
# @author  Michael Behrisch
# @author  Lena Kalleske
# @author  Mario Krumnow
# @author  Daniel Krajzewicz
# @author  Jakob Erdmann
# @date    2008-10-09
# @version $Id$

# pylint: disable=E1101

from __future__ import print_function
from __future__ import absolute_import
import socket
import time
import subprocess
import warnings
import sys
import os
import collections

if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))
else:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sumolib  # noqa
from sumolib.miscutils import getFreeSocketPort  # noqa

from .domain import _defaultDomains  # noqa
# StepListener needs to be imported for backwards compatibility
from .connection import Connection, StepListener  # noqa
from .exceptions import FatalTraCIError, TraCIException  # noqa
from . import _inductionloop, _lanearea, _multientryexit, _trafficlight  # noqa
from . import _lane, _person, _route, _vehicle, _vehicletype  # noqa
from . import _edge, _gui, _junction, _poi, _polygon, _simulation  # noqa

inductionloop = _inductionloop.InductionLoopDomain()
lanearea = _lanearea.LaneAreaDomain()
multientryexit = _multientryexit.MultiEntryExitDomain()
trafficlight = _trafficlight.TrafficLightDomain()
lane = _lane.LaneDomain()
person = _person.PersonDomain()
route = _route.RouteDomain()
vehicle = _vehicle.VehicleDomain()
vehicletype = _vehicletype.VehicleTypeDomain()
edge = _edge.EdgeDomain()
gui = _gui.GuiDomain()
junction = _junction.JunctionDomain()
poi = _poi.PoiDomain()
polygon = _polygon.PolygonDomain()
simulation = _simulation.SimulationDomain()

_connections = {}
# cannot use immutable type as global variable
_currentLabel = [""]
_pendingStepListener = collections.defaultdict(list)


def _STEPS2TIME(step):
    """Conversion from time steps in milliseconds to seconds as float"""
    return step / 1000.


def connect(port=8813, numRetries=10, host="localhost", proc=None):
    """
    Establish a connection to a TraCI-Server and return the
    connection object. The connection is not saved in the pool and not
    accessible via traci.switch. It should be safe to use different
    connections established by this method in different threads.
    """
    for wait in range(1, numRetries + 2):
        try:
            return Connection(host, port, proc)
        except socket.error as e:
            if proc is not None and proc.poll() is not None:
                raise TraCIException("TraCI server already finished")
            if wait > 1:
                print("Could not connect to TraCI server at %s:%s" % (host, port), e)
            if wait < numRetries + 1:
                print(" Retrying in %s seconds" % wait)
                time.sleep(wait)
    raise FatalTraCIError("Could not connect in %s tries" % (numRetries + 1))


def init(port=8813, numRetries=10, host="localhost", label="default", proc=None):
    """
    Establish a connection to a TraCI-Server and store it under the given
    label. This method is not thread-safe. It accesses the connection
    pool concurrently.
    """
    _connections[label] = connect(port, numRetries, host, proc)
    switch(label)
    for l in (label, ""):
        for listener in _pendingStepListener[l]:
            _connections[l].addStepListener(listener)
        del _pendingStepListener[l]
    return getVersion()


def start(cmd, port=None, numRetries=10, label="default"):
    """
    Start a sumo server using cmd, establish a connection to it and
    store it under the given label. This method is not thread-safe.
    """
    if label in _connections:
        raise TraCIException("Connection '%s' is already active." % label)
    while numRetries >= 0 and label not in _connections:
        sumoPort = sumolib.miscutils.getFreeSocketPort() if port is None else port
        sumoProcess = subprocess.Popen(cmd + ["--remote-port", str(sumoPort)])
        try:
            return init(sumoPort, numRetries, "localhost", label, sumoProcess)
        except TraCIException:
            if port is not None:
                break
            warnings.warn("Could not connect to TraCI server using port %s. Retrying with different port." % sumoPort)
            numRetries -= 1
    raise FatalTraCIError("Could not connect.")


def isLibsumo():
    return False


def load(args):
    """load([optionOrParam, ...])
    Let sumo load a simulation using the given command line like options
    Example:
      load(['-c', 'run.sumocfg'])
      load(['-n', 'net.net.xml', '-r', 'routes.rou.xml'])
    """
    return _connections[""].load(args)


def simulationStep(step=0):
    """
    Make a simulation step and simulate up to the given second in sim time.
    If the given value is 0 or absent, exactly one step is performed.
    Values smaller than or equal to the current sim time result in no action.
    """
    return _connections[""].simulationStep(step)


def addStepListener(listener, connLabel=""):
    """addStepListener(traci.StepListener) -> int

    Append the step listener (its step function is called at the end of every call to traci.simulationStep())
    to the given connection. If the connection is not set up yet, the step listener will be added once
    it is created.
    Returns the ID assigned to the listener if it was added successfully, None otherwise.
    """
    if connLabel not in _connections:
        _pendingStepListener[connLabel].append(listener)
        return None
    return _connections[""].addStepListener(listener)


def removeStepListener(listenerID, connLabel=""):
    """removeStepListener(traci.StepListener) -> bool

    Remove the step listener from the given connection's step listener container.
    Returns True if the listener was removed successfully, False if it wasn't registered.
    """
    return _connections[connLabel].removeStepListener(listenerID)


def getVersion():
    return _connections[""].getVersion()


def setOrder(order):
    return _connections[""].setOrder(order)


def close(wait=True):
    _connections[""].close(wait)
    del _connections[_currentLabel[0]]


def switch(label):
    _currentLabel[0] = label
    _connections[""] = _connections[label]
    for domain in _defaultDomains:
        domain._setConnection(_connections[""])


def getLabel():
    return _currentLabel[0]


def getConnection(label="default"):
    if label not in _connections:
        raise TraCIException("connection with label '%s' is not known")
    return _connections[label]
