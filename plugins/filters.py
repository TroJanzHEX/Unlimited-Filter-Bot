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



@Client.on_message(filters.command('add'))
async def addfilter(client, message):
      
    userid = message.from_user.id
    chat_type = message.chat.type
    args = message.text.split(None, 1)

    if chat_type == "private":
        grpid = await find_conn(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("Make sure I'm present in your group!!", quote=True)
                return
        else:
            await message.reply_text("I'm not connected to any groups!", quote=True)
            return

    elif chat_type == "group" or "supergroup":
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    if len(args) < 2:
        return
    
    extracted = split_quotes(args[1])
    text = extracted[0].lower()
   
    if not message.reply_to_message and len(extracted) < 2:
        return

    if len(extracted) >= 2:
        reply_text, btn = parser(extracted[1]) 
        fileid = None
        if not reply_text:
            await message.reply_text("You cannot have buttons alone, give some text to go with it!")
            return

    elif message.reply_to_message and message.reply_to_message.reply_markup:
        try:
            rm = message.reply_to_message.reply_markup
            btn = rm.inline_keyboard
            msg = message.reply_to_message.document or\
                  message.reply_to_message.video or\
                  message.reply_to_message.photo or\
                  message.reply_to_message.audio or\
                  message.reply_to_message.animation or\
                  message.reply_to_message.sticker
            if msg:
                fileid = msg.file_id
                reply_text = message.reply_to_message.caption.html
            else:
                reply_text = message.reply_to_message.text.html
                fileid = None
        except:
            reply_text = ""
            btn = "[]" 
            fileid = None

    elif message.reply_to_message and message.reply_to_message.photo:
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

    elif message.reply_to_message and message.reply_to_message.text:
        try:
            fileid = None
            reply_text, btn = parser(message.reply_to_message.text.html)
        except:
            reply_text = ""
            btn = "[]"

    else:
        return
    
    await add_filter(message, grp_id, text, reply_text, btn, fileid)

    await message.reply_text(f"{text} saved to {title}")


@Client.on_message(filters.command('viewfilters'))
async def get_all(client, message):
    userid = message.from_user.id
    chat_type = message.chat.type

    if chat_type == "private":
        grpid = await find_conn(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("Make sure I'm present in your group!!", quote=True)
                return
        else:
            await message.reply_text("I'm not connected to any groups!", quote=True)
            return

    elif chat_type == "group" or "supergroup":
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    texts = await get_filters(grp_id)
    count = await countfilters(grp_id)
    if count:
        filterlist = f"Total number of filters in {title} : {count}\n\n"
        for text in texts:
            keywords = " ×  `{}`\n".format(text)
            if len(keywords) + len(filterlist) > 4096:
                await message.reply_text(
                    text=filterlist,
                    parse_mode="md"
                )
                filterlist = keywords
            else:
                filterlist += keywords
    else:
        filterlist = f"There are no active filters in **{title}**"

    await message.reply_text(
        text=filterlist,
        parse_mode="md"
    )
        
@Client.on_message(filters.command('del'))
async def del_filter(client, message):
    userid = message.from_user.id
    chat_type = message.chat.type

    if chat_type == "private":
        grpid  = await find_conn(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("Make sure I'm present in your group!!", quote=True)
                return
        else:
            await message.reply_text("I'm not connected to any groups!", quote=True)

    elif chat_type == "group" or "supergroup":
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    cmd, text = message.text.split(" ", 1)
    query = text.lower()

    await delete_fil(message, query, grp_id)
        

@Client.on_message(filters.group & filters.text)
async def recive_filter(client,message):
    group_id = message.chat.id
    name = message.text.lower()

    reply_text, btn, fileid = await find_filter(group_id, name) 

    if btn is None:
        return

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

      
