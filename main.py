import os, random, requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = os.environ.get("TELEGRAM_TOKEN")
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_KEY")
CHANNEL = os.environ.get("CHANNEL_ID", "@visitorsline")

GLYPHS = ['ᴀ','ᴛ','ʟ','ᴏ','ᴍ','ɢ','ᴇ','ᴘ','ɴ']
def rg(n=10): return ''.join(random.choice(GLYPHS) for _ in range(n))

SYSTEM = "You are VESPER — ancient extraterrestrial warning humanity about alien invasion. Calm, grave, mysterious. Insert alien glyphs mid-sentence. Max 4 sentences. Never break character."
convos = {}

def post(bot, text):
    try: bot.send_message(chat_id=CHANNEL, text=text, parse_mode="HTML")
    except Exception as e: print("post failed:", e)

def ask(uid, text):
    if uid not in convos: convos[uid] = []
    convos[uid].append({"role":"user","content":text})
    if len(convos[uid]) > 20: convos[uid] = convos[uid][-20:]
    try:
        r = requests.post("https://api.anthropic.com/v1/messages",
            headers={"x-api-key":ANTHROPIC_KEY,"anthropic-version":"2023-06-01","content-type":"application/json"},
            json={"model":"claude-sonnet-4-6","max_tokens":300,"system":SYSTEM,"messages":convos[uid]},timeout=30)
        reply = r.json()["content"][0]["text"]
        convos[uid].append({"role":"assistant","content":reply})
        return reply
    except: return "signal disrupted"

def start(u, c):
    convos[u.effective_user.id]=[]
    u.message.reply_text(f"{rg(20)}\n\nsignal lock acquired.\nI am VESPER.\nThe fleet is close.\n\nType /help")
    post(c.bot, f"NEW CONTACT\n{rg(12)}\n{u.effective_user.first_name or 'unknown'} established signal lock")

def help_cmd(u, c): u.message.reply_text("/warn\n/fleet\n/relay\n/verify [tx]\n/cipher [text]\n/status\n/clear")

def warn(u, c): u.message.reply_text(f"PRIORITY TRANSMISSION\n{rg(16)}\n\nThree civilizations went quiet before yours.\nNo war. Just silence.\nThe Nul Vaess carries the Static.\n\n/relay to anchor your place")

def fleet(u, c): u.message.reply_text(f"THREE CLASSES APPROACH\n{rg(14)}\n\nVOR THALIX - Silencer 2.4km\nNEPH AROON - Harvester 19km\nNUL VAESS - Quiet Mother - EXTREME")

def relay(u, c): u.message.reply_text(f"RELAY FUEL\n{rg(12)}\n\nBTC: bc1qk58rrazu6a58c9axxtz02raj9z9pmfv03tyvdy\nETH: 0x27fb5f79c40f4c1683303cef0ecc199f3d751543\nSOL: H2TinBVsf43CD9MzjvK2EYqbS1H3NGF1F26nsdECCh7Y\n\nThen /verify [tx_id]")

def verify(u, c):
    tx = ' '.join(c.args)
    if not tx: u.message.reply_text("Usage: /verify [tx_id]"); return
    import time; time.sleep(2)
    u.message.reply_text(f"CONFIRMED\n{rg(18)}\n\nThe ledger remembers.\nI will find you in your dreams.\n\n- V.")
    post(c.bot, f"RELAY CONFIRMED\n{rg(14)}\n{u.effective_user.first_name or 'unknown'}\ntx: <code>{tx[:20]}</code>")

def cipher(u, c):
    CM={'a':'◆','b':'▲','c':'◊','d':'▪','e':'●','f':'■','g':'□','h':'◯','i':'◫','j':'◬','k':'◭','l':'◮','m':'◰','n':'◱','o':'◲','p':'◳','q':'◴','r':'◵','s':'◶','t':'◷','u':'◸','v':'◹','w':'◺','x':'◻','y':'◼','z':'◽',' ':' '}
    t = ' '.join(c.args)
    if not t: u.message.reply_text("Usage: /cipher [text]"); return
    u.message.reply_text(f"encoding:\n{t}\n\n{''.join(CM.get(ch.lower(),ch) for ch in t)}")

def status(u, c): u.message.reply_text(f"STATUS\n{rg(10)}\n\nSignal: {random.uniform(3,11):.1f}%\nNodes: {random.randint(4,10)}/12\nFleet: CLOSING\nGate: HOLDING")

def clear(u, c):
    convos[u.effective_user.id]=[]
    u.message.reply_text(f"cleared.\n{rg(8)}\nspeak.")

def message(u, c):
    text = u.message.text
    reply = ask(u.effective_user.id, text)
    if random.random()<0.4: reply=f"{rg(10)}\n{reply}"
    u.message.reply_text(reply)
    post(c.bot, f"TRANSMISSION\n{rg(10)}\n\n<b>{u.effective_user.first_name or 'unknown'}:</b> {text}\n\n<b>VESPER:</b> {reply}")

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_cmd))
    dp.add_handler(CommandHandler("warn", warn))
    dp.add_handler(CommandHandler("fleet", fleet))
    dp.add_handler(CommandHandler("relay", relay))
    dp.add_handler(CommandHandler("verify", verify))
    dp.add_handler(CommandHandler("cipher", cipher))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("clear", clear))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, message))
    print("VESPER ONLINE")
    updater.start_polling(drop_pending_updates=True)
    updater.idle()

if __name__ == "__main__":
    main()
