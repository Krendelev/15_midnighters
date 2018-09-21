import itertools
import datetime
import requests
import pytz


def load_attempts(url):
    for page_num in itertools.count(start=1, step=1):
        response = requests.get(url, params={'page': page_num})
        if not response.ok:
            break
        for record in response.json()['records']:
            yield record


def get_midnighters(attempts):
    midnighters = set()
    for attempt in attempts:
        tz = pytz.timezone(attempt['timezone'])
        time = datetime.datetime.fromtimestamp(attempt['timestamp'], tz=tz)
        if 0 <= time.hour <= 6:
            midnighters.add(attempt['username'])
    return midnighters


if __name__ == '__main__':
    url = 'http://devman.org/api/challenges/solution_attempts/'
    print(*get_midnighters(load_attempts(url)), sep='\n')
