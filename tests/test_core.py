import numpy as np
import cellular_automaton.core as core

class TestNeighborhood:
    def test_moore(self):
        moore = core.MooreNeighborhood()
        neighbors = set(moore.get_neighbors((1,1)))
        valid_neighbors = {(0,0), (0,1), (0,2), (1,0), (1,2), (2,0), (2,1), (2,2)}
        assert neighbors == valid_neighbors


class TestSolver:
    def test_next_step(self):
        neighborhood = core.MooreNeighborhood()
        state_solver = core.SimpleStateSolver()
        solver = core.Solver(neighborhood, state_solver)
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
