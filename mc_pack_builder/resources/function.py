from functools import update_wrapper
from ..resources import Resource
from ..natural_model import NaturalModel


class Function(Resource):
    def __init__(self, body=None, resource_id="", namespace="microsoft"):
        super().__init__(resource_id, namespace)
        if body is None:
            body = []
        self._body = body
        self.name = resource_id.split('/')[-1]

    def force_str(self):
        self._body = map(str, self._body)
        return self

    def gen_lines(self):
        yield f'# function {self.name}'
        for line in self._body:
            yield str(line)

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
