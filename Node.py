from Action import Action
from State import State
from PuzzleState import PuzzleState
from copy import deepcopy
ps = PuzzleState()


class Node:
    def __init__(self,
                 state: [],
                 parent_node: 'Node' = None,
                 action: Action = None,
                 path_cost: int = 0,
                 heuristic_cost: int = 0):

        self.state = state
        self.parent_node = parent_node
        self.action = action
        self.path_cost = path_cost

        if parent_node:
            self.depth = parent_node.get_depth() + 1
        else:
            self.depth = 0

        self.heuristic_cost_state_wrongs = ps.get_state_wrongs(self.get_state())
        self.heuristic_cost_manhattan = ps.total_manhattan_distance(self.get_state())
        self.heuristic_cost_euclidean = ps.total_euclidean_distance(self.get_state())
        self.heuristic_cost_custom = self.heuristic_cost_euclidean + self.heuristic_cost_manhattan

    def expand(self) -> ['Node']:
        successor_states = ps.successor(deepcopy(self.state))
        descendant_nodes = []

        for i in range(len(successor_states)):
            new_descendant_action = successor_states[i].get_action()
            new_descendant_state = successor_states[i].get_state()
            new_descendant_node = Node(new_descendant_state,
                                       self,
                                       new_descendant_action,
                                       self.get_cost() + ps.path_cost(new_descendant_action))

            descendant_nodes.append(new_descendant_node)

        return descendant_nodes

    def get_actions(self) -> ['Action']:
        actions = []

        node = self

        for i in range(self.depth):
            actions.append(node.get_action())
            node = node.get_parent()

        return actions

    def __repr__(self):
        return "<Node {}, Hash {}, Cost {}, Depth {}>".format(self.state, self.__hash__(), self.heuristic_cost_custom, self.depth)

    def __hash__(self):
        return hash((tuple([tuple(row) for row in self.state])))

    def get_action(self) -> 'Action':
        return self.action

    def get_cost(self) -> float:
        return self.path_cost

    def get_depth(self) -> int:
        return self.depth

    def get_parent(self) -> 'Node':
        return self.parent_node

    def get_state(self) -> 'State':
        return self.state
