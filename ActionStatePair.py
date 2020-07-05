class ActionStatePair:
    def __init__(self, action, state):
        self.action = action
        self.state = state

    def get_action(self):
        return self.action

    def get_state(self):
        return self.state

    def __repr__(self):
        return "<ActionStatePair <Action {}> <State {}>>".format(self.action, self.state)
