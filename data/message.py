from fuzzywuzzy import process
from requests import get
import json


# поиск и сортировка всех локаций по запросу
def search(request_):
    data = get('http://localhost:5000/api/location').json()
    list_answers = []
    for elem in data['locations']:
        answer = elem['name'] + " " + elem['city']['name']
        if elem['category'] is not None:
            answer += " " + elem['category']
        list_answers.append((answer, elem['id'], int(elem['count_visits'])))
    answers = sorted(process.extract(request_, list_answers, limit=None), key=lambda x: (-x[-1], -x[0][-1]))
    out = {}
    for elem in answers:
        out[elem[0][1]] = elem[0][0]
    with open("data_file.json", "w") as write_file:
        json.dump(out, write_file)

    return 1
