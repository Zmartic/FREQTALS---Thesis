import unittest
from freqt.src.be.intimals.freqt.config.Config import *


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.prop = None

    def test1(self):
        self.prop = Config("../../../../../test/Config/config.properties")
        self.assertEqual(self.prop.get_max_leaf(), 4)
        self.assertEqual(self.prop.get_min_node(), 2)
        self.assertEqual(self.prop.get_min_leaf(), 2)
        self.assertEqual(self.prop.build_grammar(), True)
        self.assertEqual(self.prop.get_timeout(), 10)
        self.assertEqual(self.prop.getOutputFile(), "output-abstract-data-testing")
        self.assertEqual(self.prop.get_input_files(), "test/input-artificial-data")
        self.assertEqual(self.prop.get_two_step(), False)
        self.assertEqual(self.prop.get_filter(), True)
        self.assertEqual(self.prop.get_abstract_leafs(), False)
        self.assertEqual(self.prop.get_root_label_file(), "test/conf-artifical-data/abstract-data/listRootLabel.txt")
        self.assertEqual(self.prop.get_white_label_file(), "test/conf-artifical-data/abstract-data/listWhiteLabel.txt")
        self.assertEqual(self.prop.get_xml_character_file(), "test/conf-artifical-data/abstract-data/xmlCharacters.txt")

    def test2(self):
        self.prop = Config("../../../../../test/Config/config2.properties")
        self.assertEqual(self.prop.get_2class(), False)
        self.assertEqual(self.prop.get_input_files(), "test/class_data")
        self.assertEqual(self.prop.getOutputFile(), "test/class_data_output_1")
        self.assertEqual(self.prop.get_input_files1(), "version1")
        self.assertEqual(self.prop.get_input_files2(), "version2")
        self.assertEqual(self.prop.get_ds_score(), 0.1)
        self.assertEqual(self.prop.get_num_patterns(), 100)
        self.assertEqual(self.prop.get_timeout(), 5)
        self.assertEqual(self.prop.get_min_leaf(), 1)
        self.assertEqual(self.prop.get_min_node(), 10)
        self.assertEqual(self.prop.get_max_leaf(), 3)
        self.assertEqual(self.prop.get_two_step(), True)
        self.assertEqual(self.prop.get_weighted(), True)
        self.assertEqual(self.prop.build_grammar(), True)
        self.assertEqual(self.prop.get_root_label_file(), "test/class_data_conf/listRootLabel.txt")
        self.assertEqual(self.prop.get_white_label_file(), "test/class_data_conf/listWhiteLabel.txt")
        self.assertEqual(self.prop.get_xml_character_file(), "test/class_data_conf/xmlCharacters.txt")
        self.assertEqual(self.prop.get_min_support_list(), [4, 3, 2])
        self.assertEqual(self.prop.get_input_files_list(), ["sample_data1", "sample_data2"])


if __name__ == '__main__':
    unittest.main()
