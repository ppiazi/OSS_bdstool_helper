# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import csv
import datetime
import logging
import logging.handlers

# Windows Shell Command to analyze with bdstool. Take 2 arguments(project path & project id)
COMMAND_STR="""pushd %s & call bdstool new-project %s & call bdstool analyze --all-files --verbose & call bdstool upload & popd"""

class OSS_bdstool_helper:
    def __init__(self, worker_number):
        self.conf_dict = {}
        self.max_worker = worker_number
        self.logger = logging.getLogger("OSS_bdstool_helper")

    def loadConf(self, file_name):
        """
        project_id, folder 형식의 파일을 읽는다.
        :param file_name:
        :return: error_code
        """
        self.file_name = file_name
        self.file_logger = logging.FileHandler(filename=self.file_name + ".log")
        self.stdout_logger = logging.StreamHandler()

        self.logger.addHandler(self.file_logger)
        self.logger.addHandler(self.stdout_logger)

        self.logger.setLevel(logging.DEBUG)

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
            self.logger.info("(%s) Start to analyze %s at %s" % (datetime.datetime.now().ctime(), c_project_id, self.conf_dict[c_project_id]))
            bdstool_cmd = COMMAND_STR % (self.conf_dict[c_project_id], c_project_id)
            self.logger.info(bdstool_cmd)
            process = subprocess.Popen(bdstool_cmd, stdout=subprocess.PIPE, shell=True)
            t_str = process.communicate()[0].strip()
            self.logger.info(t_str.decode('cp949'))

def printUsage():
    print("OSS_bdstool_helper.py [csv file]")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        printUsage()
        os._exit(1)

    conf_file = sys.argv[1]

    nWorker = 1
    worker = OSS_bdstool_helper(nWorker)

    worker.loadConf(conf_file)
    worker.execute()

