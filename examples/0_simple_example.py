import entitycomponentsystem
from entitycomponentsystem import *
from dataclasses import *

class Entity:
    def __init__(self,*components):
        self.components = components

@dataclass
class TransformComponent:
    x : float = 0
    y : float = 0

@dataclass
class RenderComponent:
    size : float = 0


@with_components(TransformComponent)
class TransformSystem(System):
    def update(self, world):
        dt = world.dt
        for entity,components in self.components.items():
            a, = components
            a.x += 1 * dt
            a.y += 1 * dt
            print(a)

@with_components(RenderComponent)
class RenderSystem(System):
    def update(self, world):
        dt = world.dt
        for entity,components in self.components.items():
            a, = components
            a.size *= 1.1
            print(a)

class GameWorld(World):
    def __init__(self):
        super().__init__()
        self.addSystem(TransformSystem())
        self.addSystem(RenderSystem())
        self.addEntity(Entity(TransformComponent(x=200,y=100),RenderComponent(size=5)))

    def run(self):
        self.running = 10
        while self.running > 0:
            self.update(1./60.)
            self.running -= 1
            print()

    def update(self, dt):
        self.dt = dt
        super().update()

world = GameWorld()
world.run()






