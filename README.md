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

