This is an opinionated ad-hoc script for cleaning up GED files exported from [Sierra On-Line's Generations EasyTree](https://www.gensoftreviews.com/?p=271).  Despite providing the option to choose [GEDCOM version 5.5](https://gedcom.io/specifications/ged55.pdf), the outputted files are not compliant with the [Chronoplex GEDCOM Validator](https://chronoplexsoftware.com/gedcomvalidator).  This cleans up various syntax issues and avoids unsupported tags.

Install dependencies with:
```
pip install -r requirements.txt
```

Run the script with:
```
python convert.py input_file output_file
```

Last tested with Python 3.11 on Windows 11.

Feedback and improvements are welcome.