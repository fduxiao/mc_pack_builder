from mc_pack_builder import *
from .pack import magic_ns
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


menu_trigger = functions.trigger_group('menu')


@menu_trigger.new()
def menu_func():
    yield tellraw(at_s(), "Welcome to my magic world\n\n"
                          "You have the following operations:\n"
                          "    " + Text("weapon book").color('green').run_command(books.give_weapon_book.trigger()) +
                          "    " + Text("magic book").color('green').run_command(books.give_magic_book.trigger()))
