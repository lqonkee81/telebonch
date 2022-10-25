from aiogram import Dispatcher, types


# Unknown commands handler
# @DP.message_handler()
async def echo(message: types.Message) -> None:
    """
    Удаляет сообщения с рандомным текстом ( рандомный текст - все что не специальная команда бота)
    """
    # await message.delete()
    await message.answer(text=message.text)


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(echo)
