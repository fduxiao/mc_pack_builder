import os
import tempfile
import unittest
from mc_pack_builder import Pack, DictFileSystem, DataPack, Path


class TestPack(unittest.TestCase):
    def test_dump(self):
        pack = Pack()
        pack.dir("aaa")
        pack.text("a.txt").set("some text")
        data = pack.dir("data")
        file = data.text("t/b.txt")
        file.append("some file")
        data.dir("dir")

        fs = DictFileSystem()
        pack.write_to(fs=fs)

        self.assertDictEqual(fs.dict, {
            'aaa': {},
            'a.txt': 'some text',
            'data': {
                't': {'b.txt': 'some file'},
                'dir': {}
            }
        })

        # I don't want to always test the following to save my ssd unless given a flag
        if os.getenv('TEST_FOR_OSFS', None) is None:
            return
        with tempfile.TemporaryDirectory() as tempdir:
            pack.write_to(tempdir)
            path = Path(tempdir)
            self.assertTrue((path / 'aaa').exists())
            with open(path / 'a.txt') as file:
                self.assertEqual(file.read(), 'some text')
            self.assertTrue((path / 'data').exists())
            self.assertTrue((path / 'data' / 'dir').exists())
            with open(path / 'data' / 't' / 'b.txt') as file:
                self.assertEqual(file.read(), 'some file')

    def test_data_pack(self):
        data_pack = DataPack("desc", 26)
        fs = DictFileSystem()
        data_pack.write_to(fs=fs)
        self.assertDictEqual(fs.dict, {
            'pack.mcmeta': '{"pack": {"description": "desc", "pack_format": 26}}',
            'data': {},
        })

    def test_functions(self):
        from mc_pack_builder import command as cmd

        data_pack = DataPack("desc", 26)
        ns = data_pack.namespace("some_pack")
        functions = ns.functions

        f1 = functions.new('dir/f1').body([
            cmd.say('hello')
        ])

        @functions.new()
        def f2():
            yield cmd.tell(cmd.at_s(), "some thing")

        dir2 = functions.dir("dir2")

        @dir2.new(path="f5").make
        def f3():
            """f3 doc"""
            return [
                cmd.say('f3')
            ]

        self.assertEqual(f1.resource_location(), 'some_pack:dir/f1')
        self.assertEqual(f2.resource_location(), 'some_pack:f2')
        self.assertEqual(f3.resource_location(), 'some_pack:dir2/f5')
        self.assertEqual(f3.__doc__, 'f3 doc')

        fs = DictFileSystem()
        data_pack.write_to(fs=fs)
        self.assertDictEqual(fs.dict, {
            'pack.mcmeta': '{"pack": {"description": "desc", "pack_format": 26}}',
            'data': {'some_pack': {
                'functions': {
                    'dir': {'f1.mcfunction': '# function f1\n'
                                             'say hello\n'},
                    'f2.mcfunction': '# function f2\n'
                                     'tell @s some thing\n',
                    'dir2': {'f5.mcfunction': '# function f5'
                                              '\nsay f3\n'}
                }
            }}
        })


if __name__ == '__main__':
    unittest.main()
