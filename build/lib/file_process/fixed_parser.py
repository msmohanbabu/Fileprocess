import itertools
import logging
import traceback
import random
import ast

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#############################################################
#                                                           #
#FixedWidthMetaData: class to parse the file specfication   #
#                                                           #
#FixedFileWriter: class to generate and write fixed records #
#                                                           #
#FixedFileReader: class to read fixed file based on spec    #
#                                                           #
#############################################################


class FixedWidthMetaData:
    all_parameters = ["ColumnNames", "Offsets", "FixedWidthEncoding", "include_header", "DelimitedEncoding"]
    min_parameters = ["ColumnNames", "Offsets", "include_header"]

    def __init__(self, metadata: dict):

        try:

            if all(param in self.min_parameters for param in metadata.keys()):
                raise JsonMatchException("Json specification should have all keys ", ",".join(metadata.keys()))
            else:
                self.columns = metadata["ColumnNames"]
                self.offsets = metadata["Offsets"]
                if "FixedWidthEncoding" not in metadata:
                    logging.WARN(""""\"FixedWidthEncoding\" does not exist. 
                     Default encoding \"windows-1252\" has been applied""")

                self.fixedWidthEncoding = metadata.get("FixedWidthEncoding", "windows-1252")

                if "DelimitedEncoding" not in metadata:
                    logging.WARN(""""\"DelimitedEncoding\" does not exist. 
                                    Default encoding \"utf-8\" has been applied""")
                self.delimitedEncoding = metadata.get("DelimitedEncoding", "utf-8")

                if "IncludeHeader" not in metadata:
                    logging.WARN(""""\"IncludeHeader\" does not exist. 
                     Header is not included in the file""")

                self.include_header: bool = ast.literal_eval(metadata.get("IncludeHeader", "False"))

                if len(self.columns) != len(self.offsets):
                    raise JsonMatchException("Does not have matching offsets or columns","")
                else:
                    #self.columnOffsets = dict(zip(self.columns, self.offsets))
                    self.columnOffsets = dict(zip(self.columns, [*map(int, self.offsets)]))
        except JsonMatchException as ex:
            raise ex
        except KeyError as ex:
            logger.exception(ex)
            raise JsonMatchException(ex.__str__())
        except Exception as ex:
            logger.exception(ex)
            raise ex


class JsonMatchException(Exception):
    """Raised when file specification does not match with required parameters"""

    def __init__(self, msg, errors):
        super().__init__(msg)
        self.msg = msg
        self.errors = errors


class FixedFileWriter:

    def __init__(self, file: str, layout: FixedWidthMetaData):
        self.file = file
        self.layout = layout
        self.new_file = open(self.file, "w", encoding=self.layout.fixedWidthEncoding)

    def __enter__(self):
        if self.layout.include_header:
            self.write_record(''.join(self._header_record()))
        return self

    def __exit__(self, type, value, traceback):
        self.new_file.close()
        #print(traceback)

    def _header_record(self):
        for k, v in self.layout.columnOffsets.items():
            yield k.ljust(v)[:v]

    def write_record(self, record: str):
        if self.new_file is None:
            raise Exception("Issue in accessing the file")
        self.new_file.writelines(record + "\n")

    def generate_fixed_records(self, characters: str):
        for x, y in self.layout.columnOffsets.items():
            yield ''.join(random.choices(characters, k=y))


class FixedFileReader:

    def __init__(self, file: str, layout: FixedWidthMetaData, delimiter: str):
        self.filename = file
        self.layout = layout
        self.delimiter = delimiter
        self.offsets = [*map(int, self.layout.offsets)]
        self.column_names = []
        self.file_read = open(self.filename, "r", encoding=self.layout.fixedWidthEncoding)

    def __enter__(self):
        if bool(self.layout.include_header):
            header = self.file_read.readline()
            self.column_names = [header[sum(self.offsets[:index]):sum(self.offsets[:index + 1])]
                                 for index in range(len(self.offsets))]
        return self

    def __exit__(self, type, value, traceback):
        self.file_read.close()
        #print(traceback)

    def __iter__(self):
#        if self.layout.include_header:
#            next(self.file_read)

        for row in self.file_read:
            field_list = [row[sum(self.offsets[:index]):sum(self.offsets[:index + 1])]
                          for index in range(len(self.offsets))]
            #records = self.delimiter.join(field_list)
            #print(records)
            yield field_list

