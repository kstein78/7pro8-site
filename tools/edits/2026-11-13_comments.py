import sys,json,glob
sys.path.insert(0,'tools'); import i18n
def load(f):
    t=open(f).read(); d=json.load(open(f)); assert json.dumps(d,ensure_ascii=False,indent=2)+'\n'==t,f; return d
EN=load('content/en.json'); RU=load('content/ru.json')
tabs={l:{f:load(f) for f in sorted(glob.glob(f'content/i18n/{l}*.json'))} for l in ('de','sr')}
T={l:{k:v for d in tabs[l].values() for k,v in d.items()} for l in tabs}
NEW={'de':'content/i18n/de.7.json','sr':'content/i18n/sr.7.json'}
olds=set()
def put(en,de,sr):
    tabs['de'][NEW['de']][i18n.key(en)]=de; tabs['sr'][NEW['sr']][i18n.key(en)]=sr
def old(en): return T['de'][i18n.key(en)],T['sr'][i18n.key(en)]
def page(d,s): return [p for p in d['pages'] if p.get('slug')==s][0]
def find(n,pred,out=None):
    out=[] if out is None else out
    if isinstance(n,dict):
        if pred(n): out.append(n)
        for v in n.values(): find(v,pred,out)
    elif isinstance(n,list):
        for v in n: find(v,pred,out)
    return out
def one(d,pred,what):
    r=find(d,pred); assert len(r)==1,(what,len(r)); return r[0]
def set_text(e,r,key,en_new,ru_new,de,sr):
    olds.add(e[key]); e[key]=en_new; r[key]=ru_new; put(en_new,de,sr)
def rest(s): i=s.index('. '); return s[i+2:]
def first(s): return s[:s.index('. ')+1]

# 1. Maybach: no tables (they are in the factory console); curved glass instead
for d,o,n in ((EN,"Folding work tables in the body of the partition","Curved electrochromic glass — more legroom for the rear passengers"),
              (RU,"Откидные рабочие столики в теле перегородки","Гнутое электрохромное стекло — больше места для ног пассажиров")):
    b=one(d,lambda x: isinstance(x.get('spec'),list) and o in x['spec'],'maybach spec'); b['spec'][b['spec'].index(o)]=n
olds.add("Folding work tables in the body of the partition")
put("Curved electrochromic glass — more legroom for the rear passengers","Gebogenes elektrochromes Glas — mehr Beinfreiheit für die Fondpassagiere","Zakrivljeno elektrohromno staklo — više prostora za noge putnika pozadi")
# 2. Maybach lead: plastics -> surface panels
e=one(EN,lambda x: x.get('lead','').startswith("A joint production project: the partner produces the plastics"),'lead en')
r=one(RU,lambda x: x.get('lead','').startswith("Проект совместного производства: партнёр изготавливает пластики"),'lead ru')
set_text(e,r,'lead',"A joint production project: the partner produces the surface panels, we produce the metal frame with the mechanism.",
 "Проект совместного производства: партнёр изготавливает лицевые панели, мы — металлический каркас с механизмом.",
 "Ein Gemeinschaftsprojekt: Der Partner fertigt die Sichtpaneele, wir den Metallrahmen mit Mechanik.",
 "Projekat zajedničke proizvodnje: partner izrađuje vidljive panele, a mi metalni ram sa mehanizmom.")
# 3. acoustic separation (Kosta)
e=one(EN,lambda x: x.get('title')=="Acoustic separation",'acoustic en'); r=one(RU,lambda x: x.get('title')=="Акустическое разделение",'acoustic ru')
set_text(e,r,'text',"A physical partition with the glass raised separates the rear from the front. The partition greatly reduces how much of a conversation the driver and security can hear. Confidentiality comes from the construction, not from trust.",
 "Физическая перегородка с поднятым стеклом отделяет заднюю зону от передней. Перегородка значительно снижает слышимость разговора для водителя и охраны. Конфиденциальность обеспечена конструкцией, а не доверием.",
 "Eine physische Trennwand mit hochgefahrener Scheibe trennt den Fond vom vorderen Bereich. Die Trennwand verringert deutlich, wie viel Fahrer und Sicherheitspersonal von einem Gespräch hören. Die Vertraulichkeit sichert die Konstruktion, nicht das Vertrauen.",
 "Fizička pregrada sa podignutim staklom odvaja zadnju zonu od prednje. Pregrada znatno smanjuje koliko vozač i obezbeđenje mogu da čuju od razgovora. Poverljivost obezbeđuje konstrukcija, a ne poverenje.")
