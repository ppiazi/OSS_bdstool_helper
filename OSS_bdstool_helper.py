# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import csv

COMMAND_STR="""
cd %s &
call bdstool new-project %s --verbose &
call bdstool analyze --force –-verbose &
call bdstool upload
"""

class OSS_bdstool_helper:
    def __init__(self, worker_number):
        self.conf_dict = {}
        self.max_worker = worker_number

    def loadConf(self, file_name):
        """
        project_id, folder 형식의 파일을 읽는다.
        :param file_name:
        :return: error_code
        """
        try:
            csv_file = open(file_name, "r", encoding='UTF8')
        except:
            print("Load file %s error" % (file_name))
            return -1

        csv_reader = csv.reader(csv_file, delimiter=',')

        cnt = 0
        for data in csv_reader:
            self.conf_dict[data[0]] = data[1].strip()
            print("%s / %s" % (data[0], self.conf_dict[data[0]]))
            cnt = cnt + 1

        print("Total %d configuration read." % (cnt))

    def execute(self):
        if len(self.conf_dict) == 0:
            return -1
        
        for c_project_id in self.conf_dict.keys():
            print("Start to analyze %s at %s" % (c_project_id, self.conf_dict[c_project_id]))
            bdstool_cmd = COMMAND_STR % (c_project_id, self.conf_dict[c_project_id])
            process = subprocess.Popen(bdstool_cmd, stdout=subprocess.PIPE, shell=True)
            proc_stdout = process.communicate()[0].strip()
            print(proc_stdout)
            process.close()


def printUsage():
    print("OSS_bdstool_helper.py [csv file] [the number of simultaneous workers, Maximum 4]")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        printUsage()
        os._exit(1)

    conf_file = sys.argv[1]
    try:
        t = int(sys.argv[2])
    except:
        t = 1
    if t > 4:
        t = 4

    nWorker = t
    worker = OSS_bdstool_helper(nWorker)

    worker.loadConf(conf_file)
    worker.execute()

