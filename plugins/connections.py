from pyrogram import filters, Client
from database.connections_mdb import conn_grp, delete_con



@Client.on_message(filters.private & filters.command(["connect"]))
async def connect_grp(client,message):

    try:
        cmd, group_id = message.text.split(" ", 1)
        usrid = message.from_user.id
    except:
        await message.reply_text(
            "Invalid Group ID!",
            quote=True
        )
        return    
        
    try:
        st = await client.get_chat_member(group_id, usrid)
        if (st.status == "administrator") or (st.status == "creator"):
            pass
        else:
            await message.reply_text("You should be an admin in Given group!", quote=True)
            return
    except Exception as e:
        print(e)
        await message.reply_text(
            "Invalid Group ID!",
            quote=True
        )
        return

    try:
        st = await client.get_chat_member(group_id, "me")
        if st.status == "administrator":
            ttl = await client.get_chat(group_id)
            title = ttl.title
            await conn_grp(message, group_id, usrid)
            await message.reply_text(f'Sucessfully connected to {title}')
        else:
            await message.reply_text("Add me as an admin in given group", quote=True)
    except Exception as e:
        print(e)
        await message.reply_text(
            "Invalid Group ID!",
            quote=True
        )
        return


@Client.on_message(filters.private & filters.command(["disconnect"]))
async def dis_con(client,message):
    usrid = message.from_user.id
    await delete_con(message, str(usrid))
        
        
