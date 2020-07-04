from datetime import datetime
import subprocess
import json
import re

import tempfile

def GetPlayListFromFile():
    nowdata = datetime.today()
    now_hour = int(nowdata.strftime('%H'))
    now_minut = int(nowdata.strftime('%M'))
    AllMinutNow = now_minut + now_hour * 60

    #print(now_hour, now_minut, '=', AllMinutNow)

    try:
        with open('time.json', 'r', encoding='utf-8') as file_rusult:
            print('ok')
            data = json.load(file_rusult)
            print(data)
    except:
        print('errrrr')
        return 'Not files'

    result=''
    prev=0

    for ttime, value in data.items():
        hour, minute = ttime.split(':')
        AllMinut = int(minute) + int(hour) * 60
        #print(hour, minute, '=', AllMinut, value)

        if AllMinut <= AllMinutNow and prev <= int(AllMinut):
            prev = int(AllMinut)
            result = value

    return result

def GetPlayListFromMPC():
    output=subprocess.check_output(mpc+["playlist"])
    return output.decode("utf-8")

def UpdateBase():
    output = subprocess.check_output(mpc+[ "update"])

def ClearPlayList():
    #Очистимо список збережених
    output = subprocess.check_output(mpc+[ "lsplaylists"])
    PlayListsSTR = output.decode("utf-8")
    if PlayListsSTR!="":
        for Playlist in PlayListsSTR.split('\n'):
            Playlist=Playlist.replace('\r', '')
            if Playlist!='':
                print('clear', Playlist)
                output = subprocess.check_output(mpc+[ "rm", Playlist])

    #Видалимо файли з поточного
    output = subprocess.check_output(mpc+[ "clear"])

def ShufflePlayList():
    output = subprocess.check_output(mpc+[ "shuffle"])

def PlayPlayList():
    output = subprocess.check_output(mpc+[ "play"])
    output = subprocess.check_output(mpc+[ "random", "off"])
    output = subprocess.check_output(mpc+[ "repeat", "on"])
    Volume()


def AddPlayList(NamePlayList):
    output = subprocess.check_output(mpc+[ "add",  NamePlayList])
    output = subprocess.check_output(mpc+[ "save", NamePlayList])

def ls_mpc():
    output = subprocess.check_output(mpc+["ls"])
    return output.decode("utf-8")


def StatusMpc():
    output = subprocess.check_output(mpc+[  "status"])
    outs=output.decode("utf-8").split('\n')

    if len(outs)<=2:
        return "stop"
    status = re.findall(r'\[(.*)\]', outs[1])[0]
    return status

def UpdatePlayList(NamePlayList, PlayListMPC):
    output = subprocess.check_output(mpc+[ "listall", NamePlayList])
    AllFilesSTR=output.decode("utf-8")#.split('\n')
    #print(len(AllFilesSTR.split('\n')))
    #print(len(PlayListMPC.split('\n')))

    return (len(AllFilesSTR.split('\n'))!=len(PlayListMPC.split('\n')))
   

def GetNameCurentPlayList():
    output = subprocess.check_output(mpc+[ "lsplaylists"])
    PlayListsSTR = output.decode("utf-8")
    if PlayListsSTR != "":
         return PlayListsSTR.split('\n')[0].replace('\r', '')
    return ''

def Volume(status=True):
    if status == True:
        output = subprocess.check_output(mpc+[ "volume", '+100'])
    else:
        output = subprocess.check_output(mpc+[ "volume", '-100'])



def main():
    
    global mpc
    #mpc="c:\\mpd\\mpc.exe"

    #mpc=['/usr/bin/mpc', '-h', '172.25.1.50']
    mpc = ['/usr/bin/mpc']

    UpdateBase()

    NamePlayList        = GetPlayListFromFile()
    PlayListMPC         = GetPlayListFromMPC()
    NameCurentPlayList  = GetNameCurentPlayList()

    DirName             = ls_mpc()
    
    print(NamePlayList)

    if DirName.find(NamePlayList)==-1:
        #print("Not find dir "+NamePlayList)
        return


    Update=UpdatePlayList(NamePlayList, PlayListMPC)

    #---------------------------------------------------------
    #if Update:
    #    print('update')
    print(NameCurentPlayList)
    print(NamePlayList)

    #if PlayListMPC.find(NamePlayList+".mp3")>-1 and not Update:
    if NameCurentPlayList == NamePlayList and not Update:
        #1. перевірити що зараз грає
        status=StatusMpc()
        # 2. Якщо не грає, то запустити
        if status!='playing':
            PlayPlayList()
    else:
        Volume(False)
        # 1. Очистити плей лист
        ClearPlayList()
        # 2. Додати файли з папки в плейлист
        AddPlayList(NamePlayList)
        # 3. Запустити програвач
        ShufflePlayList()
        PlayPlayList()


if __name__=="__main__" :
    main()
