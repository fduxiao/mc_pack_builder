from functools import update_wrapper
from ..resources import Resource
from ..natural_model import NaturalModel


class Function(Resource):
    def __init__(self, body=None, resource_id="", namespace="microsoft"):
        super().__init__(resource_id, namespace)
        if body is None:
            body = []
        self.before_body = []
        self._body = body
        self.after_body = []
        self.name = resource_id.split('/')[-1]
        self._trigger = None

    def trigger(self, objective=None, value=None):
        """
        When the function is used by a non-privileged player by command trigger, this method
        specifies/returns what to use

        :param objective:
        :param value:
        :return:
        """
        if objective is None:
            objective, value = self._trigger
            return f'trigger {objective} set {value}'
        self._trigger = objective, value

    def force_str(self):
        self._body = map(str, self._body)
        return self

    def gen_raw(self):
        yield f'# function {self.name}'
        yield from self.before_body
        yield from self._body
        yield from self.after_body

    def force_list(self):
        self._body = list(self.gen_raw())
        return self

    def gen_lines(self):
        return map(str, self.gen_raw())

    def body(self, body=None):
        if body is None:
            return self._body
        if not hasattr(body, '__iter__'):
            body = [body]
        self._body = body
        return self

    def make(self, func):
        """used as a decorator"""
        update_wrapper(self, func)
        self.extend(*func())
        return self

    def extend(self, *cmds):
        if isinstance(self._body, list):
            self._body.extend(cmds)
        else:
            self._body = (*self._body, *cmds)
        return self

    def __call__(self, arg=None):
        """This should give a /function call in minecraft"""
        func_call = f"function {self.resource_location()}"
        if isinstance(arg, NaturalModel):
            arg = arg.to_nbt()
        if arg is not None:
            func_call = f'{func_call} {arg}'
        return func_call
