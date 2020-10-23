## Setup instructions
* In `search.txt`, you can specify the search terms seperated by new line for which the search will be performed. 
for example - 
    > Lorem ipsum dolor sit  amet, consectetur adipiscing elit.<br>
    Donec mollis mi at quam consectetur tempor.<br>
    Proin eleifend leo ut nisl aliquam consectetur.<br>
    Nunc nec nisl at odio faucibus luctus.<br>
    Mauris et lorem congue, fringilla justo in, porttitor arcu.<br>
    >
    Here, `search.txt` has 5 lines, then script will generate a cumulative report for 5 search requests.

* In `config.py`
    * Replace API_URL with mattermost server URL 
    * Replace TEAM_ID with team id for which you want to perform the search.
    * Replace ACCESS_TOKEN with personal access token. You can refer [here](https://docs.mattermost.com/developer/personal-access-tokens.html#personal-access-tokens) to know about how to create personal access token.

## Run script
   * Use this command ```python test.py``` to generate a report.
