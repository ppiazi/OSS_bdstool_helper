# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import csv

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
            csv_file = open(file_name, "r")
        except:
            print("Load file %s error" % (file_name))
            return -1

        csv_reader = csv.reader(csv_file, delimiter=',')

        cnt = 0
        for data in csv_reader:
            self.conf_dict[data[0]] = data[1].strip()
            print("%s / %s" % (data[0], data[1]))
            cnt = cnt + 1

        print("Total %d configuration read." % (cnt))

    def execute(self):
        if len(self.conf_dict) == 0:
            return -1
        pass

def printUsage():
    print("OSS_bdstool_helper.py [csv file] [the number of simultaneous workers, Maximum 4]")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        printUsage()
        os.exit(1)

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

