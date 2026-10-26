import json,re
base=json.load(open('data_base.json'))
raw=json.loads(open('tours_raw.json').read())
def clean(s):
    if isinstance(s,list): return [clean(x) for x in s]
    if not isinstance(s,str): return s
    s=s.replace(' — ',', ').replace('—',', ').replace('’',"'")
    return s
U='https://activearenal.com/wp-content/uploads/'
# precios en vivo en drivercostarica.com (mismo dueño) : adulto, nino
LIVE={'tour-rio-celeste':(125,80),'tour-white-water-rafting':(98,79),'tour-sloth':(79,45),'tour-arenal-hanging-bridges':(85,51),'tour-arenal-volcano':(77,45),'tour-jungle-river-safari':(80,63),'tour-night-walk':(68,45)}
META={
'tour-rio-celeste':dict(short='Río Celeste Waterfall',cats=['water','volcano'],badge='Best seller',keywords=['celeste','turquoise','blue','waterfall','tenorio','cascada','catarata','full day','lunch']),
'tour-white-water-rafting':dict(short='White Water Rafting',cats=['water'],badge='Most popular',keywords=['raft','rapids','adrenaline','white water','paddle','balsa','sarapiqui','rafting','rapidos','adrenalina']),
'tour-sloth':dict(short='Sloth Tour',cats=['wildlife'],badge='Family favorite',keywords=['sloth','perezoso','kids','family','easy','toucan','ninos','familia']),
'tour-arenal-hanging-bridges':dict(short='Hanging Bridges',cats=['volcano','wildlife'],keywords=['bridge','canopy','treetop','puentes','colgantes','birds','aves']),
'tour-arenal-volcano':dict(short='Arenal Volcano Hike',cats=['volcano'],keywords=['volcano','lava','hike','volcan','caminata','lake','lago']),
'tour-jungle-river-safari':dict(short='Jungle River Safari Float',cats=['water','wildlife'],keywords=['float','safari','boat','caiman','crocodile','calm','relax','bote','lancha','cocodrilo','tranquilo','abuel','papas']),
}
tours=[]
for r in raw:
    s=r['slug'];a,c=LIVE[s]
    t=dict(slug=s,product=r['rezzerva_product'] or s,title=clean(r['title']),lead=clean(r['lead']),hero=r['hero'],card=r['hero'],
      duration=r['duration'],difficulty=r['difficulty'],guide=r['guide'],pickup=r['pickup'],price=a,child=f'${c} per child, ages 5 to 11',
      overview=clean(r['overview']),highlights=clean(r['highlights']),steps=clean(r['steps']),included=clean(r['included']),
      not_included=clean(r['not_included']),bring=clean(r['bring']),gallery=r['gallery'])
    t.update(META[s]);tours.append(t)
for t in tours:
    if t['slug']=='tour-white-water-rafting':
        t['overview'][0]="Grab a paddle and hit the whitewater. Class II and III rapids on the Balsa or Sarapiquí River wind through lush rainforest canyons, with calm stretches to soak in the scenery and spot toucans, herons and monkeys along the banks."
tours.append(dict(slug='tour-night-walk',product='tour-night-walk',short='Jungle Night Walk',title='Jungle Night Walk',
  lead='The rainforest wakes up when the sun goes down.',hero=U+'2026/09/jungle-night-walk.jpg',card=U+'2026/09/jungle-night-walk.jpg',
  duration='~2 hours',difficulty='Easy',guide='English / Spanish',pickup='La Fortuna / Arenal',price=68,child='$45 per child, ages 5 to 11',
  overview=["After dark the forest around La Fortuna belongs to a different crowd. With a naturalist guide and a slow pace, you look for the frogs, insects, sleeping birds and night creatures that hide during the day."],
  highlights=['Guided walk through the rainforest after dark','Night wildlife spotting with your guide','Bilingual guide (English / Spanish)'],
  steps=['Hotel pickup','Guided walk through the rainforest after dark','Return to your hotel'],
  included=['Round-trip transportation','Naturalist guide'],not_included=['Gratuities','Personal expenses'],
  bring='Closed shoes, long pants, insect repellent, a light rain jacket, camera.',
  gallery=[U+'2026/09/jungle-night-walk.jpg',U+'2026/08/sloth-tour.png',U+'2026/08/arenal-hanging-bridges.png'],
  cats=['night','wildlife'],keywords=['night','dark','frog','noche','nocturno','ranas','evening','tonight']))
