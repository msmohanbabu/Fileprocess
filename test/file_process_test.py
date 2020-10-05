import unittest
from test.utils import create_temporary_file
import logging
import sys
import inspect
import itertools
import tempfile
import os
import json

sys.path.append('../file_process')
from file_process.fixed_parser import FixedFileWriter, FixedWidthMetaData, FixedFileReader, JsonMatchException

JSON_PASS = ''' {
    "ColumnNames": [
        "f1",
        "f2",
        "f3"
         ],
    "Offsets": [
        "2",
        "3",
        "4"
         ],
    "FixedWidthEncoding": "windows-1252",
    "IncludeHeader": "True",
    "DelimitedEncoding": "utf-8"
}'''

JSON_FAIL = ''' {
    "ColumnNames": [
        "f1",
        "f2"
        ],
    "Offsets": [
        "2",
        "3",
        "4"
         ],
    "FixedWidthEncoding": "windows-1252",
    "IncludeHeader": "True",
    "DelimitedEncoding": "utf-8"
}'''

logging.basicConfig(stream=sys.stdout)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class FixedWidthMetaDataTest(unittest.TestCase):
    """ This class to test the Fixed File Specification """

    @classmethod
    def setUpClass( FixedWidthMetaDataTest ):
        pass

    def setUp(self):
        self.column_names = ["f1", "f2", "f3"]
        self.offset = ["2", "3", "4"]
        self.temp_file_pass = open(create_temporary_file('.json', JSON_PASS), 'r')
        self.temp_file_fail = open(create_temporary_file('.json', JSON_FAIL), 'r')
        self.output_file_name = "fixed_out_file"
        self.spec_pass = FixedWidthMetaData(json.load(self.temp_file_pass))
        self.char_set = "AB"
        self.random_list = ["AA", "AB", "BA", "BB"]
        self.record_length = sum(self.spec_pass.columnOffsets.values())
        self.fixed_test_file = tempfile.NamedTemporaryFile("w", delete=False)
        self.fixed_test_file.write("f1f2 f3  \n")
        self.fixed_test_file.write("AABBBCCCC\n")
        self.fixed_test_file.close()

    def tearDown(self):
        self.temp_file_pass.close()
        self.temp_file_fail.close()
        self.fixed_test_file.close()
        os.remove(os.path.join(self.temp_file_pass.name))
        os.remove(os.path.join(self.temp_file_fail.name))
        os.remove(os.path.join(self.fixed_test_file.name))
        pass

    def shortDescription(self):
        doc = self._testMethodDoc
        return doc

    def test_JsonSpecification(self):
        """Validate JSON for the parsed column names"""
        logger.warning(self.shortDescription())
        self.assertEqual(self.column_names, self.spec_pass.columns)
        self.assertTrue(self.spec_pass.include_header)
        self.assertEqual(self.offset, self.spec_pass.offsets)
        self.assertEqual(self.spec_pass.fixedWidthEncoding, "windows-1252")
        self.assertEqual(self.spec_pass.delimitedEncoding, "utf-8")

    def test_Exception(self):
        """Throws JsonMatchException"""
        logger.warning(self.shortDescription())

        with self.assertRaises(JsonMatchException):
            FixedWidthMetaData(json.load(self.temp_file_fail))

    def test_GenerateRecord(self):
        """Generate fixed length records based on JSON spec"""
        logger.warning(self.shortDescription())
        with FixedFileWriter(self.output_file_name, self.spec_pass) as f_write:
            record = ''.join(str(x) for x in f_write.generate_fixed_records(self.char_set))
        self.assertEqual(self.record_length, len(record))


