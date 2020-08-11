# Learning Python

Place to collect scripts and notes on learning Python.

## Tutorials

- [Tutorial - Learn Python in 10 minutes](https://www.stavros.io/tutorials/python/)
- [Python API Tutorial: Getting Started with APIs] (https://www.dataquest.io/blog/python-api-tutorial/)

## SSH issues

If you get errors like:

```
urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:833)>
```

then see [urllib and “SSL: CERTIFICATE_VERIFY_FAILED” Error](https://stackoverflow.com/a/48134650/9684). Add 

```
import certifi
import ssl
```

then in `urllib.request.urlopen` add parameter `context=ssl.create_default_context(cafile=certifi.where())`



## Read and write RIS files

Make sure we have [rispy](https://github.com/MrTango/rispy) installed:

```
pip3 install rispy
```

### Create a RIS file

Then run example `ris.py`

```
python3 ris.py
```

This should create the file `export.ris`

```
1.
TY  - JOUR
ID  - 42
T1  - The title of the reference
A1  - Marxus, Karlus
A1  - Lindgren, Astrid
ER  - 

2.
TY  - JOUR
ID  - 43
T1  - Reference 43
AB  - Lorem ipsum
ER  - 

```

### Read a RIS file

The file `readris.py` reads the RIS file created in the previous step.

