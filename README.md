## COVID-19 Daily Reports

* [Countries COVID-19 Statistics](https://4m3ndy.github.io/cb-covid-19-pipeline/countries-covid-data)
* [List 10 Countries with Last Submission](https://4m3ndy.github.io/cb-covid-19-pipeline/countries-last-submission)

Whenever you commit to this repository, GitHub Pages will run [Jekyll](https://jekyllrb.com/) to rebuild the pages in under https://4m3ndy.github.io/cb-covid-19-pipeline , from the content in `countries-covid-data.html` and `countries-last-submission.html` files.

### Requriments
- Python 3.x

## How to run

### To generate COVID-19 reports
```bash
python3 main.py
```

### To update countries list
```bash
python3 main.py --countries "Ukraine,Poland,Denmark,Switzerland,United States,Algeria"
```

