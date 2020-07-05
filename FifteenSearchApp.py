from PuzzleState import PuzzleState
from IllegalMoveException import IllegalMoveException
from Node import Node
from copy import deepcopy
from random import random
from timeit import default_timer as timer

ps = PuzzleState()


# noinspection PyShadowingNames
class Solver:
    @staticmethod
    def greedy_search(input_state: [],
                      fringe_nodes: ['Node']) -> 'Node':
        input_state = deepcopy(input_state)
        visited_states_hashes = []
        fringe_nodes.append(Node(state=input_state))

        while fringe_nodes:
            # print("gh1.sebelum_expand: \t", len(fringe_nodes), fringe_nodes)

            fringe_nodes.sort(key=lambda node: node.heuristic_cost_state_wrongs, reverse=False)

            head_node = fringe_nodes.pop(0)
            head_node_state_hash = hash((tuple([tuple(row) for row in head_node.get_state()])))
            # print("bfs.fringe : \t", fringe_nodes)
            # print("bfs.fringe len : \t", len(fringe_nodes))
            # print("bfs.expanded_node : \t", head_node.get_state())

            # print(head_node)

            if head_node_state_hash in visited_states_hashes:
                # print("node skipped : ", end="")
                # print(hash(head_node), head_node.get_state())
                continue
            else:
                visited_states_hashes.append(head_node_state_hash)

            head_node_state = head_node.get_state()
            # print(head_node_state)
            if ps.goal_test(state=head_node_state):
                return head_node, len(fringe_nodes) + len(visited_states_hashes)

            descendant_nodes = head_node.expand()

            # print("gh1.sesudah_expand: \t", len(fringe_nodes), fringe_nodes)

            fringe_nodes.extend(descendant_nodes)

            # print("gh1.sesudah_sort: \t", len(fringe_nodes), fringe_nodes)

        return None

    @staticmethod
    def breadth_first_search(input_state: [],
                             fringe_nodes: ['Node']) -> 'Node':

        input_state = deepcopy(input_state)
        visited_states_hashes = []
        fringe_nodes.append(Node(state=input_state))

        while fringe_nodes:
            head_node = fringe_nodes.pop(0)
            head_node_state_hash = hash((tuple([tuple(row) for row in head_node.get_state()])))
            # print("bfs.fringe : \t", fringe_nodes)
            # print("bfs.fringe len : \t", len(fringe_nodes))
            # print("bfs.expanded_node : \t", head_node.get_state())

            if head_node_state_hash in visited_states_hashes:
                # print("node skipped : ", end="")
                # print(hash(head_node), head_node.get_state())
                continue
            else:
                visited_states_hashes.append(head_node_state_hash)

            head_node_state = head_node.get_state()
            # print(head_node_state)
            if ps.goal_test(state=head_node_state):
                return head_node, len(fringe_nodes)

            descendant_nodes = head_node.expand()

            fringe_nodes.extend(descendant_nodes)

            # print("bfs.expanded_result: \t", fringe_nodes)

        return None

    def solve_bfs(self, puzzle_state: []) -> ['Action']:
        search_result = self.breadth_first_search(input_state=puzzle_state, fringe_nodes=[])
        actions = search_result[0].get_actions()
        total_expanded_nodes_number = search_result[1]
        depth = search_result[0].get_depth()

        return {"actions": actions, "nodes_number": total_expanded_nodes_number, "depth": depth}

    def solve_gh1(self, puzzle_state: []) -> ['Action']:
        search_result = self.greedy_search(input_state=puzzle_state, fringe_nodes=[])
        actions = search_result[0].get_actions()
        total_expanded_nodes_number = search_result[1]
        depth = search_result[0].get_depth()

        return {"actions": actions, "nodes_number": total_expanded_nodes_number, "depth": depth}

    @staticmethod
    def random_puzzle(max_shuffle: int) -> []:
        total_shuffle = 0
        randomized_state = [[1, 2, 3, 4],
                            [5, 6, 7, 8],
                            [9, 10, 11, 12],
                            [13, 14, 15, 0]]

        while total_shuffle < max_shuffle:
            r = random()
            try:
                if r < 0.25:
                    randomized_state = ps.perform_action(state=randomized_state, action=PuzzleState.act_move_left)
                elif r < 0.5:
                    randomized_state = ps.perform_action(state=randomized_state, action=PuzzleState.act_move_right)
                elif r < 0.75:
                    randomized_state = ps.perform_action(state=randomized_state, action=PuzzleState.act_move_up)
                else:
                    randomized_state = ps.perform_action(state=randomized_state, action=PuzzleState.act_move_down)
                total_shuffle += 1
            except IllegalMoveException:
                continue

        return randomized_state

    @staticmethod
    def effective_branching_factor(nodes_number, depth):
        max_error = 0.01
        delta = 0.01
        optimum_b = 0
        error_sign = 0
        while True:
            total = 1
            for i in range(1, depth + 1):
                total += optimum_b ** i
            error = total - (1 + nodes_number)
            prev_error_sign = error_sign
            if error < 0.0:
                error_sign = -1
            else:
                error_sign = +1
            if abs(error) > max_error:
                if prev_error_sign == error_sign or prev_error_sign == 0:
                    optimum_b += delta
                else:
                    optimum_b -= delta
                    delta /= 2
                    error_sign = prev_error_sign
            else:
                return optimum_b


