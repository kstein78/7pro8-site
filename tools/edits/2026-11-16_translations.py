"""16 Nov 2026: the translations of the founders' Russian rewrite, approved by
Kosta (content/i18n/review/2026-11-16.md), put into EN, DE and SR."""
import sys,json,glob
sys.path.insert(0,'tools'); import i18n
def load(f):
    t=open(f).read(); d=json.load(open(f)); assert json.dumps(d,ensure_ascii=False,indent=2)+'\n'==t,f; return d
EN=load('content/en.json')
tabs={l:{f:load(f) for f in sorted(glob.glob(f'content/i18n/{l}*.json'))} for l in ('de','sr')}
T={l:{k:v for d in tabs[l].values() for k,v in d.items()} for l in tabs}
NEW={'de':'content/i18n/de.7.json','sr':'content/i18n/sr.7.json'}
olds=[]
def put(en,de,sr):
    tabs['de'][NEW['de']][i18n.key(en)]=de; tabs['sr'][NEW['sr']][i18n.key(en)]=sr
def old(en): return T['de'][i18n.key(en)],T['sr'][i18n.key(en)]
def swap(o,n,de,sr,count=1):
    global EN
    s=json.dumps(EN,ensure_ascii=False); a=json.dumps(o,ensure_ascii=False)
    assert s.count(a)==count,(o[:60],s.count(a)); EN=json.loads(s.replace(a,json.dumps(n,ensure_ascii=False))); olds.append(o); put(n,de,sr)
def first(s): return s[:s.index('. ')+1]
def butlast(s): return s[:s.rstrip('.').rindex('. ')+1]

# 1
swap("A partition changes what the car is for. The engineering question that decides whether an owner will accept it is the second one: what does the conversion take away?",
     "A partition changes what the car is for. But before installation the owner wants to know exactly what will change in his series-production car.",
     "Eine Trennwand verändert den Zweck des Fahrzeugs. Doch vor dem Einbau will der Besitzer genau wissen, was sich an seinem Serienfahrzeug ändert.",
     "Pregrada menja namenu vozila. Ali pre ugradnje vlasnik želi da zna šta će se tačno promeniti na njegovom serijskom vozilu.")
# 2
o="Design, engineering, tooling manufacture and production are all done in-house. A partner does not have to coordinate several subcontractors, and there is nowhere for responsibility to fall between them."
de,sr=old(o)
swap(o,first(o)+" A partner does not need to approach different subcontractors and coordinate their work to get a quality product on schedule.",
     first(de)+" Ein Partner muss sich nicht an verschiedene Zulieferer wenden und deren Arbeit koordinieren, um ein hochwertiges Produkt termingerecht zu erhalten.",
     first(sr)+" Partner ne mora da se obraća različitim podizvođačima i koordinira njihov rad da bi dobio kvalitetan proizvod u planiranom roku.")
# 3
swap("Development and tooling are entirely ours — including joint projects where the partner produces part of the panels.",
     "We carry out development and tooling ourselves — including for joint projects in which the partner takes on part of the work.",
     "Entwicklung und Werkzeugbau übernehmen wir selbst — auch bei gemeinsamen Projekten, in denen der Partner einen Teil der Arbeiten ausführt.",
     "Razvoj i alate radimo sami — uključujući i zajedničke projekte u kojima deo posla preuzima partner.")
# 4
o="A partner can take on exactly the share of production it is equipped for — from a complete turnkey kit down to a single structural frame with mechanisms. Development and tooling stay with us in every case."
de,sr=old(o)
swap(o,butlast(o)+" Development and tooling are done by us in every case.",butlast(de)+" Entwicklung und Werkzeugbau liegen in jedem Fall bei uns.",butlast(sr)+" Razvoj i alati su u svakom slučaju naš posao.")
# 5
o="A partition fitted by hand exists in a single copy: the next one will be different. Tooling is what turns a good result into a repeatable one."
de,sr=old(o)
swap(o,first(o)+" Tooling is what lets the same result be repeated for as long as needed.",first(de)+" Werkzeuge machen es möglich, dasselbe Ergebnis beliebig lange zu wiederholen.",first(sr)+" Alati omogućavaju da se isti rezultat ponavlja koliko god je potrebno.")
# 6
swap("For a partner that means two things that show up directly in the workshop's costing: installation time can be planned, and there is no rework.",
     "These points matter a great deal to a partner because they shape the economics of the project: installation time can be planned, and there is no unforeseen rework or downtime.",
     "Für den Partner sind das entscheidende Punkte, die die Wirtschaftlichkeit des Projekts bestimmen: Die Einbauzeit ist planbar, unvorhergesehene Nacharbeit und Stillstand entfallen.",
     "Za partnera su to suštinski važne stvari koje utiču na ekonomiju projekta: vreme montaže može da se planira, a nema nepredviđenih prepravki ni zastoja.")
