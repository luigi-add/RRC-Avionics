#!/usr/bin/env bash

git init
git config user.name "$1"
git config user.email "$2"
git add *
git commit -m "$3"
