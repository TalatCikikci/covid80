import utils


class AI(object):
    AND = 'and'
    OR = 'or'

    def __init__(self, obj):
        self.obj = obj

    def eval_condition(self, condition):
        checks = []
        actions = condition['actions']
        operator = condition['operator']

        for action in actions:
            for key, value in action.items():
                attr = utils.rgetattr(self.obj, key)
                checks.append(utils.eval_condition(value, attr))

        if operator == AI.OR:
            return any(checks)
        else:  # default and
            return all(checks)

    def evaluate_action(self, action):
        return all(
            self.eval_condition(condition)
            for condition in action.ai_action
        )
