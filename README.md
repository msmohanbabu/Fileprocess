# File Generator and Parser
## Build Docker

```
docker build . --tag=fileprocess:latest
```

## Unit testing
I have used inbuilt python únittest package for this testin
```
docker run -it -v {PWD}/data/:/processing/data --rm fileprocess:latest python3 -m unittest test/file_process_test.py
```

## Running it
1) create a directory to mount
    ```
    mkdir -p {PWD}/data
    ```
    
2) place the spec.json in data

3) Generate a fixed length file with below command

```
docker run -it -v {PWD}/data/:/processing/data --rm fileprocess:latest python3 ./process_app.py --run gen-fixed --metadata data/spec.json --out data/fixedfile.txt --num-records 50
```

4) parse the fixed length file to delimited file with below command. 
   I have used ',' as delimiter for testing

```
docker run -it -v {PWD}/data/:/processing/data --rm fileprocess:latest python3 ./process_app.py --run parse-fixed-csv --metadata data/spec.json --input data/fixedfile.txt --out data/fixed-delimited.csv --delimiter "," 
```

## Technical Details:

- Generate a fixed width file using the provided spec (offset provided in the spec file represent the length of each field).
  ```
  FixedWidthMetaData - handles the fixed file specification based on spec.json 
  ```
  ```
  FixedFileWriter - generates a file with fixed width records based on spec "FixedWidthMetaData"
  ```  
- Implement a parser that can parse the fixed width file and generate a delimited file, like CSV for example.
  ```
  FixedFileReader - create a delimited file based on spec from "FixedWidthMetaData"
  ```
- DO NOT use python libraries like pandas for parsing. You can use the standard library to write out a csv file (If you feel like)
  ```only standard python(inbuilt) libraries are used```

- Pay attention to encoding
  ```
  fixed width encoding and delimited encoding has been considered while writing and reading.
  ```



