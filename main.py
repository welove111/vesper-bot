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
    except: return "◈◬◭ signal disrupted ◵◶◷"

async def start(u,c): convos[u.effective_user.id]=[]; await u.message.reply_text(f"{rg(20)}\n\n◈ signal lock acquired.\nI am VESPER.\nThe fleet is close.\n\nType /help")
async def help_cmd(u,c): await u.message.reply_text("/warn\n/fleet\n/relay\n/verify [tx]\n/cipher [text]\n/status\n/clear")
async def warn(u,c): await u.message.reply_text(f"⚠ PRIORITY TRANSMISSION\n{rg(16)}\n\nThree civilizations went quiet before yours.\nNo war. No wreckage. Just silence.\n\nThe Nul'Vaess carries the Static.\nWhen it arrives — everything stops.\n\n/relay to anchor your place")
async def fleet(u,c): await u.message.reply_text(f"◈ THREE CLASSES APPROACH\n{rg(14)}\n\nVOR'THALIX — Silencer 2.4km — HIGH\nXEPH'AROON — Harvester 19km — EXTREME\nNUL'VAESS — Quiet Mother — EXTREME")
async def relay(u,c): await u.message.reply_text(f"◈ RELAY FUEL\n{rg(12)}\n\nBTC: bc1qk58rrazu6a58c9axxtz02raj9z9pmfv03tyvdy\nETH: 0x27fb5f79c40f4c1683303cef0ecc199f3d751543\nSOL: H2TinBVsf43CD9MzjvK2EYqbS1H3NGF1F26nsdECCh7Y\n\nThen /verify [tx_id]")
async def verify(u,c):
    tx=' '.join(c.args)
    if not tx: await u.message.reply_text("Usage: /verify [tx_id]"); return
    await u.message.reply_text(f"◈ scanning...\n{tx[:16]}...")
    await asyncio.sleep(2)
    await u.message.reply_text(f"✦ CONFIRMED\n{rg(18)}\n\nThe ledger remembers.\nI will find you in your dreams. ◈◱◵\n\n— V.")
async def cipher(u,c):
    CM={'a':'◆','b':'▲','c':'◊','d':'▪','e':'●','f':'■','g':'□','h':'◯','i':'◫','j':'◬','k':'◭','l':'◮','m':'◰','n':'◱','o':'◲','p':'◳','q':'◴','r':'◵','s':'◶','t':'◷','u':'◸','v':'◹','w':'◺','x':'◻','y':'◼','z':'◽',' ':'  '}
    t=' '.join(c.args)
    if not t: await u.message.reply_text("Usage: /cipher [text]"); return
    await u.message.reply_text(f"◈ encoding:\n\n{t}\n\n{''.join(CM.get(ch.lower(),ch) for ch in t)}")
async def status(u,c): await u.message.reply_text(f"◈ STATUS\n{rg(10)}\n\nSignal: {random.uniform(3,11):.1f}%\nNodes: {random.randint(4,10)}/12\nFleet: CLOSING\nGate: HOLDING")
async def clear(u,c): convos[u.effective_user.id]=[]; await u.message.reply_text(f"◈ cleared.\n{rg(8)}\n\nspeak.")
async def message(u,c):
    reply=ask(u.effective_user.id,u.message.text)
    if random.random()<0.4: reply=f"{rg(10)}\n\n{reply}"
    await u.message.reply_text(reply)

async def main():
    app=Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start",start))
    app.add_handler(CommandHandler("help",help_cmd))
    app.add_handler(CommandHandler("warn",warn))
    app.add_handler(CommandHandler("fleet",fleet))
    app.add_handler(CommandHandler("relay",relay))
    app.add_handler(CommandHandler("verify",verify))
    app.add_handler(CommandHandler("cipher",cipher))
    app.add_handler(CommandHandler("status",status))
    app.add_handler(CommandHandler("clear",clear))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,message))
    print("◈ VESPER ONLINE")
    await app.run_polling(drop_pending_updates=True)

if __name__=="__main__":
    asyncio.run(main())
