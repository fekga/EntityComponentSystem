from entitycomponentsystem import *
from dataclasses import *

class TestEntity:
    def __init__(self,*components):
        self.components = components

@dataclass
class TestComponent_A:
    x : float = 0

@dataclass
class TestComponent_B:
    y : float = 0

@dataclass
class TestComponent_C:
    z : float = 0

@with_components(TestComponent_A)
class TestSystemA(System):
    def update(self, world):
        dt = world.dt
        for entity,components in self.components.items():
            a, = components
            a.x += 1 * dt

@with_components(TestComponent_B)
class TestSystemB(System):
    def update(self, world):
        dt = world.dt
        for entity,components in self.components.items():
            b, = components
            b.y += 1 * dt

@with_components(TestComponent_A,TestComponent_B)
class TestSystemAB(System):
    def update(self, world):
        dt = world.dt
        for entity,components in self.components.items():
            a,b = components
            a.x += 2 * dt
            b.y += 2 * dt

@with_components(TestComponent_B,TestComponent_A)
class TestSystemAB_reverse(System):
    def update(self, world):
        dt = world.dt
        for entity,components in self.components.items():
            a,b = components
            a.x += 1 * dt
            b.y += 2 * dt

@with_components(TestComponent_C)
class TestSystemC(System):
    def update(self, world):
        dt = world.dt
        for entity,components in self.components.items():
            a,b = components
            a.x += 2 * dt
            b.y += 2 * dt

class TestWorld(World):
    def __init__(self):
        super().__init__()
        self.addSystem(TestSystemA())
        self.addSystem(TestSystemB())
        self.addSystem(TestSystemAB())
        self.addSystem(TestSystemAB_reverse())
        self.addSystem(TestSystemC())
        self.addEntity(TestEntity(TestComponent_A(1),TestComponent_B(2)))

    def run(self):
        self.running = 10
        while self.running > 0:
            self.update(0.1)
            self.running -= 1

    def update(self, dt):
        self.dt = dt
        super().update()

from hypothesis import *
import hypothesis.strategies as st
from math import isnan


world = TestWorld()
world.run()

@given(st.floats())
def test_world(dt):
    #assume(not isnan(dt))
    world.update(dt)
    assert world.dt == dt

test_world()
world.run()






