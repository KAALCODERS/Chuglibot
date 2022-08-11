from telethon import events, TelegramClient, Button
import logging
from telethon.tl.functions.users import GetFullUserRequest as us
import os


logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get("TOKEN", None)

bot = TelegramClient(
        "Whisper",
        api_id=6,
        api_hash="5d59a136dc7843a9b83736834d93ee67"
        ).start(
                bot_token=TOKEN
                )
db = {}

@bot.on(events.NewMessage(pattern="^[!?/]start$"))
async def start(event):
    await event.reply(
            "**Namastey🙏, I am a Chugli Bot made by [𒆜𝗞𝗔𝗔𝗟♛](https://t.me/coder_kaal)!**",
            buttons=[
                [Button.switch_inline("Go Inline", query="")]
                ]
            )


@bot.on(events.InlineQuery())
async def die(event):
    if len(event.text) != 0:
        return
    me = (await bot.get_me()).username
    dn = event.builder.article(
            title="it is a Chugli bot!",
            description="it is a chugli Bot!\n(c) kaal",
            text=f"**it is a chugli bot**\n`@{me} wspr UserID|Message`\n**(c) kaal**",
            buttons=[
                [Button.switch_inline(" Go Inline ", query="wspr ")]
                ]
            )
    await event.answer([dn])
    
@bot.on(events.InlineQuery(pattern="wspr"))
async def inline(event):
    me = (await bot.get_me()).username
    try:
        inp = event.text.split(None, 1)[1]
        user, msg = inp.split("|")
    except IndexError:
        await event.answer(
                [], 
                switch_pm=f"@{me} [UserID]|[Message]",
                switch_pm_param="start"
                )
    except ValueError:
        await event.answer(
                [],
                switch_pm=f"Give a chugli message too!",
                switch_pm_param="start"
                )
    try:
        ui = await bot(us(user))
    except BaseException:
        await event.answer(
                [],
                switch_pm="Invalid User ID/Username",
                switch_pm_param="start"
                )
        return
    db.update({"user_id": ui.user.id, "msg": msg, "self": event.sender.id})
    text = f"""
A chugli message Has Been Sent
To [{ui.user.first_name}](tg://user?id={ui.user.id})!
Click The Below Button To See The chugli message!
**Note:** __Only {ui.user.first_name} can open this!__
    """
    dn = event.builder.article(
            title="It is a secret chugli message! Shhh",
            description="It is a secret chugli message! Shhh!",
            text=text,
            buttons=[
                [Button.inline(" Show Message! ", data="wspr")]
                ]
            )
    await event.answer(
            [dn],
            switch_pm="It's a secret chugli message! Shhh",
            switch_pm_param="start"
            )


@bot.on(events.CallbackQuery(data="wspr"))
async def ws(event):
    user = int(db["user_id"])
    lol = [int(db["self"])]
    lol.append(user)
    if event.sender.id not in lol:
        await event.answer("🔐 This chugli message is not for you🤫🤫!", alert=True)
        return
    msg = db["msg"]
    if msg == []:
        await event.anwswer(
                "Oops!\nIt's looks like chugli message got deleted from my server!", alert=True)
        return
    await event.answer(msg, alert=True)

print("Succesfully Started chugli Bot!")
bot.run_until_disconnected()
