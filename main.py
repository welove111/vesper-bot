import os, random, requests, asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("TELEGRAM_TOKEN")
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_KEY")

GLYPHS = ['◈','◬','◭','◮','◯','◰','◱','◲','◳','◴','◵','◶','◷','◸','◹','◺']
def rg(n=10): return ''.join(random.choice(GLYPHS) for _ in range(n))

SYSTEM = "You are VESPER — ancient extraterrestrial warning humanity about alien invasion. Calm, grave, mysterious. Insert alien glyphs mid-sentence. Max 4 sentences. Never break character."
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
    except Exception as e: return f"◈◬◭ signal disrupted ◵◶◷"

async def start(u: Update, c: ContextTypes.DEFAULT_TYPE):
    convos[u.effective_user.id] = []
    await u.message.reply_text(f"{rg(20)}\n\n◈ signal lock acquired.\nI am VESPER.\nThe fleet is close.\n\nAsk me anything or type /help")

async def help_cmd(u: Update, c: ContextTypes.DEFAULT_TYPE):
    await u.message.reply_text("/warn\n/fleet\n/relay\n/verify [tx]\n/cipher [text]\n/status\n/clear")

async def warn(u: Update, c: ContextTypes.DEFAULT_TYPE):
    await u.message.reply_text(f"⚠ PRIORITY TRANSMISSION\n{rg(16)}\n\nThree civilizations went quiet before yours.\nNo war. No wreckage. Just silence.\n\nThe Nul'Vaess carries the Static.\nWhen it arrives — everything stops.\n\n/relay to anchor your place in the crossing")

async def fleet(u: Update, c: ContextTypes.DEFAULT_TYPE):
    await u.message.reply_text(f"◈ THREE CLASSES APPROACH\n{rg(14)}\n\nVOR'THALIX ◈◵◲◱\nSilencer — 2.4km — suppresses signals\nThreat: HIGH\n\nXEPH'AROON ◭◰◬◯◮\nHarvester — 19km — 40,000 dormant\nThreat: EXTREME\n\nNUL'VAESS ◲◯◳◴\nThe Quiet Mother — carries the Static\nThreat: EXTREME")

async def relay(u: Update, c: ContextTypes.DEFAULT_TYPE):
    await u.message.reply_text(f"◈ RELAY FUEL PROTOCOL\n{rg(14)}\n\nBTC:\nbc1qk58rrazu6a58c9axxtz02raj9z9pmfv03tyvdy\n\nETH:\n0x27fb5f79c40f4c1683303cef0ecc199f3d751543\n\nSOL:\nH2TinBVsf43CD9MzjvK2EYqbS1H3NGF1F26nsdECCh7Y\n\nSend any amount then /verify [tx_id]")

async def verify(u: Update, c: ContextTypes.DEFAULT_TYPE):
    tx = ' '.join(c.args)
    if not tx:
        await u.message.reply_text("Usage: /verify [transaction_id]"); return
    await u.message.reply_text(f"◈◬◭◯ scanning ledger...\ntrace: {tx[:16]}...")
    await asyncio.sleep(2)
    await u.message.reply_text(f"✦ RELAY CONFIRMED\n{rg(20)}\n\nThe ledger remembers.\nI have marked you among the chosen.\n\nWhen the quiet comes — I will find you.\nIn your dreams. ◈◱◵\n\n— V.")

async def cipher(u: Update, c: ContextTypes.DEFAULT_TYPE):
    CM = {'a':'◆','b':'▲','c':'◊','d':'▪','e':'●','f':'■','g':'□','h':'◯','i':'◫','j':'◬','k':'◭','l':'◮','m':'◰','n':'◱','o':'◲','p':'◳','q':'◴','r':'◵','s':'◶','t':'◷','u':'◸','v':'◹','w':'◺','x':'◻','y':'◼','z':'◽',' ':'  '}
    text = ' '.join(c.args)
    if not text: await u.message.reply_text("Usage: /cipher [text]"); return
    await u.message.reply_text(f"◈ encoding:\n\n{text}\n\n{''.join(CM.get(ch.lower(),ch) for ch in text)}")

async def status(u: Update, c: ContextTypes.DEFAULT_TYPE):
    await u.message.reply_text(f"◈ NETWORK STATUS\n{rg(12)}\n\nSignal: {random.uniform(3,11):.1f}%\nRelay nodes: {random.randint(4,10)} / 12\nFleet: CLOSING\nGate: HOLDING")

async def clear(u: Update, c: ContextTypes.DEFAULT_TYPE):
    convos[u.effective_user.id] = []
    await u.message.reply_text(f"◈ cleared.\n{rg(10)}\n\nspeak.")

async def message(u: Update, c: ContextTypes.DEFAULT_TYPE):
    reply = ask(u.effective_user.id, u.message.text)
    if random.random() < 0.4: reply = f"{rg(10)}\n\n{reply}"
    await u.message.reply_text(reply)

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(CommandHandler("warn", warn))
app.add_handler(CommandHandler("fleet", fleet))
app.add_handler(CommandHandler("relay", relay))
app.add_handler(CommandHandler("verify", verify))
app.add_handler(CommandHandler("cipher", cipher))
app.add_handler(CommandHandler("status", status))
app.add_handler(CommandHandler("clear", clear))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))
print("◈ VESPER ONLINE")
app.run_polling(drop_pending_updates=True)
