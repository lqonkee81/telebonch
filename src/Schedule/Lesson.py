class Lesson:
    def __init__(self, name: str, number: str, time: str, audienceNumber: str, proffesorName: str, type: str):
        self.name = name
        self.number = number
        self.time = time
        self.audienceNumber = audienceNumber
        self.proffesorName = proffesorName
        self.type = type

    def __format_audinceNumber(self):
        """
        Форматирует номер аудитории полученный с парсера
        """

        if any([
            self.audienceNumber == "ауд.: Спортивные площадки",
            self.audienceNumber == "ауд.: ДОТ"
        ]):
            self.audienceNumber = self.audienceNumber[6::]
        else:
            self.audienceNumber = self.audienceNumber[6:8:] + self.audienceNumber[13::]
            self.audienceNumber = "Аудитория: " + self.audienceNumber[:3:] + '\n' + "Корпус: " + self.audienceNumber[-1]

    def __str__(self) -> str:
        self.__format_audinceNumber()

        return f"<b>{self.number}. {self.name}</b>\n" \
               f"{self.type}\n" \
               f"{self.time}\n" \
               f"<em>{self.audienceNumber}</em>\n" \
               f"{self.proffesorName}\n"
