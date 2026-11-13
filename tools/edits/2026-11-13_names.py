import sys,json,glob,re
sys.path.insert(0,'tools'); import i18n
def load(f):
    t=open(f).read(); d=json.load(open(f)); assert json.dumps(d,ensure_ascii=False,indent=2)+'\n'==t,f; return d
EN=load('content/en.json'); RU=load('content/ru.json')
tabs={l:{f:load(f) for f in sorted(glob.glob(f'content/i18n/{l}*.json'))} for l in ('de','sr')}
NEW={'de':'content/i18n/de.7.json','sr':'content/i18n/sr.7.json'}
def move(old_en,new_en,fix):
    """EN string changed: carry each translation to the new key, passed through fix()."""
    for l in tabs:
        k=i18n.key(old_en); hit=[d for d in tabs[l].values() if k in d]
        assert hit,(l,old_en[:50]); v=hit[0].pop(k); hit[0][i18n.key(new_en)]=fix[l](v) if callable(fix[l]) else fix[l]
def one(d,pred,what):
    out=[]
    def walk(n):
        if isinstance(n,dict):
            if pred(n): out.append(n)
            for v in n.values(): walk(v)
        elif isinstance(n,list):
            for v in n: walk(v)
    walk(d); assert len(out)==1,(what,len(out)); return out[0]

# 1. acoustic separation: "It" instead of a second "The partition"
e=one(EN,lambda x: x.get('title')=="Acoustic separation",'ac en'); r=one(RU,lambda x: x.get('title')=="Акустическое разделение",'ac ru')
o=e['text']; e['text']=o.replace(" The partition greatly reduces"," It greatly reduces"); assert e['text']!=o
r['text']=r['text'].replace(" Перегородка значительно снижает"," Она значительно снижает"); assert "Она значительно" in r['text']
move(o,e['text'],{'de':lambda v: v.replace(" Die Trennwand verringert"," Sie verringert"),'sr':lambda v: v.replace(" Pregrada znatno smanjuje"," Ona znatno smanjuje")})
# 2. interior: Alexey's text (Kosta's wording), heading to match
e=one(EN,lambda x: x.get('title')=="An interior that still looks factory",'int en'); r=one(RU,lambda x: x.get('title')=="Салон остаётся заводским на вид",'int ru')
ot,ox=e['title'],e['text']
e['title']="The original design concept is kept"; e['text']="The interior is transformed in line with the latest trends in automotive design, using the finest and most up-to-date materials, while the car's original design concept is preserved."
r['title']="Оригинальный дизайн-концепт сохраняется"; r['text']="Салон преображается по последним тенденциям автодизайна с использованием самых качественных и современных материалов, при этом с сохранением оригинального дизайн-концепта автомобиля."
move(ot,e['title'],{'de':"Das ursprüngliche Designkonzept bleibt erhalten",'sr':"Originalni dizajnerski koncept ostaje"})
move(ox,e['text'],{'de':"Der Innenraum wird nach den neuesten Trends im Automobildesign mit hochwertigsten und modernsten Materialien umgestaltet, wobei das ursprüngliche Designkonzept des Fahrzeugs erhalten bleibt.",
                   'sr':"Enterijer se preobražava prema najnovijim trendovima automobilskog dizajna, uz najkvalitetnije i najsavremenije materijale, a pritom se čuva originalni dizajnerski koncept vozila."})
# 3. Ilya, not Iliya, in every foreign version (EN source and DE/SR tables)
def strings(n,path=()):
    if isinstance(n,dict):
        for k,v in n.items(): yield from strings(v,path+(k,))
    elif isinstance(n,list):
        for i,v in enumerate(n): yield from strings(v,path+(i,))
    elif isinstance(n,str): yield path,n
def setp(d,path,v):
    for p in path[:-1]: d=d[p]
    d[path[-1]]=v
ily=lambda v: v.replace('Iliy','Ily')
changed=0
for path,s in list(strings(EN)):
    if 'Iliy' in s:
        n=ily(s); setp(EN,path,n); changed+=1
        for l in tabs:
            k=i18n.key(s); hit=[d for d in tabs[l].values() if k in d]
            if hit: v=hit[0].pop(k); hit[0][i18n.key(n)]=ily(v)
for l in tabs:
    for d in tabs[l].values():
        for k in d: d[k]=ily(d[k])
print('EN strings renamed:',changed)
# 4. German: Autohansa; "Wir sind beide seit Anfang der Neunziger" -> without "Wir sind"
for d in tabs['de'].values():
    for k in d:
        d[k]=d[k].replace('Avtoganza','Autohansa').replace('Wir sind beide seit Anfang der Neunziger in der Branche.','Beide seit Anfang der Neunziger in der Branche.')
for f,d in (('content/en.json',EN),('content/ru.json',RU)): open(f,'w').write(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
for l in tabs:
    for f,d in tabs[l].items(): open(f,'w').write(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('ok')
