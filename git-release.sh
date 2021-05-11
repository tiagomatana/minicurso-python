#!/bin/bash

version=$1
text=$2
branch=$(git rev-parse --abbrev-ref HEAD)

if [ $(git config --get remote.origin.url | grep -E 'git@github.com' | wc -l) -gt 0 ]
then 
    repo_full_name=$(git config --get remote.origin.url | grep -Po "(?<=git@github\.com:)(.*?)(?=.git)")
else
    repo_full_name=$(git config --get remote.origin.url | sed 's/.*:\/\/github.com\///;s/.git$//')
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

echo "Create release $version for repo: $repo_full_name branch: $branch"
/usr/bin/curl -X POST -H "Accept: application/vnd.github.v3+json;" -H "Authorization: token $token" -d "$( generate_post_data )" https://api.github.com/repos/$repo_full_name/releases
