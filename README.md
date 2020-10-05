# File Generator and Parser

## Processing App and Arguments

process_app.py - this is the main program takes below arguments

```
usage: Generate Fixed File or CSV file from Fixed File. [-h] --run {gen-fixed,parse-fixed-csv} --metadata JSON_FILE --out OUTPUT_FILE
                                                        [--num-records NUM_OF_RECORDS] [--delimiter DELIMITER] [--input FIXED_FILE]

  -h, --help            show this help message and exit
  --run {gen-fixed,parse-fixed-csv}
                        "gen-fixed" - to generate fixed length file. "parse-fixed-csv" - to generate delimited from fixed.
  --metadata JSON_FILE  input json file with metadata - File Specfication
  --out OUTPUT_FILE     output file to store generated fixed file
  --num-records NUM_OF_RECORDS
                        number of records to be generated
  --delimiter DELIMITER
                        pass the delimiting character. Default would be comma "," .
  --input FIXED_FILE    fixed file is required for delimited file generation
```
### Arguments to generate fixed width file
```
python3 process_app.py \
--run gen-fixed \
--metadata data/spec.json \
--out data/fixedfile.txt \ # fixed width records will be written here
--num-records 50 
```

### Arguments to parse the fixed file and create delimited file
```
python3 process_app.py \
--run parse-fixed-csv \
--metadata data/spec.json \
--input data/fixedfile.txt \
--out data/delimited_out.csv \
--delimiter "," # default one is comma ","
```
