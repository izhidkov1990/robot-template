import error_handler


"""Обработка транзакции"""


class Process:

    def __init__(self, config: dict, logger):
        self.config = config
        self.logger = logger       

    def start_processing(self, transactionItem):
        #  Проверка входных данных
        # transactionItem
        if True == False:
            try:
                self.logger.info('Начало обработки транзакции {}'.format(transactionItem.add_info1))

                # TODO Обработчик транзакции
                print('Обработка ' + str(transactionItem.add_info1))

                self.logger.info('Обработка транзакции {} завершена'.format(transactionItem.add_info1))                
            except Exception as err:
                # Ошибка при обработке транзации
                raise error_handler.TransactionError('Ошибка при проведении транзакции: {0}'.format(err), transactionItem) 
        else:
            # Ошибка в бизнесс логике
            raise error_handler.BusinessError('Ошибка при проверке данных в транзакции', transactionItem)
                       
                
        
