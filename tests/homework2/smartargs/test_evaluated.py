import unittest

from hw2.smart_args.smart_args_decorator import MagicArgumentsMisuseError, smart_args
from hw2.smart_args.supported_magic_args import Evaluated, Isolated


class EvaluatedTest(unittest.TestCase):
    def test_evaluate_raises_if_passed_isolated_value(self):
        with self.assertRaises(TypeError):
            Evaluated(Isolated())

    def test_evaluate_raises_if_passed_isolated_type(self):
        with self.assertRaises(TypeError):
            Evaluated(Isolated)

    def test_evaluated_raises_if_passed_as_a_positional_argument(self):
        with self.assertRaises(MagicArgumentsMisuseError):

            @smart_args
            def f(x=Evaluated(lambda: 1)):
                pass


class EvaluatedInvocationsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.invocations = 0

        def invoke():
            self.invocations += 1

        self.invoke = invoke

        @smart_args
        def f(*, x=Evaluated(self.invoke)):
            return x

        self.f = f

    def test_evaluated_invokes_if_no_value_passed(self):
        self.f()
        self.assertEqual(1, self.invocations)

    def test_evaluated_invokes_each_time_if_no_value_passed(self):
        for _ in range(100):
            self.f()
        self.assertEqual(100, self.invocations)

    def test_evaluated_is_not_invoked_if_argument_is_passed(self):
        self.f(x=1)
        self.assertEqual(0, self.invocations)

    def test_evaluated_is_replaced_with_passed_argument(self):
        x = self.f(x=1)
        self.assertEqual(1, x)


if __name__ == "__main__":
    unittest.main()
