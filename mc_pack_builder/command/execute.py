class Execute:
    def __init__(self):
        self.modifications = list()
        self.condition_type = None
        self.condition_expr = None
        self.cmd_run = None

    def force_str(self):
        self.modifications = {k: str(v) for k, v in self.modifications}
        self.condition_type = str(self.condition_type)
        self.condition_expr = str(self.condition_expr)
        self.cmd_run = str(self.cmd_run)
        return self

    def modify(self, **kwargs):
        for k, v in kwargs.items():
            self.modifications.append((k, v))
        return self

    def as_(self, target):
        self.modifications.append(('as', target))
        return self

    def at(self, target):
        return self.modify(at=target)

    def align(self, align='xyz'):
        return self.modify(align=align)

    def condition(self, condition_type, condition):
        self.condition_type = condition_type
        self.condition_expr = condition
        return self

    def if_entity(self, condition):
        self.condition('if entity', condition)
        return self

    def run(self, cmd):
        self.cmd_run = cmd
        return self

    def __str__(self):
        modifications = " ".join(f'{k} {v}' for k, v in self.modifications)
        cmd = 'execute'
        if modifications != "":
            cmd += " " + modifications
        if self.condition_type:
            cmd += f" {self.condition_type} {self.condition_expr}"
        if self.cmd_run:
            cmd += f" run {self.cmd_run}"
        return cmd


execute = Execute
