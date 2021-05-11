#!/bin/bash
TAG=""
if [ $(git log -1 --pretty=%B | grep -E ^feature\: | wc -l) -gt 0 ]; then TAG=$(git semver --next-minor); fi
if [ $(git log -1 --pretty=%B | grep -E ^breaking\: | wc -l) -gt 0 ]; then TAG=$(git semver --next-major); fi
if [ -z $TAG ]; then TAG=$(git semver --next-patch); fi
echo $TAG