# combos (titulos reales del WordPress; precio y duracion los da el widget)
IMG={'Zip Lines':U+'2026/08/arenal-hanging-bridges.png','Waterfall Rappelling (Canyoning)':U+'2026/09/la-fortuna-aerial-hero.jpg','ATV Adventure':U+'2026/10/arenal-volcano.jpg',
 'La Fortuna Waterfall':U+'2026/09/la-fortuna-aerial-hero.jpg','Arenal Volcano':U+'2026/10/arenal-volcano.jpg','Hanging Bridges':U+'2026/08/arenal-hanging-bridges.png','Rainforest Wildlife Walk':U+'2026/08/sloth-tour.png'}
SL={'Zip Lines':'zip-lines','Waterfall Rappelling (Canyoning)':'canyoning','ATV Adventure':'atv','La Fortuna Waterfall':'la-fortuna-waterfall','Arenal Volcano':'arenal-volcano','Hanging Bridges':'hanging-bridges','Rainforest Wildlife Walk':'rainforest-wildlife-walk'}
combos=[]
for g,pre,first,img0,cat,kw in [('Rafting +','tour-rafting-','White Water Rafting',U+'2026/08/white-water-rafting.png','water',['raft','rafting','adrenaline']),('Safari Float +','tour-safari-float-','Safari Float',U+'2026/08/jungle-river-safari-float.jpg','wildlife',['float','safari','calm'])]:
    seconds=['Zip Lines','Waterfall Rappelling (Canyoning)','ATV Adventure','La Fortuna Waterfall'] if g.startswith('Raft') else ['Zip Lines','Waterfall Rappelling (Canyoning)','ATV Adventure','Arenal Volcano','Hanging Bridges','Rainforest Wildlife Walk','La Fortuna Waterfall']
    for s2 in seconds:
        slug=pre+SL[s2];title=f'{first} + {s2}'
        extra=['zip','canopy','tirolesa','canopy'] if 'Zip' in s2 else ['rappel','canyon','cascada','waterfall'] if 'Rappel' in s2 else ['atv','quad','cuadra'] if 'ATV' in s2 else ['waterfall','catarata','fortuna'] if 'Fortuna' in s2 else ['volcano','volcan','lava'] if 'Volcano' in s2 else ['bridge','puentes'] if 'Bridges' in s2 else ['sloth','wildlife','perezoso']
        combos.append(dict(slug=slug,product=slug,group_img=img0,pair='+ '+s2,first=first,group=('Start with rafting' if g.startswith('Raft') else 'Start with the safari float'),title=title,short=title,
          lead=f'{first} and {s2} in one day, with a single hotel pickup in La Fortuna.',hero=IMG[s2],card=IMG[s2],
          duration='Two tours, one day',difficulty=None,price=None,cats=['combo',cat],keywords=kw+extra+['combo','two','dos'],
          overview=[f'Start with {first.lower()} and keep the day going with {s2.lower()}. One booking, one pickup, and a guide who connects both parts of the day so you are not waiting around.'],
          highlights=[first,s2,'Hotel pickup in La Fortuna and the Arenal area','Bilingual guide (English / Spanish)'],gallery=[img0,IMG[s2],U+'2026/10/arenal-volcano.jpg']))
# Precios y salidas del panel de Rezzerva (Mis tours), 25 oct 2026
CP={'tour-rafting-canyoning':172,'tour-rafting-la-fortuna-waterfall':154,'tour-rafting-atv':(185,'group'),'tour-rafting-zip-lines':168,
 'tour-safari-float-canyoning':172,'tour-safari-float-la-fortuna-waterfall':145,'tour-safari-float-atv':(165,'group'),'tour-safari-float-hanging-bridges':165,
 'tour-safari-float-zip-lines':158,'tour-safari-float-rainforest-wildlife-walk':160,'tour-safari-float-arenal-volcano':160}
for c in combos:
    v=CP[c['slug']]
    c['price'],c['unit']=(v if isinstance(v,tuple) else (v,'person'))
    c['departs']='8:15 a.m.' if 'rafting' in c['slug'] else '8:00 a.m.'
    if c['unit']=='group': c['price_note']={'tour-rafting-atv':'1 person $185 · 2 people $290','tour-safari-float-atv':'1 person $165 · 2 people $260'}[c['slug']]
DEP={'tour-night-walk':'5:30 p.m.','tour-arenal-volcano':'8:00 a.m. or 1:30 p.m.','tour-rio-celeste':'7:30 a.m.','tour-arenal-hanging-bridges':'8:00 a.m. or 1:30 p.m.',
 'tour-white-water-rafting':'8:15 a.m.','tour-jungle-river-safari':'8:00 a.m. or 1:30 p.m.','tour-sloth':'8:00 a.m. or 1:30 p.m.'}
