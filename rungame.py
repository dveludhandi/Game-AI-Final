'''
 * Copyright (c) 2014, 2015 Entertainment Intelligence Lab, Georgia Institute of Technology.
 * Originally developed by Mark Riedl.
 * Last edited by Mark Riedl 05/2015
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
'''

import sys, pygame, math, numpy, random, time, copy
from pygame.locals import *

from constants import *
from utils import *
from core import *
from astarnavigator import *
from agents import *
from moba2 import *
from MyHero import *
from clonenav import *
from Castle import *
from MyMinion import *
from buildBehaviors import *
############################
### How to use this file
###
### Use this file to conduct a competition with other agents.
### Step 1: Give your MyHero class an unique name, e.g., MarkHero. Change the file name to match the class name exactly.
### Step 2: python runherocompetition.py classname1 classname2

############################
### SET UP WORLD

x = 1400
y = 850


dims = (x, y)

'''obstacles = [[(0, 0), (0, 220), (80, 220), (220, 80), (220, 0)],
			 [(0, y), (0, 500), (80, 500), (220, 640), (220, 720)]]'''

obstacles = []
mirror = map(lambda poly: map(lambda point: (dims[0]-point[0], dims[1]-point[1]), poly), obstacles)

obstacles = obstacles + mirror

########################




class MyHumanMinion(MyMinion):
	def __init__(self, position, orientation, world, image=NPC, speed=SPEED, viewangle=360, hitpoints=HITPOINTS,
				 firerate=FIRERATE, bulletclass=SmallBullet):
		MyMinion.__init__(self, position, orientation, world, image, speed, viewangle, hitpoints, firerate, bulletclass)


class MyAlienMinion(MyMinion):
	def __init__(self, position, orientation, world, image=JACKAL, speed=SPEED, viewangle=360, hitpoints=HITPOINTS,
				 firerate=FIRERATE, bulletclass=SmallBullet):
		MyMinion.__init__(self, position, orientation, world, image, speed, viewangle, hitpoints, firerate, bulletclass)

########################
world = MOBAWorld(SEED, dims, dims, 0, 60)
agent = GhostAgent(ELITE, (x/4, y/2), 0, SPEED, world)
#agent = Hero((600, 500), 0, world, ELITE)
world.setPlayerAgent(agent)
world.initializeTerrain(obstacles, (0, 0, 0), 4)
agent.setNavigator(Navigator())
agent.team = 0
world.debugging = True
useBehaviorTree = False
if useBehaviorTree:
	world.behaviorTree = BuildBehavior(world,2,6)

nav = AStarNavigator()
nav.agent = agent
nav.setWorld(world)

#c1 = Castle(BASE, (75,360),world,1, MyHumanMinion)
#c2 = Castle(BASE, (1280-75,360),world,2, MyAlienMinion)
c1 = CastleBase(BASE, (180,y/2),world,1)
c2 = CastleBase(BASE, (x-180,y/2),world,2)
world.addCastle(c1)
world.addCastle(c2)

world.run()

