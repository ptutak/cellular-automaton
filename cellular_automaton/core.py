import numpy as np
import threading
from abc import ABC, abstractmethod
from PIL import Image


class Neighborhood(ABC):
    @abstractmethod
    def get_neighbors(self, index_0, index_1):
        pass


class MooreNeighborhood(Neighborhood):
    def get_neighbors(self, index_0, index_1):
        return ((index_0 - 1, index_1 - 1),
                (index_0 - 1, index_1),
                (index_0 - 1, index_1 + 1),
                (index_0, index_1 - 1),
                (index_0, index_1 + 1),
                (index_0 + 1, index_1 - 1),
                (index_0 + 1, index_1),
                (index_0 + 1, index_1 + 1))


class NeumannNeighborhood(Neighborhood):
    def get_neighbors(self, index_0, index_1):
        return (
            (index_0-1, index_1),
            (index_0, index_1 - 1),
            (index_0, index_1 + 1),
            (index_0 + 1, index_1)
        )


class HexagonalLeftNeighborhood(Neighborhood):
    def get_neighbors(self, index_0, index_1):
        return (
            (index_0 - 1, index_1),
            (index_0 - 1, index_1 + 1),
            (index_0, index_1 - 1),
            (index_0, index_1 + 1),
            (index_0 + 1, index_1 - 1),
            (index_0 + 1, index_1)
        )


class HexagonalRightNeighborhood(Neighborhood):
    def get_neighbors(self, index_0, index_1):
        return (
            (index_0 - 1, index_1 - 1),
            (index_0 - 1, index_1),
            (index_0, index_1 - 1),
            (index_0, index_1 + 1),
            (index_0 + 1, index_1),
            (index_0 + 1, index_1 + 1)
        )


class HexagonalRandom(Neighborhood):
    def get_neighbors(self, index_0, index_1):
        if np.random.randint(2):
            return (
                (index_0 - 1, index_1),
                (index_0 - 1, index_1 + 1),
                (index_0, index_1 - 1),
                (index_0, index_1 + 1),
                (index_0 + 1, index_1 - 1),
                (index_0 + 1, index_1)
            )
        return (
            (index_0 - 1, index_1 - 1),
            (index_0 - 1, index_1),
            (index_0, index_1 - 1),
            (index_0, index_1 + 1),
            (index_0 + 1, index_1),
            (index_0 + 1, index_1 + 1)
        )


class PentagonalLeft(Neighborhood):
    def get_neighbors(self, index_0, index_1):
        return (
            (index_0 - 1, index_1 - 1),
            (index_0 - 1, index_1),
            (index_0, index_1 - 1),
            (index_0 + 1, index_1 - 1),
            (index_0 + 1, index_1)
        )


class PentagonalRight(Neighborhood):
    def get_neighbors(self, index_0, index_1):
        return (
            (index_0 - 1, index_1),
            (index_0 - 1, index_1 + 1),
            (index_0, index_1 + 1),
            (index_0 + 1, index_1),
            (index_0 + 1, index_1 + 1)
        )


class PentagonalRandom(Neighborhood):
    def get_neighbors(self, index_0, index_1):
        if np.random.randint(2):
            return (
                (index_0 - 1, index_1 - 1),
                (index_0 - 1, index_1),
                (index_0, index_1 - 1),
                (index_0 + 1, index_1 - 1),
                (index_0 + 1, index_1)
            )
        return (
            (index_0 - 1, index_1),
            (index_0 - 1, index_1 + 1),
            (index_0, index_1 + 1),
            (index_0 + 1, index_1),
            (index_0 + 1, index_1 + 1)
        )


class StateSolver(ABC):
    @abstractmethod
    def get_next_state(self, neighbors):
        pass


class SimpleStateSolver(StateSolver):
    def __init__(self, empty_id=0, inclusion_id=-1):
        self._empty_id = empty_id
        self._inclusion_id = inclusion_id

    def get_next_state(self, actual_state, neighbors):
        if actual_state:
            return actual_state
        quantity = dict()
        for neighbor in neighbors:
            if not neighbor or neighbor == -1:
                continue
            if neighbor in quantity:
                quantity[neighbor] += 1
            else:
                quantity[neighbor] = 1
        if not quantity:
            return self._empty_id
        max_neigh = []
        max_quantity = 0
        for neighbor, quant in quantity.items():
            if quant > max_quantity:
                max_neigh = [neighbor]
            elif quant == max_quantity:
                max_neigh.append(neighbor)
        if len(max_neigh) > 1:
            return np.random.choice(max_neigh)
        else:
            return max_neigh[0]


class Boundary(ABC):
    @abstractmethod
    def get_value(self):
        pass


class PeriodicBoundary(Boundary):
    def get_value(self, index, array, height, width):
        index_0 = index[0]
        index_1 = index[1]
        if index_0 < 0 or index_0 >= height:
            index_0 = (index_0 + height) % height
        if index_1 < 0 or index_1 >= width:
            index_1 = (index_1 + width) % width
        return array[(index_0, index_1)]


class AbsorbBoundary(Boundary):
    def get_value(self, index, array, height, width):
        index_0 = index[0]
        index_1 = index[1]
        if index_0 < 0 or index_0 >= height:
            return 0
        if index_1 < 0 or index_1 >= width:
            return 0
        return array[(index_0, index_1)]


