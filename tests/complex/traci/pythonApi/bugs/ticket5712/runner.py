#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2008-2019 German Aerospace Center (DLR) and others.
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html
# SPDX-License-Identifier: EPL-2.0

# @file    runner.py
# @author  Jakob Erdmann
# @date    2017-01-23
# @version $Id$


from __future__ import print_function
from __future__ import absolute_import
import os
import sys
sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))
import traci  # noqa
import sumolib  # noqa


sumoBinary = os.environ["SUMO_BINARY"]
cmd = [sumoBinary,
       '-n', 'input_net2.net.xml',
       '-r', 'input_routes.rou.xml',
       '--stop-output', 'stops.xml',
       '--no-step-log',
       ]
traci.start(cmd)

veh = "veh0"
traci.simulationStep()
# remove first stop
traci.vehicle.setStop(veh, "WC", 50, 0, 0)
# keep second stop and add another one
traci.vehicle.setStop(veh, "CE", 50, 0, 0, until=100)
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()

traci.close()
