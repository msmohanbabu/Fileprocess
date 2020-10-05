import argparse
import json
import string
import sys
import traceback
import logging
import csv
from file_process.fixed_parser import FixedWidthMetaData, FixedFileWriter, JsonMatchException, FixedFileReader

###################################################################
# Arguments to be passed:                                         #
#                                                                 #
# 1) --run gen-fixed                                              #
#    --metadata JSON_FILE - [Spec File Specification]             #
#    --out OUTPUT_FILE [to Store generate fixed records]          #
#    --num-records [Number of records to be generated]            #
#                                                                 #
# 2) --run parse-fixed-csv                                        #
#    --metadata JSON_FILE - [Spec File Specification]             #
#    --input - [Fixed File to be read for parsing]                #
#    --out  - [File to store delimited file]                      #
#    --delimiter - [Delimiter]                                    #
#                                                                 #
###################################################################


def main(args):

    try:
        global_chars = string.ascii_uppercase + string.digits
        options, parser = parse_arguments(args)
        metadata = FixedWidthMetaData(json.load(options.json_file))
        num_of_records = 20 if options.num_of_records is None else options.num_of_records
        delimiter = "," if options.delimiter is None else options.delimiter

        if options.process == "gen-fixed":
            with FixedFileWriter(options.output_file, metadata) as f_write:
                    for entry in range(0, int(num_of_records)):
                        records = ''.join(str(x) for x in f_write.generate_fixed_records(global_chars))
                        f_write.write_record(records)

        elif options.process == "parse-fixed-csv":
            if options.fixed_file is None:
                parser.error("Argument \"--input\" is required for delimited file generation")
            else:
                with FixedFileReader(options.fixed_file, metadata, ",") as file_read, \
                        open(options.output_file, "w", encoding=metadata.delimitedEncoding) as f:
                    writer = csv.writer(f, delimiter=delimiter, lineterminator='\n')
                    if metadata.include_header:
                        writer.writerow(file_read.column_names)
                    for line in file_read:
                        writer.writerow(line)
        else:
            parser.error("Argument \"--run\" must be either \"gen-fixed\" and \"parse-fixed-csv\".")

    except JsonMatchException as ex:
        logging.exception(ex)
        traceback.print_exc()
        raise ex
    except Exception as e:
        logging.exception(e)
        traceback.print_exc()


def parse_arguments(args: list):
    parser = argparse.ArgumentParser("Generate Fixed File or CSV file from Fixed File.")

    parser.add_argument("--run", choices=["gen-fixed", "parse-fixed-csv"], dest="process", required=True,
                        help="""\"gen-fixed\" - to generate fixed length file. \n
                            \"parse-fixed-csv\" - to generate delimited from fixed.""")

    parser.add_argument("--metadata", dest="json_file", type=argparse.FileType("r"),
                        required=True, help="input json file with metadata - File Specfication")

    parser.add_argument("--out", dest="output_file", required=True,
                        help="output file to store generated fixed file")

    parser.add_argument("--num-records", dest="num_of_records", required=False,
                        help="number of records to be generated")

    parser.add_argument("--delimiter", dest="delimiter", required=False,
                        help="pass the delimiting character. Default would be comma \",\" .")

    parser.add_argument("--input", dest="fixed_file",
                        required=False, help="fixed file is required for delimited file generation")

    return parser.parse_args(args), parser


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
