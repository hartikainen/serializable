import unittest
from serializable import Serializable


class SimpleSerializable(Serializable):
    def __init__(self,
                 arg1,
                 *args,
                 kwarg1=None,
                 **kwargs):
        self.arg1 = arg1
        self.args = args
        self.kwarg1 = kwarg1
        self.kwargs = kwargs
        self._Serializable__initialize(locals())


class TestSerializable(unittest.TestCase):
    def test_args_functionality(self):
        pass

    def test_kwargs_functionality(self):
        pass

    def test_variable_args_functionality(self):
        pass

    def test_variable_kwargs_functionality(self):
        pass

    def test_mixed_argument_types(self):
        simple_object_1 = SimpleSerializable(
            'ARG1',
            *('ARGS[1]', 'ARGS[2]'),
            kwarg1='KWARG1',
            **{'kwargs[1]': 'KWARGS[1]', 'kwargs[2]': 'KWARGS[2]'}
        )

        simple_object_2 = Serializable.clone(simple_object_1)

        from pdb import set_trace; from pprint import pprint; set_trace()

        assert simple_object_1.arg1 == simple_object_2.arg1
        assert simple_object_1.args == simple_object_2.args
        assert simple_object_1.kwarg1 == simple_object_2.kwarg1
        assert simple_object_1.kwargs == simple_object_2.kwargs


if __name__ == '__main__':
    unittest.main()
