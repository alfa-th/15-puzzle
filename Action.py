class Action:
    label = ""

    def __init__(self, label = None):
        if label is not None:
            self.label = label

    def __eq__(self, other):
        return self.label == other.label

    def to_string(self):
        return str(self.label)

    def __repr__(self):
        return "Action <{}>".format(self.label)
