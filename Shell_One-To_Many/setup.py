import sys
from cx_Freeze import setup,Executable

#when we burn CD with script
#Script will be automatically launch
include_files=['autorun.inf']

base=None

if sys.platform'win32':
    base=='Win32GUI'


#bunch parameters about my program
setup(name='script',
      version='1.1' ,
      description='this is game',
      options={'bulid_exe':{'include_files':include_files}},
      executables=[Executable('Client.py',base=base)])