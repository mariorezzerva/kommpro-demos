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
        combos.append(dict(slug=slug,product=slug,group=('Start with rafting' if g.startswith('Raft') else 'Start with the safari float'),title=title,short=title,
          lead=f'{first} and {s2} in one day, with a single hotel pickup in La Fortuna.',hero=IMG[s2],card=IMG[s2],
          duration='Two tours, one day',difficulty=None,price=None,cats=['combo',cat],keywords=kw+extra+['combo','two','dos'],
          overview=[f'Start with {first.lower()} and keep the day going with {s2.lower()}. One booking, one pickup, and a guide who connects both parts of the day so you are not waiting around.'],
          highlights=[first,s2,'Hotel pickup in La Fortuna and the Arenal area','Bilingual guide (English / Spanish)'],gallery=[img0,IMG[s2],U+'2026/10/arenal-volcano.jpg']))
base['tours']=tours;base['combos']=combos
json.dump(base,open('data.json','w'),ensure_ascii=False,indent=1)
print(len(tours),len(combos))
