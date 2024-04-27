#!/usr/bin/pythonw

import sys
import os
from os.path import isfile, join
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
        self.max_saves = num_saves
        
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
            
    def getSaveFiles(self):
        return [f for f in os.listdir(self.save_dir) if isfile(join(self.save_dir, f))]
            
    def purgeOldestSave(self):
        savefiles = self.getSaveFiles() # List of all files in save directory
        if len(savefiles) > self.max_saves:
            print("Maximum number of saves exceeded, purging oldest")
            
            oldest_time = datetime.datetime.fromtimestamp(os.path.getmtime(savefiles[0])) # Search value
            oldest_index = 0 # Search value
            
            for f in savefiles:
                time = datetime.datetime.fromtimestamp(os.path.getmtime(f))
                if time < oldest_time:
                    oldest_time = time
                    oldest_index = savefiles.index(f)
             
            oldest_save = savefiles[oldest_index] # Oldest directory
            
            # Purge the oldest save
            os.remove(oldest_save)
            
            # Double check and ensure that we actually are at an acceptable number of backup saves.
            # If we're still over the limit, recursively delete the oldest file until we are ok.
            
            if len(self.getSaveFiles()) > self.max_saves:
                self.purgeOldestSave()
            else:
                print("Number of saves within limit.")
            
    def createBackupName(self):
        # Create the name of the backup zip
        
        # Get the date and time in log form to append
        date_string = f'{datetime.datetime.utcnow():%Y%m%d_%H%M%S}' # Log string
        zip_name = self.name+date_string+".zip"
        
        return zip_name
        
    def backup(self):
        print("Starting backup...")
        zipname = self.createBackupName() # Create the name of the zip file
        
        self.setSavePathDir() # Set ourselves in the content path
        shutil.make_archive(zipname, 'zip', self.content_dir)
        print("Backup successfully created at "+str(datetime.datetime.utcnow()))
    
    def checkTimeAndBackup(self):
        current_time = time.time()
        t = current_time - self.start_time
        if (t >= self.period):
            print("Reached backup time.")
            self.backup()
            print("Reseting timer.")
            self.start_time = current_time




