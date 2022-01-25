"""
Creates simple model file prototype
"""

import json

length_shell = {}
letter_shell = {}

with open("bigrams.json", "r") as model_file:
    k = json.load(model_file)

for i in range(20):
    length_shell[str(i+1)] = 5000

assert sum(list(length_shell.values())) == 100000

alphabet = [chr(j+ord('a')) for j in range(26)]

cur_sum = 0
for i in alphabet:
    letter_shell[i] = {}
    cur_sum = 0
    for j in alphabet:
        cur_sum += k[i+j]
    for j in alphabet:
        letter_shell[i][j] = int((100000*k[i+j]) / cur_sum)
    final_sum = sum(list(letter_shell[i].values()))
    if not final_sum == 100000:
        letter_shell[i]['e'] += 100000 - final_sum
    assert sum(list(letter_shell[i].values())) == 100000

with open("model.json", "w") as model_file:
    json.dump([length_shell, letter_shell], model_file)