# 4. category change, Russian wording only ("разъездная")
r=one(RU,lambda x: x.get('title')=="Смена категории автомобиля",'category')
r['text']="Представительский автомобиль становится автомобилем для поездок с водителем: транспорт первых лиц, дипломатические миссии, VIP-трансфер, сопровождение. Другой класс задач и другой ценовой сегмент услуги."
# 5. "Our answer ..." out
for d,start in ((EN,"Our answer is not a promise"),(RU,"Наш ответ — не обещание")):
    b=one(d,lambda x: isinstance(x.get('body'),list) and any(isinstance(p,str) and p.startswith(start) for p in x['body']),'answer')
    p=[p for p in b['body'] if p.startswith(start)][0]; b['body'].remove(p)
    if d is EN: olds.add(p)
# 6. reversibility without removal times
e=one(EN,lambda x: x.get('title')=="Reversibility",'rev en'); r=one(RU,lambda x: x.get('title')=="Обратимость",'rev ru')
de,sr=old(e['text'])
set_text(e,r,'text',"When needed, the car returns to factory configuration. "+rest(e['text']),
 "При необходимости автомобиль возвращается в заводскую конфигурацию. "+rest(r['text']),
 "Bei Bedarf wird das Fahrzeug in den Serienzustand zurückversetzt. "+rest(de),
 "Po potrebi se vozilo vraća u fabričku konfiguraciju. "+rest(sr))
# 7. "In short": complements factory engineering; nothing about taking it off
e=one(EN,lambda x: x.get('title')=="In short" and x.get('type')=='note','short en'); r=one(RU,lambda x: x.get('title')=="Итог" and x.get('type')=='note','short ru')
de,sr=old(e['body'][0]); olds.add(e['body'][0])
e['body'][0]=first(e['body'][0])+" The conversion does not compete with factory engineering — it complements it."
r['body'][0]=first(r['body'][0])+" Доработка не конкурирует с инженерией завода — она дополняет её."
put(e['body'][0],first(de)+" Der Umbau konkurriert nicht mit der Werksentwicklung — er ergänzt sie.",first(sr)+" Prerada ne konkuriše fabričkom inženjeringu — ona ga dopunjuje.")
# 8. two classes without kit counts (Kosta)
for o_en,o_ru in (("Simple — 3 to 4 kits a year","Простые — 3–4 комплекта в год"),("Complex — 30 to 40 kits a year","Сложные — 30–40 комплектов в год")):
    e=one(EN,lambda x: x.get('title')==o_en,o_en); r=one(RU,lambda x: x.get('title')==o_ru,o_ru); de,sr=old(o_en)
    set_text(e,r,'title',o_en.split(' — ')[0],o_ru.split(' — ')[0],de.split(' — ')[0],sr.split(' — ')[0])
# 9. timing: for a project in series production; no removal time (both blocks)
e=one(EN,lambda x: x.get('title')=="What the timing looks like from the partner's side",'timing en'); r=one(RU,lambda x: x.get('title')=="Как выглядят сроки со стороны партнёра",'timing ru')
set_text(e,r,'title',"What the timing looks like from the partner's side for a project in series production","Как выглядят сроки со стороны партнёра для проекта в стадии серийного производства",
 "Wie die Termine aus Sicht des Partners bei einem Projekt in Serienfertigung aussehen","Kako izgledaju rokovi iz ugla partnera za projekat u fazi serijske proizvodnje")
for en_o,ru_o in (("Installation of a simple partition by qualified technicians. Removal takes the same","Монтаж простой перегородки квалифицированными специалистами. Демонтаж — столько же"),
                  ("Installation of a simple partition by qualified technicians; removal takes the same","Монтаж простой перегородки квалифицированными специалистами; демонтаж — столько же")):
    e=one(EN,lambda x: x.get('label')==en_o,en_o); r=one(RU,lambda x: x.get('label')==ru_o,ru_o)
    set_text(e,r,'label',"Installation of a simple partition by qualified technicians","Монтаж простой перегородки квалифицированными специалистами",
     "Einbau einer einfachen Trennwand durch qualifiziertes Personal","Montaža jednostavne pregrade od strane kvalifikovanih stručnjaka")
