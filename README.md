# Lali50-repo

Az alapötlet az, hogy egy aggregált newsfeedet kapjak minden reggel. 

Ehhez először felvettem azokat az oldalakat amelyeket már most is követek, illetve kerestem újakat. 
Ezek többnyire kiberbiztonsági , geopolitikai vagy technológiákkal kapcsolatos oldalak, substack feedek stb. 
Ezek a források találhatóak a 'feeds.json'-ben

Maga az aggregálás és értelmezés egy Google Gemini API segítségével történik, ehhez kapott hozzáférést az oldal

A változtásokon látszik, hogy nem zökkenőmentes a folyamat 

Először nagyon kevés anyagból dolgozott, és ezek nem is voltak külön fájlba véve, ezeket bővítve lett meg a feeds.json

A modell alapvetően az elmúlt 48 óra híreiből működik, ezért hogy ne legyen átfedés, ismétlés készít egy yesterday.md fájlt amit későbbi napokon elolvas a modell, értelmezi, hogy amit már leadott azt ne ismételje, de ha a tegnapi hírhez van fejlemény azt jelzi

viszonylag több időt vesz igénybe egy ilyen 'eszköz' felépítése, mivel meg kell jelennie új híreknek, hogy azokat tudja kezelni, és értékelni lehessen az outputot.

Beépítésre került egy test mode is, ez arra hivatott, hogy ne fogyassza a véges API előfizetésemet. Így 429 vagy 503-as hibakódokat nem dob, tesztelhető minden más folyamat is. 

Az API nemcsak napi lekérdezések számában korlátozott, hanem max token is meg van adva, ezért szükséges volt beépíteni olyan limiteket, melyek csökkentik a Gemini felé küldött anyagok mennyiségét, hogy ne lépjem túl. 

Mivel nagyjából úgy van beállítva, hogy a napi 1 lekérdezés ki is meríti a rendelkezésre álló API erőforrást, így viszonylag nehéz gyorsan meghatározni hogy milyen is az eredmény 

Először helyi idő szerint 6:00-kor kérte az API hozzáférést a program, emiatt sokszor 503-as hibakód érkezett vissza. Ez főleg amiatt lehet, hogy "egész" órakor több kérést indítanak, ezért ezt megváltoztattam egy "nem kerek" időpontra, így már 10.09-én megkaptam az első használhatóbb napi összefoglalót.

Minimálisan változtatva lett a források feldolgozásához kötött limitek, hosszabb összefoglalókat készíthet, viszont oldalanként kevesebb cikkel, így nem dominál annyira egy oldal a jelentésben. 

Mind az API mint a github actions limitjeit vizsgálva, az látszik, hogy egyik sincs megfelelően kihasználva. Az API-nak egy 250 ezer tokenes limitje van, ez az elmúlt időszakban a 10 ezret sem érte el. Mivel másra nem használom ezt az API-t , így lehetne ezen növelni, tehát több forrást tenni a feeds-be, vagy a meglévő forrásokból hosszabb összefoglalót készíteni. 
Ezzel összefügg azonban a github actions limitje is, ez havi szinten 2000 percet jelent. Az eddigi (10.13) futások 50 mp és 2p közötti terjedelemben vannak, így bőven van kapacitás hosszabb lekérdezéseket futtatni, anélkül, hogy megütnénk a limitet. A tesztelés miatt már el lett használva cca. 60 perc ebből, viszont még így is bőven lenne lehetőség akár 20-30 perces action-öket futtatni minden reggeli jelentéshez. 

Bővítésre került a feeds, ezzel azonban az jár, hogy a közéleti, általános magyar híroldalaknál (eddig csak telex és portfolio volt benne) érdemes differenciálást alkalmazni, jelölni, hogy milyen forrásból érkezik a cikk amit feldolgoz. A korábbi cca. 20 feed helyett így most 60 felett lett, bővítve ezzel a perspektívát. 

Githubon nem látható, de egy github API segítsével, minden reggel az összefoglalót lementi az iCloud notes-ba, pontosan 7:00-kor, erről értesítést küld. Ezt az apple shortcuts segítségével tudtam automatizálni. 


