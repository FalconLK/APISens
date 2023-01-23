# APISens
This repository shares the code and demo video for APISens.

## What it is?
APISens is a sentiment scoring tool for software APIs which aims to support developers to determine the most appropriate API for a certain task. Please check the video named "APISens.mp4".

## How it works?
It first crawls the dataset from two different sources (i.e., Twitter and Youtube).
Twitter is being used for discussion analysis and Youtube is utilized for analyzing APIs' popularity.
The details can be checked in the shared video.

## How do you run it?
A user can simply run main.py to initiate the tool and test with the sample APIs in _example.txt_.
Each query can take more or less 10 seconds as it parses and processes and draw the chart.

## Replication
1. Crawling the data from the platforms with their own APIs.
We leveraged Tweepy as the Tweet crawler and built our own crawler for Youtube with the Google API (v3). 
2. Train API Recognition model and infer the results with the target texts (i.e., Twitter discussions) following https://github.com/soarsmu/Library-Recognition-In-Tweets.
3. Train Sentiment Analysis model and infer the results with the target texts following https://github.com/soarsmu/SA4SE.

## Data
By following Twitter data sharing recommendation and policy, check here https://developer.twitter.com/en/developer-terms/more-on-restricted-use-cases, we can only share the tweet ids.
