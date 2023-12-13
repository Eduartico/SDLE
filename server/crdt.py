from handlers import *
from typing import TypeVar, Generic

class Context:
    def __init__(self):
        self.clock_map = {}
        self.dot_cloud = set()

    def contain(self, resource, number):
        cloud = (resource, number) in self.dot_cloud
        clock = self.clock_map.get(resource, 0) >= number
        return cloud or clock
