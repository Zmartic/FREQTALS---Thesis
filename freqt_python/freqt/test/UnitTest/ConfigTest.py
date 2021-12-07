import unittest
from freqt.src.be.intimals.freqt.config.Config import *


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.prop = Config()

    def test1(self):
        self.prop.config("../../../../../test/Config/config.properties")
        self.assertEqual(self.prop.getMaxLeaf(), 4)
        self.assertEqual(self.prop.getMinNode(), 2)
        self.assertEqual(self.prop.getMinLeaf(), 2)
        self.assertEqual(self.prop.buildGrammar(), True)
        self.assertEqual(self.prop.getTimeout(), 10)
        self.assertEqual(self.prop.getOutputFile(), "output-abstract-data-testing")
        self.assertEqual(self.prop.getInputFiles(), "test/input-artificial-data")
        self.assertEqual(self.prop.getTwoStep(), False)
        self.assertEqual(self.prop.getFilter(), True)
        self.assertEqual(self.prop.getAbstractLeafs(), False)
        self.assertEqual(self.prop.getRootLabelFile(), "test/conf-artifical-data/abstract-data/listRootLabel.txt")
        self.assertEqual(self.prop.getWhiteLabelFile(), "test/conf-artifical-data/abstract-data/listWhiteLabel.txt")
        self.assertEqual(self.prop.getXmlCharacterFile(), "test/conf-artifical-data/abstract-data/xmlCharacters.txt")

    def test2(self):
        self.prop.config("../../../../../test/Config/config2.properties")
        self.assertEqual(self.prop.get2Class(), False)
        self.assertEqual(self.prop.getInputFiles(), "test/class_data")
        self.assertEqual(self.prop.getOutputFile(), "test/class_data_output_1")
        self.assertEqual(self.prop.getInputFiles1(), "version1")
        self.assertEqual(self.prop.getInputFiles2(), "version2")
        self.assertEqual(self.prop.getDSScore(), 0.1)
        self.assertEqual(self.prop.getNumPatterns(), 100)
        self.assertEqual(self.prop.getTimeout(), 5)
        self.assertEqual(self.prop.getMinLeaf(), 1)
        self.assertEqual(self.prop.getMinNode(), 10)
        self.assertEqual(self.prop.getMaxLeaf(), 3)
        self.assertEqual(self.prop.getTwoStep(), True)
        self.assertEqual(self.prop.getWeighted(), True)
        self.assertEqual(self.prop.buildGrammar(), True)
        self.assertEqual(self.prop.getRootLabelFile(), "test/class_data_conf/listRootLabel.txt")
        self.assertEqual(self.prop.getWhiteLabelFile(), "test/class_data_conf/listWhiteLabel.txt")
        self.assertEqual(self.prop.getXmlCharacterFile(), "test/class_data_conf/xmlCharacters.txt")
        self.assertEqual(self.prop.getMinSupportList(), [4, 3, 2])
        self.assertEqual(self.prop.getInputFilesList(), ["sample_data1", "sample_data2"])


if __name__ == '__main__':
    unittest.main()
