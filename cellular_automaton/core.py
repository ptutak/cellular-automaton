import numpy as np
import threading
from abc import ABC, abstractmethod
from PIL import Image
from fractions import Fraction


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
    def __init__(self, empty_id=0, inclusion_id=np.uint32(-1)):
        self._empty_id = empty_id
        self._inclusion_id = inclusion_id

    def get_next_state(self, actual_state, neighbors):
        if actual_state:
            return actual_state
        quantity = dict()
        for neighbor in neighbors:
            if not neighbor or neighbor == self._inclusion_id:
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
        return np.fromiter(new_elements, np.uint32).reshape(height, width)


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
        self._array_builder = ArrayBuilder()
        self._array = None
        self._displayed_array = None
        self._array_lock = threading.Lock()
        self._solver = self._solver_creator.create("Moore", "periodic")
        self._solver_lock = threading.Lock()
        self._loop_on = False
        self._loop_lock = threading.Lock()
        self._loop_gate = threading.Event()
        self._delay = None
        self._delay_lock = threading.Lock()

    def array_generator(self):
        while True:
            with self._solver_lock:
                with self._array_lock:
                    self._displayed_array = self._array
                    self._array = self._solver.next_step(self._array)
            yield self._displayed_array

    def reset(self, height, width, seed_num, inclusion_num=0, inc_min_radius=0, inc_max_radius=0):
        self._array_builder.new_array(height, width)
        self._array_builder.add_seed(seed_num)
        self._array_builder.add_inclusions(inclusion_num, inc_min_radius, inc_max_radius)
        with self._array_lock:
            self._array = self._array_builder.get_array()

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
            self._array = np.array(array, dtype=np.uint32)
        self.next_step()


class ArrayBuilder:
    def __init__(self,
                 cmyk_min=np.uint32(np.iinfo(np.uint32).max * 1 / 5),
                 cmyk_max=np.uint32(np.iinfo(np.uint32).max * 3 / 5),
                 inclusion_value=np.uint32(-1)):
        self._cmyk_min = cmyk_min
        self._cmyk_max = cmyk_max
        self._array = None
        self._inclusion_value = inclusion_value

    def get_array(self):
        return self._array

    def new_array(self, height, width):
        self._array = np.zeros((height, width), dtype=np.uint32)

    def add_seed(self, seed_num):
        empty_fields = sorted(self.get_empty_fields())
        seed_coords_indices = np.random.choice(np.arange(len(empty_fields)), seed_num)

        for index in seed_coords_indices:
            self._array[empty_fields[index]] = np.random.randint(
                self._cmyk_min,
                self._cmyk_max,
                dtype=np.uint32)

    def horizontal_line(self, x0, y0, y1):
        point_set = set()
        for y in range(y0, y1 + 1):
            point_set.add((x0, y))
        return point_set

    def filled_circle(self, x0, y0, radius):
        f = 1 - radius
        ddf_x = 1
        ddf_y = -2 * radius
        x = 0
        y = radius
        point_set = set()
        point_set.add((x0, y0 + radius))
        point_set.add((x0, y0 - radius))
        point_set |= self.horizontal_line(x0, y0 - radius, y0 + radius)
        point_set.add((x0 + radius, y0))
        point_set.add((x0 - radius, y0))

        while x < y:
            if f >= 0:
                y -= 1
                ddf_y += 2
                f += ddf_y
            x += 1
            ddf_x += 2
            f += ddf_x
            point_set.add((x0 + x, y0 + y))
            point_set.add((x0 - x, y0 + y))
            point_set.add((x0 + x, y0 - y))
            point_set.add((x0 - x, y0 - y))
            point_set.add((x0 + y, y0 + x))
            point_set.add((x0 - y, y0 + x))
            point_set.add((x0 + y, y0 - x))
            point_set.add((x0 - y, y0 - x))
            point_set |= self.horizontal_line(x0 + x, y0 - y, y0 + y)
            point_set |= self.horizontal_line(x0 - x, y0 - y, y0 + y)
            point_set |= self.horizontal_line(x0 + y, y0 - x, y0 + x)
            point_set |= self.horizontal_line(x0 - y, y0 - x, y0 + x)

        return point_set

    def add_inclusions(self, inclusion_number, min_radius, max_radius):
        empty_fields = sorted(self.get_empty_fields())

        min_index = 0
        max_height_index = self._array.shape[0] - 1
        max_width_index = self._array.shape[1] - 1

        inclusion_coords_indices = np.random.choice(np.arange(len(empty_fields)), inclusion_number)

        inclusions = set()
        for index in inclusion_coords_indices:
            inclusions.add(empty_fields[index])

        inclusion_circles = set()
        filled_fields = self.get_filled_fields()

        for coords in set(inclusions):
            inclusions.discard(coords)
            radius = np.random.randint(min_radius, max_radius + 1)
            while True:
                filled_circle = self.filled_circle(coords[0], coords[1], radius)
                if filled_circle & filled_fields\
                or filled_circle & inclusions\
                or filled_circle & inclusion_circles\
                or coords[0] + radius > max_height_index\
                or coords[0] - radius < min_index\
                or coords[1] + radius > max_width_index\
                or coords[1] - radius < min_index:
                    radius -= 1
                else:
                    break
            inclusion_circles |= filled_circle

        for coords in inclusion_circles:
            self._array[coords] = self._inclusion_value

    def get_filled_fields(self):
        field_set = {
            (x, y) for x in range(self._array.shape[0])
            for y in range(self._array.shape[1])
            if self._array[(x, y)]}
        return field_set

    def get_empty_fields(self):
        field_set = {
            (x, y) for x in range(self._array.shape[0])
            for y in range(self._array.shape[1])
            if not self._array[(x, y)]
        }
        return field_set
