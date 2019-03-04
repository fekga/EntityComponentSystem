from orderedset import OrderedSet
from collections import OrderedDict,namedtuple
from dataclasses import dataclass, asdict, field

def mergeInstances(*instances):
    classNames = [c.__class__.__name__.lower() for c in instances]
    return namedtuple('Merged',classNames)(**dict(zip(classNames,instances)))

@dataclass
class Component:
	pass

class Entity:
	def __init__(self, components):
		self.components = components

class System:
	def __init__(self, world):
		self.world = world
		self.components = OrderedDict()
		self.world.addSystem(self)

	def get_matching_components(self, entity):
		return list(component for component in entity.components if component.__class__ in self.componentMask)

	def register(self, entity):
		components = self.get_matching_components(entity)
		if len(components) == len(self.componentMask):
			self.components[entity] = mergeInstances(*components)

	def unregister(self, entity):
		self.components.pop(entity,None)

	def update(self):
		raise NotImplementedError('Implement in derived classes!')

@dataclass
class InputComponent(Component):
	pass

@dataclass
class TransformComponent(Component):
	x : float = 0
	y : float = 0
	vx : float = 0
	vy : float = 0
	ax : float = 0
	ay : float = 0

@dataclass
class RenderComponent(Component):
	pass

class InputSystem(System):
	componentMask = (InputComponent,)

	def update(self):
		for component in self.components.values():
			pass

class TransformSystem(System):
	componentMask = (TransformComponent,)

	def update(self):
		dt = self.world.dt
		for component in self.components.values():
			transform = component.transformcomponent
			transform.vx += transform.ax * dt
			transform.vy += transform.ay * dt
			transform.x += transform.vx * dt
			transform.y += transform.vy * dt
			print(transform)

class RenderSystem(System):
	componentMask = RenderComponent,TransformComponent

	def update(self):
		print(self)
		for component in self.components.values():
			transform, render = component.transformcomponent,component.rendercomponent

class World:
	def __init__(self):
		self.systems = OrderedSet()
		self.entitiesToAdd = list()
		self.entitiesToRemove = list()

	def addSystem(self,system):
		self.systems.add(system)

	def removeSystem(self,system):
		self.systems.remove(system)

	def addEntity(self, entity):
		self.entitiesToAdd.append(entity)

	def _addEntity(self,entity):
		for system in self.systems:
			system.register(entity)

	def _removeEntity(self, entity):
		for system in self.systems:
			system.unregister(entity)		

	def update(self,dt):
		self.dt = dt
		for entity in self.entitiesToRemove:
			self._removeEntity(entity)
		self.entitiesToRemove.clear()
		for entity in self.entitiesToAdd:
			self._addEntity(entity)
		self.entitiesToAdd.clear()
		for system in self.systems:
			system.update()

class GameWorld(World):
	def __init__(self):
		super().__init__()
		self.addSystem(InputSystem(self))
		self.addSystem(TransformSystem(self))
		self.addSystem(RenderSystem(self))


world = GameWorld()

player = Entity([InputComponent(),TransformComponent(ax=0.5),RenderComponent()])
world.addEntity(player)

running = 1
dt = 1./8.
while running > 0:
	world.update(dt)
	running -= 1

# change component value manually
a,b,c = player.components
b.ax = 2
player.components = [a,b,c]

#world.removeEntity(player)
#world.addEntity(player)
print('-'*15)

running = 1
while running > 0:
	world.update(dt)
	running -= 1