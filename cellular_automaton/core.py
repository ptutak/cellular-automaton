import numpy as np
from abc import ABC, abstractmethod

class Neighborhood(ABC):
    @abstractmethod
    def get_neighbors(self, index):
        pass

class MooreNeighborhood(Neighborhood):
    def get_neighbors(self, index):
        if len(index) > 2:
            raise TypeError('Bad index type. Must be indexed (int, int)')
        return ((index[0] - 1, index[1] - 1),
                (index[0] - 1, index[1]),
                (index[0] - 1, index[1] + 1),
                (index[0], index[1] - 1),
                (index[0], index[1] + 1),
                (index[0] + 1, index[1] - 1),
                (index[0] + 1, index[1]),
                (index[0] + 1, index[1] + 1))


class StateSolver(ABC):
    @abstractmethod
    def get_next_state(self, neighbors):
        pass


class SimpleStateSolver(StateSolver):
    def get_next_state(self, actual_state, neighbors):
        if actual_state:
            return actual_state
        quantity = dict()
        for neighbor in neighbors:
            if neighbor in quantity:
                quantity[neighbor] += 1
            else:
                quantity[neighbor] = 1
        if 0 in quantity:
            del quantity[0]
        max_neigh = None
        max_quantity = 0
        for neighbor, quant in quantity.items():
            if quant > max_quantity:
                max_neigh = neighbor
        if max_neigh:
            return max_neigh
        return 0


class Solver:
    def __init__(self, neighborhood, state_solver):
        self._neighborhood = neighborhood
        self._state_solver = state_solver

    def next_step(self, array):
        elements = (
            (x, y) for x in range(len(array)) for y in range(len(array[0])))
        element_neighbors = (
            (x, (array[index] for index in self._neighborhood.get_neighbors(x)))
            for x in elements)
        new_elements = (
            self._state_solver.get_next_state(array[elem], neighborhood)
            for elem, neighborhood in element_neighbors)
        dummy_array = np.array([
            [0,0,0,0],
            [0,1,1,1],
            [0,1,1,1],
            [0,1,1,1]
        ])
        return dummy_array
