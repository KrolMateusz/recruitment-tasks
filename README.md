# Csv report processing and web crawler
Intern recruitment tasks from Clearcode company

## Description
The file csv_report_processing.py is used to create CSV file with a report
containing ad views and number of users click on ads aggregated by date and
country. It also write information about invalid rows to standard error.

The script web_crawler.py contains a function site_map(url), which takes
a site URL as an argument and returns mapping of that domain. This mapping
contains all pages within that domain without anchor links.

## Requirements
All requirements are in file requirements.txt. To install dependencies use:
```commandline
pip install -r requirements.txt
```

## Usage
To run csv_report_processing.py open command line in project directory and type
this command with proper file names.
```commandline
csv_report_processing.py input_file.csv output_file.csv
```

To run site_map(url) function, type in python console
```python
>>> site_map(url_address)
```
