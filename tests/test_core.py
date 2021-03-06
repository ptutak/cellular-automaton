import numpy as np
import cellular_automaton.core as core
import os
from copy import deepcopy

class TestNeighborhood:
    def test_moore(self):
        moore = core.MooreNeighborhood()
        neighbors = set(moore.get_neighbors(1,1))
        valid_neighbors = {(0,0), (0,1), (0,2), (1,0), (1,2), (2,0), (2,1), (2,2)}
        assert neighbors == valid_neighbors

    def test_neumann(self):
        neumann = core.NeumannNeighborhood()
        neighbors = set(neumann.get_neighbors(1,1))
        valid_neighbors = {(0,1), (1,0), (1,2), (2,1)}
        assert neighbors == valid_neighbors

    def test_hexagonal_left(self):
        hexagonal_left = core.HexagonalLeftNeighborhood()
        neighbors = set(hexagonal_left.get_neighbors(1, 1))
        valid_neighbors = {(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)}
        assert neighbors == valid_neighbors

    def test_hexagonal_right(self):
        hexagonal_right = core.HexagonalRightNeighborhood()
        neighbors = set(hexagonal_right.get_neighbors(1, 1))
        valid_neighbors = {(0, 0), (0, 1), (1, 0), (1, 2), (2, 1), (2, 2)}
        assert neighbors == valid_neighbors

    def test_hexagonal_random(self):
        hexagonal_random = core.HexagonalRandom()
        np.random.seed(7)
        neighbors = set(hexagonal_random.get_neighbors(1, 1))
        valid_neighbors = {(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)}
        assert neighbors == valid_neighbors

    def test_pentagonal_left(self):
        pentagonal_left = core.PentagonalLeft()
        neighbors = set(pentagonal_left.get_neighbors(1, 1))
        valid_neighbors = {(0, 0), (0, 1), (1, 0), (2, 0), (2, 1)}
        assert neighbors == valid_neighbors

    def test_pentagonal_right(self):
        pentagonal_right = core.PentagonalRight()
        neighbors = set(pentagonal_right.get_neighbors(1, 1))
        valid_neighbors = {(0, 1), (0, 2), (1, 2), (2, 1), (2, 2)}
        assert neighbors == valid_neighbors

    def test_pentagonal_random(self):
        pentagonal_random = core.PentagonalRandom()
        np.random.seed(7)
        neighbors = set(pentagonal_random.get_neighbors(1, 1))
        valid_neighbors = {(0, 0), (0, 1), (1, 0), (2, 0), (2, 1)}
        assert neighbors == valid_neighbors

class TestSolver:
    def test_next_step(self):
        neighborhood = core.MooreNeighborhood()
        state_solver = core.SimpleStateSolver()
        boundary = core.PeriodicBoundary()
        solver = core.Solver(neighborhood, boundary, state_solver)
        array = np.array([
            [0,0,0,0],
            [0,0,0,0],
            [0,0,1,0],
            [0,0,0,0]])
        new_array = solver.next_step(array)
        assert np.array_equal(new_array, np.array([
            [0,0,0,0],
            [0,1,1,1],
            [0,1,1,1],
            [0,1,1,1]]))

    def test_get_neighbor_values(self):
        neighborhood = core.MooreNeighborhood()
        state_solver = core.SimpleStateSolver()
        boundary = core.PeriodicBoundary()
        solver = core.Solver(neighborhood, boundary, state_solver)
        array = np.array([
            [0,0,0],
            [1,0,0],
            [0,1,0]
        ])
        values = [0,0,1,0,0,0,1,0]
        assert values == list(solver._get_neighbor_values(array, (0,0))[1])

    def test_add_ignored_ids(self):
        neighborhood = core.MooreNeighborhood()
        state_solver = core.SimpleStateSolver()
        boundary = core.PeriodicBoundary()
        solver = core.Solver(neighborhood, boundary, state_solver)
        solver.add_ignored_ids([5, 6, 7])
        assert solver._state_solver._ignored_ids == {0, 5, 6, 7, 0xffffffff}

    def test_get_statistics(self):
        neighborhood = core.MooreNeighborhood()
        state_solver = core.SimpleStateSolver()
        boundary = core.AbsorbBoundary()
        solver = core.Solver(neighborhood, boundary, state_solver)
        array = np.array([
            [1,1,1,1],
            [1,1,1,1],
            [1,1,1,1],
            [1,1,1,1]], dtype=np.uint32)
        length = solver.get_boundary_length(array)
        assert length == 6

