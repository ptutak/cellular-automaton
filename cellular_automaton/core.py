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


class Boundary(ABC):
    @abstractmethod
    def get_index(self):
        pass


class PeriodicBoundary(Boundary):
    def get_index(self, index, height, width):
        index_0 = index[0]
        index_1 = index[1]
        if index_0 < 0 or index_0 >= height:
            index_0 = (index_0 + height) % height
        if index_1 < 0  or index_1 >= width:
            index_1 = (index_1 + width) % width
        return (index_0, index_1)


class Solver:
    def __init__(self, neighborhood, state_solver, boundary):
        self._neighborhood = neighborhood
        self._state_solver = state_solver
        self._boundary = boundary

    def _get_neighbor_values(self, array, index):
        height = len(array)
        width = len(array[0])
        return (
            array[self._boundary.get_index(x, height, width)]
            for x in self._neighborhood.get_neighbors(index))

    def next_step(self, array):
        height = len(array)
        width = len(array[0])
        elements = (
            (x, y) for x in range(height) for y in range(width))
        element_and_neighbors = (
            (x, self._get_neighbor_values(array, x))
            for x in elements)
        new_elements = (
            self._state_solver.get_next_state(array[elem], neighborhood)
            for elem, neighborhood in element_and_neighbors)
        return np.fromiter(new_elements, int).reshape(height, width)
