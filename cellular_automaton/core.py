import numpy as np
import threading
from copy import deepcopy
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
    def get_next_state(self, actual_state, neighbors):
        pass

    @abstractmethod
    def ignore_ids(self, ids):
        pass


class GrainCurvatureStateSolver(StateSolver):
    def __init__(self, probability=0.5, inclusion_id = np.uint32(-1)):
        self._probability = probability
        self._empty_id = 0
        self._ignored_ids = {inclusion_id, self._empty_id}
        self._cross_set = {1, 3, 4, 6}
        self._diagonal_set = {0, 2, 5, 7}

    def _rule_five_more(self, quantity):
        for grain in quantity:
            if len(quantity[grain]) >= 5:
                return grain
        return None

    def _rule_three_cross(self, quantity):
        for grain in quantity:
            if len(quantity[grain] & self._cross_set) >= 3:
                return grain
        return None

    def _rule_three_diagonal(self, quantity):
        for grain in quantity:
            if len(quantity[grain] & self._diagonal_set) >= 3:
                return grain
        return None

    def _rule_random_choice(self, quantity):
        if np.random.sample() >= self._probability:
            return None
        chosen_grains = []
        max_quantity = 0
        for grain in quantity:
            grain_quantity = len(quantity[grain])
            if grain_quantity > max_quantity:
                max_quantity = grain_quantity
                chosen_grains = [grain]
            elif grain_quantity == max_quantity:
                chosen_grains.append(grain)
        return np.random.choice(chosen_grains)

    def ignore_ids(self, ids):
        self._ignored_ids |= set(ids)

    def get_next_state(self, actual_state, neighbors):
        if actual_state != self._empty_id:
            return actual_state
        quantity = dict()
        for i, neighbor in enumerate(neighbors):
            if neighbor in self._ignored_ids:
                continue
            if neighbor in quantity:
                quantity[neighbor].add(i)
            else:
                quantity[neighbor] = {i}
        if not quantity:
            return self._empty_id
        chosen_grain = self._rule_five_more(quantity)
        if chosen_grain:
            return chosen_grain
        chosen_grain = self._rule_three_cross(quantity)
        if chosen_grain:
            return chosen_grain
        chosen_grain = self._rule_three_diagonal(quantity)
        if chosen_grain:
            return chosen_grain
        chosen_grain = self._rule_random_choice(quantity)
        if chosen_grain:
            return chosen_grain
        return self._empty_id


class SimpleStateSolver(StateSolver):
    def __init__(self, inclusion_id=np.uint32(-1)):
        self._empty_id = 0
        self._ignored_ids = {inclusion_id, self._empty_id}

    def ignore_ids(self, ids):
        self._ignored_ids |= set(ids)

    def get_next_state(self, actual_state, neighbors):
        if actual_state:
            return actual_state
        quantity = dict()
        for neighbor in neighbors:
            if neighbor in self._ignored_ids:
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

    def add_ignored_ids(self, ids):
        self._state_solver.ignore_ids(ids)

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
    def create(self, neighborhood, boundary, state="simple-random-standard"):
        if state == "simple-random-standard":
            state = SimpleStateSolver()
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
        elif state.startswith("grain-curvature-probability:"):
            state = GrainCurvatureStateSolver(probability=float(state.split(':')[-1]))
            neighborhood = MooreNeighborhood()
        else:
            raise TypeError("No such state solver")

        if boundary == "periodic":
            boundary = PeriodicBoundary()
        elif boundary == "absorb":
            boundary = AbsorbBoundary()
        else:
            raise TypeError("No such boundary")

        return Solver(neighborhood, boundary, state)


class GrainHistory:
    def __init__(self):
        self._log = list()
        self._present_log_entry = set()

    def log_grain(self, grain):
        self._present_log_entry.add(grain)

    def log_grains(self, grains):
        for grain in grains:
            self._present_log_entry.add(grain)

    def new_phase(self):
        present_log = tuple(sorted(self._present_log_entry))
        if present_log:
            self._log.append(present_log)
        self._present_log_entry = set()

    def get_log(self):
        present_log = self._present_log_entry
        log = deepcopy(self._log)
        if present_log:
            log.append(present_log)
        return log

    def remove_grains(self, grains):
        grains = set(grains)
        for i, log_entry in enumerate(self._log):
            self._log[i] = tuple(sorted(set(log_entry) - grains))
        self._present_log_entry -= grains

    def clear(self):
        self._present_log_entry = set()
        self._log = list()

    def set_log(self, history):
        if not history:
            return
        if isinstance(history[-1], set):
            self._present_log_entry = deepcopy(history[-1])
            self._log = history[:-1]
        else:
            self._log = deepcopy(history)

    def get_flattened_closed_phases(self):
        return (x for log_entry in self._log for x in log_entry)

