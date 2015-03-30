# 7z2zip_converter

This utility is created to convert 7z archive into ordinary zip archive with
which it is possible to work using Python's zipfile module without unarchiving. 
The difference of this util from other tools is that it extracts and 
zips files from archive one by one. Other tools like 'atoo' at first extract 
everything in a separate temporary folder and then archive everything in the
folder to zip archive. This behaviour is not desirable in case if extracted data
occupies a lot of space.

This utility has been created for Kaggle's competition "Microsoft Malware 
Classification Challenge (BIG 2015)".

To run this utility you must have 7z installed.

The work has been verified on Kubuntu 14.04 with Python 2.7 installed.

The command syntax:

```
python convert.py -jN <input_7z_file> <output_zip_file> 
```

where N is the number of threads used to extract data. Usually, it is equal to
the number of threads that your processor is able to process simultaneously, 
e.g., if you have an Intel processor with 2 cores and enabled Hyperthreading
technology, N is equal to 4.
