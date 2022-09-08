import os
import json
import datetime
import requests
import dateutil.parser
import multiprocessing

disclude = {
    'os3224/anubis-assignment-tests',
    'os3224/os_devcontainer',
    'os3224/ds-final-project',
    'os3224/OS_HW_3_recitation_notes'
}

token = os.environ['GITHUB_TOKEN']

def backup_delete(repo):
    r = os.system(f'mkdir -p {repo} && git clone git@github.com:{repo}.git {repo}')
    if r != 0:
        return repo
    requests.delete(
        f'https://api.github.com/repos/{repo}',
        headers={
            'Accept': 'application/vnd.github+json',
            'Authorization': f'Bearer {token}',
        },
    )
    return True

with multiprocessing.Pool(16) as pool:
    repos = json.load(open('repos.json', 'r'))
    res = pool.map(backup_delete, repos)
    failed = list(filter(lambda x: isinstance(x, str), res))
    print(failed)
    json.dump(failed, open('failed.json', 'w'))
