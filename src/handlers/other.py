from aiogram import Dispatcher, types


# Unknown commands handler
# @DP.message_handler()
async def remove_empty_mesaage(message: types.Message) -> None:
    """
    Удаляет сообщения с рандомным текстом ( рандомный текст - все что не специальная команда бота)
    """
    # await message.delete()
    await message.delete()


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(remove_empty_mesaage)
