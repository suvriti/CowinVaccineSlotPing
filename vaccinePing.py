import datetime #for reading present date
import time
import requests
import json
import sys
from plyer import notification
from apscheduler.schedulers.blocking import BlockingScheduler

def pingCowin():
    today = datetime.date.today().strftime("%d-%m-%Y")
    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    #pincode = '140401'
    if sys.argv[1] is not None:
        pincode = sys.argv[1]
        print('Pinging for pincode : ' + pincode)
    r =requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=' + pincode  +'&date='+today, headers=headers)
    CoData = (r.text)
    CoData_Json = json.loads(CoData)['centers']
    for x in CoData_Json:
        ses = x['sessions']
        for s in ses:
            if s['min_age_limit'] == 18 and s['available_capacity'] > 0:
                print('Vaccine available at center : ' + x['name'])
                notification.notify(
                            #title of the notification,
                            title = "Slot Available",
                            #the body of the notification
                            message = "Slot available at center : {}".format(x['name']),
                            # the notification stays for 50sec
                            timeout  = 50
                        )

scheduler = BlockingScheduler()
scheduler.add_job(pingCowin, 'interval', minutes=10)
scheduler.start()
