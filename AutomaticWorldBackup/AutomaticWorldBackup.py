#!/usr/bin/pythonw

import sys
import os
import time
import configparser

from BackupState import BackupState


CONFIG_FILE = "config.ini" # Default config file

def loadConfig(cfg_file):
    config = configparser.ConfigParser()
    config.read(cfg_file)
    
    period = int(config.get('General', 'period'))
    save_dir = config.get('General', 'save_dir')
    content_dir = config.get('General', 'content_dir')
    name = config.get('General', 'name')
    num_saves = int(config.get('General', 'num_saves'))
    
    return_data = {'period': period,
                   'save_dir': save_dir,
                   'content_dir': content_dir,
                   'name': name,
                   'num_saves': num_saves}
    
    return return_data

def main():
    print(f"Setting Working Directory...")
    current_dir = os.getcwd()
    print(f"Current Directory is: ",current_dir)
    
    # Retrieve our config values
    cfg = loadConfig(CONFIG_FILE)
    print("Config loaded.")
    
    # Create our backupstate
    backupState = BackupState(cfg['save_dir'], cfg['content_dir'], cfg['name'], int(cfg['period']))
    
    print("Backupstate Succesfully Initialized.")
    
    backupState.backup()
    
    print("Successfully backed up once.")
    
if __name__ == '__main__':
    main()
