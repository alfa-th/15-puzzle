from State import State
from Action import Action
from ActionStatePair import ActionStatePair
from IllegalMoveException import IllegalMoveException
from copy import deepcopy
from math import sqrt


class PuzzleState(State):
    actions = []

    act_move_left = Action("left")
    actions.append(act_move_left)
    act_move_right = Action("right")
    actions.append(act_move_right)
    act_move_up = Action("up")
    actions.append(act_move_up)
    act_move_down = Action("down")
    actions.append(act_move_down)

    def __init__(self,
                 goal: [] = None):

        if goal is None:
            self.goal = [[1, 2, 3, 4],
                         [5, 6, 7, 8],
                         [9, 10, 11, 12],
                         [13, 14, 15, 0]]

    def __repr__(self):
        return "<PuzzleState {}>>".format(self.action_sequences)

    def perform_action(self,
                       state: [],
                       action: 'Action'):

        blank_loc = ()
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == 0:
                    blank_loc = (i, j)
                    break

        if action == self.act_move_up and blank_loc[0] is not 0:
            state[blank_loc[0]][blank_loc[1]] = state[blank_loc[0] - 1][blank_loc[1]]
            state[blank_loc[0] - 1][blank_loc[1]] = 0
        elif action == self.act_move_down and blank_loc[0] is not 3:
            state[blank_loc[0]][blank_loc[1]] = state[blank_loc[0] + 1][blank_loc[1]]
            state[blank_loc[0] + 1][blank_loc[1]] = 0
        elif action == self.act_move_left and blank_loc[1] is not 0:
            state[blank_loc[0]][blank_loc[1]] = state[blank_loc[0]][blank_loc[1] - 1]
            state[blank_loc[0]][blank_loc[1] - 1] = 0
        elif action == self.act_move_right and blank_loc[1] is not 3:
            state[blank_loc[0]][blank_loc[1]] = state[blank_loc[0]][blank_loc[1] + 1]
            state[blank_loc[0]][blank_loc[1] + 1] = 0
        else:
            raise IllegalMoveException

        return state

    def goal_test(self, state) -> bool:
        return state == self.goal

    def successor(self,
                  state: []) -> '[ActionStatePair]':

        possible_actions = deepcopy(self.actions)
        possible_action_state_pair = []

        blank_loc = ()
        for i in range(len(state)):
            for j in range(len(state)):
                if state[i][j] == 0:
                    blank_loc = (i, j)
                    break

        if blank_loc[1] == 0:
            possible_actions.remove(Action("left"))
        if blank_loc[1] == 3:
            possible_actions.remove(Action("right"))
        if blank_loc[0] == 0:
            possible_actions.remove(Action("up"))
        if blank_loc[0] == 3:
            possible_actions.remove(Action("down"))

        for action in possible_actions:
            current_state = deepcopy(state)
            possible_action_state_pair.append(
                ActionStatePair(action=action,
                                state=self.perform_action(current_state, action)))

        return possible_action_state_pair

    @staticmethod
    def get_state_wrongs(state):
        wrongs_sum = 0
        for i in range(len(state)):
            for j in range(len(state)):
                if state[i][j] != i * 4 + j + 1:
                    wrongs_sum += 1

        return wrongs_sum

    @staticmethod
    def manhattan_function(loc1: tuple(), loc2: tuple()):
        return abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1])

    @staticmethod
    def euclidean_function(loc1: tuple(), loc2: tuple()):
        return sqrt((loc1[0] - loc2[0]) ** 2 + (loc1[1] - loc2[1]) ** 2)

    def total_manhattan_distance(self, state):
        total = 0
        for i in range(len(state)):
            for j in range(len(state)):
                best_pos = self.get_good_pos(state[i][j])
                total += self.manhattan_function((i, j), best_pos)

        return total

    def total_euclidean_distance(self, state):
        total = 0
        for i in range(len(state)):
            for j in range(len(state)):
                best_pos = self.get_good_pos(state[i][j])
                total += self.euclidean_function((i, j), best_pos)

        return total

    @staticmethod
    def get_good_pos(number):
        post_dict = {
            1: (0, 0),
            2: (0, 1),
            3: (0, 2),
            4: (0, 3),
            5: (1, 0),
            6: (1, 1),
            7: (1, 2),
            8: (1, 3),
            9: (2, 0),
            10: (2, 1),
            11: (2, 2),
            12: (2, 3),
            13: (3, 0),
            14: (3, 1),
            15: (3, 2),
            0: (3, 3)
        }

        return post_dict[number]

    # @staticmethod
    # def custom_heuristic(state):

    @staticmethod
    def path_cost(action):
        return 1

    @staticmethod
    def distance(loc_one: [int, int],
                 loc_two: [int, int]) -> float:

        distance = 0
        for i in range(0, len(loc_one)):
            for j in range(0, len(loc_two)):
                if loc_one[i][j] is not loc_two[i][j]:
                    distance += 1

        return distance

    def __eq__(self,
               other: any) -> bool:

        if type(other) is type(self):
            for i in range(len(self.tiles)):
                for j in range(len(self.tiles[i])):
                    if other[i][j] is not self.tiles[i][j]:
                        return False
            return True
        return False

    @staticmethod
    def to_string(state) -> str:
        s = [[str(i) for i in row] for row in state]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '\t'.join("{{:{}}}".format(x) for x in lens)
        table = [fmt.format(*row) for row in s]

        return "\n".join(table)


if __name__ == "__main__":
    test = PuzzleState()
