#!/bin/bash

# BASE URL 
BASE_URL="http://localhost:5000/api/timeline_post"

# Generate RANDOM

RANDOM_ID=$RANDOM
NAME="Anitha${RANDOM_ID}"
EMAIL="anitha${RANDOM_ID}@gmail.com"
CONTENT="Just Added Database to my portfolio site with ${RANDOM_ID}"


echo "CREATE POST data.." 

CREATE_DATA=$(curl --request POST "$BASE_URL" -d "name=$NAME&email=$EMAIL&content=$CONTENT")

echo "Created post: $CREATE_DATA"

echo "Fetching timeline data"

GET_DATA=$(curl "$BASE_URL")
echo "Timeline data"
echo "$GET_DATA"

echo "Delete Timeline data"

echo "Enter post id"
read USER_INPUT_ID

if ! [[ "$USER_INPUT_ID" =~ ^[0-9]+$ ]]; then
   echo "Error"
   exit 1
fi
echo "$BASE_URL/$USER_INPUT_ID"

USER_DELETE_DATA=$(curl --silent --request DELETE "$BASE_URL/$USER_INPUT_ID")
echo "Deleted $USER_DELETE_DATA"
  
