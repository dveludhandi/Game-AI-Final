
from behaviortree import *
from Minions import TankMinion, ADCMinion, AoEMinion, AoEWarrior

class CheckNumBuilding(BTNode):
	def parseArgs(self, args):
		BTNode.parseArgs(self, args)
		self.buildingThreshold = 0
		self.buildingType = 0
		if len(args) > 0:
			self.buildingType = args[0]
		if len(args) > 1:
			self.buildingThreshold = args[1]
	def execute(self, delta = 0):
		ret = BTNode.execute(self, delta)
		if self.buildingType == 0:
			return self.agent.team1type1 < self.buildingThreshold
		elif self.buildingType == 1:
			return self.agent.team1type2 < self.buildingThreshold
		elif self.buildingType == 2:
			return self.agent.team1type3 < self.buildingThreshold
		elif self.buildingType == 3:
			return self.agent.team1tower < self.buildingThreshold
		elif self.buildingType == 4:
			return self.agent.team1goldbldg < self.buildingThreshold
		elif self.buildingType == 5:
			return self.agent.team1attack < self.buildingThreshold
		elif self.buildingType == 6:
			return self.agent.team1bldgcount < self.buildingThreshold

class CheckEnemyBuilding(BTNode):
	def parseArgs(self, args):
		BTNode.parseArgs(self, args)
		self.buildingThreshold = 0
		self.buildingType = 0
		if len(args) > 0:
			self.buildingType = args[0]
		if len(args) > 1:
			self.buildingThreshold = args[1]
	def execute(self, delta = 0):
		ret = BTNode.execute(self, delta)
		if self.buildingType == 0:
			return self.agent.team2type1 > self.buildingThreshold
		elif self.buildingType == 1:
			return self.agent.team2type2 > self.buildingThreshold
		elif self.buildingType == 2:
			return self.agent.team2type3 > self.buildingThreshold
		elif self.buildingType == 3:
			return self.agent.team2tower > self.buildingThreshold
		elif self.buildingType == 4:
			return self.agent.team2goldbldg > self.buildingThreshold
		elif self.buildingType == 5:
			return self.agent.team2attack > self.buildingThreshold
		elif self.buildingType == 6:
			return self.agent.team2bldgcount > self.buildingThreshold

class BuildFactory(BTNode):
	def parseArgs(self, args):
		BTNode.parseArgs(self, args)
		self.factoryType = 0
		if len(args) > 0:
			self.factoryType = args[0]
	def execute(self, delta = 0):
		ret = BTNode.execute(self, delta)
		if self.agent.basetype is not None:
			return None
		elif self.agent.gold > self.agent.costarr[self.factoryType]:
			self.agent.basetype = self.factoryType
			return True
		else:
			return None

class BuildTower(BTNode):
	def execute(self, delta = 0):
		ret = BTNode.execute(self, delta)
		if self.agent.basetype is not None:
			return None
		elif self.agent.gold > self.agent.costarr[3]:
			self.agent.basetype = 3
			return True
		else:
			return None

class BuildMine(BTNode):
	def execute(self, delta = 0):
		ret = BTNode.execute(self, delta)
		if self.agent.basetype is not None:
			return None
		elif self.agent.gold > self.agent.costarr[4]:
			self.agent.basetype = 4
			return True
		else:
			return None

class BuildBooster(BTNode):
	def execute(self, delta = 0):
		ret = BTNode.execute(self, delta)
		if self.agent.basetype is not None:
			return None
		elif self.agent.gold > self.agent.costarr[5]:
			self.agent.basetype = 5
			return True
		else:
			return None