class SeedSelector:
    def __init__(self):
        self._selected = set()

    def toggle_seed(self, seed):
        if seed in self._selected:
            self._selected.remove(seed)
        else:
            self._selected.add(seed)

    def get_selected(self):
        selected = deepcopy(self._selected)
        return selected

    def clear(self):
        self._selected = set()


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
        self._loop_mode_lock = threading.Lock()
        self._loop_mode_function = self._array_solver_function
        self._delay = None
        self._delay_lock = threading.Lock()
        self._grain_history = GrainHistory()
        self._grain_history_lock = threading.Lock()
        self._seed_selector = SeedSelector()
        self._seed_selector_lock = threading.Lock()

    def _array_solver_function(self, array):
        with self._solver_lock:
            return self._solver.next_step(array)

    def _set_loop_mode(self, mode):
        with self._loop_mode_lock:
            if mode == 'vision':
                self._loop_mode_function = deepcopy
            elif mode == 'generation':
                self._loop_mode_function = self._array_solver_function

    def array_generator(self):
        while True:
            with self._loop_mode_lock:
                with self._array_lock:
                    self._displayed_array = self._array
                    self._array = self._loop_mode_function(self._array)
            self._set_loop_mode('generation')
            yield self._displayed_array

    def reset(self, height, width, seed_num, inclusion_num=0, inc_min_radius=0, inc_max_radius=0):
        self._array_builder.new_array(height, width)
        added_seeds = self._array_builder.add_seed(seed_num)
        self._array_builder.add_inclusions(inclusion_num, inc_min_radius, inc_max_radius)
        with self._array_lock:
            self._array = self._array_builder.get_array()
            with self._grain_history_lock:
                self._grain_history.clear()
                self._grain_history.log_grains(added_seeds)
        self.next_step()

    def clear(self):
        with self._array_lock:
            self._array = np.zeros(self._array.shape, dtype=np.uint32)
        with self._grain_history_lock:
            self._grain_history.clear()
        self.next_step()

    def select_field(self, field):
        if field:
            with self._seed_selector_lock:
                self._seed_selector.toggle_seed(field)

    def get_selected(self):
        with self._seed_selector_lock:
            return self._seed_selector.get_selected()

    def remove_selected_fields(self):
        with self._array_lock:
            if self._displayed_array is not None:
                self._array = self._displayed_array
            self._array_builder.set_array(self._array)
            with self._seed_selector_lock:
                selected = self._seed_selector.get_selected()
                self._seed_selector.clear()
            self._array_builder.remove_fields(selected)
            self._grain_history.remove_grains(selected)
            self._array = self._array_builder.get_array()
        self.next_step()

    def reseed(self, seed_num, inclusion_num=0, inc_min_radius=0, inc_max_radius=0):
        with self._array_lock:
            if self._displayed_array is not None:
                self._array = self._displayed_array
            self._array_builder.set_array(self._array)
            added_seeds = self._array_builder.add_seed(seed_num)
            with self._grain_history_lock:
                self._grain_history.log_grains(added_seeds)
            self._array_builder.add_inclusions(inclusion_num, inc_min_radius, inc_max_radius)
            self._array = self._array_builder.get_array()
            from pprint import PrettyPrinter
        self.next_step()

    def new_phase(self):
        with self._grain_history_lock:
            self._grain_history.new_phase()
            log = self._grain_history.get_log()
        with self._solver_lock:
            if log:
                self._solver.add_ignored_ids(log[-1])
        self.next_vision_step()

    def update_solver(self, neighborhood, boundary, state="simple-random-standard"):
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

    def next_vision_step(self):
        self._set_loop_mode('vision')
        self.next_step()

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

    def save(self, filename, mode="single"):
        with self._array_lock:
            array = self._displayed_array
            with self._grain_history_lock:
                log = self._grain_history.get_log()
        if filename.endswith('.csv'):
            with open(filename, 'w') as file:
                for row in array:
                    file.write(','.join((str(x) for x in row)))
                    file.write('\n')
                file.write("#grains:{}:{}\n".format(log, mode))
        if filename.endswith('.png'):
            image = Image.fromarray(array, 'CMYK').convert('RGB')
            image.save(filename)

    def load(self, filename):
        array = []
        if filename.endswith('.csv'):
            lines = (
                line.strip().split(',')
                for line in open(filename)
                if line.strip() and not line.startswith('#grains'))
            _, log, mode = next(
                line.strip().split(':')
                for line in open(filename)
                if line.strip().startswith('#grains'))
            array.extend(lines)
        with self._array_lock:
            self._array = np.array(array, dtype=np.uint32)
            log = eval(log)
            with self._grain_history_lock:
                self._grain_history.set_log(log)
                ignored_ids =  self._grain_history.get_flattened_closed_phases()
            with self._solver_lock:
                self._solver.add_ignored_ids(ignored_ids)
        self.next_step()


