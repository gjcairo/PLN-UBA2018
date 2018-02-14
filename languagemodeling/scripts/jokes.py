import json

with open("wocka.json", "r") as file:
	all_jokes_str = file.read()

all_jokes = json.loads(all_jokes_str)

all_jokes_plain = ""
for joke_str in all_jokes:
	all_jokes_plain += joke_str['body'] + "\n"

with open("jokes.txt", "w") as jokes_file:
	jokes_file.write(all_jokes_plain)