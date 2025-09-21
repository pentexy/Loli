import requests, asyncio
from AnonXMusic import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_URL = "https://userapi-i9r2.onrender.com/address"

# --- monocaps font map ---
MONO = {
    'a':'ᴀ','b':'ʙ','c':'ᴄ','d':'ᴅ','e':'ᴇ','f':'ғ','g':'ɢ','h':'ʜ','i':'ɪ','j':'ᴊ','k':'ᴋ',
    'l':'ʟ','m':'ᴍ','n':'ɴ','o':'ᴏ','p':'ᴘ','q':'ǫ','r':'ʀ','s':'s','t':'ᴛ','u':'ᴜ','v':'ᴠ',
    'w':'ᴡ','x':'x','y':'ʏ','z':'ᴢ',
    '0':'𝟢','1':'𝟣','2':'𝟤','3':'𝟥','4':'𝟦','5':'𝟧','6':'𝟨','7':'𝟩','8':'𝟪','9':'𝟫'
}
def mono(t: str) -> str:
    return ''.join(MONO.get(c, c) for c in t)

# --- format address (labels mono, values clean) ---
def format_address(data: dict) -> str:
    return f"""
<b>{mono("⌬ random address ⌬")}</b>

<b>{mono("name:")}</b> <code>{data.get("name","")} {data.get("surname","")}</code>
<b>{mono("house no:")}</b> <code>{data.get("house_no")}</code>
<b>{mono("street:")}</b> <code>{data.get("street","")}</code>
<b>{mono("city:")}</b> <code>{data.get("city","")}</code>
<b>{mono("state:")}</b> <code>{data.get("state","")}</code>
<b>{mono("country:")}</b> <code>{data.get("country","")} ({data.get("country_code")})</code>
<b>{mono("postal code:")}</b> <code>{data.get("postal_code")}</code>
<b>{mono("phone:")}</b> <code>{data.get("phone")}</code>
<b>{mono("coordinates:")}</b> <code>{data.get("latitude")}, {data.get("longitude")}</code>
"""

# --- keyboard ---
def build_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(mono("new"), callback_data="new"),
        InlineKeyboardButton(mono("close"), callback_data="close")
    ]])

# --- /address command ---
@app.on_message(filters.command(["address","addr"]))
async def address_cmd(_, msg):
    await msg.reply_text(
        mono("press new to generate an address"),
        reply_markup=build_keyboard()
    )

# --- button handler ---
@app.on_callback_query(filters.regex("^(new|close)$"))
async def nav_handler(_, query):
    if query.data == "close":
        return await query.message.delete()

    # dot animation (loops a few steps)
    for dots in [".", "..", "...", "....", ".....", "......"]:
        await query.edit_message_text(
            f"{mono('gathering info')} {dots}",
            reply_markup=build_keyboard()
        )
        await asyncio.sleep(0.5)

    # fetch and display new address
    try:
        r = requests.get(API_URL, timeout=10).json()
        data = r.get("address", r.get("addresses", [{}])[0])
        text = format_address(data)
        await query.edit_message_text(text, reply_markup=build_keyboard())
    except Exception as e:
        await query.edit_message_text(f"<b>{mono('error')}:</b> <code>{e}</code>", reply_markup=build_keyboard())
