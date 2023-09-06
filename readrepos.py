import os
import pytz
import json
import datetime
import requests
import datetime
import dateutil.parser

token = os.environ['GITHUB_TOKEN']

page = 0
last_len = 1
repos = []

day = datetime.datetime(2023, 9, 1).replace(tzinfo=pytz.UTC)

while last_len != 0:
    print(f'page = {page}')
    res = requests.get(
        'https://api.github.com/orgs/os3224/repos',
        headers={
            'Accept': 'application/vnd.github+json',
            'Authorization': f'Bearer {token}',
        },
        params={
            'sort': 'created',
            'direction': 'asc',
            'per_page': '100',
            'page': str(page),
        }
    )
    data =res.json()
    for repo in data:
        if day < dateutil.parser.parse(repo['created_at']):
            continue
        if repo['is_template'] is True:
            continue
        repos.append(repo['full_name'])
    last_len = len(data)
    page += 1
    json.dump(repos, open('repos.json', 'w'))
