from .orderedset import OrderedSet

class World:
    def __init__(self):
        self.systems = OrderedSet()
        self.entitiesToAdd = set()
        self.entitiesToRemove = set()

    def addSystem(self,system):
        self.systems.add(system)

    def removeSystem(self,system):
        self.systems.remove(system)

    def addEntity(self, entity):
        self.entitiesToAdd.add(entity)

    def removeEntity(self,entity):
        self.entitiesToRemove.add(entity)

    def _addEntity(self,entity):
        for system in self.systems:
            system.register(entity)

    def _removeEntity(self, entity):
        for system in self.systems:
            system.unregister(entity)

    def update(self):
        for entity in self.entitiesToRemove:
            self._removeEntity(entity)
        self.entitiesToRemove.clear()
        for entity in self.entitiesToAdd:
            self._addEntity(entity)
        self.entitiesToAdd.clear()
        for system in self.systems:
            system.update(self)