# 10. capabilities: closing "a new model takes up to a year" out
for d,t in ((EN,"A new model takes up to a year"),(RU,"Новая модель занимает до года")):
    p=page(d,'capabilities'); b=[b for b in p['blocks'] if b.get('title')==t]; assert len(b)==1; p['blocks'].remove(b[0])
    if d is EN: olds.update([b[0]['title'],b[0]['text']])
# 11/12. 70 000 € out
e=one(EN,lambda x: isinstance(x.get('body'),list) and any('€70,000 and up to a year' in s for s in x['body']),'70 en')
r=one(RU,lambda x: isinstance(x.get('body'),list) and any('70 000 € и до года' in s for s in x['body']),'70 ru')
de,sr=old(e['body'][0]); olds.add(e['body'][0])
e['body'][0]="Before a model goes into series production, we build the tooling for it. "+rest(e['body'][0])
r['body'][0]="Прежде чем запускать модель в серию, мы изготавливаем для неё оснастку. "+rest(r['body'][0])
put(e['body'][0],"Bevor ein Modell in Serie geht, bauen wir die Werkzeuge dafür. "+rest(de),"Pre nego što model uđe u serijsku proizvodnju, izrađujemo alate za njega. "+rest(sr))
e=one(EN,lambda x: isinstance(x.get('body'),list) and any(s.startswith('Around €70,000') for s in x['body']),'rr en')
r=one(RU,lambda x: isinstance(x.get('body'),list) and any(s.startswith('В разработку перегородки нового поколения вложено') for s in x['body']),'rr ru')
de,sr=old(e['body'][0]); olds.add(e['body'][0])
e['body'][0]="Development of the new-generation partition is complete. "+rest(e['body'][0])
r['body'][0]="Разработка перегородки нового поколения завершена. "+rest(r['body'][0])
put(e['body'][0],"Die Entwicklung der Trennwand für die neue Generation ist abgeschlossen. "+rest(de),"Razvoj pregrade za novu generaciju je završen. "+rest(sr))
# 13. line 1 caption
e=one(EN,lambda x: x.get('src')=='portfolio/v-class-line-1/03.jpg','l1 en'); r=one(RU,lambda x: x.get('src')=='portfolio/v-class-line-1/03.jpg','l1 ru')
set_text(e,r,'caption',"The partition in the car","Перегородка в автомобиле","Die Trennwand im Fahrzeug","Pregrada u vozilu")
# 14/15. equipment lists
L1_EN=["Two electrically operated fold-out seats with document pockets","Central sliding drawer, electrically operated","Electrochromic glass with electric raise-and-lower mechanism","Samsung 43-inch television with electric lift","Ambient lighting","Clock","Umbrella holders"]
L1_RU=["Два раскладных сиденья с электроприводами и карманами для бумаг","Центральный выдвижной ящик с электроприводом","Электрохромное стекло с электрическим механизмом подъёма-опускания","Телевизор Samsung 43″ с электрическим подъёмом","Контурная подсветка","Часы","Крепления для зонтов"]
e=one(EN,lambda x: x.get('spec')==["Two electrically operated folding seats","Central folding box, electrically operated","Electrochromic glass with electric raise-and-lower mechanism","Samsung 43-inch television with electric lift"],'l1 spec en')
r=one(RU,lambda x: isinstance(x.get('spec'),list) and "Центральный откидной бокс с электроприводом" in x['spec'],'l1 spec ru')
olds.update(e['spec']); e['spec']=L1_EN; r['spec']=L1_RU
for en,de,sr in ((L1_EN[0],"Zwei elektrisch betätigte Klappsitze mit Dokumententaschen","Dva sklopiva sedišta na električni pogon sa džepovima za dokumenta"),
                 (L1_EN[1],"Zentrale ausfahrbare Schublade, elektrisch betätigt","Centralna izvlačna fioka na električni pogon"),
                 ("Ambient lighting","Ambientebeleuchtung","Ambijentalno osvetljenje"),("Clock","Uhr","Sat"),("Umbrella holders","Schirmhalterungen","Držači za kišobrane"),
                 ("Audio preparation (speakers)","Akustikvorbereitung (Lautsprecher)","Akustička priprema (zvučnici)"),("Umbrella holder","Schirmhalterung","Držač za kišobran")):
    put(en,de,sr)
