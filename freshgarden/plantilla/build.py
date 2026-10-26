import base64, json, re
FG="Gala.webp Fuji.webp Honeycrisp.webp PinkLady.webp Granny-Smith.webp RedDelicious.jpeg Ambrosia.webp Opal.webp RedGlobe.webp VerdesinSemilla.webp RojaSinSemilla.webp NegraSinsemilla.webp UvaSweeta.webp Limon-Amarillo.webp naranja.webp mandarina.webp toronjasFG.webp KiwiSunGold.webp Hayward.jpeg kiwirojo-kiwifruit.png cereza.webp nectarina.webp durazno.webp Ciruelarojanegra.jpeg pluot-e1778630581240.webp duraznoparaguayo.webp Anjou.webp Bosc.webp RedAnjou.webp Asiatica.webp Forelle.webp Aguacate-Haas.png granadaFG.webp persimon.webp 594579015eb5d45f10e35b42-1.webp Esparragos.webp pngtree-ddatilfg.webp ajonegroFB.png ChumisGALA.webp CHUMISRoja.webp ChumisGRANNY.webp BolsaManzanas6pack.png m.mixta_.png kiwi-bolsa.webp pera-bolsa.webp ManzanaRoja.webp uvassss.webp %E2%80%94Pngtree%E2%80%94orange-png-png-free-download_3619070.webp Kiwi-raw.png Durazno.webp Peras.png".split()
def uri(p):
    mime={'webp':'image/webp','jpg':'image/jpeg','png':'image/png'}[p.rsplit('.',1)[1]]
    return f"data:{mime};base64,"+base64.b64encode(open(p,'rb').read()).decode()
h=open('template.html').read()
used=set(re.findall(r'"([^"]+\.(?:webp|png|jpeg))"',h))
A={f:uri('img/p_%02d.webp'%i) for i,f in enumerate(FG) if f in used}
A['chumisLogo']=uri('img/chumis-logo.png')
for k,f in [('arandanoBowl','arandano-bowl.jpg'),('chumisHw','chumishw.jpg'),('grapeRed','grapered.jpg'),('grapeBlack','grapeblack.jpg'),('seasonHw','season-hw.jpg'),('seasonNav','season-nav.jpg'),('chumisBg','chumis-bg.jpg'),('arandanosPhoto','arandanos.jpg')]:
    A[k]=uri('img/'+f)
for k,f in [('logo','logo.png'),('iso','iso.png'),('hero1','hero1.jpg'),('hero2','hero2.jpg'),('arandanos','arandanos.jpg')]:
    h=h.replace('{{%s}}'%k, uri('img/'+f))
h=h.replace('{{ASSETS}}', json.dumps(A))
missing=[f for f in used if f not in A]
open('../index.html','w').write(h)
print(len(h)//1024,'KB; missing:',missing)