# 7
o="Eight models have been taken through to production tooling. Volume on those scales without any new investment in development."
de,sr=old(o)
swap(o,first(o)+" Their production can be scaled up at any time without new investment in development.",first(de)+" Ihre Fertigung lässt sich jederzeit ohne neue Entwicklungsinvestitionen hochskalieren.",first(sr)+" Njihova proizvodnja može se u svakom trenutku povećati bez novih ulaganja u razvoj.")
# 8
swap("New generation ready 2026 · 14 kits 2015–2019","New generation developed in 2026 · 14 kits 2015–2019","Neue Generation 2026 entwickelt · 14 Bausätze 2015–2019","Nova generacija razvijena 2026. · 14 kompleta 2015–2019")
swap("New generation, ready 2026","New generation developed in 2026","Neue Generation 2026 entwickelt","Nova generacija razvijena 2026.")
# 9
o="Every project since 2007, including the early one-off works and the VW Multivan series, is listed on the availability page with years, volumes and the nature of each project."
de,sr=old(o); assert "Art des Projekts" in de and "vrstom svakog projekta" in sr,(de,sr)
swap(o,o.replace("the nature of each project","the complexity of each project"),de.replace("Art des Projekts","Komplexität jedes Projekts"),sr.replace("vrstom svakog projekta","složenošću svakog projekta"))
# 10
swap("Three states, and the difference between them is what a partner has to invest before the first kit arrives.",
     "Three stages of readiness for our products; what sets them apart is how far each has been realised.",
     "Drei Reifegrade unserer Produkte — sie unterscheiden sich im Grad der Umsetzung.",
     "Tri faze spremnosti naših proizvoda, a razlika među njima je u stepenu realizacije.")
# 11: footnote -> callout
r=[p for p in EN['pages'] if p.get('slug')=='range'][0]; lu=[b for b in r['blocks'] if b['type']=='lineup'][0]
olds.append(lu.pop('footnote'))
note={"type":"note","title":"Full-cycle interior development",
 "body":["Besides partitions, we develop and produce rear modules — a platform frame with a console armrest for fitting an optional rear bench — and any interior panels to a bespoke design.",
         "At a partner's request we can take on the full development cycle for any element of the interior — up to a completely bespoke version of the car's interior.",
         "For cooperation and business expansion, contact Evgenii Abramov directly."],
 "action":{"label":"Write to Evgenii Abramov","href":"https://t.me/Eugy01"}}
r['blocks'].insert(r['blocks'].index(lu)+1,note)
for en,de,sr in ((note['title'],"Innenraumentwicklung aus einer Hand","Razvoj enterijera u punom ciklusu"),
    (note['body'][0],"Neben Trennwänden entwickeln und fertigen wir Heckmodule — einen Podestrahmen mit Konsole und Armlehne für eine optionale Rückbank — sowie beliebige Innenraumverkleidungen nach individuellem Design.",
     "Pored pregrada razvijamo i proizvodimo zadnji modul — ram-podijum sa konzolom i naslonom za ruke za ugradnju opcionog zadnjeg sedišta — i bilo koje unutrašnje panele po individualnom dizajnu."),
    (note['body'][1],"Auf Wunsch des Partners können wir den kompletten Entwicklungszyklus für jedes Element des Innenraums übernehmen — bis hin zu einer vollständig eigenen Version des Fahrzeuginterieurs.",
     "Na zahtev partnera možemo da preuzmemo pun ciklus razvoja bilo kog elementa enterijera — sve do potpuno sopstvene verzije enterijera vozila."),
    (note['body'][2],"Für Zusammenarbeit und Geschäftserweiterung wenden Sie sich direkt an Evgenii Abramov.","Za saradnju i širenje poslovanja obratite se direktno Evgeniju Abramovu."),
    (note['action']['label'],"Evgenii Abramov schreiben","Pišite Evgeniju Abramovu")): put(en,de,sr)
# 12
swap("Price is a function of annual volume, so we quote against a model, a market and a plan rather than publishing a list.",
     "Cost is calculated from technological readiness and potential production volume, so quotes for new developments are always individual; price lists exist only for series products already in production.",
     "Der Preis ergibt sich aus der technologischen Reife und dem möglichen Produktionsvolumen. Kalkulationen für Neuentwicklungen sind daher immer individuell; Preislisten gibt es nur für Serienprodukte, die bereits gefertigt werden.",
     "Cena se računa na osnovu tehnološke spremnosti i potencijalnog obima proizvodnje, pa su proračuni za nove razvoje uvek individualni, a cenovnici postoje samo za serijske proizvode koji su već u proizvodnji.")
# 13
swap("The partner receives a kit ready for installation. Everything up to that point is ours; everything from trimming onwards is the partner's. The line is drawn in the same place on every project.",
     "The partner receives a kit ready for installation. What remains is to trim it and install the partition. At the partner's request we are ready to discuss other arrangements and find joint solutions.",
     "Der Partner erhält einen einbaufertigen Bausatz. Ihm bleiben der Bezug und der Einbau der Trennwand. Auf Wunsch des Partners besprechen wir gern andere Varianten und finden gemeinsame Lösungen.",
     "Partner dobija komplet spreman za montažu. Preostaje mu da uradi presvlačenje i ugradi pregradu. Na zahtev partnera spremni smo da razgovaramo o drugim varijantama i nađemo zajednička rešenja.")
