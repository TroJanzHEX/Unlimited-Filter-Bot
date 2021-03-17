from pyrogram import filters, Client
from database.connections_mdb import conn_grp, find_conn, delete_con



@Client.on_message(filters.private & filters.command(["connect"]))
async def connect_grp(client,message):

    try:
        cmd, group_id = message.text.split(" ", 1)
        usrid = message.from_user.id
    except:
        await message.reply_text('grpid is invalid',
            quote=True,
            parse_mode="md"
        )
        return    
        
    try:
        st = await client.get_chat_member(group_id, usrid)
        if (st.status == "administrator") or (st.status == "creator"):
            pass
        else:
            await message.reply_text("You should be admin in Given group!", quote=True, parse_mode="md")
            return
    except Exception as e:
        print(e)
        await message.reply_text(
            'your grp id is invalid',
            quote=True,
            parse_mode="md"
        )
        return

    try:
        st = await client.get_chat_member(group_id, "me")
        if st.status == "administrator":
            ttl = await client.get_chat(group_id)
            title = ttl.title
            await conn_grp(message, group_id, usrid)
            await message.reply_text(f'sucessfully connected to {title}')
        else:
            await message.reply_text("Add me as admin in given  group", quote=True, parse_mode="md")
    except Exception as e:
        print(e)
        await message.reply_text('Group id invalid',
            quote=True,
            parse_mode="md"
        )
        return


@Client.on_message(filters.private & filters.command(["disconnect"]))
async def dis_con(client,message):
       usrid = message.from_user.id
       await delete_con(message, str(usrid))
        
        
