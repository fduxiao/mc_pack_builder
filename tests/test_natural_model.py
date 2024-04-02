import unittest
from mc_pack_builder import DictModel, Field


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

        b = B()
        c: A = b.a
        self.assertEqual(c.a, 2)
        self.assertEqual(b.dump(), {'aa': {}})
        c.b = 2
        self.assertEqual(b.dump(), {'aa': {'name': 2}})
        b.b = 1
        b.a = a
        self.assertEqual(b.dump(), {'aa': {'a': 1, 'c': 'new', 'name': 'abc'}, 'b': 1})


if __name__ == '__main__':
    unittest.main()
