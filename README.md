# mattermost-search-perf-test
A simple utility to perform a series of searches and record the response time of each one. This can be used with different Mattermost search engines (MySQL, ElasticSearch, etc.) to benchmark performance.

<br>

## Setup Instructions
* Install Python 3.6+ and pip.

* Clone this repo:
  ```
  $ git clone https://github.com/Brightscout/mattermost-search-perf-test
  ```
* Install requirements:
  ```
  $ pip3 install -r requirements.txt
  ````
* Create a `.env` file with the contents of `.env.sample`:
    ```
    $ cat .env.sample > .env
    ```
    Update the following values:
    ```
    API_URL=<the URL of your Mattermost site>
    TEAM_NAME=<name of team to search within. e.g: test-team>
    ACCESS_TOKEN=<your Mattermost Personal Access Token>
    ```
    You can learn more about [Personal Access Tokens here](https://docs.mattermost.com/developer/personal-access-tokens.html#personal-access-tokens).

* Create a search query input file similar to `search.txt.sample`. 

<br>

## Executing the python Script
   * Use this command to run the test and generate a report:
     ```
     $ python search.py <input-file> <output-file>
     ```
   * If no `<output-file>` is provided, then it will generate a report with the filename 
   `<input-file>-timestamp.csv`.
   
   * For example: <br> 
      ```
      $ python search.py search.txt output.csv
      ```

## Executing the bash script(for single search)
  * To run this script, you only need to set up .env file
  * Use this command to run the script
    ```
    $ sh search.sh <search-term>
    ```
  * For example: <br> 
    ```
    $ sh search.sh hello world
    ```