class TestSimpleStateSolver:
    def test_next_elem(self):
        array = np.array([
            [0,0,0,0],
            [0,0,0,0],
            [0,0,1,0],
            [0,0,0,0]])
        neighborhood = core.MooreNeighborhood()
        neighbors_indices = neighborhood.get_neighbors(1,1)
        neighbors_1_1 = (array[index] for index in neighbors_indices)
        state_solver = core.SimpleStateSolver()
        new_state = state_solver.get_next_state(array[(1,1)], neighbors_1_1)
        assert new_state == 1

    def test_ignore_ids(self):
        solver = core.SimpleStateSolver()
        assert solver._ignored_ids == {0, 0xffffffff}
        solver.ignore_ids([5, 6])
        assert solver._ignored_ids == {0, 5, 6, 0xffffffff}


class TestGrainCurvatureStateSolver:
    """
    grain placement numeration:
    [
        [0, 1, 2],
        [3, x, 4],
        [5, 6, 7]
    ]
    """
    def test_next_elem(self):
        np.random.seed(7)
        solver = core.GrainCurvatureStateSolver(probability=0.5)
        state = 0
        neighbors = [
            1, 1, 1,
            1,    0,
            1, 0, 0
        ]
        assert solver.get_next_state(state, neighbors) == 1
        neighbors = [
            0, 1, 0,
            1,    0,
            1, 0, 0
        ]
        solver._probability = 0.07
        assert solver.get_next_state(state, neighbors) == 0

    def test_rule_five_more(self):
        solver = core.GrainCurvatureStateSolver()
        quantity = {
            3 : {0, 1, 2, 3, 4},
            2 : {5, 6}
        }
        assert solver._rule_five_more(quantity) == 3
        quantity = {
            1 : {1, 2, 3},
            2 : {4, 5}
        }
        assert solver._rule_five_more(quantity) is None

    def test_rule_three_cross(self):
        solver = core.GrainCurvatureStateSolver()
        quantity = {
            1 : {3, 4, 6},
            2 : {1, 5, 7}
        }
        assert solver._rule_three_cross(quantity) == 1
        quantity = {
            1 : {1, 5, 7},
            2 : {3, 4}
        }
        assert solver._rule_three_cross(quantity) is None

    def test_rule_three_diagonal(self):
        solver = core.GrainCurvatureStateSolver()
        quantity = {
            1 : {0, 2, 7},
            2 : {4, 6, 5}
        }
        assert solver._rule_three_diagonal(quantity) == 1
        quantity = {
            1 : {0, 2, 4},
            2 : {5, 6, 7}
        }
        assert solver._rule_three_diagonal(quantity) is None

    def test_rule_random_choice(self):
        solver = core.GrainCurvatureStateSolver(probability=0)
        quantity = {
            1 : {0, 1, 2},
            2 : {3, 5, 6},
            3 : {4, 7}
        }
        np.random.seed(7)
        assert solver._rule_random_choice(quantity) is None
        solver._probability = 0.8
        assert solver._rule_random_choice(quantity) == 2

    def test_ignore_ids(self):
        solver = core.GrainCurvatureStateSolver(probability=0)
        assert solver._ignored_ids == {0, np.uint32(-1)}
        solver.ignore_ids([3, 4])
        assert solver._ignored_ids == {0, 3, 4, np.uint32(-1)}


class TestPeriodicBoundary:
    def test_get_boundary(self):
        boundary = core.PeriodicBoundary()
        height = 100
        width = 50
        array = np.eye(100, 50, 0, np.int32)
        assert 0 == boundary.get_value((-1, -1), array, height, width)
        assert 1 == boundary.get_value((100, 50), array, height, width)
        assert 1 == boundary.get_value((5, 5), array, height, width)


class TestAbsorbBoundary:
    def test_get_boundary(self):
        boundary = core.AbsorbBoundary()
        height = 100
        width = 50
        array = np.eye(100, 50, 0, np.int32)
        assert 0 == boundary.get_value((-1, -1), array, height, width)
        assert 0 == boundary.get_value((100, 50), array, height, width)
        assert 1 == boundary.get_value((5, 5), array, height, width)


class TestSolverCreator:
    def test_create(self):
        creator = core.SolverCreator()
        solver = creator.create("Moore", "periodic")
        assert isinstance(solver._neighborhood, core.MooreNeighborhood)
        assert isinstance(solver._boundary, core.PeriodicBoundary)
        assert isinstance(solver._state_solver, core.SimpleStateSolver)
        solver = creator.create(None, "periodic", "grain-curvature-probability:0.4")
        assert isinstance(solver._neighborhood, core.MooreNeighborhood)
        assert isinstance(solver._boundary, core.PeriodicBoundary)
        assert isinstance(solver._state_solver, core.GrainCurvatureStateSolver)
        assert solver._state_solver._probability == 0.4