treeSpec = [None] * 10
#just loop over build sequences
treeSpec[0] = [Sequence, (BuildFactory,0), BuildBooster]
treeSpec[1] = [Sequence, BuildMine, (BuildFactory,0)]
treeSpec[2] = [Sequence, BuildTower, (BuildFactory,0)]
treeSpec[3] = [Sequence, (BuildFactory,0), (BuildFactory,1), (BuildFactory,2)]
treeSpec[4] = [Sequence, BuildMine, BuildTower, (BuildFactory,0), (BuildFactory,1), (BuildFactory,2), BuildBooster]
#build 3 mines, then 3 towers, then always factories
treeSpec[5] = [Selector, [Sequence, (CheckNumBuilding,4,3), BuildMine], [Sequence, (CheckNumBuilding,3,3), BuildTower], (BuildFactory,0)]
#build towers if < 3 towers or enemy has > 5 factories, else build factories
treeSpec[6] = [Selector, [Selector, [Sequence, (CheckNumBuilding,3,3), BuildTower], [Sequence, (CheckEnemyBuilding,6,5), BuildTower] ], (BuildFactory,0)]

class BuildBehavior(BehaviorTree):

	def __init__(self,world,teamId,behaviourId):
		self.world = world
		self.basetype = None
		self.team1type1 = 0
		self.team1type2 = 0
		self.team1type3 = 0
		self.team1attack = 0
		self.team1goldbldg = 0
		self.team1tower = 0
		self.team2type1 = 0
		self.team2type2 = 0
		self.team2type3 = 0
		self.team2attack = 0
		self.team2goldbldg = 0
		self.team2tower = 0
		self.team1bldgcount = 0
		self.team2bldgcount = 0
		self.gold = 0
		self.teamId = teamId
		self.costarr = [300, 500, 700, 500, 500, 500]
		#buildingtype = [FACTORY1, FACTORY2, FACTORY3, TOWER, MINE, RESOURCE]
		BehaviorTree.__init__(self)
		self.buildTree(treeSpec[behaviourId])
		BehaviorTree.start(self)

	def update(self):
		self.gold = self.world.gold[self.teamId-1]
		miniontypes = [ADCMinion, TankMinion, AoEWarrior]
		self.team1bases = self.world.getCastlesAndBuildingsForTeam(self.teamId) #my team
		self.team2bases = self.world.getCastlesAndBuildingsForTeam(2 if self.teamId==1 else 1) #enemy team
		self.team1type1 = 0
		self.team1type2 = 0
		self.team1type3 = 0
		self.team1attack = 0
		self.team1goldbldg = 0
		self.team1tower = 0

		self.team2type1 = 0
		self.team2type2 = 0
		self.team2type3 = 0
		self.team2attack = 0
		self.team2goldbldg = 0
		self.team2tower = 0

		self.team1bldgcount = 0
		self.team2bldgcount = 0

		for baseitem in self.team1bases:

			if baseitem.buildingType == "Building" or baseitem.buildingType == 'Spawner':
				self.team1bldgcount += 1
				if baseitem.minionType == miniontypes[0]:
					self.team1type1 += 1
				elif baseitem.minionType == miniontypes[1]:
					self.team1type2 += 1
				elif baseitem.minionType == miniontypes[2]:
					self.team1type3 += 1
			elif baseitem.buildingType == "Defense":
				self.team1tower += 1
			elif baseitem.buildingType == "AttackBooster":
				self.team1attack += 1
			elif baseitem.buildingType == "GoldMiner":
				self.team1goldbldg += 1

		for baseitem in self.team2bases:
			if baseitem.buildingType == "Building" or baseitem.buildingType == 'Spawner':
				self.team2bldgcount += 1
				if baseitem.minionType == miniontypes[0]:
					self.team2type1 += 1
				elif baseitem.minionType == miniontypes[1]:
					self.team2type2 += 1
				elif baseitem.minionType == miniontypes[2]:
					self.team2type3 += 1
			elif baseitem.buildingType == "Defense":
				self.team2tower += 1
			elif baseitem.buildingType == "AttackBooster":
				self.team2attack += 1
			elif baseitem.buildingType == "GoldMiner":
				self.team2goldbldg += 1

		return BehaviorTree.update(self)


