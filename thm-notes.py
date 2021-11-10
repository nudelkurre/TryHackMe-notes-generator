#!/usr/bin/env python3

import requests
from datetime import datetime
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("url", type=str, help="Specify an url to a room")
parser.add_argument("-n", dest="name", help="Specify a name to put in the notes")
args = parser.parse_args()

tags = re.compile(r'(<!--.*?-->|<[^>]*>)')

def url_to_room(url):
    room = url.split("/")[-1]
    url = "/".join(url.split("/")[:-1])
    if(url == "https://tryhackme.com/room"):
        return room
    else:
        print("Not an url to a THM room")
        return

def get_details(room):
    return requests.get(f"https://tryhackme.com/api/room/details?codes={room}").json()[room]

def get_tasks(room):
    return requests.get(f"https://tryhackme.com/api/tasks/{room}").json()['data']

def get_date():
    return datetime.now().strftime("%B %d, %Y")

def format_question(question):
    return(tags.sub("","".join(f"\n```\n{question['question']}\n\n> \n```\n".replace("<p>", "").replace("</p>", ""))))

def write_notes(room):
    details = get_details(room)
    title = details['title']
    with open(f"{title}.md".replace(" ", "").replace("/", "_"), "w") as f:
        f.write(f"# {title}\n")
        if(args.name):
            f.write(f"{args.name}\n")
        f.write(f"> {get_date()}\n")
        for t in get_tasks(room):
            f.write(f"---\n## TASK {t['taskNo']}\n")
            for q in t['questions']:
                f.write(f"{format_question(q)}")
            
room = url_to_room(args.url)
if(room):
    write_notes(room)