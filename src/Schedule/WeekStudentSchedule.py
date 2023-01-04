class StudentWeekSchedule:
    def __init__(self, daysScheduleList: list):
        self.daysScheduleList = daysScheduleList
        self.schedule_str = str()

    def get_today_schedule(self):
        pass

    def get_week_schedule(self) -> str:
        for daySchedule in self.daysScheduleList:
            self.schedule_str += str(daySchedule.weekday)

            for less in daySchedule.lessonsList:
                self.schedule_str += str(less)

            self.schedule_str += '\n'

        return self.schedule_str


    def __str__(self):
        for day in self.daysScheduleList:
            self.schedule_str += str(day)
            self.schedule_str += '\n'

        return self.schedule_str
