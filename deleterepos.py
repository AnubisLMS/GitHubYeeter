import os
import json
import time
import datetime
import requests
import dateutil.parser
import multiprocessing

disclude = {
    'os3224/anubis-assignment-tests',
    'os3224/os_devcontainer',
    'os3224/xv6-containers',
    'os3224/course_docs',
    'os3224/cut-template',
    'os3224/ds-final-project',
    'os3224/OS_HW_3_recitation_notes'
}

token = os.environ['GITHUB_TOKEN']

def backup_delete(repo):
    if repo in disclude:
        return True
    if not os.path.exists(repo):
        r = os.system(f'mkdir -p {repo} && git clone git@github.com:{repo}.git {repo}')
        if r != 0:
            return repo
    r = requests.delete(
        f'https://api.github.com/repos/{repo}',
        headers={
            'Accept': 'application/vnd.github+json',
            'Authorization': f'Bearer {token}',
        },
    )
    match r.status_code:
        case 404 | 204:
            print(f'delete {repo}')
            return True
        case _:
            if 'retry-after' in r.headers:
                wait = int(r.headers['retry-after'])
                print(f'waiting {wait} s')
                time.sleep(wait + 0.5)
                return backup_delete(repo)
            return repo

with multiprocessing.Pool(16) as pool:
    fp = 'repos.json'
    #if os.path.exists('failed.json'):
    #    fp = 'repos.json'
    repos = json.load(open(fp, 'r'))
    res = []
    for repo in repos:
        res.append(backup_delete(repo))
    # res = pool.map(backup_delete, repos)
    failed = list(filter(lambda x: isinstance(x, str), res))
    print(failed)
    json.dump(failed, open('failed.json', 'w'))
