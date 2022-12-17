class User:
    def __init__(self, id: int, group: str, status: str):
        self.__id = id
        self.__group = group
        self.__status = status
        self.__name = None
        self._sorename = None

    def get_id(self):
        return self.__id

    def get_group(self):
        return self.__group

    def get_status(self):
        return self.__status
