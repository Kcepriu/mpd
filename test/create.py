from datetime import datetime
import subprocess
import json
import re

import tempfile

def main():
    nowdata = datetime.today()
    now_hour = (nowdata.strftime('%H'))
    #now_minut = int(nowdata.strftime('%M'))

    #print(now_hour, now_minut, '=', AllMinutNow)

    min=range(0,60)
    nn='day'
    strs=''
    for i in min:
       if i%2 == 0:
          nn='day'
       else:
          nn='night'
       strs=strs+'"'+now_hour+":"+str(i)+'": "'+nn+'", \n'
    


    strs='{'+strs+'}'
    print(strs)


    try:
        with open('time.json', 'w', encoding='utf-8') as f:
            f.write(strs)
    except:
        print('errrrr')

if __name__=="__main__" :
    main()
