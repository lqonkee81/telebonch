class Lesson:
    def __init__(self, name: str, time: str, audienceNumber: str, proffesorName: str, type: str):
        self.name = name
        self.time = time
        self.audienceNumber = audienceNumber
        self.proffesorName = proffesorName
        self.type = type

    def is_full(self) -> bool:
        if any([
            self.name == '',
            self.time == '',
            self.audienceNumber == '',
            self.proffesorName == '',
            self.type == ''
        ]):
            return False

        return True

    def __str__(self) -> str:
        return f"{self.name}\n{self.type}\n{self.time}\n{self.audienceNumber}\n{self.proffesorName}\n"
