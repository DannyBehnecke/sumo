#!/usr/bin/env python
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2009-2019 German Aerospace Center (DLR) and others.
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html
# SPDX-License-Identifier: EPL-2.0

# @file    test.py
# @author  Pablo Alvarez Lopez
# @date    2019-07-16
# @version $Id$

# import common functions for netedit tests
import os
import sys

testRoot = os.path.join(os.environ.get('SUMO_HOME', '.'), 'tests')
neteditTestRoot = os.path.join(
    os.environ.get('TEXTTEST_HOME', testRoot), 'netedit')
sys.path.append(neteditTestRoot)
import neteditTestFunctions as netedit  # noqa

# Open netedit
neteditProcess, referencePosition = netedit.setupAndStart(neteditTestRoot, ['--gui-testing-debug-gl'])

# go to demand mode
netedit.supermodeDemand()

# go to route mode
netedit.routeMode()

# create route using three edges
netedit.leftClick(referencePosition, 274, 414)
netedit.leftClick(referencePosition, 570, 250)

# press enter to create route
netedit.typeEnter()

# create second route
netedit.leftClick(referencePosition, 280, 60)

# press enter to create route
netedit.typeEnter()

# go to inspect mode
netedit.inspectMode()

# inspect route
netedit.leftClick(referencePosition, 280, 417)

# Change parameter id with a non valid value (empty)
netedit.modifyAttribute(0, "", True)

# Change parameter id with a non valid value (invalid characters)
netedit.modifyAttribute(0, "<><><><>$%%%", True)

# Change parameter id with a non valid value (spaces)
netedit.modifyAttribute(0, "route with spaces", True)

# Change parameter id with a non valid value (duplicated)
netedit.modifyAttribute(0, "route_1", True)

# Change parameter id with valid value
netedit.modifyAttribute(0, "custom_route", True)

# Check undo redo
netedit.undo(referencePosition, 3)
netedit.redo(referencePosition, 3)

# click over reference (to avoid problem with undo-redo)
netedit.leftClick(referencePosition, 0, 0)

# save routes
netedit.saveRoutes()

# save network
netedit.saveNetwork()

# quit netedit
netedit.quit(neteditProcess)
