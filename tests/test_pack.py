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

        self.assertDictEqual(fs.dict, {'aaa': {}, 'a.txt': 'some text', 'data': {'t': {'b.txt': 'some file'}, 'dir': {}}})

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


if __name__ == '__main__':
    unittest.main()