class ArrayBuilder:
    def __init__(self,
                 cmyk_min=np.uint32(np.iinfo(np.uint32).max * 1 / 5),
                 cmyk_max=np.uint32(np.iinfo(np.uint32).max * 3 / 5),
                 inclusion_id=np.uint32(-1)):
        self._cmyk_min = cmyk_min
        self._cmyk_max = cmyk_max
        self._array = None
        self._inclusion_id = inclusion_id
        self._empty_id = 0
        self._seed_ids = set()

    def get_array(self):
        return self._array

    def set_array(self, array):
        self._array = array

    def new_array(self, height, width):
        self._array = np.zeros((height, width), dtype=np.uint32)

    def remove_fields(self, id_set):
        def get_proper_array_value(elem):
            if elem in id_set:
                return self._empty_id
            return elem
        new_array_gen = (get_proper_array_value(elem) for row in self._array for elem in row)
        new_array = np.array(list(new_array_gen), dtype=np.uint32)
        new_array.resize(self._array.shape)
        self._array = new_array

    def add_seed(self, seed_num):
        empty_fields = sorted(self.get_empty_fields())
        seed_coords_indices = np.random.choice(np.arange(len(empty_fields)), seed_num)
        present_seeds = self.get_seed_ids()
        added_seeds = set()
        for index in seed_coords_indices:
            while True:
                seed = np.random.randint(
                    self._cmyk_min,
                    self._cmyk_max,
                    dtype=np.uint32)
                if seed not in present_seeds and seed not in added_seeds:
                    break
            added_seeds.add(seed)
            self._array[empty_fields[index]] = seed
        return added_seeds

    def _horizontal_line(self, x0, y0, y1):
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
        point_set |= self._horizontal_line(x0, y0 - radius, y0 + radius)
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
            point_set |= self._horizontal_line(x0 + x, y0 - y, y0 + y)
            point_set |= self._horizontal_line(x0 - x, y0 - y, y0 + y)
            point_set |= self._horizontal_line(x0 + y, y0 - x, y0 + x)
            point_set |= self._horizontal_line(x0 - y, y0 - x, y0 + x)

        return point_set

    def add_inclusions(self, inclusion_number, min_radius, max_radius):
        min_index = 0
        max_height_index = self._array.shape[0] - 1
        max_width_index = self._array.shape[1] - 1

        empty_fields = self.get_empty_fields()
        filled_fields = set(self.get_filled_fields())

        empty_filtered_fields = set(
            field
            for field in empty_fields
            if field[0] >= min_index + min_radius
            and field[0] <= max_height_index - min_radius
            and field[1] >= min_index + min_radius
            and field[1] <= max_width_index - min_radius)

        for filled in filled_fields:
            circle = self.filled_circle(filled[0], filled[1], min_radius)
            empty_filtered_fields -= circle

        inclusions = set()

        while len(inclusions) < inclusion_number:
            empty_fields_left = len(empty_filtered_fields)
            if not empty_fields_left:
                break
            field_index = np.random.randint(empty_fields_left)
            field = list(empty_filtered_fields)[field_index]
            inclusions.add(field)
            circle = self.filled_circle(field[0], field[1], min_radius + max_radius)
            empty_filtered_fields -= circle

        inclusion_circles = set()

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
            self._array[coords] = self._inclusion_id

    def get_filled_fields(self):
        field_set = (
            (x, y) for x in range(self._array.shape[0])
            for y in range(self._array.shape[1])
            if self._array[(x, y)] != self._empty_id
        )
        return field_set

    def get_empty_fields(self):
        field_set = (
            (x, y) for x in range(self._array.shape[0])
            for y in range(self._array.shape[1])
            if self._array[(x, y)] == self._empty_id
        )
        return field_set

    def get_seed_ids(self):
        ids = {
            x for row in self._array
            for x in row
            if x != self._empty_id and x != self._inclusion_id}
        return ids