class TestMainController:
    def test_update_solver(self):
        controller = core.MainController()
        controller.update_solver("Neumann", "absorb")
        assert isinstance(
            controller._solver._neighborhood,
            core.NeumannNeighborhood)
        assert isinstance(
            controller._solver._boundary,
            core.AbsorbBoundary)

    def test_update_delay(self):
        controller = core.MainController()
        controller.update_delay(0.55)
        assert controller.get_delay() == 0.55

    def test_array_generator(self):
        controller = core.MainController()
        arrays = controller.array_generator()
        controller._array = np.zeros((3, 3), np.int32)
        array = next(arrays)
        assert np.array_equal(array, np.zeros((3, 3), np.int32))
        array = next(arrays)
        assert np.array_equal(array, np.zeros((3, 3), np.int32))

    def test_array_solver_function(self):
        controller = core.MainController()
        array = np.array([
            [1, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ], dtype=np.uint32)
        next_array = controller._array_solver_function(array)
        assert np.array_equal(next_array, np.ones((3, 3), dtype=np.uint32))

    def test_set_loop_mode(self):
        controller = core.MainController()
        assert controller._loop_mode_function == controller._array_solver_function
        controller._set_loop_mode('vision')
        assert controller._loop_mode_function == deepcopy

    def test_reset(self):
        controller = core.MainController()
        np.random.seed(7)
        controller.reset(3, 3, 3, 2, 0, 0)
        arrays = controller.array_generator()
        array = next(arrays)
        good_array = np.array([
            [4294967295, 4294967295, 0],
            [1024331969, 1818769098, 0],
            [2181898220, 0, 0]
        ])
        assert np.array_equal(array, good_array)

    def test_clear(self):
        controller = core.MainController()
        controller._array = np.array([
            [0, 0, 1],
            [0, 0, 1],
            [2, 0, 3]
        ], dtype=np.uint32)
        controller.clear()
        array = next(controller.array_generator())
        assert np.array_equal(array, np.array([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]))

    def test_remove_selected_fields(self):
        controller = core.MainController()
        controller._array = np.array([
            [0, 0, 1],
            [0, 0, 1],
            [2, 0, 3]
        ], dtype=np.uint32)
        controller._grain_history.log_grains({1, 2, 3})
        controller.new_phase()
        controller.select_field(1)
        controller.select_field(2)
        controller.remove_selected_fields()
        array = next(controller.array_generator())
        assert np.array_equal(
            array,
            np.array([
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 3]
            ]))
        assert controller._grain_history.get_log() == [(3,)]

    def test_select_fields(self):
        controller = core.MainController()
        controller.select_field(1)
        controller.select_field(2)
        assert controller._seed_selector.get_selected() == {1, 2}

    def test_reseed(self):
        controller = core.MainController()
        controller._array = np.array([
            [0, 0, 1],
            [0, 0, 1],
            [2, 0, 3]
        ], dtype=np.uint32)
        np.random.seed(7)
        controller.reseed(2, 0, 0, 0)
        array = next(controller.array_generator())
        assert np.array_equal(
            array,
            np.array([
                [0, 1818769098, 1],
                [0, 0, 1],
                [2, 2228968745, 3]
            ])
        )

    def test_open_gate(self):
        controller = core.MainController()
        controller._loop_on = False
        controller._loop_gate.clear()
        controller.open_gate()
        assert controller._loop_gate.is_set()
        assert controller._loop_on

    def test_close_gate(self):
        controller = core.MainController()
        controller._loop_on = True
        controller._loop_gate.set()
        controller.close_gate()
        assert not controller._loop_gate.is_set()
        assert not controller._loop_on

    def test_control_gate(self):
        controller = core.MainController()
        controller._loop_gate.set()
        controller._loop_on = False
        controller.control_gate()
        assert not controller._loop_gate.is_set()

    def test_next_step(self):
        controller = core.MainController()
        controller._loop_gate.clear()
        controller.next_step()
        assert controller._loop_gate.is_set()

    def test_next_vision_step(self):
        controller = core.MainController()
        controller.next_vision_step()
        assert controller._loop_mode_function == deepcopy

    def test_start_stop(self):
        controller = core.MainController()
        assert not controller._loop_on
        assert not controller._loop_gate.is_set()
        controller.start_stop()
        assert controller._loop_on
        assert controller._loop_gate.is_set()
        controller.start_stop()
        assert not controller._loop_on
        assert not controller._loop_gate.is_set()

    def test_get_delay(self):
        controller = core.MainController()
        assert controller.get_delay() is None
        controller.update_delay(0.5)
        assert controller.get_delay() == 0.5

    def test_get_selected(self):
        controller = core.MainController()
        controller.select_field(5)
        controller.select_field(4)
        assert controller.get_selected() == {4, 5}

    def test_save(self):
        controller = core.MainController()
        np.random.seed(7)
        controller._displayed_array = np.array([
                [0, 0, 0],
                [0, 1, 0],
                [0, 0, 0]
            ], dtype=np.uint32)
        filename = 'test.save.core.main.controller.csv'
        controller.save(filename)
        lines = (line.strip().split(',') for line in open(filename) if line.strip() and not line.startswith('#'))
        os.remove(filename)
        array = []
        array.extend(lines)
        assert np.array_equal(np.array(array, dtype=np.uint32), controller._displayed_array)

    def test_load(self):
        controller = core.MainController()
        filecontent = """1,1,1
2,1,2
3,1,1
#grains:[]:single
"""
        filename = 'test.load.core.main.controller.csv'
        with open(filename, 'w') as f:
            f.write(filecontent)

        controller.load(filename)
        good_array = np.array([
            [1, 1, 1],
            [2, 1, 2],
            [3, 1, 1]
        ], dtype=np.uint32)
        os.remove(filename)
        assert np.array_equal(good_array, controller._array)

    def test_new_phase(self):
        controller = core.MainController()
        controller._array = np.array([
            [0, 0, 1],
            [0, 0, 1],
            [2, 0, 3]
        ], dtype=np.uint32)
        controller._grain_history.log_grains([1, 2, 3])
        controller.new_phase()
        next(controller.array_generator())
        assert np.array_equal(
            next(controller.array_generator()),
            np.array([
                [0, 0, 1],
                [0, 0, 1],
                [2, 0, 3]
            ]))

    def test_get_statistcs(self):
        controller = core.MainController()
        controller._displayed_array = np.array([
            [2, 2, 3, 3, 3],
            [2, 2, 3, 3, 3],
            [2, 2, 3, 3, 3],
            [2, 2, 3, 3, 3]
        ], dtype=np.uint32)
        controller._grain_history.log_grains([2, 3])
        controller._solver = core.SolverCreator().create("Moore", "periodic")
        statistics = controller.get_statistics()
        assert statistics == {
            "grain_boundary_length": 8,
            "average_size": 10
        }

