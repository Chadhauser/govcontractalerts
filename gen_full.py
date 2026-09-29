import os, html
from gc_tmpl import *
from gc_data import TRADES, STATES, STATE_PORTALS

def render(path, title, desc, body, P, naics="", statecode="", trade_lc="", state="", canon=None):
    doc = HEAD.replace("{{TITLE}}",esc(title)).replace("{{DESC}}",esc(desc)).replace("{{CANON}}",canon or (DOMAIN+"/"+path)).replace("{{P}}",P)
    doc += body
    doc += SCRIPT.replace("{{API}}",API).replace("{{NAICS}}",naics).replace("{{STATECODE}}",statecode).replace("{{TRADE_LC}}",esc(trade_lc)).replace("{{STATE}}",esc(state))
    doc += FOOT.replace("{{P}}",P).replace("{{BRAND}}",BRAND)
    full=os.path.join(OUT,path); os.makedirs(os.path.dirname(full) or ".",exist_ok=True); open(full,"w").write(doc)

def signup_block(trade,trade_lc,ss=""):
    return SIGNUP.replace("{{TRADE}}",esc(trade)).replace("{{TRADE_LC}}",esc(trade_lc)).replace("{{SS}}",ss)

count=0
# trade x state pages (depth 1 -> prefix ../)
for trade,trade_lc,naics,tslug in TRADES:
    for state,code,sslug in STATES:
        portal,purl = STATE_PORTALS.get(code,("your state's procurement portal","#"))
        title="Government Contracts for %s in %s (%s)"%(trade,state,YEAR)
        desc="Live US government contract opportunities for %s in %s, plus how to register on SAM.gov and win. Free weekly email alerts."%(trade_lc,state)
        body=('<div class="hero"><div class="wrap"><p class="eyebrow">Federal &amp; %s &middot; NAICS %s</p><h1>Government contracts for %s in %s</h1>'
              '<p>Open federal and %s opportunities for %s, updated from public procurement systems - with a plain-English guide to winning them.</p></div></div>'
              '<main class="wrap"><div class="panel live"><h2>Open %s contracts in %s this week</h2><div id="liveList"><div class="empty">Loading current opportunities...</div></div></div>%s'
              '<div class="prose"><h2>How to win %s government contracts in %s</h2>'
              '<h3>1. Register on SAM.gov (free)</h3><p>Every federal buyer requires an active <strong>SAM.gov</strong> registration and a Unique Entity ID (UEI). It is free - never pay a third party. See our <a href="../sam-registration-guide.html">SAM registration guide</a>.</p>'
              '<h3>2. Know your NAICS code - %s</h3><p>%s work is classified under <strong>NAICS %s</strong>. Buyers search by NAICS and it sets the small-business size standard. Make sure %s is on your SAM profile.</p>'
              '<h3>3. Use set-asides</h3><p>Many %s contracts are reserved for small businesses, and more for SDVOSB, WOSB, HUBZone and 8(a) firms. If you qualify, these cut your competition sharply.</p>'
              '<h3>4. Register with %s too</h3><p>%s agencies, counties, cities and school districts buy %s through <a href="%s" target="_blank" rel="noopener">%s</a>. Register there for state and local work SAM.gov does not list.</p>'
              '<h3>5. Win on the response, not just price</h3><p>Meet every mandatory requirement, price realistically, and evidence past performance. A missed compliance item is the top reason a qualified %s bid is rejected before scoring.</p></div>'
              '<div class="panel faq"><h2>%s contracts in %s - FAQ</h2><h3>How often are new opportunities posted?</h3><p>New federal and %s %s opportunities appear most weeks; our free alert emails the new ones.</p>'
              '<h3>Do I need to be a big company?</h3><p>No - most %s opportunities are small-business-friendly, many set aside for small firms.</p>'
              '<h3>Is there a paid option?</h3><p>Yes - $39/month for daily alerts with filters and a one-page bid checklist per opportunity.</p></div></main>')%(
              esc(state),naics,esc(trade_lc),esc(state),esc(state),esc(trade_lc),esc(trade_lc),esc(state),
              signup_block(trade,trade_lc," in "+esc(state)),
              esc(trade_lc),esc(state),naics,esc(trade),naics,naics,esc(trade_lc),esc(state),esc(state),esc(trade_lc),purl,esc(portal),esc(trade_lc),
              esc(trade),esc(state),esc(state),esc(trade_lc),esc(trade_lc))
        render("%s/%s.html"%(tslug,sslug),title,desc,body,"../",naics=naics,statecode=code,trade_lc=trade_lc,state=state)
        count+=1

# home
tr_links="".join('<a href="%s/texas.html">%s</a>'%(t[3],esc(t[0])) for t in TRADES[:12])
home_body=('<div class="hero"><div class="wrap"><p class="eyebrow">Free weekly government-contract alerts</p><h1>Never miss a government contract for your trade again</h1>'
 '<p>We watch SAM.gov and state procurement portals and email you the new opportunities for your trade and state - free, every week.</p></div></div>'
 '<main class="wrap">%s<div class="prose"><h2>How it works</h2><p><strong>1.</strong> Tell us your trade and state. <strong>2.</strong> We match new federal and state opportunities as they post. <strong>3.</strong> You get one clear email a week - or upgrade to daily alerts with filters and a bid checklist for $39/month.</p>'
 '<h2>Popular guides</h2><p><a href="government-contracts-for-small-business.html">Government contracts for small business</a> &middot; <a href="sam-registration-guide.html">SAM registration guide</a> &middot; <a href="how-to-bid-on-state-contracts.html">How to bid on state contracts</a></p>'
 '<h2>Browse by trade</h2><div class="grid">%s</div></div></main>')%(signup_block("government contract","government contract"),tr_links)
