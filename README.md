# Lali50-repo

A platform egy kiberbiztonsági és geopolitikai aggregált hírforrás. Az ötlet alapvetően az volt, hogy reggelente kapjak egy összefoglalót a "nagy világ" történéseiről, de persze elsősorban a kiberbiztonsági relevanciával bíró hírekről. 

A program kiberbiztonsági, geopolitikai, technológiai valamint közéleti oldalakat, substack feedeket dolgoz fel. Az aggregálás és értelmezés Google Gemini API (személyes előfizetéssel) történik. 

  Felépítés 

Az adatforrások egy könnyen változtatható .json-ben lettek meghatározva. Ide bármikor új RSS feedet lehet csatolni

Mivel az hírforrások egy része közéleti, így fontosnak tartottam, hogy differenciálva legyen a politikai beállítottságuk, ne csak jelöletlenül érkezzen be hír ezekről az oldalakról. Fontosnak tartom a több, változó forrásból való tájékozódást, függetlenül a hírforrás függetlenségi szintjétől, viszont helyén kell kezelni ezeket az adatokat. 

Klaszterenként és oldalanként is lettek limitek meghatározva, hogy ne csak egy oldal hírei lepjék el a jelentést, illetve minden klaszterről egyenlően érkezzen be adat. Ezek a limitek szabadon változtathatók, egészen biztosan kell is majd rajtuk alakítani, ehhez azonban idő kell, hogy tisztázódjon miből kell több, és miből esetleg kevesebb. 

A githubon nem látható, de a jelentés miután bekerült az 'Issues' fül alá, Apple Shortcuts segítségével a telefonomra, iCloud Notes-ba kerül, így valamivel egyszerűbben hozzáférek, valamint egy másik helyen is mentésre kerül a jelentés, így ha valamilyen oknál fogva megszűnne ez a github repo, akkor is hozzáférnék korábbi jelentésekhez. 


  Memória 

A hírösszefoglaláson kívül egyfajta memóriával is rendelkezik a program, ez több részből áll fel: 

1. Profil: Személyre szabható, specifikus infrastruktúra, szoftverek, támadók jelölhetőek ki, így relevánsabb információt ad a jelentés. Ez egyelőre részemről ki van kapcsolva, nincs megadva környezet.
2. Redundancia csökkentés, kampánykövetés:
     yesterday.md: tárgynapot megelőző napi jelentést tartalmazza, így a hírösszefoglaló tudja mit nem kell már leírnia, viszont új információ esetén frissítést tud adni korábban már leírt eseményről
     active_campaigns.json: nagyobb távlatú, 30 napos tár, kifejezetten a támadásokra fókuszálva, hetekkel később is tud frissítést adni (elvileg)
3. Kereshető adatbázis: intel_ledger_jsonl egy hosszú távú, támadások paramétereit leíró adatbázis/lenyomat későbbi elemzés céljából


  Tapasztalatok: 

A projekt során a legnagyobb nehézséget a Gemini API okozta. Automatizálva van a futás, először 6:00-ra lett beállítva, ez mivel "egész óra" sokszor 503-as hibakódot dobott, így átraktam egy másik időpontra helyi idő szerint hajnalban, ahol eddig nem volt vele még probléma. 

Ez csak az automatikus futásra igaz sajnos. Mivel napközben foglakoztam a programmal, így akkor is szerettem volna kipróbálni, hogy adott új funkció vagy megváltoztatott limit hogyan változtat a végeredményen. Mivel ezek munkaidőben történetek, szinte mindig 503-as hibakód érkezett vissza 10 óra után, és ez délutánra sem javult.

A hibakód ellenére a program közel nem használja ki a Gemini API és a GitHub által biztosított limiteket. Egy átlagos futtatás 2-3 percet vesz igénybe, 10-15 ezer token mellett. A Gemini API-nál releváns limit (napi 1 futásnál) a 250 ezer percenkénti token, ezt közel sem éri el. GitHub-nál havi 2000 perc limit van, ez bőven lehetőséget  adna akár napi 20-30 perces futtatásokra is. 

A jelenlegit verzió stabil, kiküldésre is kerül és megfelel az alapkövetelményeknek. Főleg a klaszterenkénti/oldalankénti limiteket lesz majd szükséges változtatni, hogy minél több adatot tudjon feldolgozni az API, anélkül hogy 429-es (too many requests) hibakódba ütközzön a lekérdezés. 

