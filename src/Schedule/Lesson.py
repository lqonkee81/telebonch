class Lesson:
    def __init__(self, name: str, number: str, time: str, audienceNumber: str, proffesorName: str, type: str):
        self.name = name
        self.number = number
        self.time = time
        self.audienceNumber = audienceNumber
        print("__init__", self.audienceNumber)
        self.proffesorName = proffesorName
        self.type = type

    def __format_audinceNumber(self):
        """
        Форматирует номер аудитории полученный с парсера
        """

        # if (str(self.audienceNumber) == "ауд.: Спортивные площадки") or (str(self.audienceNumber) == "ауд.: ДОТ"):
        #     self.audienceNumber = self.audienceNumber[6::]

        if any([
                    self.audienceNumber == "ауд.: Спортивные площадки",
                    self.audienceNumber == "ауд.: ДОТ"
                ]):
            self.audienceNumber = self.audienceNumber[6::]

        else:
            self.audienceNumber = self.audienceNumber[6:9:] + self.audienceNumber[15::]
            self.audienceNumber = "Аудитория: " + self.audienceNumber[:3:] + '\n' \
                                + "Корпус: " + self.audienceNumber[-1]

    def is_empty(self):
        if any([
            self.name == "" or self.name is None,
            self.audienceNumber == "" or self.audienceNumber is None,
            self.type == "" or self.type is None,
            self.time == "" or self.time is None,
            self.number == "" or self.number is None,
            self.proffesorName == "" or self.proffesorName is None
        ]):
            return True
        else:
            return False

    def __str__(self) -> str:
        self.__format_audinceNumber()

        return f"<b>{self.number}. {self.name}</b>\n" \
               f"{self.type}\n" \
               f"{self.time}\n" \
               f"<em>{self.audienceNumber}</em>\n" \
               f"{self.proffesorName}\n"
