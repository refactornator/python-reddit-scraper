# Python Reddit Scraper

A simple tool for downloading content from reddit and sticking it into a database. Right now this just gets Showerthoughts that I needed for a chatbot.

### Getting Started

#### Dependencies
```
pip install praw --user
```

#### Running
Fill in environment variables after creating an app at https://www.reddit.com/prefs/apps/. Create the app as a script and use `http://localhost:8080` as your redirect uri.
```
PRAW_USER_AGENT= PRAW_CLIENT_ID= PRAW_CLIENT_SECRET= PRAW_USERNAME= PRAW_PASSWORD= ./scraper.py
```