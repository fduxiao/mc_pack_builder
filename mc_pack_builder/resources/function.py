from ..resources import Resource


class Function(Resource):
    def __init__(self, body=None, resource_id="", namespace="microsoft"):
        super().__init__(resource_id, namespace)
        if body is None:
            body = []
        self._body = body
        self.name = resource_id.split('/')[-1]

    def gen_lines(self):
        yield f'# function {self.name}'
        for line in self._body:
            yield str(line)

    def body(self, body=None):
        if body is None:
            return self._body
        self._body = body
        return self
