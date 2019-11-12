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


class TestSolver:
    def test_next_step(self):
        neighborhood = core.MooreNeighborhood()
        state_solver = core.SimpleStateSolver()
        boundary = core.PeriodicBoundary()
        solver = core.Solver(neighborhood, state_solver, boundary)
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
        solver = core.Solver(neighborhood, state_solver, boundary)
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
        assert (99, 49) == boundary.get_index((-1, -1), height, width)
        assert (0, 0) == boundary.get_index((100, 50), height, width)
        assert (5, 5) == boundary.get_index((5, 5), height, width)
