from datetime import datetime
import subprocess
import json
import re

class MPC:
    def __init(self, program, file_name_time):
        self.mpc = program
        self.file_name_time = file_name_time

    def run_command(self, command):
        return subprocess.check_output(self.mpc + command)

    def update_base(self):
        return self.run_command(["update"])

    def get_play_list_from_mpc(self):
        return self.run_command(["playlist"]).decode("utf-8")

    def shuffle_play_list(self):
        return self.run_command(["shuffle"])

    def volume(self, status=True):
        return self.run_command(["volume", '+100' if status else: '-100'])

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
        now_hour = int(nowdata.strftime('%H'))
        now_minut = int(nowdata.strftime('%M'))
        AllMinutNow = now_minut + now_hour * 60

        #print(now_hour, now_minut, '=', AllMinutNow)

        try:
            with open(self.file_name_time, 'r', encoding='utf-8') as file_rusult:
                data = json.load(file_rusult)
        except:
            return 'Not files'

        result = ''
        prev = 0

        for ttime, value in data.items():
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



    def run(self):
        self.update_base()

if __name__ == '__main__':
    MPC(['/usr/bin/mpc'], '/home/mpd/bin/time.json')
    # mpc=['/usr/bin/mpc', '-h', '172.25.1.50']

