from TICSUtil import log_time, TICSLogger, emoji

# print(log_time(), "Starting test script...")

# Old Method
# Logger = TICSLogger()
# Log = Logger.get_log
# Log.info(f'Logger Configured...')
# Log.log(50 , f'Sample LOG message')
# Log.debug(f'Sample DEBUG message')
# Log.info(f'Sample INFO message')
# Log.warning(f'Sample WARNING message')
# Log.critical(f'Sample CRITICAL message')
# Log.info(emoji["namaste"])

# New Method
# Logger = TICSLogger(filename="testlog.log", dir="./logs")
Logger = TICSLogger()
Log = Logger.get_log
Log.info(f'Logger Configured...')
Log.log(50 , f'Sample LOG message')
Log.debug(f'Sample DEBUG message')
Log.info(f'Sample INFO message')
Log.warning(f'Sample WARNING message')
Log.critical(f'Sample CRITICAL message')
Log.info(emoji["namaste"])


try:
    a = 1/0
except Exception as e:
    Log.error(f'Sample ERROR message. Error: {e}')

    #Exception type log requires exception object to display. Uncomment below line to test exception message
    # Log.exception(f'Sample EXCEPTION message. Exception: {e}')        


class TestClass:
    def __init__(self):
        Log.info(f'TestClass Initialized')

    def test_func(self):
        Log.info(f'Inside Test Func')


test1 = TestClass()
test1.test_func()