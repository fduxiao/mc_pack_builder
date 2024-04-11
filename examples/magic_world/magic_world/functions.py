from mc_pack_builder import *
from .pack import magic_ns, trigger_group
from . import books

functions = magic_ns.functions

f1 = functions.new('dir/f1').body([
    say('hello')
])


@functions.new()
def f2():
    yield tell(at_s(), "some thing")


@functions.new()
def test_menu():
    yield tell(at_s(), "Test the following functions")
    yield tellraw(at_s(), Text("[f1]: say hello").color("yellow").run_command(f1()))
    yield tellraw(at_s(), Text("[f2]: tell something").color("yellow").run_command(f2()))


@trigger_group.new()
def menu_func():
    yield tellraw(at_s(), "Welcome to my magic world\n\n"
                          "You have the following operations:\n"
                          "    " + Text("weapon book").run_command(books.give_weapon_book.trigger()) +
                          "    " + Text("magic book").run_command(books.give_magic_book.trigger()))
