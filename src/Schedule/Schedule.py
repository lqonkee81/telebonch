class Schedule:
    def __init__(self, lessonsList: list):
        self.lessonslist = lessonsList
        self.schedule_str = str()

        for lesson in self.lessonslist:
            self.schedule_str += (str(lesson) + '\n')

    def get_today_schedule(self):
        pass

    def get_week_schedule(self) -> str:
        return self.schedule_str