Az jelentés angolul érkezik, ennek egyszerű oka van: reggel, este egyébként is olvasok magyarul, viszont angol nyelven változó hogy mennyit tudok egy nap, viszont szeretném szinten tartani a tudásomat. Mivel a Gemini képes lenne magyarul is megírni a jelentést, így ennek megváltoztatása nem lenne nagy feladat. 

Update 10.14 9:00: Rossz időformátum volt megadva, így fennállt a lehetőség hogy bizonyos cikkek kiestek a 48 órás keresésből, annak ellenére, hogy még azon belül voltak. Ez javítva lett, más módszerrel dolgozza fel a cikkek megjelenési idejét.

Update 10.14 9:15: 1.: A reggeli jelentés cca. 40k tokent használt fel, ez még mindig bőven a korlát alatt van, így a keresési limiteket megnöveltem, hogy kategóriánként több cikket tudjon feldolgozni, hosszabb jelentést készíthessen. 
2.: Több oldal is hibaüzenetet dob fel, amikor a feedparser megpróbál hozzáférni. Ezért hozzáadásra került egy sor mely elméletben álcázza a szkriptet, úgy mintha egy böngészőből lett volna indítva a keresés. 

Update 10.14 12:00: Mivel elég zavaró, hogy program rengetegszer nem éri el a legfrissebb gemini API-t (3.8-flash ebben az esetben, ez a legjobb amit az előfizetésem tud), ezért beépítésre került egy megoldás. Amennyiben nem éri el a legfrissebb modellt, vélt egy régebbire, illetve ha azt sem akkor egy még régebbire. Mivel nem a legbonyolultabb feladat amit el kell végeznie, ezért a "régiebbi" egyáltalán nem biztos hogy érzékelhetően rosszabb megoldást adna, ez egyfajta biztosításként lett beépítve, mivel napközben amikor dolgoznék a projekten, nagyon sokszor érkezik 503-as hibakód. 

Update 10.14 12:45: Megint egy nagyobb változtatási csomag, Gemini Argon modell segítségével: 
1. Limitek ismét növelve, így már egy lekérdezés cca. 75 ezer token, még mindig bőven a 250 ezres limit alatt.
2. Substackek-nél bővebb elemzési paraméterek, ne csak a 'summary'-t gyűjtse össze.
3. A hírkategóriákon belül ki lett alakítva egy rendszer, hogy vegye figyelembe mindegyik hírportált, ne üsse meg a limitet rögtön az elsőnél, így mindegyik oldalról be tudja gyűjteni a friss és releváns hírt. Példa: eddig a magyar hírek kategóriában a telex-et kérdezte le először, volt arra példa, hogy ezzel meg is ütötte a limitet így az NKI, MNB és többiek hírei nem jutottak el az elemzésig.
4. A jelentés végére odakerül egy technikai rész is, ami az elemzés menetéről (cikkszámok, használt modell, sikertelen lekérdezés, etc.) szól. Így látom, hogy a reggeli jelentésben melyik híroldalt nem sikerült elérni, el tudom dönteni hogy akkor azt vagy elolvasom a jelentésen kívül, vagy újrafuttatom a jelentést. Ez a technikai lenyomat nem kerül be 'yesterday.md'-be. 
  
Update 10.16 8:00: Néhány oldal nem volt elérhető, feltehetően web scraper-ek elleni védelemmel vannak ellátva. Ezért egy ezt kikerülő módszert alkalmaz ezentúl a program. Ez részben sikeres, vannak azonban továbbra is feedek, melyek nem elérhetőek, főleg a .substack domainnel rendelkezők. Ezeket vagy ki kell venni a feed-ek közül, vagy megoldást találni az automatikus lekérdezésükre. 
már 130 ezer token inputot kap a gemini API, ez továbbra is bőven a limit alatt, 50%-nál. Működött a legjobb modellek elérését célzó változtatás is. Míg a hajnali automatikus lekérdezés gond nélkül futott, a reggeli már manuálisan futatott nem tudta elérni a legfrissebbet, de automatikusan visszalépett egy régebbire, ez már elérhető volt. A jelentés minőségében, formájában nem vehető észre ez a változás. 

