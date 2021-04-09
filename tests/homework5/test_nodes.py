import unittest

from hw5.nodes import EmptyNode, NotEmptyNode


def generate_left_bamboo(start: int, end: int) -> NotEmptyNode[int, int]:
    if start == end:
        raise TypeError("Size of bamboo cannot be 0")
    root = NotEmptyNode(start, start)
    for i in range(start + 1, end):
        root = NotEmptyNode(i, i, root)
    return root


def generate_right_bamboo(start: int, end: int) -> NotEmptyNode[int, int]:
    if start == end:
        raise TypeError("Size of bamboo cannot be 0")
    root = NotEmptyNode(end - 1, -(end - 1))
    for i in range(end - 2, start - 1, -1):
        root = NotEmptyNode(i, -i, EmptyNode(), root)
    return root


def generate_two_sided_bamboo(start: int, middle: int, end: int):
    left = generate_left_bamboo(start, middle)
    right = generate_right_bamboo(middle + 1, end)
    return NotEmptyNode(middle, middle, left, right)


class EmptyNodeTestCase(unittest.TestCase):
    def test_splitting_empty_node_should_return_empty_nodes(self):
        node = EmptyNode()
        (left, right) = node.split(100)
        self.assertIsInstance(left, EmptyNode)
        self.assertIsInstance(right, EmptyNode)

    def test_merging_two_empty_nodes_should_be_an_empty_node(self):
        self.assertIsInstance(EmptyNode().merge(EmptyNode()), EmptyNode)

    def test_merging_empty_node_and_other_node_should_return_other_node(self):
        node = EmptyNode()
        other_node = NotEmptyNode(1, 100)
        self.assertEqual(node.merge(other_node), other_node)

    def test_pre_order_should_be_empty(self):
        self.assertEqual([], list(EmptyNode().ascending_order()))

    def test_post_order_should_be_empty(self):
        self.assertEqual([], list(EmptyNode().descending_order()))

    def test_remove_key_should_raise_exception(self):
        with self.assertRaises(KeyError):
            EmptyNode().remove_key(1)

    def test_insert_key_should_return_correct_subtree(self):
        expected = NotEmptyNode(1, "100")
        actual = EmptyNode().insert_key(1, "100")
        self.assertEqual(expected, actual)

    def test_empty_node_should_not_contain_any_value(self):
        self.assertNotIn(100, EmptyNode())

    def test_remove_key_should_raise(self):
        with self.assertRaises(KeyError):
            EmptyNode().remove_key(1)

    def test_should_become_simple_tree_when_inserted(self):
        self.assertEqual(NotEmptyNode(1, 1), EmptyNode().insert_key(1, 1))


