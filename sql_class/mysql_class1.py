import csv

titles = {}

with open("dados_cerveja.csv") as file:
    reader = csv.DictReader(file, delimiter=';')
    for row in reader:
        title = row["classe"].strip().lower()
        if title not in titles:
            titles[title] = 0
        titles[title] += 1

def f(title):
    return titles[title]


for title in sorted(titles, key = f, reverse=True):
    print(title, titles[title])