import os

from pyrogram import filters
from pyrogram import Client as trojanz
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

from script import Script


@trojanz.on_message(filters.command(["start"]) & filters.private)
async def start(client, message):
    await message.reply_text(
        text=Script.START_MSG.format(message.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("HELP", callback_data="help_data"),
                    InlineKeyboardButton("ABOUT", callback_data="about_data"),
                ],
                [
                    InlineKeyboardButton(
                        "⭕️ JOIN OUR CHANNEL ⭕️", url="https://t.me/TroJanzHEX")
                ]
            ]
        ),
        reply_to_message_id=message.message_id
    )


@trojanz.on_message(filters.command(["help"]) & filters.private)
async def help(client, message):
    await message.reply_text(
        text=Script.HELP_MSG,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("BACK", callback_data="start_data"),
                    InlineKeyboardButton("ABOUT", callback_data="about_data"),
                ],
                [
                    InlineKeyboardButton(
                        "⭕️ SUPPORT ⭕️", url="https://t.me/TroJanzSupport")
                ]
            ]
        ),
        reply_to_message_id=message.message_id
    )


@trojanz.on_message(filters.command(["about"]) & filters.private)
async def about(client, message):
    await message.reply_text(
        text=Script.ABOUT_MSG,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("BACK", callback_data="help_data"),
                    InlineKeyboardButton("START", callback_data="start_data"),
                ],
                [
                    InlineKeyboardButton(
                        "SOURCE CODE", url="https://github.com/TroJanzHEX/Unlimited-Filter-Bot")
                ]
            ]
        ),
        reply_to_message_id=message.message_id
    )



@trojanz.on_callback_query()
async def cb_handler(client, query):

    if query.data == "start_data":
        await query.answer()
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("HELP", callback_data="help_data"),
                InlineKeyboardButton("ABOUT", callback_data="about_data")],
            [InlineKeyboardButton("⭕️ JOIN OUR CHANNEL ⭕️", url="https://t.me/TroJanzHEX")]
        ])

        await query.message.edit_text(
            Script.START_MSG.format(query.from_user.mention),
            reply_markup=keyboard,
            disable_web_page_preview=True
        )
        return


    elif query.data == "help_data":
        await query.answer()
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("BACK", callback_data="start_data"),
                InlineKeyboardButton("ABOUT", callback_data="about_data")],
            [InlineKeyboardButton("⭕️ SUPPORT ⭕️", url="https://t.me/TroJanzSupport")]
        ])

        await query.message.edit_text(
            Script.HELP_MSG,
            reply_markup=keyboard,
            disable_web_page_preview=True
        )
        return


    elif query.data == "about_data":
        await query.answer()
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("BACK", callback_data="help_data"),
                InlineKeyboardButton("START", callback_data="start_data")],
            [InlineKeyboardButton("SOURCE CODE", url="https://github.com/TroJanzHEX/Unlimited-Filter-Bot")]
        ])

        await query.message.edit_text(
            Script.ABOUT_MSG,
            reply_markup=keyboard,
            disable_web_page_preview=True
        )
        return