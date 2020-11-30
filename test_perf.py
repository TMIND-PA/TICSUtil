
import timeit 

############ Perf Test for Logging ###################
# code snippet to be executed only once  
mysetup = '''
from TICSUtil import TICSLogger
Logger = TICSLogger()
Logger.console_dbglevel("info")
Logger.file_dbglevel("debug")
Log = Logger.get_log
'''
  
# code snippet whose execution time is to be measured  
mycode = '''  
Log.debug("I")
'''
  
# timeit statement  
exec_time = timeit.timeit(setup = mysetup, stmt = mycode, number = 10000) 
print(f"Perf Test Execution time: {exec_time} secs")