import os

from pyrogram import Client as trojanz
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

from script import Script
from plugins.filters import delall
from database.connections_mdb import all_connections, if_active, delete_connection, make_active, make_inactive


@trojanz.on_callback_query()
async def cb_handler(client, query):

    if query.data == "start_data":
        await query.answer()
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Command Help", callback_data="help_data")
                ]
            ]
        )

        await query.message.edit_text(
            Script.START_MSG.format(query.from_user.mention),
            reply_markup=keyboard,
            disable_web_page_preview=True
        )
        return

    elif query.data == "help_data":
        await query.answer()
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("How to Deploy?", url="https://youtu.be/hkmc3e7U7R4"),
                    InlineKeyboardButton("About Me", callback_data="about_data")
                ],
                [
                    InlineKeyboardButton("BOT Channel", url="https://t.me/TroJanzHEX"),
                    InlineKeyboardButton("Support Group", url="https://t.me/TroJanzSupport")
                ]
            ]
        )

        await query.message.edit_text(
            Script.HELP_MSG,
            reply_markup=keyboard,
            disable_web_page_preview=True
        )
        return

    elif query.data == "about_data":
        await query.answer()
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "SOURCE CODE", url="https://github.com/TroJanzHEX/Unlimited-Filter-Bot")
                ],
                [
                    InlineKeyboardButton("BACK", callback_data="help_data"),
                    InlineKeyboardButton("CLOSE", callback_data="close_data"),
                ]                
            ]
        )

        await query.message.edit_text(
            Script.ABOUT_MSG,
            reply_markup=keyboard,
            disable_web_page_preview=True
        )
        return

    elif query.data == "close_data":
        await query.message.delete()
        

    elif query.data == "delallconfirm":
        clicked = query.from_user.id
        typed = query.message.reply_to_message.from_user.id

        if (clicked == typed) or (str(clicked) in Config.AUTH_USERS):
            await delall(client, query.message)
            await query.message.delete()
        else:
            await query.answer("Thats not for you!!",show_alert=True)
    
    elif query.data == "delallcancel":
        clicked = query.from_user.id
        typed = query.message.reply_to_message.from_user.id

        if (clicked == typed) or (str(clicked) in Config.AUTH_USERS):
            await query.message.reply_to_message.delete()
            await query.message.delete()
        else:
            await query.answer("Thats not for you!!",show_alert=True)


    elif "groupcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]
        title = query.data.split(":")[2]
        act = query.data.split(":")[3]
        user_id = query.from_user.id

        if act == "":
            stat = "CONNECT"
            cb = "connectcb"
        else:
            stat = "DISCONNECT"
            cb = "disconnect"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{stat}", callback_data=f"{cb}:{group_id}:{title}"),
                InlineKeyboardButton("DELETE", callback_data=f"deletecb:{group_id}")],
            [InlineKeyboardButton("BACK", callback_data="backcb")]
        ])

        await query.message.edit_text(
            f"Group Name : **{title}**\nGroup ID : `{group_id}`",
            reply_markup=keyboard,
            parse_mode="md"
        )
        return

    elif "connectcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]
        title = query.data.split(":")[2]
        user_id = query.from_user.id

        mkact = await make_active(str(user_id), str(group_id))

        if mkact:
            await query.message.edit_text(
                f"Connected to **{title}**",
                parse_mode="md"
            )
            return
        else:
            await query.message.edit_text(
                f"Some error occured!!",
                parse_mode="md"
            )
            return

    elif "disconnect" in query.data:
        await query.answer()

        title = query.data.split(":")[2]
        user_id = query.from_user.id

        mkinact = await make_inactive(str(user_id))

        if mkinact:
            await query.message.edit_text(
                f"Disconnected from **{title}**",
                parse_mode="md"
            )
            return
        else:
            await query.message.edit_text(
                f"Some error occured!!",
                parse_mode="md"
            )
            return
    elif "deletecb" in query.data:
        await query.answer()

        user_id = query.from_user.id
        group_id = query.data.split(":")[1]

        delcon = await delete_connection(str(user_id), str(group_id))

        if delcon:
            await query.message.edit_text(
                "Successfully deleted connection"
            )
            return
        else:
            await query.message.edit_text(
                f"Some error occured!!",
                parse_mode="md"
            )
            return
    
    elif query.data == "backcb":
        await query.answer()

        userid = query.from_user.id

        groupids = await all_connections(str(userid))
        if groupids is None:
            await query.message.edit_text(
                "There are no active connections!! Connect to some groups first.",
            )
            return
        buttons = []
        for groupid in groupids:
            try:
                ttl = await client.get_chat(int(groupid))
                title = ttl.title
                active = await if_active(str(userid), str(groupid))
                if active:
                    act = " - ACTIVE"
                else:
                    act = ""
                buttons.append(
                    [
                        InlineKeyboardButton(
                            text=f"{title}{act}", callback_data=f"groupcb:{groupid}:{title}:{act}"
                        )
                    ]
                )
            except:
                pass
        if buttons:
            await query.message.edit_text(
                "Your connected group details ;\n\n",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
