"""
This module contains the code to generate a search report(in csv)
for multiple mattermost search.
"""
import calendar
import csv
import json
import logging
import os
import sys
import time
from statistics import mean

import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")
TEAM_NAME = os.getenv("TEAM_NAME")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def get_team_id():
    """
    This function return the team_id for TEAM_NAME
    """
    url = "{}/api/v4/teams/name/{}".format(API_URL, TEAM_NAME)
    headers = {
        'Authorization': 'Bearer {}'.format(ACCESS_TOKEN),
    }
    response = requests.get(url, headers=headers)
    return response.json()['id']


def save_to_csv(filename, fields, rows):
    """
    This function saves a csv file with given fields and rows.
    """
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, lineterminator='\n')
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)


def test(args):
    """
    This function reads a search query file, perform search for each search query
    and then saves the result metric to csv.
    """
    if len(args) == 0:
        raise BaseException('filename is required')

    team_id = get_team_id()
    url = "{}/api/v4/teams/{}/posts/search".format(
        API_URL, team_id)
    headers = {
        'Authorization': 'Bearer {}'.format(ACCESS_TOKEN),
    }

    # field names
    fields = ['search_text', 'count', 'time(in ms)']

    # name of csv file
    filename = ''
    if len(args) == 2:
        filename = args[1]
    else:
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
        results.append([term.rstrip(),
                        len(response.json()['order']),
                        elapsed_seconds * 1000])

    save_to_csv(filename, fields, results)

    # log the minimum, average and maximum reponse time in ms
    response_duration = [record[2] for record in results]
    if len(response_duration) > 0:
        logging.info("Mininum response time(in ms): %f", min(response_duration))
        logging.info("Maximum response time(in ms): %f", max(response_duration))
        logging.info("Average response time(in ms): %f", mean(response_duration))


if __name__ == "__main__":
    try:
        test(sys.argv[1:])
    except BaseException as error:  # pylint: disable=broad-except
        logging.error(error)
