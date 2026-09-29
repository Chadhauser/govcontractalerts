#!/usr/bin/env python3
# GovContract Alerts - full programmatic generator.
# One template -> 40 trades x 50 states (2000) + money pages + sitemap + robots.
# Internal links use a per-depth prefix so the site works at a domain root AND at
# a github.io project subpath. Live data + sign-up hit the Supabase edge functions.
import os, html

API = "https://xeadalusejspxhqesisv.supabase.co/functions/v1"
BRAND = "GovContract Alerts"
DOMAIN = "https://govcontractalerts.com"
YEAR = "2026"
OUT = os.environ.get("OUT_DIR", "site")
os.makedirs(OUT, exist_ok=True)


def esc(s): return html.escape(str(s))

HEAD = """<!DOCTYPE html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{{TITLE}}</title><meta name="description" content="{{DESC}}"><meta name="robots" content="index,follow">
<link rel="canonical" href="{{CANON}}"><meta name="theme-color" content="#0B3D6B">
<meta property="og:title" content="{{TITLE}}"><meta property="og:description" content="{{DESC}}"><meta property="og:type" content="website">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500&display=swap" rel="stylesheet">
<style>
:root{--navy:#0B3D6B;--navy2:#0a3358;--ink:#132030;--body:#3a4658;--muted:#6b7688;--line:#e2e7ee;--paper:#f6f8fb;--panel:#fff;--accent:#c8102e;box-sizing:border-box;padding-top:env(safe-area-inset-top,0)}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:Inter,system-ui,sans-serif;font-size:16px;line-height:1.6;-webkit-font-smoothing:antialiased}
.wrap{max-width:920px;margin:0 auto;padding:0 20px}a{color:var(--navy)}
h1,h2,h3{line-height:1.15;letter-spacing:-.01em}h1{font-size:34px;font-weight:700;margin:0 0 12px}h2{font-size:23px;font-weight:700;margin:34px 0 12px}h3{font-size:17px;font-weight:600;margin:20px 0 6px}
@media(max-width:640px){h1{font-size:27px}}
header{background:var(--navy);color:#fff}.bar{display:flex;align-items:center;justify-content:space-between;padding:14px 0}
.brand{font-weight:700;font-size:18px;color:#fff;text-decoration:none;letter-spacing:-.02em}.brand span{color:#9ec7ff}
.nav a{color:#d6e4f5;text-decoration:none;font-size:14px;font-weight:500;margin-left:18px}.nav a:hover{color:#fff}
.cta{background:var(--accent);color:#fff;text-decoration:none;font-weight:600;font-size:14px;padding:9px 15px;border-radius:6px;margin-left:18px}
.hero{background:linear-gradient(180deg,var(--navy),var(--navy2));color:#fff;padding:36px 0 30px}.hero h1{color:#fff}.hero p{color:#cfe0f2;font-size:18px;max-width:60ch;margin:0}
.eyebrow{font-family:'IBM Plex Mono',monospace;font-size:12px;color:#9ec7ff;text-transform:uppercase;letter-spacing:.08em;margin:0 0 10px}
main{padding:8px 0 10px}.panel{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:22px;margin:22px 0}.live h2{margin-top:0}
.opp{border-top:1px solid var(--line);padding:13px 0;display:flex;flex-direction:column;gap:3px}.opp:first-of-type{border-top:0}.opp .t{font-weight:600;font-size:15.5px}
.opp .m{font-size:13px;color:var(--muted);display:flex;flex-wrap:wrap;gap:6px 14px}.opp .tag{background:#eef3f9;color:var(--navy);border-radius:4px;padding:1px 7px;font-size:12px;font-weight:600}.opp a.view{align-self:flex-start;font-size:13px;font-weight:600}
.empty{color:var(--body);font-size:15px;background:var(--paper);border:1px dashed var(--line);border-radius:8px;padding:16px}
.signup{background:var(--navy);color:#fff;border-radius:10px;padding:22px;margin:22px 0}.signup h2{color:#fff;margin-top:0}.signup p{color:#cfe0f2;margin:0 0 14px;font-size:15px}
.signup form{display:flex;gap:10px;flex-wrap:wrap}.signup input[type=email]{flex:1;min-width:220px;font:inherit;font-size:15px;padding:11px 13px;border:0;border-radius:6px}
.signup button{background:var(--accent);color:#fff;border:0;font:inherit;font-size:15px;font-weight:600;padding:11px 20px;border-radius:6px;cursor:pointer}
.signup .note{font-size:12.5px;color:#9ec7ff;margin:10px 0 0}.signup .msg{font-size:14px;margin:10px 0 0;font-weight:600}.hp{position:absolute;left:-9999px}
.prose p{color:var(--body)}.prose li{color:var(--body);margin:5px 0}.faq h3{margin-bottom:2px}.faq p{margin-top:2px;color:var(--body)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:8px 18px;margin:10px 0}.grid a{font-size:14px;text-decoration:none}
footer{border-top:1px solid var(--line);margin-top:30px;padding:24px 0 40px;color:var(--muted);font-size:13px}footer a{color:var(--muted)}.footlinks a{margin-right:16px}
</style></head><body>
<header><div class="wrap bar">
<a class="brand" href="{{P}}index.html">GovContract<span>Alerts</span></a>
<nav class="nav"><a href="{{P}}government-contracts-for-small-business.html">Small business</a><a href="{{P}}sam-registration-guide.html">SAM guide</a><a class="cta" href="#signup">Free alerts</a></nav>
</div></header>
"""

