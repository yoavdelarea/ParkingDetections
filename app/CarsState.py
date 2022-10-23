ATTEMPTS_THRESHOLD = 3


class CarState:

    def __init__(self):
        self.count = 0
        self.__change_attempts = 0
        self.__change_candidate = -1
        self.__last_cars_amount = -1

    def update_count(self, num):

        if num == self.count or num == self.__last_cars_amount:
            return

        if self.__change_attempts > ATTEMPTS_THRESHOLD:
            self.__change_attempts = 0
            self.__change_candidate = -1
            if num == self.__last_cars_amount:
                return False
            self.count = num
            return True

        if num != self.count:
            self.__change_candidate = num
            self.__change_attempts += 1

        return self.count
