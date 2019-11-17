import numpy as np
import cellular_automaton.core as core

class TestNeighborhood:
    def test_moore(self):
        moore = core.MooreNeighborhood()
        neighbors = set(moore.get_neighbors((1,1)))
        valid_neighbors = {(0,0), (0,1), (0,2), (1,0), (1,2), (2,0), (2,1), (2,2)}
        assert neighbors == valid_neighbors
        try:
            moore.get_neighbors((1,1,1))
        except TypeError:
            assert True
        else:
            assert False

    def test_neumann(self):
        neumann = core.NeumannNeighborhood()
        neighbors = set(neumann.get_neighbors((1,1)))
        valid_neighbors = {(0,1), (1,0), (1,2), (2,1)}
        assert neighbors == valid_neighbors
        try:
            neumann.get_neighbors((1,1,1))
        except TypeError:
            assert True
        else:
            assert False


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
        assert values == list(solver._get_neighbor_values(array, (0,0)))


class TestStateSolver:
    def test_next_elem(self):
        array = np.array([
            [0,0,0,0],
            [0,0,0,0],
            [0,0,1,0],
            [0,0,0,0]])
        neighborhood = core.MooreNeighborhood()
        neighbors_indices = neighborhood.get_neighbors((1,1))
        neighbors_1_1 = (array[index] for index in neighbors_indices)
        state_solver = core.SimpleStateSolver()
        new_state = state_solver.get_next_state(array[(1,1)], neighbors_1_1)
        assert new_state == 1


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
        array = next(arrays)
        assert np.array_equal(array, np.zeros((50, 100), np.int32))
        array = next(arrays)
        assert np.array_equal(array, np.zeros((50, 100), np.int32))

    def test_reset(self):
        controller = core.MainController()
        np.random.seed(7)
        controller.reset(3, 3, 3)
        arrays = controller.array_generator()
        array = next(arrays)
        good_array = np.array([
            [0, 0, -190761369],
            [0, 959775639, 0],
            [2053951699, 0, 0]])
        assert np.array_equal(array, good_array)
