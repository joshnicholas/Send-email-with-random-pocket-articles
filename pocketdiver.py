import requests
import json
import random

# Select a random number to

offset_randomiser = random.choice(range(100,1000))

# Parameters to get articles from pocket

payload = {"count" : "10", "sort": "oldest", "offset": {}, "consumer_key":"POCKET CONSUMER KEY", "access_token":"POCKET ACCESS TOKEN".format(str(offset_randomiser))}

r = requests.post("https://getpocket.com/v3/get", data = payload)

r_dict = json.loads(r.text)

items = r_dict['list']

item_number_list = []
title_links_list = []

# Create a list of article ID numbers as well as a list of tuples with article name and link

for k, v in items.items():
    item_number_list.append(k)
    title_links_tuple = (v['resolved_title'], v['resolved_url'])
    title_links_list.append(title_links_tuple)

# Create a string with just article names and links

message = "".join("%s\n %s\n" % tup for tup in title_links_list)

# Archive the articles that have been selected using the article ID

for item in item_number_list:
    r2 = requests.post('https://getpocket.com/v3/send', data={
            'consumer_key': 'POCKET CONSUMER KEY',
            'access_token': 'POCKET ACCESS TOKEN',
            'actions': json.dumps([{
                'item_id': '{}'.format(item),
                'action':'archive'
             }])
        })

# Send an email using mailgun with the list of articles

def send_list():
	return requests.post(
		"MAILGUN API ENDPOINT",
		auth=("api", "API KEY"),
		data={"from": "NAME <SENDING EMAIL ADDRESS>",
			"to": ["RECEIVING EMAIL ADDRESS"],
			"subject": "Random pocket articles",
			"text": """
            Howdy,

            Here's a yummy list of stuff to read:

            {}""".format(message)})

send_list()
