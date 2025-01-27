from typing import Optional

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.exceptions import BadRequest

from keyboards.inline.questionnaires_inline import (
    questionnaires_keyboard,
    reciprocity_keyboard
)
from loader import bot, _
from loader import logger
from utils.db_api import db_commands


async def send_questionnaire(
        chat_id: int,
        owner_id: Optional[int] = None,
        markup: Optional[InlineKeyboardMarkup] = None,
        add_text: Optional[str] = None,
        monitoring: bool = False,
        report_system: bool = False
) -> None:
    user = await db_commands.select_user(owner_id)
    text_template = _("{}, {} лет, {} {verification}\n\n")
    user_verification = "✅" if user["verification"] else ""

    text_without_inst = _(text_template + "{commentary}").format(
        user.get("varname"),
        user.get("age"),
        user.get("city"),
        commentary=user.get("commentary"),
        verification=user_verification
    )

    text_with_inst_template = text_template + _("<b>Инстаграм</b> - <code>{instagram}</code>\n")
    text_with_inst = _(text_with_inst_template).format(
        user.get("varname"),
        user.get("age"),
        user.get("city"),
        user.get("commentary"),
        verification=user_verification,
        instagram=user.get("instagram")
    )

    caption_with_add_text = _("{}\n\n" + text_template + "{}").format(
        add_text,
        user.get("varname"),
        user.get("age"),
        user.get("city"),
        user.get("commentary"),
        verification=user_verification
    )

    add_text_with_inst = _("{}\n\n" + text_template +
                           "<b>Инстаграм</b> - <code>{instagram}</code>\n").format(
        add_text,
        user.get("varname"),
        user.get("age"),
        user.get("city"),
        user.get("commentary"),
        verification=user_verification,
        instagram=user.get("instagram")
    )
    try:
        if add_text is None and user.get("instagram") is None:
            await bot.send_photo(
                chat_id=chat_id,
                caption=text_without_inst,
                photo=user.get("photo_id"),
                reply_markup=await questionnaires_keyboard(
                    target_id=owner_id,
                    monitoring=monitoring
                )
            )
        elif add_text is None:
            await bot.send_photo(
                chat_id=chat_id,
                caption=text_with_inst,
                photo=user.get("photo_id"),
                reply_markup=await questionnaires_keyboard(
                    target_id=owner_id,
                    monitoring=monitoring
                )
            )
        elif markup is None and user.get("instagram") is None:
            await bot.send_photo(
                chat_id=chat_id,
                caption=caption_with_add_text,
                photo=user.get("photo_id")
            )
        elif markup is None:
            await bot.send_photo(
                chat_id=chat_id,
                caption=add_text_with_inst,
                photo=user.get("photo_id")
            )

        elif user.get("instagram") is None:
            await bot.send_photo(
                chat_id=chat_id,
                caption=caption_with_add_text,
                photo=user.get("photo_id"),
                reply_markup=await reciprocity_keyboard(user_for_like=owner_id)
            )
        elif report_system:
            await bot.send_photo(
                chat_id=chat_id,
                caption=add_text,
                photo=user.get("photo_id"),
            )
        else:
            await bot.send_photo(
                chat_id=chat_id,
                caption=add_text_with_inst,
                photo=user.get("photo_id"),
                reply_markup=await reciprocity_keyboard(user_for_like=owner_id)
            )
    except BadRequest as err:
        logger.info(f"{err}. Error in the send_questionnaire function")