e=one(EN,lambda x: isinstance(x.get('spec'),list) and "Central sliding boxes, electrically operated" in x['spec'],'l2 spec en')
r=one(RU,lambda x: isinstance(x.get('spec'),list) and "Центральные выдвижные боксы с электроприводом" in x['spec'],'l2 spec ru')
e['spec']+=["Audio preparation (speakers)","Umbrella holder","Clock","Ambient lighting"]
r['spec']+=["Акустическая подготовка (динамики)","Крепление для зонта","Часы","Контурная подсветка"]
# 16. line 2 caption
e=one(EN,lambda x: x.get('src')=='portfolio/v-class-line-2/02.jpg','l2 en'); r=one(RU,lambda x: x.get('src')=='portfolio/v-class-line-2/02.jpg','l2 ru')
for k in ('alt','caption'): set_text(e,r,k,"The partition in the car with the seats folded out","Перегородка в машине с открытыми креслами","Die Trennwand im Fahrzeug mit ausgeklappten Sitzen","Pregrada u vozilu sa rasklopljenim sedištima")
# 17. production technologies
e=one(EN,lambda x: x.get('text')=="The kit ships assembled and checked. What is left for the partner is trimming, fitting and connection.",'prod en')
r=one(RU,lambda x: x.get('text')=="Комплект отгружается собранным и проверенным. Партнёру остаётся обтяжка, монтаж и подключение.",'prod ru')
de,sr=old(e['text'])
set_text(e,r,'text',e['text']+" We make active use of current technology: laser scanning, additive manufacturing, CAD/CAM systems on licensed software, vacuum and infusion moulding of parts. We keep looking for ways to raise the technological level of production.",
 r['text']+" Мы активно используем современные технологии: лазерное сканирование, аддитивное производство, CAD/CAM-системы на лицензионном программном обеспечении, вакуумную и инфузионную формовку деталей. Нас интересует повышение технологического уровня производства.",
 de+" Wir setzen aktiv moderne Technologien ein: Laserscanning, additive Fertigung, CAD/CAM-Systeme mit lizenzierter Software, Vakuum- und Infusionsformen von Bauteilen. Uns geht es darum, das technologische Niveau der Fertigung weiter zu steigern.",
 sr+" Aktivno koristimo savremene tehnologije: lasersko skeniranje, aditivnu proizvodnju, CAD/CAM sisteme sa licenciranim softverom, vakuumsko i infuziono oblikovanje delova. Zanima nas podizanje tehnološkog nivoa proizvodnje.")
# 18. CAD: mechanism and surfaces side by side
for d in (EN,RU):
    b=one(d,lambda x: isinstance(x.get('image'),dict) and x['image'].get('src')=='capabilities/cad-model.jpg','cad')
    im=b.pop('image')
    if d is EN:
        b['figure']={"images":[{"src":"capabilities/cad-model.jpg","alt":im['alt']},{"src":"vle/cad-development.jpg","alt":"CAD model of the partition's surfaces"}],
                     "caption":"Surface and mechanism engineering — the CAD models the tooling is built from"}
        olds.add(im['caption'])
    else:
        b['figure']={"images":[{"src":"capabilities/cad-model.jpg","alt":im['alt']},{"src":"vle/cad-development.jpg","alt":"CAD-модель поверхностей перегородки"}],
                     "caption":"Инжиниринг поверхностей и механизмов — CAD-модели, по которым делается оснастка"}
put("CAD model of the partition's surfaces","CAD-Modell der Flächen der Trennwand","CAD model površina pregrade")
put("Surface and mechanism engineering — the CAD models the tooling is built from","Flächen- und Mechanik-Engineering — die CAD-Modelle, nach denen das Werkzeug gebaut wird","Inženjering površina i mehanizama — CAD modeli po kojima se izrađuje alat")

s=json.dumps(EN,ensure_ascii=False)
for o in olds:
    if json.dumps(o,ensure_ascii=False) not in s:
        for l in tabs:
            for dd in tabs[l].values(): dd.pop(i18n.key(o),None)
for f,d in (('content/en.json',EN),('content/ru.json',RU)): open(f,'w').write(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
for l in tabs:
    for f,d in tabs[l].items(): open(f,'w').write(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('ok')
