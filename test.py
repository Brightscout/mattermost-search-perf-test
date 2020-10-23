import requests
import sys
import config
import json


def test():
    url = "{}/api/v4/teams/{}/posts/search".format(
        config.API_URL, config.TEAM_ID)
    headers = {
        'Authorization': 'Bearer {}'.format(config.ACCESS_TOKEN),
    }
    f = open("search.txt", "r")

    min_time = 10000
    max_time = 0
    total_time = 0
    total_search_count = 0

    # traverse through all the search term in "search.txt"
    for x in f:
        data = {
            "terms": x,
            "is_or_search": True
        }
        try:
            # fetch search response and calculate response time
            response = requests.post(
                url, headers=headers, data=json.dumps(data))
            if(response.status_code != 200):
                raise sys.exit("Error: recieved {} from URL with message:{}".format(
                    response.status_code, response.text))
            elapsed_seconds = response.elapsed.total_seconds()
            min_time = min(min_time, elapsed_seconds)
            max_time = max(max_time, elapsed_seconds)
            total_time += elapsed_seconds
            total_search_count += 1
        except requests.exceptions.RequestException as e:
            raise sys.exit(e)

    print("Total Time(in ms): {}".format(total_time*1000))
    print("Average Time(in ms): {}".format(total_time/total_search_count*1000))
    print("Minimum Respose Time(in ms): {}".format(min_time*1000))
    print("Maximum Response Time(in ms): {}".format(max_time*1000))


test()
