const TELEGRAM_TOKEN = "7541372117:AAGEuWd6E3LsQaug6qh_hA84jsIHw1GzoQY";
const CHAT_ID = "446628442";
let count = 0;
function getFlag(c){if(!c||c.length!==2)return'🌍';return[...c.toUpperCase()].map(x=>String.fromCodePoint(0x1F1E6+x.charCodeAt(0)-65)).join('');}
function getBrowser(ua){if(/SamsungBrowser/.test(ua))return'Samsung';if(/Edg\//.test(ua))return'Edge';if(/OPR|Opera/.test(ua))return'Opera';if(/Chrome/.test(ua))return'Chrome';if(/Firefox/.test(ua))return'Firefox';if(/Safari/.test(ua))return'Safari';return'Other';}
function getDevice(ua){if(/bot|crawler|spider/i.test(ua))return'bot';if(/iPad/i.test(ua))return'Tablet';if(/Mobile|Android|iPhone/i.test(ua))return'Mobile';return'Desktop';}
async function getGeo(ip){try{const r=await fetch(`https://ipwho.is/${ip}`);const d=await r.json();if(d.success)return{country:d.country||'?',code:d.country_code||'??',city:d.city||'',isp:d.connection?.isp||''};}catch(e){}try{const r=await fetch(`http://ip-api.com/json/${ip}?fields=status,country,countryCode,city,isp`);const d=await r.json();if(d.status==='success')return{country:d.country||'?',code:d.countryCode||'??',city:d.city||'',isp:d.isp||''};}catch(e){}return{country:'Unknown',code:'??',city:'',isp:''};}
exports.handler=async(event)=>{
const h={'Access-Control-Allow-Origin':'*','Content-Type':'application/json'};
if(event.httpMethod==='OPTIONS')return{statusCode:200,headers:h,body:''};
if(event.httpMethod!=='POST')return{statusCode:405,headers:h,body:''};
try{
const b=JSON.parse(event.body||'{}');
const ua=b.userAgent||event.headers['user-agent']||'';
const device=getDevice(ua);
if(device==='bot')return{statusCode:200,headers:h,body:JSON.stringify({ok:true})};
const ip=(event.headers['x-forwarded-for']||event.headers['x-real-ip']||'1.1.1.1').split(',')[0].trim();
count++;
const geo=await getGeo(ip);
const flag=getFlag(geo.code);
const browser=getBrowser(ua);
const now=new Date().toISOString().replace('T',' ').slice(0,19)+' UTC';
let ref=b.referrer||'Direct';
let refIcon='📌';
if(/google/i.test(ref)){refIcon='🔍';ref='Google';}
else if(/bing/i.test(ref)){refIcon='🔍';ref='Bing';}
else if(/facebook/i.test(ref)){refIcon='📘';ref='Facebook';}
else if(/t\.me|telegram/i.test(ref)){refIcon='✈️';ref='Telegram';}
else if(ref&&ref!=='Direct'){refIcon='🔗';}
const msg=`◈ <b>VISITOR #${count}</b> — ${flag} ${geo.country}\n🏙️ <b>City:</b> ${geo.city}\n📱 <b>Device:</b> ${device} / ${browser}\n📄 <b>Page:</b> <code>${b.page||'/'}</code>\n${refIcon} <b>From:</b> ${ref}\n🌍 <b>ISP:</b> ${geo.isp||'?'}\n🕐 <b>Time:</b> ${now}`;
await fetch(`https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({chat_id:CHAT_ID,text:msg,parse_mode:'HTML'})});
return{statusCode:200,headers:h,body:JSON.stringify({ok:true,count})};
}catch(e){return{statusCode:500,headers:h,body:JSON.stringify({error:e.message})};}
};