class TestArrayBuilder:
    def test_get_array(self):
        builder = core.ArrayBuilder()
        assert builder.get_array() is None

    def test_set_array(self):
        builder = core.ArrayBuilder()
        builder.set_array(np.ones((5, 5)))
        assert np.array_equal(builder.get_array(), np.ones((5, 5)))

    def test_new_array(self):
        builder = core.ArrayBuilder()
        builder.new_array(3, 3)
        assert np.array_equal(builder.get_array(), np.zeros((3, 3), dtype=np.uint32))

    def test_add_seed(self):
        builder = core.ArrayBuilder()
        builder.new_array(3, 3)
        np.random.seed(7)
        builder.add_seed(3)
        assert np.array_equal(
            builder.get_array(),
            np.array([
                [0, 0, 0],
                [1024331969, 1818769098, 0],
                [2181898220, 0, 0]
            ]))

    def test_add_inclusions(self):
        builder = core.ArrayBuilder()
        builder.new_array(3, 3)
        np.random.seed(7)
        builder.add_seed(3)
        builder.add_inclusions(2, 0, 0)
        assert np.array_equal(
            builder.get_array(),
            np.array([
                [4294967295, 4294967295, 0],
                [1024331969, 1818769098, 0],
                [2181898220, 0, 0]
            ])
        )

    def test_horizontal_line(self):
        builder = core.ArrayBuilder()
        line = builder._horizontal_line(5, -3, 0)
        assert line == set(((5, -3), (5, -2), (5, -1), (5, 0)))
        line = builder._horizontal_line(5, 0, -3)
        assert line == set()
        line = builder._horizontal_line(5, 0, 0)
        assert line == set(((5, 0),))

    def test_filled_circle(self):
        builder = core.ArrayBuilder()
        circle = builder.filled_circle(5, 5, 2)
        good_circle = {
            (6, 4), (5, 4), (4, 7), (6, 6), (5, 6), (4, 5), (7, 5),
            (6, 5), (3, 5), (5, 3), (6, 7), (5, 5), (4, 6), (7, 6),
            (5, 7), (4, 4), (6, 3), (7, 4), (4, 3), (3, 6), (3, 4)}
        assert circle == good_circle

    def test_get_filled_fields(self):
        builder = core.ArrayBuilder()
        builder.new_array(3, 3)
        np.random.seed(7)
        builder.add_seed(3)
        assert set(builder.get_filled_fields()) == set((
            (1, 0),
            (2, 0),
            (1, 1)))

    def test_get_empty_fields(self):
        builder = core.ArrayBuilder()
        builder.new_array(3, 3)
        np.random.seed(7)
        builder.add_seed(3)
        assert set(builder.get_empty_fields()) == set((
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 2),
            (2, 1),
            (2, 2)))

    def test_remove_fields(self):
        builder = core.ArrayBuilder()
        builder.set_array(
            np.array([
                [5, 0, 0],
                [1, 0, 1],
                [3, 0, 0]
            ], dtype=np.uint32)
        )
        builder.remove_fields({1})
        array = builder.get_array()
        assert np.array_equal(
            np.array([
                [5, 0, 0],
                [0, 0, 0],
                [3, 0, 0]
            ], dtype=np.uint32),
            array
        )

    def test_get_seed_ids(self):
        builder = core.ArrayBuilder()
        builder.set_array(
            np.array([
                [5, 0, 0],
                [1, 0, 1],
                [3, 0, 3]
            ], dtype=np.uint32)
        )
        assert builder.get_seed_ids() == {1, 3, 5}