# 14
swap("What kind of partner each class needs","Possible kinds of partnership","Mögliche Formen der Partnerschaft","Mogući oblici partnerstva")
# 15
p=[p for p in EN['pages'] if p.get('slug')=='partners'][0]; b=[b for b in p['blocks'] if b.get('title')=="How pricing works"]; assert len(b)==1; b=b[0]
olds.append(b['title']); olds+=b['body']
b['title']="Why don't we publish price lists?"
b['body']=["The price of a finished product depends on the technological groundwork in place, the readiness of the tooling and, above all, the planning of production volumes. The price of a partition is always agreed with the partner in advance. A larger batch can bring it down; if orders fall, it is reviewed as well.",
 "Delivery follows a plan that can be adjusted — but in good time. The production cycle of a kit is four months, but with an agreed volume and timely advance payment the product ships from stock within a predictable time.",
 "For the EU, US and Canadian markets we supply partitions from Serbia, an EU candidate country (Serbian industrial goods have entered the Union free of customs duty since 2000; this regime was later written into the Stabilisation and Association Agreement). For a partner in the EU that means no duty on a kit — only import VAT and the usual customs clearance. Outside the EU the importing country's tariff applies. For deliveries to other countries we will choose the best arrangement and country of shipment.",
 "Tell us the model, the market and the planned quantity, and we will send indicative pricing, scope of supply and a delivery plan."]
DE=["Warum veröffentlichen wir keine Preislisten?",
 "Der Preis eines fertigen Produkts hängt von der vorhandenen technologischen Basis, der Bereitschaft der Werkzeuge und vor allem von der Planung der Produktionsmengen ab. Der Preis einer Trennwand wird immer im Voraus mit dem Partner vereinbart. Bei größeren Losen kann er sinken, bei rückläufigen Bestellungen wird er ebenfalls überprüft.",
 "Die Lieferung folgt einem Plan, der angepasst werden kann — aber rechtzeitig. Der Produktionszyklus eines Bausatzes beträgt vier Monate; bei vereinbarter Menge und rechtzeitiger Anzahlung wird das Produkt innerhalb einer planbaren Frist ab Lager versandt.",
 "Für die Märkte der EU, der USA und Kanadas liefern wir Trennwände aus Serbien, einem EU-Beitrittskandidaten (serbische Industriewaren gelangen seit 2000 zollfrei in die Union; diese Regelung wurde später im Stabilisierungs- und Assoziierungsabkommen festgeschrieben). Für einen Partner in der EU bedeutet das: kein Zoll auf den Bausatz — nur Einfuhrumsatzsteuer und die übliche Zollabfertigung. Außerhalb der EU gilt der Tarif des Einfuhrlandes. Für Lieferungen in andere Länder wählen wir das optimale Vorgehen und das Versandland.",
 "Nennen Sie uns Modell, Markt und geplante Stückzahl — wir schicken Ihnen Richtwerte zum Preis, den Lieferumfang und einen Lieferplan."]
SR=["Zašto ne objavljujemo cenovnike?",
 "Na cenu gotovog proizvoda utiču postojeća tehnološka osnova, spremnost alata i, pre svega, planiranje obima proizvodnje. Cena pregrade se uvek unapred dogovara sa partnerom. Pri većoj seriji može da se smanji, a pri manjem broju porudžbina se takođe preispituje.",
 "Isporuka ide po planu koji može da se menja — ali blagovremeno. Proizvodni ciklus jednog kompleta traje četiri meseca, ali uz dogovoreni obim isporuka i blagovremeno avansno plaćanje proizvod se otprema iz magacina u predvidivom roku.",
 "Za tržišta EU, SAD i Kanade pregrade isporučujemo iz Srbije, zemlje kandidata za članstvo u EU (srpska industrijska roba od 2000. godine ulazi u Uniju bez carine; taj režim je kasnije potvrđen Sporazumom o stabilizaciji i pridruživanju). Za partnera u EU to znači da na komplet nema carine — ostaju samo uvozni PDV i uobičajeno carinjenje. Van EU važi tarifa zemlje uvoza. Za isporuke u druge zemlje izabraćemo optimalnu šemu i zemlju otpreme.",
 "Navedite model, tržište i planiranu količinu — poslaćemo okvirne cene, obim isporuke i plan otpreme."]
for en,de,sr in zip([b['title']]+b['body'],DE,SR): put(en,de,sr)

s=json.dumps(EN,ensure_ascii=False)
for o in olds:
    if json.dumps(o,ensure_ascii=False) not in s:
        for l in tabs:
            for d in tabs[l].values(): d.pop(i18n.key(o),None)
open('content/en.json','w').write(json.dumps(EN,ensure_ascii=False,indent=2)+'\n')
for l in tabs:
    for f,d in tabs[l].items(): open(f,'w').write(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('ok',len(olds))
