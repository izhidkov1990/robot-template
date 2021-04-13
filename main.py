from queue import Queue

from process import Process
import config
import logger
import data
import error_handler
from error_handler import Error
from end import EndTransaction

LOG_PATH = r'log.log'
CONFIG_PATH = r'config.xlsx'
MODE = 'Test'  # Test or Prod mode


class Robot:

    """RPA Standard Template"""

    def __init__(self):
        self.config = config.read(CONFIG_PATH, MODE)
        self.logger = logger.Logger(self.config['robot_name'], LOG_PATH)

        self.process = Process(self.config, self.logger)
        self.queue = Queue()  # Job queue for the robot
        self.error = Error(self.config, self.logger)
        self.end = EndTransaction()

        self.status = None

        self.error_count = self.config['error_count']


    def get_data(self):  

        """Get transactions and add to Queue"""
        
        try:
            self.logger.info('Get transactions...')
            # Get transaction
            transaction_items = data.get() 
            # Add to queue
            for item in transaction_items:
                self.queue.put(item)            
        except Exception as err:
            raise error_handler.GetDataError('Error while getting data: {}'.format(err))
 
    def run(self):

        """Robot start"""
        
        self.get_data()

        while not self.queue.empty() and self. error_count != 0:    
            transaction_item = self.queue.get()
            try:            
                self.process.start_processing(transaction_item)
                self.status = 'Success'

            except error_handler.BusinessError as business_error:                
                self.status = 'Business error'
                self.error.handler(business_error, transaction_item)                
                
            except error_handler.TransactionError as transaction_error:
                self.error_count -= 1
                self.status = 'Error'
                self.error.handler(transaction_error, transaction_item)
                
            except Exception as err:
                self.error_count -= 1
                raise Exception('Unknown error: {}'.format(err))

            finally:
                self.end.finish(transaction_item)

            if self.error_count == 0:
                raise error_handler.ExceptionCountError('The number of unsuccessful attempts is more than {}. The robot is terminated'.format(self.config['error_count']))
    
    
if __name__ == '__main__':
    robot = Robot()
    robot.run()