render("index.html","%s - Free US Government Contract Alerts by Trade &amp; State"%BRAND,
 "Free weekly email alerts for new US government contract opportunities by trade and state, from SAM.gov and state portals.",home_body,"",
 trade_lc="government contract",state="the US",canon=DOMAIN+"/")

def money(path,title,desc,h1,eyebrow,inner):
    body=('<div class="hero"><div class="wrap"><p class="eyebrow">%s</p><h1>%s</h1></div></div><main class="wrap"><div class="prose">%s</div>%s</main>')%(eyebrow,esc(h1),inner,signup_block("government contract","government contract"))
    render(path,title,desc,body,"",trade_lc="government contract",state="the US")

money("sam-registration-guide.html","SAM.gov Registration Guide for Small Businesses (2026) | "+BRAND,
 "Step-by-step SAM.gov registration: get your UEI, add NAICS codes, and start bidding on federal contracts for free.","SAM.gov registration guide for small businesses (2026)","Free guide",
 "<p><strong>SAM.gov registration is free and mandatory</strong> to win federal contracts. Ignore anyone offering to register you for a fee.</p><h2>Step 1 - Login.gov account</h2><p>SAM.gov sign-in runs through Login.gov; create one with two-factor.</p><h2>Step 2 - Unique Entity ID (UEI)</h2><p>The UEI replaced the DUNS number; request it in SAM.gov by confirming your legal name and address exactly.</p><h2>Step 3 - Entity registration</h2><p>Enter business details, NAICS codes, size, banking for payment, and reps &amp; certs. Accuracy avoids delays.</p><h2>Step 4 - Add NAICS codes</h2><p>Your NAICS codes decide which opportunities you match and your size standards.</p><h2>Step 5 - Renew yearly</h2><p>Registration lapses annually; let it lapse and you cannot be awarded.</p><h2>How long?</h2><p>Allow one to two weeks, mostly the entity-validation step.</p>")

money("government-contracts-for-small-business.html","Government Contracts for Small Business: How to Start (2026) | "+BRAND,
 "How small businesses win US government contracts: SAM.gov, NAICS, set-asides and alerts. Free plain-English guide.","Government contracts for small business: how to start (2026)","Free guide",
 "<h2>Why small businesses win government work</h2><p>Federal law reserves a large share of contracts for small businesses, and more for SDVOSB, WOSB, HUBZone and 8(a) firms.</p><h2>Five steps to your first contract</h2><p><strong>1.</strong> Register on SAM.gov (see the <a href='sam-registration-guide.html'>SAM guide</a>). <strong>2.</strong> Identify your NAICS codes. <strong>3.</strong> Check set-aside eligibility. <strong>4.</strong> Register with state and local buyers (<a href='how-to-bid-on-state-contracts.html'>how to bid on state contracts</a>). <strong>5.</strong> Track opportunities and bid.</p><h2>Start with alerts, not searching</h2><p>The hardest part is seeing the right opportunities in time - get a free weekly alert for your trade and state below.</p>")

money("how-to-bid-on-state-contracts.html","How to Bid on State Government Contracts (2026) | "+BRAND,
 "How to register and bid on US state and local government contracts, portal by portal. Free weekly alerts by state.","How to bid on state government contracts (2026)","Free guide",
 "<p>Federal is only half the market. States, counties, cities and school districts buy constantly through their own procurement portals.</p><h2>1. Register on your state portal</h2><p>Each state runs a vendor registration and bid system (for example Texas SmartBuy, Cal eProcure, MyFloridaMarketPlace).</p><h2>2. Add your commodity/NAICS codes</h2><p>State systems match you to opportunities by code, like SAM.gov.</p><h2>3. Check state-level set-asides</h2><p>Many states run small, minority, women and veteran-owned business programs with their own certifications.</p><h2>4. Watch local buyers too</h2><p>Counties, cities and school districts often post separately from the state portal.</p><h2>5. Get alerts</h2><p>Sign up below for free weekly alerts for your trade and state.</p>")

# sitemap + robots
urls=[DOMAIN+"/",DOMAIN+"/government-contracts-for-small-business.html",DOMAIN+"/sam-registration-guide.html",DOMAIN+"/how-to-bid-on-state-contracts.html"]
for trade,trade_lc,naics,tslug in TRADES:
    for state,code,sslug in STATES:
        urls.append("%s/%s/%s.html"%(DOMAIN,tslug,sslug))
NL=chr(10)
sm='<?xml version="1.0" encoding="UTF-8"?>'+NL+'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+NL+"".join("<url><loc>%s</loc></url>"%u+NL for u in urls)+"</urlset>"+NL
open(os.path.join(OUT,"sitemap.xml"),"w").write(sm)
open(os.path.join(OUT,"robots.txt"),"w").write("User-agent: *"+NL+"Allow: /"+NL+"Sitemap: %s/sitemap.xml"%DOMAIN+NL)

print("trade_state_pages:",count)
print("total_urls_in_sitemap:",len(urls))
import glob
print("html_files_written:",len(glob.glob(OUT+"/**/*.html",recursive=True)))
