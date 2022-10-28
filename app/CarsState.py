ATTEMPTS_THRESHOLD = 5
import os
import logging.config

PATH = os.getcwd()
log_file_path = f"{PATH}/app/logger.conf"
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)


class CarState:

    def __init__(self):
        self.count = 0
        self.__change_attempts = 0
        self.__change_candidate = -1
        self.logger = logging.getLogger("__name__")

    def update_count(self, num):

        if num == self.count:
            return

        if self.__change_attempts > ATTEMPTS_THRESHOLD:
            self.__change_attempts = 0
            self.__change_candidate = -1

            self.count = num
            return True

        if num != self.count:
            self.logger.info(f"attempts :{self.__change_attempts} amout of cars {num} current state :{self.count} ")
            self.__change_candidate = num
            self.__change_attempts += 1

        return self.count
