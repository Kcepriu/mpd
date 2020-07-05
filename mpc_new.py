from datetime import datetime
import subprocess
import json
import re

class MPC:
    def __init__(self, program, file_name_time, debug=False):
        self.mpc = program
        self.file_name_time = file_name_time
        self.tmp_dir = '/tmp'
        self.debug = debug

    def run_command(self, command):
        result = subprocess.check_output(self.mpc + command)
        if self.debug:
            print(command)
            print(result)
        return result

    def update_base(self):
        return self.run_command(["update"])

    def get_play_list_from_mpc(self):
        return self.run_command(["playlist"]).decode("utf-8")

    def shuffle_play_list(self):
        return self.run_command(["shuffle"])

    def volume(self, status=True):
        return self.run_command(["volume", '+100' if status else '-100'])

    def ls_mpc(self):
        return self.run_command(["ls"]).decode("utf-8")

    def play_play_list(self):
        self.run_command(["play"])
        self.run_command(["random", "off"])
        self.run_command(["repeat", "on"])
        self.volume()

    def add_play_list(self, name_play_list):
        self.run_command(["add", name_play_list])
        self.run_command(["save", name_play_list])

    def clear_play_list(self):
        # Очистимо список збережених
        play_lists_str = self.run_command(["lsplaylists"]).decode("utf-8")

        if play_lists_str:
            for play_list in play_lists_str.split('\n'):
                play_list = play_list.replace('\r', '')
                if play_list:
                    #print('clear', Playlist)
                    self.run_command(["rm", play_list])

        # Видалимо файли з поточного
        self.run_command(["clear"])

    def get_play_list_from_file(self):
        nowdata = datetime.today()
        weec_day = str(datetime.today().isoweekday())
        now_hour = int(nowdata.strftime('%H'))
        now_minut = int(nowdata.strftime('%M'))
        AllMinutNow = now_minut + now_hour * 60

        # print(now_hour, now_minut, '=', AllMinutNow)

        try:
            with open(self.file_name_time, 'r', encoding='utf-8') as file_rusult:
                data = json.load(file_rusult)
                # print(data)
        except:
            return 'Not files'

        for key in data.keys():
            if weec_day in key:
                dic_time = data[key]
                break
        else:
            dic_time = data[list(data.keys())[0]]

        result = ''
        prev = 0

        for ttime, value in dic_time.items():
            hour, minute = ttime.split(':')
            AllMinut = int(minute) + int(hour) * 60
            # print(hour, minute, '=', AllMinut, value)

            if AllMinut <= AllMinutNow and prev <= int(AllMinut):
                prev = int(AllMinut)
                result = value
        # print(hour, minute, '=', AllMinut, value)

        return result

    def status_mpc(self):
        output = self.run_command(["status"]).decode("utf-8").split('\n')
        if len(output) <= 2:
            return "stop"
        status = re.findall(r'\[(.*)\]', output[1])[0]
        return status

    def update_play_list(self, name_play_list, play_list_mpc):
        all_files_str = self.run_command(["listall", name_play_list]).decode("utf-8")
        return (len(all_files_str.split('\n')) != len(play_list_mpc.split('\n')))

    def get_name_curent_play_list(self):
        play_lists_str = self.run_command(["lsplaylists"]).decode("utf-8")
        if play_lists_str:
            return play_lists_str.split('\n')[0].replace('\r', '')
        return ''

    def log_play_lists(self):
        name_curent_play_list = self.get_name_curent_play_list()
        now_hour = datetime.today().strftime('%H_%M')
        filename = self.tmp_dir+'/' + name_curent_play_list + '_' + now_hour + '.log'

        play_lists_str = self.run_command(["playlist"]).decode("utf-8")

        with open(filename, 'w', encoding='utf-8') as file_rusult:
            file_rusult.write(play_lists_str)

    def log_play_lists_name(self):
        now_hour = datetime.today().strftime('%Y_%m_%d_%H_%M')
        filename = '/tmp/mpd_play.log'

        play_lists_str = self.run_command([]).decode("utf-8")

        name_song = ""
        nom_song = ""
        if play_lists_str:
            name_song = play_lists_str.split('\n')[0].replace('\r', '')
            nom_song = play_lists_str.split('\n')[1].replace('\r', '')

        with open(filename, 'a', encoding='utf-8') as file_rusult:
            file_rusult.write(now_hour + ':' + name_song + ":" + nom_song + "\n")

    def run(self):
        self.update_base()


        name_play_list = self.get_play_list_from_file()
        play_lists_mpc = self.get_play_list_from_mpc()
        name_curent_play_list = self.get_name_curent_play_list()
        dir_name = self.ls_mpc()

        # print('name_play_list:', name_play_list)

        if dir_name.find(name_play_list) == -1:
            # print("Not find dir "+NamePlayList)
            return

        update = self.update_play_list(name_play_list, play_lists_mpc)

        # ---------------------------------------------------------
        # if Update:
        #    print('update')
        if self.debug:
            print(name_curent_play_list)
            print(name_play_list)

        self.log_play_lists_name()

        # if PlayListMPC.find(NamePlayList+".mp3")>-1 and not Update:
        if name_curent_play_list == name_play_list and not update:
            # 1. перевірити що зараз грає
            status = self.status_mpc()
            # 2. Якщо не грає, то запустити
            if status != 'playing':
                self.play_play_list()
        else:
            self.volume(False)
            # 1. Очистити плей лист
            self.clear_play_list()

            # 2. Додати файли з папки в плейлист
            self.add_play_list(name_play_list)

            # 3. Запустити програвач
            self.shuffle_play_list()
            self.play_play_list()
            self.log_play_lists()

    def test(self):
        name_play_list = self.get_play_list_from_file()
        print(name_play_list)

if __name__ == '__main__':
    # mpc = MPC(['/usr/bin/mpc'], '/home/mpd/bin/time.json')
    mpc = MPC(['/usr/bin/mpc'], '/home/segiy/PycharmProjects/mpc/time.json', debug=False)
    mpc.run()
    # mpc.test()

    # mpc=['/usr/bin/mpc', '-h', '172.25.1.50']

