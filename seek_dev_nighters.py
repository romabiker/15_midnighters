from collections import Counter
from datetime import datetime
from operator import itemgetter
from pytz import timezone, utc
import json
import pytz
import requests


def get_devman_api_solution_attempts(page):
    url = 'https://devman.org/api/challenges/solution_attempts'
    response = requests.get(url, params={'page': page})
    if not response.ok:
        response.raise_for_status()
    return response.text


def get_midnighters_list():
    midnighters_list = []
    for page_of_attempts in load_attempts():
        midnighters_list.extend(get_page_of_midnighters(page_of_attempts))
    return midnighters_list


def get_page_of_midnighters(page_of_attempts):
    midnighters = []
    for attempt in page_of_attempts['records']:
        attempt_timestamp = attempt['timestamp']
        if not attempt_timestamp:
            continue
        attempt_tz = timezone(attempt['timezone'])
        attempt_utc_dt = datetime.fromtimestamp(attempt_timestamp, tz=utc)
        attempt_local_dt = attempt_utc_dt.astimezone(attempt_tz)
        if attempt_local_dt.hour < 7:
            midnighters.append(attempt['username'])
    return midnighters


def load_attempts():
    page = 1
    while True:
        attempts_json = json.loads(get_devman_api_solution_attempts(page))
        yield attempts_json
        page += 1
        if not page <= attempts_json['number_of_pages']:
            break


def output_midnighters_to_console(midnighters_counter):
    print('\nMidnighters:            Solution attempts\n')
    for midnighter, attempts in midnighters_counter.most_common():
        print('{:<20}  | {}'.format(midnighter, attempts))
    print()


if __name__ == '__main__':
    midnighters_counter = Counter(get_midnighters_list())
    output_midnighters_to_console(midnighters_counter)
