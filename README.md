#Build Docker

docker build . --tag=fileprocess:latest

#Unit testing
I have used inbuilt python únittest package for this testing

docker run -it -v `pwd`/data/:/processing/data --rm fileprocess:latest python3 -m unittest test/file_process_test.py
#Running it
1) create a directory to mount
    ```mkdir -p {PWD}/data```
    
2) place the spec.json in data

3) Generate a fixed length file with below command

```docker run -it -v `pwd`/data/:/processing/data --rm fileprocess:latest python3 ./process_app.py --run gen-fixed --metadata data/spec.json --out data/fixedfile.txt --num-records 50``

4) parse the fixed length file to delimited file with below command
   I have used ',' as delimiter
   
```docker run -it -v `pwd`/data/:/processing/data --rm fileprocess:latest python3 ./process_app.py --run parse-fixed-csv --metadata data/spec.json --input data/fixedfile.txt --out data/fixed-delimited.csv```


