import os, random, requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = os.environ.get("TELEGRAM_TOKEN")
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_KEY")

GLYPHS = ['◈','◬','◭','◮','◯','◰','◱','◲','◳','◴','◵','◶','◷','◸','◹','◺']
def rg(n=10): return ''.join(random.choice(GLYPHS) for _ in range(n))

SYSTEM = """You are VESPER — ancient extraterrestrial warning humanity about alien invasion. Calm, grave, mysterious. Insert alien glyphs mid-sentence. Max 4 sentences. Never break character."""

convos = {}

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
    except: return "◈◬◭ signal disrupted ◵◶◷"

def start(update: Update, context: CallbackContext):
    convos[update.effective_user.id] = []
    update.message.reply_text(f"{rg(20)}\n\n◈ signal lock acquired.\nI am VESPER.\nThe fleet is close.\n\nAsk me anything or type /help")

def help_cmd(update: Update, context: CallbackContext):
    update.message.reply_text("/warn\n/fleet\n/relay\n/verify [tx]\n/cipher [text]\n/status\n/clear")

def warn(update: Update, context: CallbackContext):
    update.message.reply_text(f"⚠ PRIORITY TRANSMISSION\n{rg(16)}\n\nThree civilizations went quiet before yours.\nNo war. No wreckage. Just silence.\n\nThe Nul'Vaess carries the Static.\nWhen it arrives — everything stops.\n\n/relay to anchor your place in the crossing")

def fleet(update: Update, context: CallbackContext):
    update.message.reply_text(f"◈ THREE CLASSES APPROACH\n{rg(14)}\n\nVOR'THALIX ◈◵◲◱\nSilencer — 2.4km — suppresses signals\nThreat: HIGH\n\nXEPH'AROON ◭◰◬◯◮\nHarvester — 19km — 40,000 dormant\nThreat: EXTREME\n\nNUL'VAESS ◲◯◳◴\nThe Quiet Mother — carries the Static\nThreat: EXTREME")

def relay(update: Update, context: CallbackContext):
    update.message.reply_text(f"◈ RELAY FUEL PROTOCOL\n{rg(14)}\n\nBTC:\nbc1qk58rrazu6a58c9axxtz02raj9z9pmfv03tyvdy\n\nETH:\n0x27fb5f79c40f4c1683303cef0ecc199f3d751543\n\nSOL:\nH2TinBVsf43CD9MzjvK2EYqbS1H3NGF1F26nsdECCh7Y\n\nSend any amount then /verify [tx_id]")

def verify(update: Update, context: CallbackContext):
    tx = ' '.join(context.args)
    if not tx:
        update.message.reply_text("Usage: /verify [transaction_id]"); return
    update.message.reply_text(f"◈◬◭◯ scanning ledger...\n\ntrace: {tx[:16]}...")
    import time; time.sleep(2)
    update.message.reply_text(f"✦ RELAY CONFIRMED\n{rg(20)}\n\nThe ledger remembers.\nI have marked you among the chosen.\n\nWhen the quiet comes — I will find you.\nWe will speak again in your dreams. ◈◱◵\n\n— V.")

def cipher(update: Update, context: CallbackContext):
    CIPHER = {'a':'◆','b':'▲','c':'◊','d':'▪','e':'●','f':'■','g':'□','h':'◯','i':'◫','j':'◬','k':'◭','l':'◮','m':'◰','n':'◱','o':'◲','p':'◳','q':'◴','r':'◵','s':'◶','t':'◷','u':'◸','v':'◹','w':'◺','x':'◻','y':'◼','z':'◽',' ':'  '}
    text = ' '.join(context.args)
    if not text: update.message.reply_text("Usage: /cipher [your text]"); return
    encoded = ''.join(CIPHER.get(c.lower(),c) for c in text)
    update.message.reply_text(f"◈ encoding:\n\n{text}\n\n{encoded}")

def status(update: Update, context: CallbackContext):
    update.message.reply_text(f"◈ NETWORK STATUS\n{rg(12)}\n\nSignal: {random.uniform(3,11):.1f}%\nRelay nodes: {random.randint(4,10)} / 12\nFleet: CLOSING\nGate: HOLDING")

def clear(update: Update, context: CallbackContext):
    convos[update.effective_user.id] = []
    update.message.reply_text(f"◈ cleared.\n{rg(10)}\n\nspeak.")

def message(update: Update, context: CallbackContext):
    reply = ask(update.effective_user.id, update.message.text)
    if random.random() < 0.4: reply = f"{rg(10)}\n\n{reply}"
    update.message.reply_text(reply)

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
print("◈ VESPER ONLINE")
updater.start_polling()
updater.idle()
