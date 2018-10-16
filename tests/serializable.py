import unittest
from serializable import Serializable


class SimpleSerializable(Serializable):

    def __init__(self, arg1, *args, kwarg1=None, **kwargs):
        self.arg1 = arg1
        self.args = args
        self.kwarg1 = kwarg1
        self.kwargs = kwargs
        self._Serializable__initialize(locals())


class UninitializedSerializable(Serializable):

    def __init__(self, arg1, *args, kwarg1=None, **kwargs):
        self.arg1 = arg1
        self.args = args
        self.kwarg1 = kwarg1
        self.kwargs = kwargs


def assert_objects_match(object1, object2):
    assert object1.arg1 == object2.arg1
    assert object1.args == object2.args
    assert object1.kwarg1 == object2.kwarg1
    assert object1.kwargs == object2.kwargs


class TestSerializable(unittest.TestCase):

    def test_args_functionality(self):
        simple_object_1 = SimpleSerializable('ARG1')
        simple_object_2 = Serializable.clone(simple_object_1)

        assert_objects_match(simple_object_1, simple_object_2)

    def test_kwargs_functionality(self):
        simple_object_1 = SimpleSerializable('ARG1', kwarg1='KWARG1')
        simple_object_2 = Serializable.clone(simple_object_1)

        assert_objects_match(simple_object_1, simple_object_2)

    def test_variable_args_functionality(self):
        simple_object_1 = SimpleSerializable('ARG1', *('ARGS[1]', 'ARGS[2]'))
        simple_object_2 = Serializable.clone(simple_object_1)

        assert_objects_match(simple_object_1, simple_object_2)

    def test_empty_variable_args_functionality(self):
        simple_object_1 = SimpleSerializable(
            'ARG1',
            kwarg1='KWARG1',
            **{'kwargs[1]': 'KWARGS[1]',
               'kwargs[2]': 'KWARGS[2]'})

        simple_object_2 = Serializable.clone(simple_object_1)

        assert_objects_match(simple_object_1, simple_object_2)

    def test_variable_kwargs_functionality(self):
        simple_object_1 = SimpleSerializable(
            'ARG1', **{'kwargs[1]': 'KWARGS[1]',
                       'kwargs[2]': 'KWARGS[2]'})

        simple_object_2 = Serializable.clone(simple_object_1)

        assert_objects_match(simple_object_1, simple_object_2)

    def test_empty_variable_kwargs_functionality(self):
        simple_object_1 = SimpleSerializable(
            'ARG1', *('ARGS[1]', 'ARGS[2]'), kwarg1='KWARG1')

        simple_object_2 = Serializable.clone(simple_object_1)

        assert_objects_match(simple_object_1, simple_object_2)

    def test_mixed_argument_types(self):
        simple_object_1 = SimpleSerializable(
            'ARG1',
            *('ARGS[1]', 'ARGS[2]'),
            kwarg1='KWARG1',
            **{'kwargs[1]': 'KWARGS[1]',
               'kwargs[2]': 'KWARGS[2]'})

        simple_object_2 = Serializable.clone(simple_object_1)

        assert_objects_match(simple_object_1, simple_object_2)

    def test_missing_default_values(self):
        simple_object_1 = SimpleSerializable(
            'ARG1', *('ARGS[1]', 'ARGS[2]'),
            **{'kwargs[1]': 'KWARGS[1]',
               'kwargs[2]': 'KWARGS[2]'})

        simple_object_2 = Serializable.clone(simple_object_1)

        assert_objects_match(simple_object_1, simple_object_2)

    def test_default_initialization(self):
        simple_object_1 = UninitializedSerializable(
            'ARG1',
            *('ARGS[1]', 'ARGS[2]'),
            kwarg1='KWARG1',
            **{'kwargs[1]': 'KWARGS[1]',
               'kwargs[2]': 'KWARGS[2]'})

        with self.assertRaises(AssertionError):
            Serializable.clone(simple_object_1)

    def test_clone_non_serializable(self):
        pass


if __name__ == '__main__':
    unittest.main()
