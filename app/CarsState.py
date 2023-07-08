ATTEMPTS_THRESHOLD = 100
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
        self.logger = logging.getLogger("CarsState_")

    def update_count(self, num):

        if num == self.count:
            # self.logger.info(f"skipped update count {num} is the sane as current count")
            self.__change_attempts = 0
            return

        if self.__change_attempts > ATTEMPTS_THRESHOLD:
            self.__change_attempts = 0
            self.__change_candidate = -1

            self.count = num
            return True

        if num != self.__change_candidate:
            self.__change_attempts = 0

        if num != self.count:
            if self.__change_attempts > 9 and self.__change_attempts % 10 == 0 :
                self.logger.debug(f"attempts :{self.__change_attempts} amout of cars {num} current state :{self.count} ")
            self.__change_candidate = num
            self.__change_attempts += 1

        return self.count
