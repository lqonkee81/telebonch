"""
profesor - Обработчик сообщений от преподавателя
student - Обработчик сообщений от студента
handman - Обработчик сообщений от старосты
other - Обработчик неожидаемых сообщений

registration - Машина состояний для регистрации пользователя
"""

from handlers import handman
from handlers import other
from handlers import profesor
from handlers import student

from handlers import registration
