class Lesson:
    def __init__(self, date: str, name: str, time: str, audienceNumber: int, proffesorName: str, type: str):
        self.date = date
        self.name = name
        self.time = time
        self.audienceNumber = audienceNumber
        self.proffesorName = proffesorName
        self.type = type

    def __str__(self):
        return f"{self.date}\n{self.name}\n{self.type}\n{self.time}\n{self.audienceNumber}\n{self.proffesorName}"


if __name__ == "__main__":
    les = Lesson(date="27.10.2022",
                 name="Para",
                 time="9:00-10:35",
                 audienceNumber="239",
                 proffesorName="Kekov Petrusha",
                 type="leks")

    print(les.date)
