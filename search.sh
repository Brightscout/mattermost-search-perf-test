#!/bin/bash

#Read environment variables
export $(grep -v '^#' .env | xargs)

#Get TEAM_ID from TEAM_NAME

TEAM_ID=$(curl -s "$API_URL/api/v4/teams/name/$TEAM_NAME" \
--header "Authorization: Bearer $ACCESS_TOKEN" \
--header "Content-Type: application/json" \
| sed -e 's/[{}]/''/g' | sed s/\"//g | awk -v RS=',' -F: '$1=="id"{print $2}'
)

# perform search for given team_id and term
curl --location --request POST "$API_URL/api/v4/teams/$TEAM_ID/posts/search" \
--header "Authorization: Bearer $ACCESS_TOKEN" \
--header "Content-Type: application/json" \
--data-raw '{
    "page": 0,
    "per_page": 100,
    "terms": "'"$*"'",
    "is_or_search":true
    }'
