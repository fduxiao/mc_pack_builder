import unittest
from mc_pack_builder import DictModel, Field, nbt


class TestNaturalModel(unittest.TestCase):
    def test_field_and_model(self):
        class A(DictModel):
            a = Field(default=2)
            b = Field(name='name')

        a = A()
        self.assertEqual(a.a, 2)
        a.a = 1
        a.b = "abc"
        a['c'] = 'new'
        self.assertDictEqual(a.dump(), {'a': 1, 'c': 'new', 'name': 'abc'})

        class B(DictModel):
            a = A(name="aa")
            b = Field()
            c = Field(name="aa/a")

        b = B()
        c: A = b.a
        self.assertEqual(c.a, 2)
        self.assertEqual(b.dump(), {'aa': {'a': 2}})
        b.c = 3
        c.b = 2
        self.assertEqual(b.dump(), {'aa': {'a': 3, 'name': 2}})
        b.b = 1
        b.a = a
        self.assertEqual(b.dump(), {'aa': {'a': 1, 'c': 'new', 'name': 'abc'}, 'b': 1})
        self.assertEqual(b.c, 1)

    def test_to_nbt(self):
        class A(DictModel):
            a = Field(default=2)
            b = Field(name='name')

        a = A()
        a.a = nbt.String("aaa")
        a.b = nbt.Byte(3)
        self.assertEqual(a.to_nbt(), '{a: "aaa", name: 3b}')


if __name__ == '__main__':
    unittest.main()
