import os
import pyrogram

from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

from database.filters_mdb import(
   add_filter,
   find_filter,
   get_filters,
   delete_fil,
   countfilters
)

from database.connections_mdb import find_conn

from plugins.helpers import parser,split_quotes



@Client.on_message(filters.command('start'))
async def _start(client, message):
    await message.reply_text("soon")


@Client.on_message(filters.command('add'))
async def _filter(client, message):
      
    userid = message.from_user.id
    chat_type = message.chat.type
    args = message.text.split(None, 1)

    if chat_type == "private":
        grpid = await find_conn(message, str(userid))
        if grpid is not None:
            grp_id = grpid
            a = await client.get_chat(grpid)
            title = a.title
        else:
            await message.reply_text('not conected')
    elif chat_type == "group" or "supergroup":
        grp_id = message.chat.id
        title = message.chat.title

    if len(args) < 2:
        return
    
    extracted = split_quotes(args[1])
    keyword = extracted[0].lower()
    text = keyword
   
    if len(extracted) < 1:
        return

    if len(extracted) >= 2:
        reply_text, btn = parser(extracted[1]) 
        fileid = None
        if not reply_text:
            await message.reply_text('You cannot have the buttons alone without even a text')

    if message.reply_to_message and message.reply_to_message.photo:
        try:
            fileid = message.reply_to_message.photo.file_id
            reply_text, btn = parser(message.reply_to_message.caption.html)
        except:
            reply_text = ""
            btn = "[]"

    elif message.reply_to_message and message.reply_to_message.video:
        try:
            fileid = message.reply_to_message.video.file_id
            reply_text,btn = parser(message.reply_to_message.caption.html)
        except:
            reply_text = ""
            btn = "[]"

    elif message.reply_to_message and message.reply_to_message.audio:
        try:
            fileid = message.reply_to_message.audio.file_id
            reply_text,btn = parser(message.reply_to_message.caption.html)
        except:
            reply_text = ""
            btn = "[]"  
   
    elif message.reply_to_message and message.reply_to_message.document:
        try:
            fileid = message.reply_to_message.document.file_id
            reply_text,btn = parser(message.reply_to_message.caption.html)
        except:
            reply_text = ""
            btn = "[]"

    elif message.reply_to_message and message.reply_to_message.animation:
        try:
            fileid = message.reply_to_message.animation.file_id
            reply_text,btn = parser(message.reply_to_message.caption.html)
        except:
            reply_text = ""
            btn = "[]"

    elif message.reply_to_message and message.reply_to_message.sticker:
        try:
            fileid = message.reply_to_message.sticker.file_id
            reply_text,btn =  parser(extracted[1])
        
        except:
            reply_text = ""
            btn = "[]"                   
    
    
    await add_filter(message, grp_id, text, reply_text, btn, fileid)

    await message.reply_text(f"{text} saved to {title}")


@Client.on_message(filters.command('filters'))
async def get_all(client, message):
    userid = message.from_user.id
    chat_type = message.chat.type
    if chat_type == "private":
        grpid = await find_conn(message,str(userid))
        if grpid is not None:
            grp_id = grpid
            a = await client.get_chat(grpid)
            title = a.title
        else:
            await message.reply_text('not conectred')

    elif chat_type == "group" or "supergroup":
        grp_id = message.chat.id
        title = message.chat.title

    texts = await get_filters(grp_id)
    count = await countfilters(grp_id)

    b = "\n".join(texts)

    await message.reply_text(
        f"Total number of filters in {title} {count}\n{b}"
    )

        
@Client.on_message(filters.command('del'))
async def del_filter(client, message):
    userid = message.from_user.id
    chat_type = message.chat.type
    if chat_type == "private":
        grpid  = await find_conn(message,str(userid))
        if grpid is not None:
            grpid = grpid
            a = await client.get_chat(grpid)
            title = a.title
        else:
            await message.reply_text('not conectred')

    elif chat_type == "group" or "supergroup":
        grp_id = message.chat.id
        title = message.chat.title

    cmd, g = message.text.split(" ", 1)
    text = g

    await delete_fil(message, text, grpid)
        

@Client.on_message(filters.group & filters.text)
async def recive_filter(client,message):
    group_id = message.chat.id
    name = message.text.lower()

    reply_text, btn, fileid = await find_filter(group_id, name) 

    if fileid == "None":
        if btn == "[]":
            await message.reply_text(reply_text)
        else:
            button = eval(btn)
            await message.reply_text(
                reply_text,
                parse_mode="html",
                reply_markup=InlineKeyboardMarkup(button)
            )
    else:
        if btn == "[]":
            await message.reply_cached_media(
                fileid,
                caption=reply_text or ""
            )
        else:
            button = eval(btn) 
            await message.reply_cached_media(
                fileid,
                caption=reply_text or "",
                reply_markup=InlineKeyboardMarkup(button)
            )

      
