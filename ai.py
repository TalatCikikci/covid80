import utils


class AI(object):
    AND = 'and'
    OR = 'or'

    def __init__(self, obj):
        self.obj = obj

    def eval_condition(self, condition):
        actions = condition['actions']
        operator = condition.get('operator', AI.AND)

        action_checks = []
        for action in actions:
            checks = []
            for key, value in action.items():
                attr = utils.rgetattr(self.obj, key)
                checks.append(utils.eval_condition(value, attr))

            if operator == AI.OR:
                action_checks.append(any(checks))
            elif operator == AI.AND:
                action_checks.append(all(checks))
            else:
                raise Exception('no valid operator')

        return all(action_checks)

    def evaluate_action(self, action):
        return all(
            self.eval_condition(condition)
            for condition in action.ai_action
        )