class FixedFileWriterTest(unittest.TestCase):
    """ This class to test the Fixed File Writer """

    @classmethod
    def setUpClass(FixedFileWriterTest):
        pass

    def setUp(self):
        self.spec_file = open(create_temporary_file('.json', JSON_PASS), 'r')
        self.test_spec = FixedWidthMetaData(json.load(self.spec_file))
        self.test_record_fields = []
        self.test_record = ""
        self.fixed_file = tempfile.NamedTemporaryFile("w", delete=False)
        self.fixed_file.close()
        self.char_set = "AB"
        self.record_length = sum(self.test_spec.columnOffsets.values())

    def tearDown(self):
        self.spec_file.close()
        self.fixed_file.close()
        os.remove(os.path.join(self.fixed_file.name))
        os.remove(os.path.join(self.spec_file.name))

    def shortDescription(self):
        doc = self._testMethodDoc
        return doc

    def test_GenerateRecord(self):
        """Generate fixed length records based on JSON spec"""
        logger.warning(self.shortDescription())
        with FixedFileWriter(self.fixed_file.name, self.test_spec) as fixed_writer:
            self.test_record_fields = fixed_writer.generate_fixed_records(self.char_set)
            self.test_record = ''.join(str(x) for x in fixed_writer.generate_fixed_records(self.char_set))

        f1_element = next(self.test_record_fields)
        self.assertEqual(self.test_spec.columnOffsets["f1"], len(f1_element))
        f2_element = next(self.test_record_fields)
        self.assertEqual(self.test_spec.columnOffsets["f2"], len(f2_element))
        f3_element = next(self.test_record_fields)
        self.assertEqual(self.test_spec.columnOffsets["f3"], len(f3_element))
        self.assertEqual(self.record_length, len(self.test_record))

    def test_WriteFixedRecord(self):
        """ Write the generated record in to the fixed out file"""
        logger.warning(self.shortDescription())
        test_generated_fields = ["AA", "BBB", "CCCC"]
        with FixedFileWriter(self.fixed_file.name, self.test_spec) as fixed_writer:
            first_record = ''.join(str(x) for x in test_generated_fields)
            fixed_writer.write_record(first_record)

        self.fixed_file = open(self.fixed_file.name, "r")
        parse_out_file = iter(self.fixed_file)
        header = next(parse_out_file)
        first_line = next(parse_out_file)
        self.assertEqual("f1f2 f3  \n", header)
        self.assertEqual(''.join(test_generated_fields) + "\n", first_line)


class FixedFileReaderTest(unittest.TestCase):
    """ This class to test the Fixed File Reader """

    @classmethod
    def setUpClass(FixedFileReaderTest):
        pass

    def setUp(self):
        self.spec_file = open(create_temporary_file('.json', JSON_PASS), 'r')
        self.test_spec = FixedWidthMetaData(json.load(self.spec_file))
        self.test_read_file = tempfile.NamedTemporaryFile("w", delete=False)
        self.test_read_file.write("f1f2 f3  \n")
        self.test_read_file.write("AABBBCCCC\n")
        self.test_read_file.close()
        self.test_delimited_file = tempfile.NamedTemporaryFile("r", delete=False)
        self.test_delimited_file.close()

    def tearDown(self):
        self.test_delimited_file.close()
        self.spec_file.close()
        self.test_read_file.close()
        os.remove(os.path.join(self.test_delimited_file.name))
        os.remove(os.path.join(self.spec_file.name))
        os.remove(os.path.join(self.test_read_file.name))
        pass

    def shortDescription(self):
        doc = self._testMethodDoc
        return doc

    def test_ParseRead(self):
        """Validate delimited file contents"""
        import csv
        logger.warning(self.shortDescription())
        with FixedFileReader(self.test_read_file.name, self.test_spec, ",") as test_file_read, \
            open(self.test_delimited_file.name, "w", encoding=self.test_spec.delimitedEncoding) as f:
            writer = csv.writer(f, delimiter=",", lineterminator='\n')
            if self.test_spec.include_header:
                writer.writerow(test_file_read.column_names)
            for line in test_file_read:
                writer.writerow(line)

        self.test_delimited_file = open(self.test_delimited_file.name, "r")
        parse_out_file = iter(self.test_delimited_file)
        header = next(parse_out_file)
        record = next(parse_out_file)
        self.assertEqual("f1,f2 ,f3  \n", header)
        self.assertEqual("AA,BBB,CCCC\n", record)
        self.test_delimited_file.close()


if __name__ == '__main__':
    import io

    suite = unittest.TestLoader().loadTestsFromTestCase(FixedWidthMetaDataTest)
    #from pprint import pprint
    result = unittest.TestResult()
    runner = unittest.TextTestRunner(verbosity=2, stream=io.StringIO()).run(suite)
    runner._makeResult = lambda: result
    runner.run(unittest.TestSuite())
    unittest.main()
    #pprint(suite)

