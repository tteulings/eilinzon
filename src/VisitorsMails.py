import json
from Levenshtein import distance

def get_visitors(event ):
    with open("mails.json", mode="r") as json_file:
        mails = json.load(json_file)

    visitors = [n for n in event['summary'].split() if n != "" and n != "&"]

    visitors_mails = []

    for visitor in visitors:
        distance_list = [(name,distance(visitor, name)) for name in mails.keys()]
        distance_list.sort(key=lambda x:x[1])
        if distance_list[0][1] <= 1:
            visitors_mails.append(mails.get(distance_list[0][0]))

    return visitors, visitors_mails