if __name__ == "__main__":
    solver = Solver()
    initial_state = solver.random_puzzle(15)
    # initial_state = [[9, 1, 3, 6],
    #                  [10, 5, 8, 2],
    #                  [14, 7, 4, 0],
    #                  [13, 11, 15, 12]]

    # # Breadth First Search
    # time_start = timer()
    # initial_state_bfs = deepcopy(initial_state)
    # solve_result = solver.solve_bfs(deepcopy(initial_state_bfs))
    # bfs_actions = solve_result["actions"]
    # bfs_nodes_number = solve_result["nodes_number"]
    # bfs_depth = solve_result["depth"]
    # print("Initial State")
    # print(ps.to_string(initial_state_bfs))
    #
    # print("Solution Breadth First Search")
    # for i in range(0, len(bfs_actions)):
    #     print(i + 1, bfs_actions[len(bfs_actions) - 1 - i])
    #     state = ps.perform_action(initial_state_bfs, bfs_actions[len(bfs_actions) - 1 - i])
    #     print(ps.to_string(state))
    #
    # time_end = timer()
    #
    # print("Execution Time : ", time_end - time_start)
    # print("Effective Branching Factor :", solver.effective_branching_factor(bfs_nodes_number, bfs_depth))
    # print("Nodes Generated : ", bfs_nodes_number)
    # print("Solution Depth : ", bfs_depth, end="\n\n")

    # Greedy Search
    time_start = timer()
    initial_state_gh1 = deepcopy(initial_state)
    solve_result = solver.solve_gh1(deepcopy(initial_state_gh1))
    gh1_actions = solve_result["actions"]
    gh1_nodes_number = solve_result["nodes_number"]
    gh1_depth = solve_result["depth"]
    print("Initial State")
    print(ps.to_string(initial_state_gh1))

    print("Solution Greedy Search Heuristic 1")
    for i in range(0, len(gh1_actions)):
        print(i + 1, gh1_actions[len(gh1_actions) - 1 - i])
        state = ps.perform_action(initial_state_gh1, gh1_actions[len(gh1_actions) - 1 - i])
        print(ps.to_string(state))

    time_end = timer()

    print("Execution Time : ", time_end - time_start)
    print("Effective Branching Factor :", solver.effective_branching_factor(gh1_nodes_number, gh1_depth))
    print("Nodes Generated : ", gh1_nodes_number)
    print("Solution Depth : ", gh1_depth)
