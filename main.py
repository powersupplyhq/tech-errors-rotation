import random
import datetime
import json
import os
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
load_dotenv()

def is_valid_selection(name, duty_history):
    # Engineer is on the ignore list (ex: on vacation)
    ignore_str = os.getenv('IGNORE')
    if ignore_str is not None:
        ignore = ignore_str.split(',')
        if name in ignore:
            return False


    # Engineer has never been on duty
    if duty_history.get(name) is None:
        return True

    dates = [datetime.datetime.strptime(d, '%Y-%m-%d').date() for d in duty_history[name]]
    today = datetime.date.today()
    monday = today - datetime.timedelta(days=today.weekday())
    
    # The person was on call today but we want to pick someone else
    if today in dates:
        return False

    # If engineer was on duty yesterday, skip them
    if today - datetime.timedelta(days=1) in dates:
        return False
    
    # If engineer has been on duty twice this week, skip them
    recent_dates = [d for d in dates[-2:] if d >= monday]
    if len(recent_dates) >= 2:
        return False

    # Engineer is eligible
    return True

# Read in the list of names from the .env file
names_str = os.getenv('ENGINEERS')
if names_str is not None:
    names = names_str.split(',')
else:
    logging.error('ENGINEERS environment variable is missing in .env')
    exit(1)

if names == [""]:
    logging.error('ENGINEERS environment variable is empty in .env')
    exit(1)

# Load duty history from file
if os.path.exists('duty_history.json'):
    try:
        with open('duty_history.json') as f:
            duty_history = json.load(f)
    except json.decoder.JSONDecodeError:
        logging.warn('Error loading duty history from file. Resetting history.')
        duty_history = {}
else:
    duty_history = {}

# Select a random eligible engineer
valid_names = list(filter(lambda name: is_valid_selection(name, duty_history), names))
if len(valid_names) == 0:
    logging.warning('No engineers are eligible for duty')
    exit(1)

name = random.choice(list(valid_names))
logging.info(f'{name} is on tech error duty today')

# Update the duty history for the selected name
today = datetime.date.today()
if name in duty_history:
    duty_history[name].append(str(today))
else:
    duty_history[name] = [str(today)]

# Write the duty history back to file
with open('duty_history.json', 'w') as f:
    json.dump(duty_history, f)

# # Send a Slack notification with the selected name
# message = f'{name} is on tech error duty today'
# params = {'channel': '#tech-errors', 'text': message}
# headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer <SLACK_API_TOKEN>'}

# res = requests.post('https://slack.com/api/chat.postMessage', json=params, headers=headers)

# if res.ok:
#     print(f'Sent Slack notification: {message}')
# else:
#     print(f'Error sending Slack notification: {res.text}')
