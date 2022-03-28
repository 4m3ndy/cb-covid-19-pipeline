#!/usr/bin/env python3

import csv, os, argparse
from operator import truediv
from jinja2 import Environment, FileSystemLoader

def generate_html_doc(template_data, template_file_name):
    root = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(root, 'templates')
    env = Environment( loader = FileSystemLoader(templates_dir), trim_blocks=True)
    template = env.get_template( template_file_name + '.html.j2')

    rendered_doc = os.path.join(root, template_file_name + '.html')
    with open(rendered_doc, 'w') as fh:
        fh.write(template.render(
            template_data = template_data
        ))

def add_new_countries(countries_list) -> bool:
    try:
        rendered_countries = os.path.join('countries.txt')
        with open(rendered_countries, 'w') as fh:
            for country in countries_list.split(","):
                fh.write(country + "\n")
        return True
    except Exception as x:
        print("Couldn't add new countries, for more details: ", x )
        return False

def get_country_per_last_submission_date() -> str:
    reported_locations = {}
    try:
        with open(os.getenv('COVID_DATA_CSV_FILE_PATH', "../owid-covid-data.csv")) as csv_file:
            locations = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in locations:
                if line_count == 0:
                    pass
                else: 
                    reported_locations[str(row[2])] = str(row[3])
                line_count += 1
    except Exception as x:
        print("Couldn't Read CSV file, for more details: ", x )
    
    return reported_locations

def get_country_covid_statistics(country_per_last_submission_date_list) -> str:
    countries_list = []
    country_statistics_list = []

    with open('countries.txt') as f:
        countries_list = [line.rstrip() for line in f]

    try:
        with open(os.getenv('COVID_DATA_CSV_FILE_PATH', "../owid-covid-data.csv")) as csv_file:
            submission = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in submission:
                if line_count == 0:
                    pass
                else:
                    for country in countries_list:
                        country_statistics = {"name": country, "last_submission_date": country_per_last_submission_date_list[country]}
                        if str(row[2]) == country and str(row[3]) == country_per_last_submission_date_list[country]:
                            country_statistics["total_cases"] = int(float(row[4])) if str(row[4]) != '' else "N/A"
                            country_statistics["new_cases"] = int(float(row[5])) if str(row[5]) != '' else "N/A"
                            country_statistics["total_vaccinations"] = int(float(row[34])) if str(row[34]) != '' else "N/A"
                            country_statistics["new_vaccinations"] = int(float(row[38])) if str(row[38]) != '' else "N/A"
                            country_statistics_list.append(country_statistics)                  
                line_count += 1
    except Exception as x:
        print("Couldn't Read CSV file, for more details: ", x )
        exit(1)
    
    return country_statistics_list


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--countries", nargs='?', help="list of countries comma separated", type=str, default=None)
    args = parser.parse_args()

    if args.countries:
        if add_new_countries(args.countries):
            print("New countries added")
            exit(0)
        else:
            print("Failed to add new countries")
            exit(1)


    country_per_last_submission_date_list = get_country_per_last_submission_date()
    sorted_country_per_last_submission_date_list = sorted(country_per_last_submission_date_list.items(), key=lambda x: x[1])
    generate_html_doc(sorted_country_per_last_submission_date_list[:10], "countries-last-submission")

    country_statistics_list = get_country_covid_statistics(country_per_last_submission_date_list)
    generate_html_doc(country_statistics_list, "countries-covid-data")
