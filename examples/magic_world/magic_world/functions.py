from mc_pack_builder import command as cmd
from .pack import magic

functions = magic.functions

f1 = functions.new('dir/f1').body([
    cmd.say('hello')
])


@functions.make()
def f2():
    yield cmd.tell(cmd.at_s(), "some thing")
