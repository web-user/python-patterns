# principle is a specific methodology for loosely coupling software modules
from enum import Enum
from abc import abstractmethod


class Relationship(Enum):
    PARENT = 0
    CHILD = 1
    SIBLING = 2


class Person:

    def __init__(self, name):
        self.name = name


class RelationshipBrowser:
    @abstractmethod
    def find_all_children_of(self, name): pass


class Relationships(RelationshipBrowser):   # low-level

    relations = []

    def add_parent_and_child(self, parent, child):
        self.relations.append((parent, Relationship.PARENT, child))
        self.relations.append((child, Relationship.PARENT, parent))

    def find_all_children_of(self, name):
        for r in self.relations:
            if r[0].name == name and r[1] == Relationship.PARENT:
                yield r[2].name

class Research:
    # dependency on a low-level module directly
    # bad because strongly dependent on e.g. storage type

    def __init__(self, browser, name):
        for p in browser.find_all_children_of(name):
            print(f'John has a child called {p}')


parent = Person('John')
child1 = Person('Chris 1')
child2 = Person('Matt')


# low-level module
relationships = Relationships()
relationships.add_parent_and_child(parent, child1)
relationships.add_parent_and_child(parent, child2)

Research(relationships, 'John')