FOOT = """<footer><div class="wrap">
<p class="footlinks"><a href="{{P}}government-contracts-for-small-business.html">Small business contracts</a><a href="{{P}}sam-registration-guide.html">SAM registration</a><a href="{{P}}how-to-bid-on-state-contracts.html">Bid on state contracts</a></p>
<p>{{BRAND}} sends free weekly email alerts for new US government contract opportunities by trade and state. Independent alert service, not affiliated with SAM.gov or any government agency. Data from public procurement systems; confirm details on the official notice before bidding.</p>
</div></footer></body></html>"""

SIGNUP = """<div class="signup" id="signup"><h2>Free weekly {{TRADE}} contract alerts{{SS}}</h2>
<p>Get an email every week with new {{TRADE_LC}} opportunities{{SS}} - no charge, unsubscribe anytime.</p>
<form id="subForm"><input type="email" id="subEmail" placeholder="you@company.com" autocomplete="email" required>
<input type="text" id="subHp" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true"><button type="submit">Get free alerts</button></form>
<div class="msg" id="subMsg"></div><p class="note">Weekly alerts are free. Paid daily alerts with filters and a bid checklist are $39/month.</p></div>"""

SCRIPT = """<script>
var API="{{API}}",NAICS="{{NAICS}}",STATE="{{STATECODE}}",TRADE="{{TRADE_LC}}",STATENAME="{{STATE}}";
(function(){var box=document.getElementById("liveList");
if(box&&NAICS&&STATE){fetch(API+"/opportunities?naics="+NAICS+"&state="+STATE+"&limit=25").then(function(r){return r.json();}).then(function(d){
var o=(d&&d.opportunities)||[];if(!o.length){box.innerHTML='<div class="empty">No open '+TRADE+' contracts in '+STATENAME+' right now. New ones appear regularly - get the free weekly alert below and we will email you the moment one is posted.</div>';return;}
box.innerHTML=o.map(function(x){var dl=x.deadline?new Date(x.deadline).toLocaleDateString("en-US",{year:"numeric",month:"short",day:"numeric"}):"";var sa=x.set_aside?'<span class="tag">'+esc(x.set_aside)+'</span>':'';
return '<div class="opp"><div class="t">'+esc(x.title||"Opportunity")+'</div><div class="m">'+sa+'<span>'+esc(x.agency||"")+'</span>'+(dl?'<span>Closes '+dl+'</span>':'')+'</div>'+(x.ui_link?'<a class="view" href="'+esc(x.ui_link)+'" target="_blank" rel="noopener">View on SAM.gov</a>':'')+'</div>';}).join("");
}).catch(function(){box.innerHTML='<div class="empty">Live listings are updating - get the free weekly alert below.</div>';});}
var f=document.getElementById("subForm");if(f){f.addEventListener("submit",function(e){e.preventDefault();
var email=document.getElementById("subEmail").value.trim(),hp=document.getElementById("subHp").value,msg=document.getElementById("subMsg");
var at=email.indexOf("@"),dot=email.lastIndexOf(".");
if(!(at>0&&dot>at+1&&dot<email.length-1)){msg.style.color="#ffd7d7";msg.textContent="Please enter a valid email.";return;}
var btn=f.querySelector("button");btn.disabled=true;btn.textContent="Signing up...";
fetch(API+"/subscribe",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({email:email,trade:NAICS,state:STATE,website:hp,source:"site"})}).then(function(r){return r.json();}).then(function(){msg.style.color="#bfe8cf";msg.textContent="You are in - your first weekly alert is on its way.";f.reset();}).catch(function(){msg.style.color="#ffd7d7";msg.textContent="Something went wrong - please try again.";}).finally(function(){btn.disabled=false;btn.textContent="Get free alerts";});});}})();
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c];});}
</script>"""