class Solver:
    def __init__(self, neighborhood, boundary, state_solver):
        self._neighborhood = neighborhood
        self._state_solver = state_solver
        self._boundary = boundary

    def _get_neighbor_values(self, array, index):
        height = len(array)
        width = len(array[0])
        index_value = array[index]
        if index_value:
            return (index_value, ())
        return (
            index_value,
            (self._boundary.get_value(x, array, height, width)
             for x in self._neighborhood.get_neighbors(index[0], index[1])))

    def next_step(self, array):
        height = len(array)
        width = len(array[0])
        elements = (
            (x, y) for x in range(height) for y in range(width))
        element_and_neighbors = (
            self._get_neighbor_values(array, x)
            for x in elements)
        new_elements = (
            self._state_solver.get_next_state(elem, neighborhood)
            for elem, neighborhood in element_and_neighbors)
        return np.fromiter(new_elements, np.int32).reshape(height, width)


class SolverCreator:
    def create(self, neighborhood, boundary, state="left-standard"):
        if neighborhood == "Moore":
            neighborhood = MooreNeighborhood()
        elif neighborhood == "Neumann":
            neighborhood = NeumannNeighborhood()
        elif neighborhood == "hexagonal-left":
            neighborhood = HexagonalLeftNeighborhood()
        elif neighborhood == "hexagonal-right":
            neighborhood = HexagonalRightNeighborhood()
        elif neighborhood == "hexagonal-random":
            neighborhood = HexagonalRandom()
        elif neighborhood == "pentagonal-left":
            neighborhood = PentagonalLeft()
        elif neighborhood == "pentagonal-right":
            neighborhood = PentagonalRight()
        elif neighborhood == "pentagonal-random":
            neighborhood = PentagonalRandom()
        else:
            raise TypeError("No such neighborhood")

        if boundary == "periodic":
            boundary = PeriodicBoundary()
        elif boundary == "absorb":
            boundary = AbsorbBoundary()
        else:
            raise TypeError("No such boundary")

        if state == "left-standard":
            state = SimpleStateSolver()
        else:
            raise TypeError("No such state solver")

        return Solver(neighborhood, boundary, state)


class MainController:
    def __init__(self):
        self._solver_creator = SolverCreator()
        self._array = None
        self._displayed_array = None
        self._array_lock = threading.Lock()
        self._solver = self._solver_creator.create("Moore", "periodic")
        self._solver_lock = threading.Lock()
        self._cmyk_min = 0
        self._cmyk_max = np.uint32(np.iinfo(np.uint32).max * 3 / 5)
        self._loop_on = False
        self._delay = None
        self._loop_lock = threading.Lock()
        self._delay_lock = threading.Lock()
        self._loop_gate = threading.Event()

    def array_generator(self):
        while True:
            with self._solver_lock:
                with self._array_lock:
                    self._displayed_array = self._array
                    self._array = self._solver.next_step(self._array)
            yield self._displayed_array

    def reset(self, height, width, seed_num):
        heights = np.arange(height)
        np.random.shuffle(heights)
        widths = np.arange(width)
        np.random.shuffle(widths)
        coordinates = zip(
            heights[:seed_num],
            widths[:seed_num],
            np.random.randint(self._cmyk_min, self._cmyk_max, size=seed_num, dtype=np.uint32))
        array = np.zeros((height, width), np.int32)
        for coords in coordinates:
            array[coords[:2]] = coords[2]
        with self._array_lock:
            self._array = array

    def update_solver(self, neighborhood, boundary, state="left-standard"):
        with self._solver_lock:
            self._solver = self._solver_creator.create(
                neighborhood,
                boundary,
                state)

    def open_gate(self):
        with self._loop_lock:
            self._loop_on = True
            self._loop_gate.set()

    def close_gate(self):
        with self._loop_lock:
            self._loop_on = False
            self._loop_gate.clear()

    def control_gate(self):
        self._loop_gate.wait()
        with self._loop_lock:
            if self._loop_gate.is_set() and not self._loop_on:
                self._loop_gate.clear()

    def next_step(self):
        self._loop_gate.set()

    def start_stop(self):
        with self._loop_lock:
            if self._loop_on:
                self._loop_on = False
                self._loop_gate.clear()
            else:
                self._loop_on = True
                self._loop_gate.set()


    def update_delay(self, delay):
        with self._delay_lock:
            self._delay = delay

    def get_delay(self):
        with self._delay_lock:
            return self._delay

    def save(self, filename):
        with self._array_lock:
            array = self._displayed_array
        if filename.endswith('.csv'):
            with open(filename, 'w') as file:
                for row in array:
                    file.write(','.join((str(x) for x in row)))
                    file.write('\n')
        if filename.endswith('.png'):
            image = Image.fromarray(array, 'CMYK').convert('RGB')
            image.save(filename)

    def load(self, filename):
        array = []
        if filename.endswith('.csv'):
            lines = (line.strip().split(',') for line in open(filename) if line.strip())
            array.extend(lines)
        with self._array_lock:
            self._array = np.array(array, dtype=np.int32)
        self.next_step()

