from datetime import datetime
import subprocess
import json
import re

import tempfile

def main():
    nowdata = datetime.today()
    now_hour = int(nowdata.strftime('%H'))
    now_minut = int(nowdata.strftime('%M'))
    AllMinutNow = now_minut + now_hour * 60

    #print(now_hour, now_minut, '=', AllMinutNow)

    
    with open('time.json', 'r', encoding='utf-8') as file_rusult:
        print('ok')
        data = json.load(file_rusult)
    print(data)

    result=''
    prev=0

    for ttime, value in data.items():
        hour, minute = ttime.split(':')
        AllMinut = int(minute) + int(hour) * 60
        #print(hour, minute, '=', AllMinut, value)

        if AllMinut <= AllMinutNow and prev <= int(AllMinut):
            prev = int(AllMinut)
            result = value

if __name__=="__main__" :
    main()
