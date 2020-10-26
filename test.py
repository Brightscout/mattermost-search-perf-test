"""
This module contains the code to generate a search report(in csv)
for multiple mattermost search.
"""
import calendar
import csv
import json
import os
import sys
import time

import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")
TEAM_ID = os.getenv("TEAM_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")


def save_to_csv(filename, fields, rows):
    """
    This function saves a csv file with given fields and rows.
    """
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)


def test(args):
    """
    This function reads a search query file, perform search for each search query
    and then saves the result metric to csv.
    """
    if len(args) == 0:
        raise BaseException('filename is required')

    url = "{}/api/v4/teams/{}/posts/search".format(
        API_URL, TEAM_ID)
    headers = {
        'Authorization': 'Bearer {}'.format(ACCESS_TOKEN),
    }

    # field names
    fields = ['search_text', 'count', 'time(in ms)']

    # name of csv file
    filename = "{}-{}.csv".format(args[0], calendar.timegm(time.gmtime()))

    input_file = open(args[0], "r")

    results = []

    # traverse through all the search term
    for term in input_file:
        data = {
            "terms": term,
        }
        # fetch search response and store response in results array.
        response = requests.post(
            url, headers=headers, data=json.dumps(data))
        if response.status_code != 200:
            raise BaseException(
                "Error: recieved {} from URL with message:{}".format(
                    response.status_code, response.text))
        elapsed_seconds = response.elapsed.total_seconds()
        results.append([term,
                        len(response.json()['order']),
                        elapsed_seconds * 1000])

    # save results to csv
    save_to_csv(filename, fields, results)


if __name__ == "__main__":
    try:
        test(sys.argv[1:])
    except BaseException as error:  # pylint: disable=broad-except
        print(error)
