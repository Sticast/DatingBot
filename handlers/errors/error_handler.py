from aiogram.utils.exceptions import (
    Unauthorized,
    InvalidQueryID,
    TelegramAPIError,
    CantDemoteChatCreator,
    MessageNotModified,
    MessageToDeleteNotFound,
    MessageTextIsEmpty,
    RetryAfter,
    CantParseEntities,
    MessageCantBeDeleted
)

from loader import dp


@dp.errors_handler()
async def errors_handler(update, exception):
    if isinstance(exception, CantDemoteChatCreator):
        return True

    elif isinstance(exception, MessageNotModified):
        return True
    elif isinstance(exception, MessageCantBeDeleted):
        return True

    elif isinstance(exception, MessageToDeleteNotFound):
        return True

    elif isinstance(exception, MessageTextIsEmpty):
        return True

    elif isinstance(exception, Unauthorized):
        return True

    elif isinstance(exception, InvalidQueryID):
        return True

    elif isinstance(exception, TelegramAPIError):
        return True
    elif isinstance(exception, RetryAfter):
        return True
    elif isinstance(exception, CantParseEntities):
        return True
