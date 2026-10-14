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




  
