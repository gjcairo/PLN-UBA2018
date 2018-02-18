import json
import re

with open("wocka.json", "r") as file:
	all_jokes_str = file.read()

all_jokes = json.loads(all_jokes_str)

all_jokes_plain = ""
for joke_str in all_jokes:
	# remove multiple newlines
	fixed_joke_str = re.sub(r'''[\n\r]+''', '\n', joke_str['body'])

	all_jokes_plain += fixed_joke_str + "\n\n"

with open("jokes.txt", "w") as jokes_file:
	jokes_file.write(all_jokes_plain)

corpus_size = len(all_jokes_plain)
train_corpus_size = int(0.9 * corpus_size)
with open("jokes_train.txt", "w") as jokes_file:
	jokes_file.write(all_jokes_plain[:train_corpus_size])

with open("jokes_test.txt", "w") as jokes_file:
	jokes_file.write(all_jokes_plain[train_corpus_size:])