class TestGrainHistory:
    def test_log_grain(self):
        history = core.GrainHistory()
        history.log_grain(4)
        history.log_grain(1)
        history.log_grain(3)
        assert history._present_log_entry == {1, 3, 4}

    def test_log_grains(self):
        history = core.GrainHistory()
        history.log_grains([1,2,4])
        assert history.get_log() == [{1, 2, 4}]

    def test_new_grain(self):
        history = core.GrainHistory()
        history.new_phase()
        history.log_grain(5)
        history.log_grain(3)
        history.new_phase()
        history.log_grain(4)
        history.log_grain(1)
        history.new_phase()
        assert history._log == [(3, 5), (1, 4)]

    def test_get_history(self):
        history = core.GrainHistory()
        history.log_grain(5)
        history.log_grain(3)
        history.new_phase()
        history.log_grain(4)
        history.log_grain(1)
        assert history.get_log() == [(3, 5), {1, 4}]
        history.log_grain(2)
        assert history.get_log() == [(3, 5), {1, 2, 4}]

    def test_clear_history(self):
        history = core.GrainHistory()
        history.log_grains([5, 3])
        history.new_phase()
        history.log_grains([4, 2])
        history.clear()
        assert history.get_log() == []

    def test_remove_grains(self):
        history = core.GrainHistory()
        history.log_grains([1, 2, 3])
        history.new_phase()
        history.log_grains([4, 5, 6])
        history.remove_grains([1, 4])
        assert history.get_log() == [(2, 3), {5, 6}]

    def test_set_log(self):
        history = core.GrainHistory()
        history_log = [(1,2,3), {4, 5}]
        history.set_log(history_log)
        assert history._present_log_entry == {4, 5}
        assert history._log == [(1, 2, 3)]
        history.set_log([(1, 2, 3), (4, 5)])
        assert history._log == [(1, 2, 3), (4, 5)]

    def test_get_flattened_closed_phases(self):
        history = core.GrainHistory()
        history.set_log([(1, 2, 3), (4, 5, 6), {7, 8}])
        assert tuple(history.get_flattened_closed_phases()) == (1, 2, 3, 4, 5 ,6)

class TestSeedSelector:
    def test_toggle_grain(self):
        selector = core.SeedSelector()
        selector.toggle_seed(5)
        selector.toggle_seed(4)
        selector.toggle_seed(5)
        selector.toggle_seed(3)
        assert selector.get_selected() == {3, 4}
        assert selector.get_selected() == {3, 4}

    def test_get_selected(self):
        selector = core.SeedSelector()
        selector._selected = set([3, 5, 4])
        assert selector.get_selected() == {3, 4, 5}

    def test_clear(self):
        selector = core.SeedSelector()
        selector._selected = set([3, 4, 5])
        selector.clear()
        assert selector.get_selected() == set()
