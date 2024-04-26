#!/usr/bin/pythonw

import sys
import os
import time
import shutil
import datetime

DEFAULT_BACKUP_PERIOD = 8 * 3600 # This is the default time in seconds for backing up
DEFAULT_NUM_SAVES = 10

class BackupState(object):
    
    def __init__(self, save_dir, content_dir, name='world', period=DEFAULT_BACKUP_PERIOD, num_saves=DEFAULT_NUM_SAVES):
        self.name = name # The name of the world you are backing up
        self.save_dir = str(save_dir)
        self.content_dir = str(content_dir)
        self.period = period
        self.num_saves = num_saves
        
        self.start_time = time.time()
        
    def setSavePathDir(self):
        print("Attempting to set working directory to save path...")
        try:
            os.chdir(self.save_dir)
            print("Loaded save path ok.")
        except:
            print("ERROR: Save Path does not exist")
            print("Making dirrectory!!!")
            os.makedirs(self.save_dir, exist_ok = True)
            os.chdir(self.save_dir)
            print("Loaded save path ok.")
            
    def setContentPath(self):
        print("Attempting to load content path...")
        try:
            os.chdir(self.content_path)
            print("Loaded content path ok.")
        except:
            print("ERROR: content path does not exist.")
            
    def createBackupName(self):
        # Create the name of the backup zip
        
        # Get the date and time in log form to append
        date_string = f'{datetime.datetime.utcnow():%Y%m%d_%H%M%S}' # Log string
        zip_name = self.name+date_string+".zip"
        
        return zip_name
        
    def backup(self):
        zipname = self.createBackupName() # Create the name of the zip file
        
        self.setSavePathDir() # Set ourselves in the content path
        shutil.make_archive(zipname, 'zip', self.content_dir)
    
    def checkTimeAndBackup(self):
        current_time = time.time()
        t = current_time - self.start_time
        if (t >= self.period):
            self.start_time = current_time
            self.backup()




