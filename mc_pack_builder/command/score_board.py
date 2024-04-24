from functools import wraps
from .basic import Command, trigger, brace
from .target_selector import at_s
from .execute import execute


class ScoreBoard:
    """
    Represent the scoreboard command with an OOP style
    """
    def __init__(self, objective, criteria="dummy", display_name=None):
        self.objective = objective
        self.criteria = criteria
        self.display_name = display_name
        self.cmd = Command('scoreboard')
        self.cmd_obj = self.cmd('objectives')
        self.cmd_player = self.cmd('players')

    def add_objective(self):
        cmd = self.cmd_obj('add', self.objective, self.criteria)
        if self.display_name:
            cmd = cmd(self.display_name)
        return cmd

    # player functions
    def enable(self, target):
        return self.cmd_player('enable', target, self.objective)

    def set_player(self, target, score):
        return self.cmd_player('set', target, self.objective, score)

    def add_player(self, target, value=0):
        return self.cmd_player('add', target, self.objective, value)

    def get_player(self, target):
        return self.cmd_player('get', target, self.objective)

    def trigger(self, add_value=None, set_value=None):
        cmd = trigger(self.objective)
        if add_value:
            cmd = cmd('add', add_value)
        if set_value:
            cmd = cmd('set', set_value)
        return cmd

    def __lt__(self, other):
        return Command(self.objective, '=', '..', other - 1, sep='')

    def level_guard_cmds(self, min_score):
        yield execute().if_entity(at_s(type='player')).force_str().run(self.add_player(at_s(), 0))
        yield execute().if_entity(
            at_s(type='player', scores=brace(self < min_score))
        ).run('return fail')

    def level_guard(self, min_score):
        """used as a decorator"""
        def wrapper(func):
            @wraps(func)
            def wrapped():
                yield from self.level_guard_cmds(min_score)
                yield from func()
            return wrapped
        return wrapper


def scoreboard(objective):
    return ScoreBoard(objective)
