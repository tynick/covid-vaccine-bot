import time
from twilio.rest import Client
from bs4 import BeautifulSoup
import requests
from slack_webhook import Slack
import config

# twilio creds
account_sid = ''
auth_token = ''
target_number = '+15555555555'
source_number = '+15555555555'

# slack webhook
slack_url = 'https://hooks.slack.com/services/XXXXXXXXXXX/XXXXXXXXXXXX/XXXXXXXXXXXXXXXXXXXXXXXX'

# how many seconds to sleep in between loops
retry_timer = 15

# messaging limiter
# Phoenix Municipal Stadium
site_1 = 'on'
# State Farm Stadium
site_2 = 'on'

# URLs for each site we want to check.
vaccine_sites = {'Phoenix Municipal Stadium': 'https://www.handsonphoenix.org/opportunity/a0N1J00000QGgU1UAL',
                 'State Farm Stadium': 'https://www.handsonphoenix.org/opportunity/a0N1J00000NW4CHUA1'}

# send a message via twilio
def send_twilio_message(body):
    twilioCli = Client(account_sid, auth_token)
    message = twilioCli.messages.create(body=body, from_=source_number, to=target_number)
    logging.debug(message.sid)

# send a message via slack
def send_slack_message(slack_url, message):
    slack = Slack(url=slack_url)
    slack.post(text=message)

# get all content from the site and parse it
def get_site(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    return soup

while True:
    for site, site_url in vaccine_sites.items():
        print('getting site...')
        vaccine_site_info = get_site(site_url)
        print('site retrieved...')
        if str(vaccine_site_info).find("no longer available") == -1:
            new_message = 'There is an opening at {0}. Check {1} for more info.'.format(site, site_url)
            if 'Phoenix Municipal' in site and site_1 == 'on':
                print(new_message)
                send_slack_message(slack_url, new_message)
                send_twilio_message(new_message)
            elif 'State Farm' in site and site_2 == 'on':
                print(new_message)
                send_slack_message(slack_url, new_message)
                send_twilio_message(new_message)
        else:
            new_message = 'nothing was available'
            print(new_message)
            if 'Phoenix Municipal' in site:
                site_1 = 'on'
            elif 'State Farm' in site:
                site_2 = 'on'
    time.sleep(retry_timer)
