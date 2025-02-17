import unittest

from anytree import AnyNode
from anytree.exporter import DictExporter
from license_sh.helpers import flatten_dependency_tree, annotate_dep_tree


def get_tree():
    """
  Please always re-generate this comment when changing the tree.
  You can use `print(RenderTree(tree))`

  :return:
  AnyNode(license='MIT', license_problem=False, name='Name', subtree_problem=True, version='')
  |-- AnyNode(license='MIT', license_problem=False, name='@company/package1', subtree_problem=True, version='1.1.1')
  |   |-- AnyNode(license='MIT', license_problem=False, name='package2', subtree_problem=False, version='2.2.2')
  |   |   |-- AnyNode(license='MIT', license_problem=False, name='package5', subtree_problem=False, version='5.5.5')
  |   |   +-- AnyNode(license='MIT', license_problem=False, name='package7', subtree_problem=False, version='7.7.7')
  |   |-- AnyNode(license='MIT', license_problem=False, name='package3', subtree_problem=True, version='3.3.3')
  |   |   +-- AnyNode(license='GPL', license_problem=True, name='package7', subtree_problem=False, version='7.7.6')
  |   |-- AnyNode(license='MIT', license_problem=False, name='package4', subtree_problem=False, version='4.4.4')
  |   +-- AnyNode(license='MIT', license_problem=False, name='package5', subtree_problem=True, version='5.5.5')
  |       +-- AnyNode(license='GPL', license_problem=True, name='package6', subtree_problem=False, version='6.6.6')
  +-- AnyNode(license='MIT', license_problem=False, name='package4', subtree_problem=True, version='4.4.4')
      +-- AnyNode(license='GPL', license_problem=True, name='package6', subtree_problem=False, version='6.6.6')

  print(RenderTree(tree, style=AsciiStyle()))
  """
    tree = AnyNode(name="Name", version="", license="MIT")
    # first level
    package1 = AnyNode(
        name="@company/package1", parent=tree, version="1.1.1", license="MIT"
    )
    package4 = AnyNode(name="package4", parent=tree, version="4.4.4", license="MIT")

    package2 = AnyNode(name="package2", parent=package1, version="2.2.2", license="MIT")
    AnyNode(name="package5", parent=package2, version="5.5.5", license="MIT")
    AnyNode(name="package7", parent=package2, version="7.7.7", license="MIT")

    package3 = AnyNode(name="package3", parent=package1, version="3.3.3", license="MIT")
    AnyNode(name="package7", parent=package3, version="7.7.6", license="GPL")

    AnyNode(name="package4", parent=package1, version="4.4.4", license="MIT")

    package5 = AnyNode(name="package5", parent=package1, version="5.5.5", license="MIT")
    AnyNode(name="package6", parent=package5, version="6.6.6", license="GPL")

    AnyNode(name="package6", parent=package4, version="6.6.6", license="GPL")
    return tree


class NpmRunnerTestCase(unittest.TestCase):
    maxDiff = None

    def test_dependency_tree_is_flattened(self):
        tree = get_tree()
        dependencies = flatten_dependency_tree(tree)
        self.assertSetEqual(
            dependencies,
            {
                ("@company/package1", "1.1.1"),
                ("package2", "2.2.2"),
                ("package3", "3.3.3"),
                ("package4", "4.4.4"),
                ("package5", "5.5.5"),
                ("package6", "6.6.6"),
                ("package7", "7.7.6"),
                ("package7", "7.7.7"),
            },
        )

    def test_bad_licenses_identified(self):
        tree = get_tree()

        whitelist = ["MIT", "Apache-2.0"]
        _, unknown_licenses = annotate_dep_tree(tree, whitelist)
        self.assertSetEqual(set({"GPL"}), unknown_licenses)

    def test_annotate_dependency_tree(self):
        tree = get_tree()

        whitelist = ["MIT", "Apache-2.0"]
        annotated_tree, _ = annotate_dep_tree(tree, whitelist)

        expected_tree = AnyNode(
            name="Name",
            version="",
            license="MIT",
            license_problem=False,
            subtree_problem=True,
            license_normalized="MIT",
        )
        # first level
        package1 = AnyNode(
            name="@company/package1",
            parent=expected_tree,
            version="1.1.1",
            license="MIT",
            license_problem=False,
            subtree_problem=True,
            license_normalized="MIT",
        )
        package4 = AnyNode(
            name="package4",
            parent=expected_tree,
            version="4.4.4",
            license="MIT",
            license_problem=False,
            subtree_problem=True,
            license_normalized="MIT",
        )

        package2 = AnyNode(
            name="package2",
            parent=package1,
            version="2.2.2",
            license="MIT",
            license_problem=False,
            subtree_problem=False,
            license_normalized="MIT",
        )
        AnyNode(
            name="package5",
            parent=package2,
            version="5.5.5",
            license="MIT",
            license_problem=False,
            subtree_problem=False,
            license_normalized="MIT",
        )
        AnyNode(
            name="package7",
            parent=package2,
            version="7.7.7",
            license="MIT",
            license_problem=False,
            subtree_problem=False,
            license_normalized="MIT",
        )

        package3 = AnyNode(
            name="package3",
            parent=package1,
            version="3.3.3",
            license="MIT",
            license_problem=False,
            subtree_problem=True,
            license_normalized="MIT",
        )
        AnyNode(
            name="package7",
            parent=package3,
            version="7.7.6",
            license="GPL",
            license_problem=True,
            subtree_problem=False,
            license_normalized="GPL",
        )

        AnyNode(
            name="package4",
            parent=package1,
            version="4.4.4",
            license="MIT",
            license_problem=False,
            subtree_problem=False,
            license_normalized="MIT",
        )

        package5 = AnyNode(
            name="package5",
            parent=package1,
            version="5.5.5",
            license="MIT",
            license_problem=False,
            subtree_problem=True,
            license_normalized="MIT",
        )
        AnyNode(
            name="package6",
            parent=package5,
            version="6.6.6",
            license="GPL",
            license_problem=True,
            subtree_problem=False,
            license_normalized="GPL",
        )

        AnyNode(
            name="package6",
            parent=package4,
            version="6.6.6",
            license="GPL",
            license_problem=True,
            subtree_problem=False,
            license_normalized="GPL",
        )

        exporter = DictExporter()
        self.assertDictEqual(
            exporter.export(expected_tree), exporter.export(annotated_tree)
        )


if __name__ == "__main__":
    unittest.main()
