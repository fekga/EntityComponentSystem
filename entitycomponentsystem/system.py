from collections import OrderedDict,namedtuple

def with_components(*components):
    if len(components) != len(set(components)):
        raise ValueError('Multiple component of the same type!')
    def decorator(cls):
        setattr(cls,'componentMask',components)
        return cls
    return decorator

class System:

    @staticmethod
    def _mergeComponentInstances(components):
        classNames = [c.__class__.__name__ for c in components]
        Merged = namedtuple('Merged',classNames)
        return Merged(**dict(zip(classNames,components)))

    def __init__(self):
        self.components = OrderedDict()

    def get_matching_components(self, entity):
        return list(component for component in entity.components if component.__class__ in self.componentMask)

    def register(self, entity):
        components = self.get_matching_components(entity)
        if len(components) == len(self.componentMask):
            self.components[entity] = System._mergeComponentInstances(components)

    def unregister(self, entity):
        self.components.pop(entity,None)