import calendar
import csv
import json
import sys
import time

import config
import requests


def save_to_csv(filename, fields, rows):
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)


def test(args):
    if(len(args) == 0):
        raise BaseException('filename is required')

    url = "{}/api/v4/teams/{}/posts/search".format(
        config.API_URL, config.TEAM_ID)
    headers = {
        'Authorization': 'Bearer {}'.format(config.ACCESS_TOKEN),
    }

    # field names
    fields = ['Search', 'Count', 'Time(in ms)']

    # name of csv file
    filename = "{}-{}.csv".format(args[0], calendar.timegm(time.gmtime()))

    f = open(args[0], "r")

    results = []

    # traverse through all the search term
    for x in f:
        data = {
            "terms": x,
        }
        # fetch search response and store response in results array.
        response = requests.post(
            url, headers=headers, data=json.dumps(data))
        if(response.status_code != 200):
            raise BaseException("Error: recieved {} from URL with message:{}".format(response.status_code, response.text))
        elapsed_seconds = response.elapsed.total_seconds()
        results.append([x, len(response.json()['order']), elapsed_seconds*1000])

    # save results to csv
    save_to_csv(filename, fields, results)


if __name__ == "__main__":
    try:
        test(sys.argv[1:])
    except BaseException as e:
        print(e)
