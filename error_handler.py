from outlook import Outlook
from logger import Logger
import config

from mss import mss
import shutil
import os
from datetime import datetime
from data import Transaction
    

def send_exception_notification(self, **kwargs) -> None:
    outlook = Outlook()
    outlook.send_mail(to=kwargs['to'], subject='Ошибка в роботе {}.'.format(kwargs['robot_name']), html_body=kwargs['message'])

def take_screenshot(filename: str=None) -> None:

    """ Функция делает скриншонт экрана и перемещает скрин в папку 'err_screenshots'.
        Если папки нету - создает ее в директории робота """

    if filename:
        new_path = r'err_screenshots' + '\\' + datetime.now().strftime("%d_%m_%Y %H%M%S") + ' ' + filename + '.png'
    else:
        new_path = r'err_screenshots' + '\\' + datetime.now().strftime("%d_%m_%Y %H%M%S") + ' ' + 'unnamed' + '.png'
    with mss() as sct:
        screen = sct.shot() #  screen - путь к скрину
        if os.path.exists(r'err_screenshots'):
            shutil.move(screen, new_path)
        else:
            os.mkdir('err_screenshots')
            shutil.move(screen, new_path)


class Error:

    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

        self.txt = None
        self.transaction = None

    def handler(self, exception: Exception, transaction: Transaction):

        """Обработчик исключения"""

        self.txt = exception.txt
        self.transaction = transaction
        self.print_log()

        if isinstance(exception, BusinessError):
            pass
        elif isinstance(exception, TransactionError):
            pass
        elif isinstance(exception, GetDataError):
            pass
        self.print_log()
              
    def print_log(self):
        self.logger.error('Произошла {0}'.format(self.txt.lower()))
            

class BusinessError(Exception):
    def __init__(self, transaction, text=None):
        if text:
            self.txt = text
        self.transactio = transaction

    # TODO BusinessErrorHandler


class TransactionError(Exception):
    def __init__(self, text, transaction):
        self.txt = text
        self.transactio = transaction

    # TODO TransactionErrorHandler


class GetDataError(Exception):
    def __init__(self, text):
        self.txt = text

    # TODO GetDataErrorHandler


class ExceptionCountError(Exception):
    def __init__(self, text):
        self.txt = text