class NotEmptyNodeTestCase(unittest.TestCase):
    def test_splitting_simple_tree_should_work_for_keys_smaller_than_root(self):
        tree = NotEmptyNode(50, "100")
        expected = (EmptyNode(), tree)
        self.assertEqual(expected, tree.split(1))

    def test_splitting_simple_tree_should_work_for_keys_equal_to_root(self):
        tree = NotEmptyNode(50, "100")
        expected = (EmptyNode(), tree)
        self.assertEqual(expected, tree.split(50))

    def test_splitting_simple_tree_should_work_for_keys_greater_than_root(self):
        tree = NotEmptyNode(50, "100")
        expected = (tree, EmptyNode())
        self.assertEqual(expected, tree.split(100))

    def test_splitting_3_node_tree_should_cut_the_leftmost_child(self):
        tree = NotEmptyNode(2, 1, NotEmptyNode(1, 0), NotEmptyNode(3, 0))
        expected = (NotEmptyNode(1, 0), NotEmptyNode(2, 1, EmptyNode(), NotEmptyNode(3, 0)))
        self.assertEqual(expected, tree.split(2))

    def test_splitting_should_correctly_split_bamboo_in_half(self):
        bamboo = generate_left_bamboo(0, 100)
        expected = (generate_left_bamboo(0, 50), generate_left_bamboo(50, 100))
        self.assertEqual(expected, bamboo.split(50))

    def test_splitting_should_correctly_split_bamboo_in_3_by_7_ratio(self):
        bamboo = generate_left_bamboo(0, 100)
        expected = (generate_left_bamboo(0, 30), generate_left_bamboo(30, 100))
        self.assertEqual(expected, bamboo.split(30))

    def test_merge_should_raise_if_2nd_node_contains_keys_that_are_smaller_than_some_keys_of_1st_node(self):
        first = NotEmptyNode(10, 0)
        second = NotEmptyNode(1, 0)
        with self.assertRaises(ValueError):
            first.merge(second)

    def test_merge_should_return_first_node_if_second_is_empty(self):
        first = NotEmptyNode(10, 0)
        second = EmptyNode()
        self.assertEqual(first, first.merge(second))

    def test_merge_should_correctly_merge_2_nodes(self):
        root = NotEmptyNode(100, 100)
        left = NotEmptyNode(0, 0)
        expected = NotEmptyNode(100, 100, left)
        self.assertEqual(expected, left.merge(root))

    def test_merge_should_create_bamboo(self):
        nodes = [NotEmptyNode(i, i) for i in range(100)]
        root = nodes[0]
        for node in nodes[1:]:
            root = root.merge(node)
        self.assertEqual(generate_left_bamboo(0, 100), root)

    def test_simple_tree_should_contain_its_value(self):
        tree = NotEmptyNode(100, 100)
        self.assertIn(100, tree)

    def test_simple_tree_should_not_contain_another_value(self):
        tree = NotEmptyNode(100, 100)
        self.assertNotIn(1, tree)

    def test_bamboo_should_contain_the_leftmost_value(self):
        bamboo = generate_left_bamboo(0, 100)
        self.assertTrue(0 in bamboo)

    def test_bamboo_should_not_contain_the_another_value(self):
        bamboo = generate_left_bamboo(0, 100)
        self.assertNotIn(-1, bamboo)

    def test_simple_tree_should_become_empty_if_root_is_removed(self):
        node = NotEmptyNode(1, 1)
        self.assertEqual(EmptyNode(), node.remove_key(1))

    def test_should_be_able_to_remove_end_of_short_bamboo(self):
        bamboo = NotEmptyNode(2, 2, NotEmptyNode(1, 1))
        self.assertEqual(NotEmptyNode(2, 2), bamboo.remove_key(1))

    def test_should_be_able_to_remove_root_of_short_bamboo(self):
        bamboo = NotEmptyNode(2, 2, NotEmptyNode(1, 1))
        self.assertEqual(NotEmptyNode(1, 1), bamboo.remove_key(2))

    def test_should_be_able_to_remove_end_of_bamboo(self):
        bamboo = generate_left_bamboo(1, 100)
        self.assertEqual(generate_left_bamboo(2, 100), bamboo.remove_key(1))

    def test_should_be_able_to_remove_root_of_bamboo(self):
        bamboo = generate_left_bamboo(1, 100)
        self.assertEqual(generate_left_bamboo(1, 99), bamboo.remove_key(99))

    def test_should_be_able_to_create_two_sided_bamboo(self):
        node = EmptyNode()
        for i in range(0, 11):
            node = node.insert_key(i, i)
        for i in range(11, 20):
            node = node.insert_key(i, -i)
        self.assertEqual(generate_two_sided_bamboo(0, 10, 20), node)

    def test_should_be_able_to_set_root_of_two_sided_bamboo(self):
        bamboo = generate_two_sided_bamboo(0, 100, 200)
        expected = NotEmptyNode(100, 999, bamboo.left, bamboo.right)
        self.assertEqual(expected, bamboo.insert_key(100, 999))

    def test_should_be_able_to_remove_root_of_two_sided_bamboo(self):
        bamboo = generate_two_sided_bamboo(0, 100, 200)
        expected = NotEmptyNode(99, 99, generate_left_bamboo(0, 99), generate_right_bamboo(101, 200))
        self.assertEqual(expected, bamboo.remove_key(100))

    def test_bamboo_len_should_be_correctly_calculated(self):
        self.assertEqual(100, len(generate_left_bamboo(0, 100)))

    def test_should_contain_key_in_the_middle_of_bamboo(self):
        self.assertIn(50, generate_left_bamboo(1, 100))

    def test_should_produce_sorted_list_in_ascending_order_from_bamboo(self):
        expected = list(zip(range(100), range(100)))
        actual = list(generate_left_bamboo(0, 100).ascending_order())
        self.assertEqual(expected, actual)

    def test_should_produce_sorted_list_in_descending_order_from_bamboo(self):
        expected = [(i, i) for i in reversed(range(100))]
        actual = list(generate_left_bamboo(0, 100).descending_order())
        self.assertEqual(expected, actual)

    def test_should_produce_sorted_list_in_ascending_order_from_two_sided_bamboo(self):
        bamboo = generate_two_sided_bamboo(0, 50, 100)
        expected = [(i, i) for i in range(51)] + [(i, -i) for i in range(51, 100)]
        self.assertEqual(expected, list(bamboo.ascending_order()))

    def test_should_extend_bamboo_by_inserting_key(self):
        bamboo = generate_right_bamboo(100, 200)
        expected = generate_right_bamboo(99, 200)
        self.assertEqual(expected, bamboo.insert_key(99, -99))


if __name__ == "__main__":
    unittest.main()
