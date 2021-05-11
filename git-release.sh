#!/bin/bash

version=$1
text=$2
branch=$(git rev-parse --abbrev-ref HEAD)

if [ $(git config --get remote.origin.url | grep -E 'git@github.com' | wc -l) -gt 0 ]
then 
    export repo_full_name=$(git config --get remote.origin.url | grep -Po "(?<=git@github\.com:)(.*?)(?=.git)")
else
    export repo_full_name=$(git config --get remote.origin.url | sed 's/.*:\/\/github.com\///;s/.git$//')
fi


token=$(git config --global github.token)

generate_post_data()
{
  cat <<EOF
{
  "tag_name": "$version",
  "target_commitish": "$branch",
  "name": "$version",
  "body": "$text",
  "draft": false,
  "prerelease": false
}
EOF
}

generate_post_data