for t in tours: t['departs']=DEP[t['slug']];t['unit']='adult'
# Fotos propias en alta (img/), de la carpeta WEBSITE de Driver Costa Rica
PH={
 'tour-rio-celeste':('img/rio-celeste-wide.webp','img/rio-celeste-trail.webp',['img/rio-celeste-wide.webp','img/rio-celeste-trail.webp','img/rio-celeste-pool.webp']),
 'tour-white-water-rafting':('img/rafting-rapids.webp','img/rafting-rapids.webp',['img/rafting-rapids.webp','img/rafting-river.webp','img/rafting-crew.webp']),
 'tour-sloth':('img/sloth-mother.webp','img/sloth-mother.webp',['img/sloth-mother.webp','img/sloth.webp','img/owl.webp']),
 'tour-arenal-hanging-bridges':('img/hanging-bridges-aerial.webp','img/hanging-bridges-aerial.webp',['img/hanging-bridges-aerial.webp','img/hanging-bridges.webp','img/motmot.webp']),
 'tour-arenal-volcano':('img/arenal-volcano-lake.webp','img/arenal-volcano-lake.webp',['img/arenal-volcano-lake.webp','img/volcano-hiker.webp','img/kayak-volcano.webp']),
 'tour-jungle-river-safari':('img/safari-float.webp','img/safari-float.webp',['img/safari-float.webp','img/safari-float-river.webp','img/crocodiles.webp']),
 'tour-night-walk':('img/frog-night.webp','img/frog-night.webp',['img/frog-night.webp','img/frog.webp',U+'2026/09/jungle-night-walk.jpg']),
}
# Volcán: Leo lo vende como "Arenal Volcano Hike" (no amarrado al Parque Nacional, por si un día cierra)
for t in tours:
    if t['slug']=='tour-arenal-volcano':
        t['title']='Arenal Volcano Hike'; t['short']='Arenal Volcano Hike'
        t['lead']='Hike the lava trails at the foot of an iconic volcano.'
        t['overview']=["Stand in the shadow of one of the world's most perfectly shaped volcanoes. This guided hike follows trails across old lava flows from Arenal's active years, through regenerating forest alive with wildlife, to viewpoints that frame the volcano and Lake Arenal.",
                       "Your guide brings the landscape to life with the geology, history and ecology of the volcano and the forest around it."]
        t['highlights']=['Short drive to the volcano trails','Guided hike across lava fields and rainforest trails','Panoramic volcano and lake viewpoints','Bilingual guide (English / Spanish)']
        t['steps']=['Hotel pickup','Short drive to the volcano trails','Guided hike across lava fields and rainforest trails','Panoramic volcano and lake viewpoints','Return to your hotel']
        t['included']=['Round-trip transportation','Naturalist guide','Trail entrance']
POS={'tour-sloth':'center 45%','tour-white-water-rafting':'center 35%','tour-rio-celeste':'center 60%','tour-night-walk':'center 32%'}
for t in tours:
    t['hero_pos']=POS.get(t['slug'],'center')
    h,c,g=PH[t['slug']]
    if h: t['hero']=h
    if c: t['card']=c
    t['gallery']=g
CIMG={'Zip Lines':'img/zipline.webp','Waterfall Rappelling (Canyoning)':'img/rappel.webp','ATV Adventure':'img/atv.webp','Arenal Volcano':'img/arenal-volcano-lake.webp','Hanging Bridges':'img/hanging-bridges-aerial.webp','Rainforest Wildlife Walk':'img/sloth-mother.webp'}
for c in combos:
    s2=c['pair'][2:]
    if s2 in CIMG: c['hero']=c['card']=CIMG[s2]
    c['group_img']='img/rafting-rapids.webp' if 'rafting' in c['slug'] else 'img/safari-float.webp'
    c['gallery']=[c['group_img'],c['hero'],'img/arenal-volcano-lake.webp']
base['brand']['hero_images']=['img/arenal-volcano-lake.webp','img/rio-celeste-wide.webp']
base['brand']['band_image']='img/kayak-volcano.webp'
CAT={'water':'img/rio-celeste-trail.webp','wildlife':'img/sloth-mother.webp','volcano':'img/hanging-bridges-aerial.webp','night':'img/frog-night.webp','combo':'img/rafting-rapids.webp'}
for cat in base['categories']: cat['image']=CAT.get(cat['id'],cat['image'])
base['tours']=tours;base['combos']=combos
json.dump(base,open('data.json','w'),ensure_ascii=False,indent=1)
print(len(tours),len(combos))
