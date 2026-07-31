# Debug and Test Results — the working journal of this mod

**What this file is.** The running log of every in-game test session and every
fix pass that answered one. It is the only document that records *what was
actually observed in the running game* — every other doc in this repo describes
intent. When a claim here and a claim elsewhere disagree, this file wins.

**How to read it.** Strictly chronological, oldest at the top, newest at the
bottom. **Start at the bottom.** Sections alternate between two kinds:

| Heading | Author | Contains |
|---|---|---|
| `<date> TEST RESULTS` | the mod author, in Turkish | Numbered findings from a real game run: error.log lines, things that looked wrong, feature requests, and open questions. This is the input. |
| `<date> CLAUDE FIX PASS` / `AUDIT` | the assistant, mostly Turkish, ASCII-only | What was changed in response, numbered against the findings above it, with the vanilla `file:line` that justified each change. This is the output. |

A finding is answered in the fix pass immediately below it. Items marked
`(FIXED)` in a TEST RESULTS heading were resolved by the author before the
session started.

**Conventions.**
- Findings are numbered per section; later sections refer back as e.g. "24.07 #12".
- The assistant's entries avoid Turkish characters so the file survives any
  encoding round-trip. The author's entries do not — that is fine and expected.
- "Statik dogrulamadan gecti" means `tools/verify_mod.py` passed. It never means
  the change was tested in game. **Only the TEST RESULTS sections are evidence
  of in-game behaviour.**
- File is UTF-8 **with BOM**, like every other `.txt`/`.yml` in the repo.

**Where the durable rules live.** This file is a journal, not a rulebook. When a
finding here produces a rule, that rule is copied into:
- `CLAUDE.md` — the standing rules and architecture. Read that first.
- `docs/EU5-MODDING-GUIDE.md` — the general method, including the verification
  discipline (§9).
- `docs/TESTING-GUIDE.md` — a checkable row per behaviour, so the next test run
  covers it.
- `docs/FUTURE-DEVELOPMENT.md` §5 — anything knowingly left unfixed.

If you are an assistant picking this repo up cold: read `CLAUDE.md`, then the
**last two sections of this file**, then ask what to work on. Do not infer that
something works because a fix pass says it was written — check whether a TEST
RESULTS section after it confirms the behaviour.

---

##### 22.07.2026 TEST RESULTS FIXED ALL #####

#### 1. Variables set but never used: MR_dominance_events.txt in game error logs (FIXED)

- Variable `mr_history_babur` is set but never used.
- Variable `mr_history_ilkhanate_fragmanted` is set but never used.
- Variable `mr_history_oirat_challenge` is set but never used.
- Variable `mr_history_delhi_sacked` is set but never used.
- Variable `mr_history_chagatai_schism` is set but never used.
- Variable `mr_history_yuan_decline` is set but never used.
- Variable `mr_history_tokhtamysh` is set but never used.

Bu variableları set etmişsin ama hiç kullanmamışsın ya kaldıralım ya da kullanalım ama nasıl kullanıcan zor gibi belki event yollayarak kullanabilirsin: Mesela delhi sacked olur eğer bizim main mongol ülkesi bi situationı tamamlayınca  veya delhiyle savaşırsa o event hem bize gelir delhiyi sackedladık diye, hem de delhiye veya delhi toprağını elinde kim tutuyorsa ona gider bizi sacked yaptılar gibi. Ama sen anladın yani eğer tarihsel güzel akıcı bir hikaye kurabilceksen variableları tut ve uygula eğer kurulmaz dersen komple kaldırabiliriz mantığı bu şekilde boşu boşuna kodlar kalmasın orda error verip oyunu çöktürmüyor ama boşuna duruyor diye in game logda uyarı verdi.

#### 2. Army balance support for AI support Events: (FIXED)

Bunu eklememişsin asker basma eventine ve manpower basma bina eventini ben biraz steppe advancelerine göre biraz düzenledim bu şekilde:

MR_dominance_event.txt içine ki 996 ve 995. eventler için kodlar düzenlendi ve dğeiştirildi cost multipler reasonvs eklendi ve dediğim gibi steppeye özel advance binaları kurultai gibi manpower binası ve Steppe Horse Archers gibi unit birimler eklendi ordu basma(AI support) kısmı için.

#### 3. mr_dominance.997 gibi AI railroad: declare the unification war eventlerindeki problem: (FIXED)

Bu eventlerde tüm kodu savaş açma variable sıfırlama vs. hepsini immediate bloğuna yazmışsın benim Prussian Destiny modumdaki pd_brandenburg.103 eventimdeki gibi option kısmına yazmamışsın bu sebeple event geldiği an ülke direk savaş ilan edecek. Peki ya gerçek insan oyuncu savaş ilan etmek istemezse?

- Burda asıl olması gereken pd_brandenburg.103 eventindeki gibi o savaş açmayı option ksımına koymamız lazım o option ksımı event ekranı geldiği ve fırelandığı zamanda ekranda çıkan event ekranı ve buton kısmı orda iki tane option.a ve option.b yapmamız gerek çünkü bir tek AI oynamıcak bu modu eğer gerçek insanda oynamak isterse ve saldırmak istemezse option b seçicek ve savaşı erteler aynı Prussian Destiny modumda olduğu gibi ve after = bloğu açarak ondan sonra o savaş açtırma variablelarını sıfırlatabilirisin o kodum çok iyi ve çalışıyor prussian destiny modumdaki 103. eventteki kdo o tarz yap ve diğer bu sıkıntı olabilecek tüm eventleri vs araştır ve onlarıda bu şekilde düzelt bence.

- Ayrıca şunu da farkettim situationda :
		set_variable = {
			name = mr_conquest_cooldown
			value = 0
		}
		set_variable = {
			name = mr_conquest_target
			value = 0
		}
var ama Prussian Destinyde bir de şunu set variable etmişiz bu yok: set_variable = {name = PD_conquest_target_country value = c:BRA} bunu setlememizim amacı bizim ana ülkeyi situation sahibi yani railroad yaptırdığımız ülkeyi on_start bloğunda böyle variable'a setliyorduk çünkü hedef bulma bloğunda şöyle yapıyorduk: situation:mongol_resurgence = {set_variable = {name = mr_conquest_target_country value = prev}} diyerek burda prev'e setliyorduk bu prev demek o an içine girdiğimiz ülke demek yani c:MGO ordered_neighbor_country koduyla içeri giriyor ve limitlerde elediği sıralayıp güçsüz olarka bulduğu ve mun of locatinos ile en küçük en güçsüz ülkeyi buluyor onun tagını ismini prev olarak bizim mr_conquest_target_country set ediyor prev diyerek mesela örnek orderladı buldu o variable c:CHI oluyor. Biz Prussian Destiny modunda bunu on_startta set ediyorduk ve kendi ülkeye atıyorduk c:BRA diyerek sonra hedef bulduğu zaman ordan yeni saldıracağı hedef ülkeye set ediyordu ve sonra onun 103. pr3ussia saldırma eventinde immediate bloğunda bu şekilde scope'a kaydedip: immediate = {situation:the_prussian_ambition = {change_variable = {name = PD_conquest_cooldown multiply = 0} var:PD_conquest_target_country = {save_scope_as = target_country}}} ondan sonra aşağıda savaş açıyordu bu mantık daha temiz ve mantıklı gibi çünkü sen situation içinde sadece hedef arama(AI RAILROAD: FIND A TARGET) bloğunda ilk defa onu set etmişsin {set_variable = {name = mr_conquest_target_country value = prev}} diyerek ama onu tekrar ana ülkeye döndürmemişsin c:BRA veya c:MGO diyerek örnek mesela 103. eventte after bloğuında tekrar c:BRA diyerek onu nromalde döndüşmüşüz ki tekrar situation on_monthly bloğunda doğru okusun mantığı anladın mı bilmiyorum.

- Böyle yaparsak aklıma gelen tek sorun sanırım ilk situationda hemen MGO ülkesi olmuyor ya sonradan çıkıyor situation başladığın on_startta set etsek mr_conquest_target_country'i sıkıntı olur mu onu tam bilmiyorum ülke daha mevcut değil çünkü ama belki çökmeden çalışabilir.

#### 4. MR_mongol_preparing_for_conquest modifierının yanlış kullanılması ve anlaşılmaması: (FIXED)

Sen sanırım bu modifierı daha mantığın anlamamışsın neden yaptığımızı hemen anlatayım:
- Bu modifierın amacı her farklı situation başladığında o situation sahibi ülkeye mesela benim Prussian Destiny modumda bu perparing_for_conquest modifierını Prussiaya veya Brandenburga veriyorduk çünkü AI için bu tamamen. Situation başladığı zaman AI kendi kafasına göre savaş açmasını engelleyelim ki bizim savaş açma komutumuz railroad kodumuz (AI RAILROAD: FIND A TARGET) ile savaş açılsın. AI kendisi savaş açıp kendini bitirmesin hem de o railroad kodumuzu engellemesin (çünkü at_war = no koyduk) çalıştırsın bizim istediğimiz kişilere saldırsın. Ana mantığı bu ve önemli!

#### 5. Modu test edicem o nedenle tam olarak situationlarda ve kodda ne oluyor anlatır mısın: (FIXED)

Kodu güzel bir plan ile test etmem gerek yani mesela situationlar ne zaman oluyor situationlarda ne olacak veya olması planlandı onları sıra sıra düzgün test edeyim birbiriyle bağlantılı şeyleri birlikte test edeyim ki karışmasın. Kod testi yaparken çok kod var çünkü bana güzel bir modu test etme rehberi lazım. "Şunlara bak şurda şu olması gerekiyor bak oluyor mu falan gibi" rehber lazım dediğimi anladın umarım. Daha iyi bir fikrin varsa o şekilde de yapabiliriz yeter ki modu komple düzgün bir şekilde test edebileyim.

#### 6. Kullanılmayan Game Rules Locları ve Ayrı Localization Dosyaları: (FIXED)

 # ==============================================================================
 # ----------------- GAME RULES -----------------
 # ==============================================================================
 # --- Situation 1 Conquest Automation ---
 # --- Military Buffs ---
 # --- Imperial Expansion Automation ---
 # --- Timeline & Pacing ---

 - Bu Game rules  localizationlarını yazmışsın ama bunları game rulestan kaldırmışız. Neden kaldırdık Prussian Destiny modundaki gibi kullanmıyoruz bunları ve bence bunlar lazım ki insan oyuncu istediği gibi kendi oynasa da AI içinde ayarlasa da kendisi customize edebilmeli bence. Modifierların loclarıda kalmış onları komple düzenler misin situationda veya eventlerle onları ben ekliyordum Prussian Destiny modum da yiice bi bak yani oralar karışmış komple. 

 - Ayrıca 2 tane hem in-_game de hemde main_menude localization dosyaları var ama vanilla EU5 bütün şeyleri sadece main_menudeki localizationlara koymuşlar. Biz neden in_game/localizationlara da ekstradan koyduk onu anlamadım ona bakar mısın. Prussian Destiny modumda da öyle yapmışız sadece localizationlar main_menu/localizaton_english'in içindeler vanillada da öyle ve ben neden olduğunu bulamadım ama oyun içinde girinc eülke sçeme ekranında Game Rulesum geliyor mr_railroad diye ama localizationları yok uygulanmamış rule_mr_railroad, setting_mr_railroad_historical, setting_mr_railroad_historical_desc şeklinde gözüküyor bunu da çözer misin ve diğer ekstra bi game rule vs. eklersek ona da bu çözümü ekleyelim. Hatta sanırım o sebepten dolayı oyundaki debug logdaki şu hatalar geldi: 

[game] [error] [localization_util.cpp:103] war_goal_MR_war_goal_steppe_unification: "War goal MR war goal steppe unification" 
[game] [error] [localization_util.cpp:103] war_goal_MR_war_goal_steppe_unification_desc: "War goal MR war goal steppe unification desc" 
[game] [error] [localization_util.cpp:103] war_goal_MR_war_goal_silk_road: "War goal MR war goal silk road"
[game] [error] [localization_util.cpp:103] war_goal_MR_war_goal_silk_road_desc: "War goal MR war goal silk road desc" 
[game] [error] [localization_util.cpp:103] war_goal_MR_war_goal_westward_advance: "War goal MR war goal westward advance" 
[game] [error] [localization_util.cpp:103] war_goal_MR_war_goal_westward_advance_desc: "War goal MR war goal westward advance desc"

- Bunları sanırım Mongol Resurgence\in_game\localization\english\MR_l_english.yml içinde koyduğumuz için okumuyor ve locları yok gözüktüğü için bu hataları veriyor olabilir. Aynı sıkıntı bunlar içinde geçerli:

mr_chahar_reunification: "Mr chahar reunification" 
mr_chahar_reunification_desc: "TODO: Write a desc" 
mr_torghut_migration: "Mr torghut migration" 
mr_torghut_migration_desc: "TODO: Write a desc" 
mr_dzungar_khanate: "Mr dzungar khanate" 
mr_dzungar_khanate_desc: "TODO: Write a desc"

- O sebeple tüm kodlarımı gözden geçir ve bu sorunları kökünden çözmemiz gerekiyor.
- Edit yeni bilgi: Baktım mesela mongol_resurgence situation GUI'sindeki end requirements ve situation_mongol_resurgence_desc vs çalışıyor gözüküyor locları.

#### 8. MR_on_actions.txt dosyasındaki invalid right side hatası: (FIXED)

- Böyle bir hata geldi bu sanırım on_actionda biz OR = {this = c:MGO this = c:MGE} böyle yazmışız önceden tag = MGO yerine this:MGO şeklinde yazdığımız için olmuş bu hatu sanırım. Baktım Prussian Destinyde de öyle yapmamışız tag = BRA olarak yapmışız on_actionstaki kodlarımızda o sebeple bu hatayı düzelttim ben kendim ama sen yinede bir kontrol et. on_action.txt dışındaki dosyalarda this = c:MGO kullanı mı error logda hata vermiyor gözüküyor bilgin olsun. Aynı zamanda Mongol_resurgence situationı başladığı an direk bu hatalarıda verdi oyun çökmüyor tabi ki çalışıyor ama debug.logunda gördüm oyun içinde ki:

## Gelmiş olan hata ilk hata benim düzelttiğim fixledim sadece bilgi al diye attım: (FIXED)
[game] [error] [jomini_script_system.cpp:252] Script system error! Error: Invalid right side during comparison 'c'
Script location:
common/on_action/MR_on_actions.txt:38

## Gelmiş olan 2. hata ben fixleyemedim sana bıraktım: (FIXED)
[game] [error] [jomini_script_system.cpp:252] Script system error! Error: Invalid right side during comparison 'c'
Script location:
common/situations/MR_mongol_resurgence.txt:592

- Acaba o ülke var olmadığı için olabilir mi çünkü c:MGO diye arıyor bulamıyor biz MGO yu 1368de situation başlıyor ama hala mevcut değil. Biz mongol_resurgence situationun da 1375e kadar kimse claim almadıysa ondan sonra oluşturuyoruz MGO yu çıkartıyoruz ama claim alma nasıl oluyor tam anlamadım yani bağlantı da bir sıkıntı var mı yoksa doğru mu onuda bir teyit eder misin. Çünkü bu 2. hatadan 100bin tane falan atıyor logda situation başladığı için her ay bakmaya çalışıyor ve sürekli spamlıyor bu hatayı logda.
- Edit: Evet ülke var olmadığı içinmiş 1375 te MGO çıkınca error logları gitti ama ondan önce dediğim gibi çok fazla hata atıyor ona bir çözüm bulmak lazım.

#### 9. Modifierlar ve Karakter yaratılması hakkında (FIXED)

- 1. Mongol Horde yani MGO 1375te çıktıktan sonra ona giden modifierları gördüm mesela mongol warrior spirit(terminator) diye bir modifier gitmiş ama terminator game rule'u yok ki bizde mesela neye göre neden gitti bu? Ayrıca bu modifierlar doğru zamanda kaldırılmıyordu oyun sonuna kadar kalıyor onlarıda Prussian Destinydeki gibi situation bitince kaldırmamız gerekiyor ayrıca MR_mongol_preparing_for_conquest: "Mongol War Preparations" modifierın locları STATIC_MODIFIER_NAME_MR_mongol_preparing_for_conquest olarak gözüküyor Mongol War Preparations olarak gözükmesi gerekirken, yani loclar çalışmamış neden bilmiyorum ama mongol warrior spirit(terminator) ün locları çalışıyor. Başka böyle sorunlu modifierda varsa düzelt lütfen.

- 2. Birde şu özelliği eklesek çok güzel olur vanilla timurdaki gibi: Vanilla timur da timur ülkesi spawnlandığı zaman eventle timur ülkenin başına geliyor ve emir timurda yani sadece ülkeye değil karakterin kendisine de bufflar geliyor Conquerer's Vitaly ismin de Character life expentacy buffu ve The Scourge From Central Asia ismin de diye baya detaylı bir buff alıyor bizde bu tarz bir şey yapabiliriz ve bizim mgo ülkemiz çıktığı anda Borjigin hanedanından mı sence bir karakter oluşturmak güzel olur mu Borjigin den bir karakter ya da bizim modumuza göre tarihsel en iyi hangisi ne şekilde olursa öyle yapalım.

#### 10. Mongol Imperial situation GUI sindeki sorunlar !!!(NOT FIXED LOOK AGAIN)!!!

- 1. (NOT FIXED LOOK AGAIN): GUI de karakter portresi böyle simsiyah boş gözüküyor sanki karakter yok gibi ilk situationda yani mongol resurgence de doğru gözüküyorda ama bu 2. mongol imperial situationında bozuk gözüküyor. Loglara baktım loglarda böyle diyor ve 2. situation gui panelini açtığım anda ve açık tuttuğum sürece bu aşağıda attım errorleri spawnlıyor logda oyun çökmüyor ama spnawlıyor bu hataları:

[cw] [error] [pdx_gui_data_manager.cpp:233] FetchData failed for 'Not(Character.IsAlive)' - gui/shared/cards.gui:1037
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Character' for 'Character.GetDeathInfo' 
[cw] [error] [pdx_data_localize_helper.cpp:290] FetchData failed for 'Character.GetDeathInfo'
[cw] [error] [pdx_gui_localize.cpp:140] PdxDataFetch Localized Data failed for '[Character.GetDeathInfo]'
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Character' for 'Character.IsAlive'
[cw] [error] [pdx_gui_data_manager.cpp:233] FetchData failed for 'Character.IsAlive' - gui/shared/cards.gui:1053
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Character' for 'Character.HasCourt Country'
[cw] [error] [pdx_gui_data_manager.cpp:233] FetchData failed for 'Character.HasCourt Country' - gui/shared/cards.gui:1055
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Character' for 'Character.GetCourt Country.IsReal' 
[cw] [error] [pdx_gui_data_manager.cpp:233] FetchData failed for 'Character.GetCourt Country.IsReal' - gui/shared/cards.gui:1057
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Character' for 'Character.GetCourt Country' 
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Character' for 'Character.GetRoleName' 
[cw] [error] [pdx_gui_data_manager.cpp:233] FetchData failed for 'Not(EqualTo_string(Character.GetRoleName, "'))' - gui/shared/cards.gui:1066 
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Character' for 'Character.GetRoleName' 
[cw] [error] [pdx_data_localize_helper.cpp:290] FetchData failed for 'Character.GetRoleName'
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Character' for 'Character.GetCourt Country.GetName' 
[cw] [error] [pdx_data_localize_helper.cpp:290] FetchData failed for 'Character.GetCourt Country.GetName'
[cw] [error] [pdx_gui_localize.cpp:140] PdxDataFetchLocalizedData failed for 'EVENT_CHARACTER_FOREIGN'
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Character' for 'Character.GetRoleName'
[cw] [error] [pdx_gui_data_manager.cpp:233] FetchData failed for 'EqualTo_string(Character.GetRoleName, "')' - gui/shared/cards.gui:1073
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Character' for 'Character.GetCourt Country.GetName'
[cw] [error] [pdx_data_localize_helper.cpp:290] FetchData failed for 'Character.Get Court Country.GetName'
[cw] [error] [pdx_gui_localize.cpp:140] PdxDataFetchLocalizedData failed for 'EVENT_CHARACTER_FOREIGN_NO_ROLE'
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Character' for 'Character.GetCourt Country'
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Character' for 'Character.GetNameToFit('(int32)22', '(bool)yes')' 
[cw] [error] [pdx_data_localize_helper.cpp:290] FetchData failed for 'Character.GetNameToFit('(int32)22', '(bool)yes')'
[cw] [error] [pdx_gui_localize.cpp:140] PdxDataFetchLocalized Data failed for '[Character.GetNameToFit('(int32)22', '(bool)yes')]'
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Country' for 'Country.GetGovernment'
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Government' for 'Government.GetRuler' 
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Government' for 'Government.HasRuler' 
[cw] [error] [pdx_gui_data_manager.cpp:233] FetchData failed for 'Government.HasRuler' - gui/character_header.gui:281
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Character' for 'Character.GetReligion' 
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Government' for 'Government.GetActiveRegent' 
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Government' for 'Government.HasActiveRegent' 
[cw] [error] [pdx_gui_data_manager.cpp:233] FetchData failed for 'Government.HasActiveRegent' - gui/character_header.gui:291
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Character' for 'Character.GetReligion'
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Government' for 'Government.GetRegencyInfo' 
[cw] [error] [pdx_data_localize_helper.cpp:290] FetchData failed for 'Government.GetRegencyInfo'
[cw] [error] [pdx_gui_localize.cpp:140] PdxDataFetchLocalized Data failed for '[Government.GetRegencyInfo]'

- 2. (NOT FIXED LOOK AGAIN): Aynı zamanda Imperial Expansion Progress sekmesi boş gözüküyor hiç bir şey gözükmüyor. Aynı zamanda o sekme neden vardı bide bilmiyorum açıklarsan iyi olur.
- 3. (NEW ERROR): 3. Situationda da aynı şekilde situation başladı başladıktan sonrasituation'ın guisini açıtğım anda bu error log spamlanıyor oyun içinde aam oyun çökmüyor:

[cw] [error] [pdx_data_localize_helper.cpp:290] FetchData failed for 'Character.Get Court Country.GetName'
[cw] [error] [pdx_gui_localize.cpp:140] PdxDataFetch LocalizedData failed for 'EVENT_CHARACTER_FOREIGN'
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Character' for 'Character.GetRoleName'
[cw] [error] [pdx_gui_data_manager.cpp:233] FetchData failed for 'EqualTo_string(Character.GetRoleName, "')' - gui/shared/cards.gui:1073
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Character' for 'Character.GetCourt Country.GetName'
[cw] [error] [pdx_data_localize_helper.cpp:290] FetchData failed for 'Character.GetCourt Country.GetName'
[cw] [error] [pdx_gui_localize.cpp:140] PdxDataFetchLocalized Data failed for 'EVENT_CHARACTER_FOREIGN_NO_ROLE'
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Character' for 'Character.GetCourt Country'
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Character' for 'Character.GetNameToFit('(int32)22', '(bool)yes')' 
[cw] [error] [pdx_data_localize_helper.cpp:290] FetchData failed for 'Character.GetNameToFit('(int32)22', '(bool)yes')'
[cw] [error] [pdx_gui_localize.cpp:140] PdxDataFetchLocalized Data failed for '[Character.GetNameToFit('(int32)22', '(bool)yes')]'
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Country' for 'Country.GetGovernment' 
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Government' for 'Government.GetRuler' 
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Government' for 'Government.HasRuler' 
[cw] [error] [pdx_gui_data_manager.cpp:233] FetchData failed for 'Government.HasRuler' - gui/character_header.gui:281
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Character' for 'Character.GetReligion' 
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Government' for 'Government.GetActiveRegent' 
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Government' for 'Government.HasActiveRegent' 
[cw] [error] [pdx_gui_data_manager.cpp:233] FetchData failed for 'Government.HasActiveRegent' - gui/character_header.gui:291
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Character' for 'Character.GetReligion'
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Government' for 'Government.GetRegencyInfo' 
[cw] [error] [pdx_data_localize_helper.cpp:290] FetchData failed for 'Government.GetRegencyInfo'
[cw] [error] [pdx_gui_localize.cpp:140] PdxDataFetch Localized Data failed for '[Government.GetRegencyInfo]'


##### 23.07.2026 TEST RESULTS #####


#### 1. Event Entryleri eksik:

- Dhe eventlerin entryleri eksik onları ekler misin. Oyun içi debug logunda yazdı o şekilde fark ettim:

[game] [error] [localization_util.cpp:103] mr_history.1.entry: "Mr history.1.entry" 
[game] [error] [localization_util.cpp:103] mr_history.2.entry: "Mr history.2.entry" 
[game] [error] [localization_util.cpp:103] mr_history.3.entry: "Mr history.3.entry" 
[game] [error] [localization_util.cpp:103] mr_history.5.entry: "Mr history.5.entry" 
[game] [error] [localization_util.cpp:103] mr_history.6.entry: "Mr history.6.entry" 
[game] [error] [localization_util.cpp:103] mr_history.7.entry: "Mr history.7.entry" 
[game] [error] [localization_util.cpp:103] mr_history.8.entry: "Mr history.8.entry"

- Ayrıca Dhe eventlerinin içeriklerini çok daha güzel tarihsel düzenler misin mesela mr_history.1 eventinde 1337 de Yuan (CHI) direk eventi alıyor ama Red turban rebellion daha çıkmamış mesela ve eventlerin özellikleri için verdiği aldığı etkiler nerdeyse yok hiç veya sadece bir army tradition gibi buff vermektense onları güzel bir şekilde nasıl yapabiliriz doldurabiliriz sence mesela benim Prussian Destiny modumdan ya da EU5 vanilla DHE eventlerine bakabilirsin fikir istersen ama bizim konumuzla uyumlu olsun yani tarihsel olsun. Aklıma gelen örnekler: market kurma başkente buff verme bina/asker basma vs.

#### 2. Situation guisindeki localization geliştirmeleri:

- Situation end requirementlarında mesela mr_resurgence_end_tt: "#Y MGO holds Karakorum and the entire Mongolian heartland.#! No rival banner remains anywhere in the Mongolia region." gibi yazmaktansa benim Prussian Destiny modumdaki gibi: prussian_ascension_silesia_tt: "Prussia or its subjects own all [locations|e] in the [ShowAreaName('silesia_area')] [area|e]" gibi ve prussian_ambition_brandenburg_tt: "Prussia or its subjects own all [locations|e] in the [ShowAreaName('brandenburg_area')] [area|e]" tarzı bu şeyleri gösterlim çünkü bunları kullanınca (area|e locations|e) gibi kullanınca situation üstünde fare ile üstüne gelip o bölgeleri görebiliyoruz o şekilde yaparsak çok daha açıklayıcı olur oyuncu için ve daha stil olarak profesyonel olur çünkü vanilla EU5 te hep o şekilde yapıyor situationların da ordan da örnek alabilirsin istersen.

#### 3. Mongol_Resurgence yani ilk Situation guisindeki sıkıntılar:

- guinin o altındaki mr_first_claimant doğru sadece monoglia regionından seçiliyor ama mr_first_rival mongolia region limiti yok oyüzden bütün governmenti steppe_horde olanlardan seçiliyor ta gidip irandaki perste yerdeki horde ülkesi gidip mongolia regionındaki mr_first_claimant'a rival oluyor saçma oluyor onu ben düzelttim kodda ama sen yine bir kontrol et doğru mu diye. Birde aklıma şu geldi mr_first_rival'ı random seçmek yerine en güçlü askeri gücü olan ülkeyi seçmemiz daha mantıklı olur gibi mr_first_claimant için yapmasakta olur galiba zaten ilerde MGO oraya geçicek diye düşündüm. Ben ayrıca situation başladığında verilen buff ülkelerini, situationa dahil olan ülkeleri ve map colorlarını sınırladım middle eastteki veya avrupadaki hordelar almasın diye şu şekilde: capital ?= {OR = {sub_continent = sub_continent:east_asia sub_continent = sub_continent:north_asia}}.

#### 4. Oyun ilk başlayınca loga düşen uyarı ve hatalar:

1. Hata:
[game] [error] [country_database.cpp:98] MGE has the name 'empire' in it, which does not work for a tag, which would like silly as 'The Great TAG Empire Empire'
- Bu hatada aklıma gelmişken şunu da sorayım: Biz neden loc dosyasında FLAG LOCALIZATION diyerek orda mgo ve mgeyi tekrar tanımladık zaten vanillada var olan ülkeler ya ondan kafam karıştı tanımlamamız gerekiyor muydu yine orda?

2. Hatalar:
[cw_gui] [error] [pdx_gui_factory.cpp:624] gui/panels/situation/mongol_imperial.gui:116 - 'textbox_single' is not a valid widget/type/property 
[cw_gui] [error] [pdx_gui_factory.cpp:624] gui/panels/situation/mongol_imperial.gui:125 - 'progress' is not a valid widget/type/property
[cw_gui] [error] [pdx_gui_factory.cpp:624] gui/panels/situation/mongol_dominance.gui:117-'textbox_single' is not a valid widget/type/property
[cw_gui] [error] [pdx_gui_factory.cpp:624] gui/panels/situation/mongol_dominance.gui:126 - 'progress' is not a valid widget/type/property


#### 5. MGO ortaya çıkma ile ilgili soru soruyorum sana:

- Şu MGO nun ortaya çıkma mantığını tam anlamadım. 1368 de ilk situation başlıyor ama hiç MGO haritada olmuyor. 1375 ten sonra çıkmazsa 1375te biz rastgele ülkeyi ona çeviriyoruz ya, peki bu 1375 ten önce yani 1368 den 1375'e kadar olan zamanda çıkma ihtimali var mı ki nasıl oluyor orası yani tam anlamadım o kısmı.

#### 6. İlk situation çağırılınca gelen 8bine yakın hata:

- İlk situation geldiği anda ve ben situationı guisini açtığım anda oyun içinde ki debug logda böyle 8bine yakın bu aynı errorden error bu:

[cw] [error] [pdx_text_formatter.cpp:807] Unknown formatting tag 'l'

- Ama bu error bizim guilemi alakalı bilmiyorum ama dediğim gibi bizim situation geldiği anda geldiğine göre bu error logu heralde bizimkiyle alakalı.  Ama oyunu çöktürmüyor sadece logda yazıyor bi bakar mısın.

#### 7. MGO için seçilen ülke sıkıntısı:

- MGO için seçilen ülke mesela başka horde ülkesinin veya başka ülkenin vassalı da olabiliyor. Bu bence çok saçma ya seçilen ülke vassal olmayan ülke olsun ya da vassal ülke seçiliyorsa vassalığı bitsin. Ayrıca bu MGO olacak ülke seçilirken o situation bölgesindeki en güçlü horde ülkesi de seçilebilir, rastgele seçilme olmasındansa bence daha mantıklı olur.
- Ayrıca aklıma şu da geldi seçilecek ülke savaşta ikende seçilebiliyor şuan onu da acaba savaşta değilken seçilecek şekilde mi yapsak sence hangisi daha mantıklı olur?

#### 8. Çoğu eventte aynı modifierları tekrar vermişsin her situation veya eventlerde:

- Çoğu dhe veya normal evetnlerde ve situation içindeki kodlarda hep aynı modifierları country olarak eklemişsin mesela MR_unified_mongol_banner hem mongol imperialda var hem MR_dominance_dhe_events'te var hem MR_dominance_events.txt te var hem de MR_late_steppe_events'te var ve bazı eventlerde ve dhe eventlerinde veya MR_late_steppe_events'teki mr_steppe.22 veya mr_dominance.1 eventinde direk buff game rule'una bakmadan eklemişsin modifierı onları komple düzeltelim ayrıca ekstra tarihsel bir sürü modifier veya başka bir şey ekleyebilirsin farklı farklı önemli değil yeter ki tarihsel, mantıklı, çeşitli ve özgün olsun. Daha fazla bilgi için 9.madde (9. Kendi eklemelerim hakkında bilgilendirme ve isteklerim:) kısmına da bakabilirsin.
- Ayrıca modifier isimlerini ve genel oalrak tüm locları ve açıklamaları daha özgün ve tarihsel yapabilirsin yani demek istediğimi örnekle açıklayayım: Prussian Destiny ile çok benzer olmasına gerek yok, mesela Fullfilled prussian destiny modifier ismini mongolda da Fulfilled mongol destiny yapmışsın illa o kadar çok benzer yapmaya gerek yok.

#### 9. Kendi eklemelerim hakkında bilgilendirme ve isteklerim:

- Kendim başka moddan gördüm MR_great_khan modifier'ını güncelledim ve ekstra o çıkan MGO lideri için bi modifier daha ekledim MR_historically_needed adında onu da mr_dominance.104 eventin de ekledim ve ayrıca conqueror traitinin yanına ekstra tactical_genius, strategist ve cruel ekledim.
- Ayrıca bazı modifierlar da reason_to_elect modifierlarını unutmuşsun onları sildim onlar HRE içindi Prussian Destiny modum da, ve monthly_legitimacy olanları monthly_horde_unity yaptım hordelarda legitimacy yerine horde_unity var çünkü. Ayrıca bu scopeları: exists = scope:mr_first_rival, exists = scope:mr_first_claimant bunları exists yapmışsın sadece, ben onları elimle hepsini country_exists yaptım haberin olsun. 
- Ayrıca  dhe eventlerin monthly_chancelerini hep 1 yapmışsın o 1% oluyor ben hepsini 100% yaptım o tarih gelince gelsin 1% yapmayalım.
- Ekstra DHE event ekledim Prussian Destiny modumda pd_brandenburg_dhe.1 ve pd_brandenburg_dhe.2 mirror olarak MR_dominance_dhe_events.txt içine ekledim onları düzeltir misin bize uygun olarak mantıklı olmaz mı o eventler daha önce de senden istemiştim 8. madde de hatırlarsan. İstersen pd_brandenburg_dhe.3, pd_brandenburg_dhe.4 ve devamını da entegre edebilirsin bizim modumuza tarihsel ve çzgün mantıklı olacaksa normal eventlere de bakıp ordan da fikir alabilirsin.
- Benim diğer isteğim 2. ve 3. situationlarda da veya aralarda da bence MGO çıkarken eklediğimiz gibi character oluşturup ekleyelim bence güçlü olsun diye. Çünkü düşünsene tarihte de Genghis Khan yani Temüjin öldüğünde bile tahta gelen oğulları çok uzun süre çok güçlü ve başarılı fetihler yapmıştı o sebeple ona da özgün ve güzel bir şeyler düşünebiliriz, belki character oluşturmaktansa mevcut gelen o Batu Khan'ın oğlu varsa mesela ona da verebiliyorsak öyle de yapabiliriz gibi düşündüm, bence çok güzel olur.

#### 10. Time Pacing game rule'u hakkında:

- Prussian destiny de evet game rule'unda timeline pacing game rule'u vardı çünkü prusya tarihte çok daha geç ortaya çıktığı için bizim o modumuz tam tarihsel olmuyordu ondan eklemiştik tamamen tarihsel oynamak isteyenler iyice bekleyip situationları ve eventleri uzatabilsin diye mantık buydu. Ama bizim mongol modumuzda buna gerek yok bence o sebeple  MR_timeline_pacing_rule game rule ve mantığını komple çıkartabiliriz ona iyice bakar mısın detaylı düzgünce kaldıralım onu ve ona bağlı olan kod varsra onları düzeltir misin.

#### 11. MR_mongol_imperial.txt Link Hatası
- Logda böyle hata geldi fixleyebilir bir sıkıntı olmadı daha sonra da gelmedi ve oyunu çökertmedi. Çözümü sanırım o owner kısımlarını owner = yerine owner ?= yapmak ki o toprak veya ülkeye bir şey olursa hata gelmesin diye capital ?= mantığı gibi.

[game] [error] [jomini_script_system.cpp:252] Script system error! Error: Event target link 'owner' returned an invalid object
Script location: common/situations/MR_mongol_imperial.txt:559

#### 12. Üçüncü situationa geldim:

- 3.Situation (Mongol Dominance) da MR_late_steppe.txt ek situationlarının yapısı ve amacı nedir? Daha iyi, özgün ve mantıklı olabilir. Daha önce de sana söylediğim o situationdaki eventler (MR_late_steppe_events.txt) içindeki ödüller falan hep eski ve aynı modifierlar, yaratıcılıktan yoksun basit ödüller var. Lütfen o kısımları daha önce de 9. madde de belirttiğim gibi özgün, yaratıcı ve tarihsel yapalım.

#### 13. Son isteğim:
 
- MGE_F yani Mongol Empire'ı bence direk formlatabiliriz. form_country kodunu kullanınca formable country requirementlarına gerek olmadan direk onları ezip formlatabiliyoruz. Onu sen yanlış anlamışsın sanırım. O sebeple benim isteğim çok geç formlatmaktansa mesela 2. situation bitince formlatmak daha mantıklı ve tarihsel olmaz mı? Sende karar verebilirsin formlatma zamanı için. Ama tabi böyle yapacaksak ona göre tagların MGE veya MGO yazan yerleri ve diğer tüm kodları bu değişikliğe göre güncellememiz gerekicek çünkü erken formlatıcaz ya, hata veya loop bug falan çıkmasın. Bu nedenle o Mongol Empire formlama için istenilen topraklara gerek olmayabilir çüğnkü onlar kodsuz normal oynarken formlayacaksan gereken zorunluluklar. 3. situation yapısını toprak isteklerini de falan komple değiştirebilirisn bu konuştuklarımıza göre ve mesela iran kısımları, anadoluya kadar benim bildiğim moğollar gitmişti/fetih etmişti. Tarihsel olarak oraları atladık oraların situationları falan yok ayrı bir situation da yapabilirsin veya başka situation ile birleştirme de yapabilirsin. Sana bırakıyorum ve güveniyorum.


#### FİNAL NOT: Evet şuan gözüme çarpan ve oyun içinde debug logda ortaya çıkan hatalar bu şekildeydi bunları düzelttikten sonra tekrar bizim ana CLAUDE.md, diğer tüm .md dosyalarımızı ve bunlarla ilgili bir içerik rehber falan varsa onları da güncelleyip elden geçirir misin detaylı bir şekilde. MD dosyalarımız güncel kalsın ki ilerde bu modu kullanıcaksam veya başka sıfırdan bir mod yapacaksam işimize yarasın.


##### 23.07.2026 CLAUDE FIX PASS (23.07 maddelerinin hepsi + 22.07 #10) #####

Tum degisiklikler statik dogrulamadan gecti (verify_mod.py: all checks passed). Oyun ici test edilmedi — TESTING-GUIDE.md guncellendi, oradaki yeni checkpointlerle test et.

- (22.07 #10.1/10.3 FIXED) Siyah portre: one_country_header_template'in blok adi "CountryContext" + "character_portrait_anchor" imis (vanilla rise_of_the_ottomans.gui:13 birebir ayni pattern); biz iki-ulke template'inin "FirstCountryContext" adini override ediyorduk, o yuzden context hic baglanmiyordu. Iki GUI'de de duzeltildi — Character/Government log spami de bununla birlikte gitmeli.
- (22.07 #10.2 FIXED) Bos "Imperial Expansion Progress" sekmesi: "textbox_single" ve "progress" diye widget/property YOK (vanilla 0 kullanim). text_single + progressbar'in value/min/max'i ile yeniden yazildi. O sekmenin amaci: fazin 0-100 hedef ilerleme cubugu (MR_mge_score / MR_dominance_score).
- (#1 FIXED) mr_history.N.entry loc anahtarlari eklendi (7 event + yeni .9). Tarihler tarihsellestirildi: Yuan cokusu artik 1351 (Red Turban cikisi, 1337 degil), Chagatai bolunmesi 1347, Tokhtamysh 1380, Delhi yagmasi 1398 (TIM'e ganimet + DLH'ye yeni ayna event mr_history.9 "The City of Ashes"), Oirat/Esen 1435, Babur 1500. Hepsi monthly_chance = 100 (yuzde; vanilla'da 80 kullanim var, tarih gelince kesin atiyor).
- (#2 FIXED) End requirement tooltipleri PD stiline cevrildi: [ShowLocationName/ShowAreaName/ShowRegionName(...)] + [locations|e]/[area|e]/[region|e].
- (#3 FIXED) Senin rival duzeltmen dogrulandi + rival artik random degil EN GUCLU steppe horde (order_by = military_strength, max = 1, check_range_bounds = no — vanilla war_of_religions.txt:54 idiomu). Claimant secimine mongolia_region sarti geri kondu (senin subcontinent filtren rival'da duruyor).
- (#4.1 FIXED) "MGE has the name 'empire'" uyarisi: hicbir vanilla tag adinda "Empire" gecmiyor (vanilla MGE = "Mongolia"). Bizim override "Mongol Empire" oldugu icin uyari geliyordu. Tag adi artik "Yeke Mongol Ulus" (tarihsel ad), formable butonu "Mongol Empire" kaldi. FLAG LOCALIZATION'in nedeni: vanilla iki tagi da duz "Mongolia" diye adlandiriyor, biz Horde/Ulus ayrimi icin override ediyoruz — gerekli ve dogru.
- (#4.2 FIXED) textbox_single/progress gui factory hatalari — yukaridaki widget duzeltmesiyle gitti.
- (#5 CEVAP) 1368-1375 arasi MGO'nun ORGANIK cikis yolu aslinda kodda yoktu (sadece oyuncu manuel formlayabilirdi, MGO_f'nin sarti Mogolistan'in %85'i!). Simdi eklendi: Karakorum'u alan ozgur Mongol steppe horde aninda MGO olur (form_country allow'u bypass eder, PD dhe.4 pattern'i). 1375 failsafe artik EN GUCLU adayi seciyor (kademeli: baristaki ozgur horde → ozgur horde → son care herkes; son carede vassalsa once overlord'u cancel_subject ile serbest birakiyor).
- (#6 ACIKLAMA) "Unknown formatting tag 'l'" spami: mod dosyalarinda #l YOK (byte byte tarandi; #L gecerli ama kucuk 'l' vanilla'da da yok). Kaynak, horde hukumdari/naiplik metnini formatlayan VANILLA loc ciktisi — bizim duzeltebilecegimiz bir satir yok. Zararsiz log gurultusu; P2/P3 panelleri artik render oldugu icin orada da gorulebilir. TESTING-GUIDE Track 8'e "watch-only" diye eklendi.
- (#7 FIXED) MGO adayi secimi yukarida (#5). Savas durumu karari: dogum failsafe'i savas filtresiyle KILITLENMEMELI (herkes savastaysa railroad olur), o yuzden "baristaki en guclu" sadece 1. tercih kademesi.
- (#8 FIXED) Modifier tekrari bitti: dhe.1 → yeni MR_forge_of_warriors, dhe.4 → MR_kurultai_mandate, mr_imperial.201 → MR_western_ulus_restored, mr_steppe.22 → MR_dzungar_legacy. Faz buff/odulleri SADECE situationlarda ve buff rule'a bagli. "Fulfilled Mongol Destiny" → "Master of the Steppe" olarak ozgunlestirildi.
- (#9 FIXED) Senin eklediklerin dogrulandi: country_exists = scope:/var: vanilla-attested (PD brandenburg_rise.txt:449 ayni yerde kullaniyor — degistirmene gerek yoktu ama dogru); monthly_chance = 100 gecerli; traitler (tactical_genius/strategist/cruel) + is_immortal + monthly_horde_unity hepsi mevcut. MR_modifiers'ta bir yazim hatasi duzeltildi: army_light_cavalry_power = 0.0.5 → 0.1. PD dhe.1/2 kopyalari Mongollastirildi: mr_dominance_dhe.9 "The Reforged Tumen" (Karakorum'da kurultai+armory binalari, steppe horse archers, pop donusumu, horse_lords advance) ve .10 "Karakorum Restored" (sehir ranki, kale, barracks, MARKET kurma, oirat/buryat/khamag kabul). P2/P3 baslarken yeni Borjigin hanlar: Adai (1420) ve Altan (1550) — Beat 104 seklinin aynisi, Scourge + Historically Needed + era traitleri.
- (#10 FIXED) MR_timeline_pacing_rule komple kaldirildi (rule + loc + kod). Tempo artik SADECE buff rule: Terminator ~6 ay, Historical ~1 yil, Vanilla ~2 yil. NOT: senin duzenlemede buff-disabled + frontloaded kombinasyonunda hicbir dal calismiyordu (railroad hic savas acmazdi) — uc kademeli yeni yapida her tier'in dali var.
- (#11 FIXED) owner ?= taramasi: uc situation'daki TUM failsafe bloklari (P1 1, P2 3, P3 10 blok) owner ?= yapildi — sahipsiz lokasyon link hatasi sinifi kapandi.
- (#12 FIXED) Late-steppe odulleri ozgunlestirildi: Chahar → The Seal of Chinggis, Torghut → The Volga Pastures + tribal_cohesion/horde_unity dokunuslari, Dzungar → The Dzungar Legacy + research_progress (top dokumhaneleri temasi).
- (#13 FIXED — BUYUK DEGISIKLIK) MGE artik P2 basariyla biter bitmez ilan ediliyor (on_ending'de form_country; MGE_f'nin form_effect'i empire rank + vanilla'nin 50 yillik restoration modifierini de veriyor). P3 komple yeniden tasarlandi: "The Four Khanates" — hedef artik MGE_f'nin dokuz formable lokasyonu degil, tarihsel dort hanlik: Karakorum+Dadu (Yuan), Samarkand (Chagatay), Sarai+Kazan (Altin Orda), Tabriz+Baghdad (Ilhanli) + TUM persia_region temiz + Rus topraklari + Kapadokya (Kosedag) ayak izi. Westward CB kapsami persia/anatolia/iraq_arabi/armenian_highlands'i da kapsiyor (kapsam kurali korundu), failsafe yeni hedefleri devrediyor, skor 10x10 yeni hedeflerle, 992 tiyatro secimi guncellendi. Guney Cin koltuklari (Kaffa/Shangyuan/Baxian/Guangzhou) hedeften cikti. Yan etki: P3'un c:MGE hata spami sinifi tamamen bitti (MGE artik fazin ilk gununden var) ve dhe.7/8 (tag=MGE) artik gercekten atabiliyor.
- (FINAL NOT FIXED) CLAUDE.md (yeni referans yolu dahil — bu makinede "Reference EU5 vanilla and Prussian Destiny/" klasoru!), MOD-DESIGN-IDEA.md, TESTING-GUIDE.md ve 3 skill guncellendi. verify_mod.py'ye noktali tooltip anahtari destegi eklendi.


##### 23.07.2026 AUDIT TURLARI (2-3) + YENI ICERIK #####

Denetim turlarinda 6 gercek bug daha bulunup duzeltildi (hepsi statik dogrulamadan gecti, oyun ici test bekliyor — TESTING-GUIDE'daki yeni satirlar: 2.5, 2.14, 3.7, 3.11, 4.10, 5.7, 5.8, Track 8):

- (FIXED) FAZ GECISI KOPUKTU: P2 basariyla bitince mr_phase_two_complete set edilmiyordu (ilan MGO'yu MGE yapinca on_ended'daki trigger yeniden-degerlendirmesi false donuyordu) — Faz 3 hic baslamazdi. Global artik on_ending basari dalinda set ediliyor + mr_dominance.125'te yedek.
- (FIXED) UYUYAN HORDE KILIDI: P1 BASARISIZ bitse bile AI MGO'ya Sleeping Horde veriliyordu — P2 hic baslamayacagi icin AI sonsuza dek savas acamazdi. Grant artik sadece basari yolunda.
- (FIXED) TUMU ULASILMAZDI: mr_steppe.2 (Tumu tepkisi) sadece 1604+ Chahar'dan dinleniyordu ama kriz ~1449'da olur. Izleyici P2 on_monthly'ye tasindi (Chahar'daki fallback olarak durur).
- (FIXED) owner = c:MGO x3: dhe.9/10'a eklenen tag = MGE sonrasi MGE olarak atarsa olu link olurdu — owner = root yapildi, market kontrolundeki owner sarti kaldirildi.
- (FIXED) HAN ISTIFI: uc kusak hanin MR_great_khan + olumsuzluk modifierlari ust uste binebilirdi — yeni han tahta cikarken eskisinden sokuluyor (ruler ?= remove_character_modifier, vanilla grand_embassy.txt:46).
- (FIXED) INSAN OYUNCU KORUMALARI: (a) Karakorum'u alan INSAN horde artik zorla MGO yapilmiyor — yeni "The Banner Offered" eventi (mr_dominance.11) teklif ediyor, reddedilebilir; 1375 failsafe'i AI adaylari tercih ediyor. (b) Vanilla-buff kuralinda insan oyuncu P2 ortasinda MGE'yi elle formlarsa faz kazanilamaz oluyordu — mr_imperial_end_trigger ve P2 on_ending cift-tag yapildi.

- (YENI ICERIK) mr_dominance_dhe.11 "The Observatory of Samarkand" (Ulug Bey rasathanesi, 1424+, oyuncuya da gelir), mr_dominance_dhe.12 "The Count of the Herds" (Yasa sayimi, iki secenekli: asker vs vergi), mr_dominance.135 "The Four Corners" (dort hanlik baskenti ayni anda tutulunca atan P3 kilometre tasi), mr_dominance.11 "The Banner Offered" (insan organik dogus teklifi).
- (MD GUNCELLEMESI) EU5-MODDING-GUIDE'daki eski iki-loc-agaci kurali tek-dosya kuralina cekildi, harness sayisi 22 oldu; README duzgun Ingilizce tanitim + dokuman haritasi yapildi; YENI docs/FUTURE-DEVELOPMENT.md eklendi (Ingilizce, detayli: genisletme yollari, tarif kitaplari, bilinen borclar, done-tanimi).




##### 24.07.2026 AND 25.07.2026 TEST RESULTS #####

### 1. GUI bilgilendirmesi daha açıklayıcı yapalım:

- Mongol resurgence situationın da Mongol Horde yani MGO ülkesinin nasıl çıktığını falan guiye bence bilgilendirme olarak yazalım ayrıca onuda görsün oyuncular bakarlarken.

- Ayrıca unknow formatting [cw] [error] [pdx_text_formatter.cpp:807] Unknown formatting tag 'l' hatası hala geliyor situation guisini açtığım an her situaton da, acaba bu şeyden olabilir mi: Vanilla gui formatlarına baktım hepsi sadece UTF-8. BOM yapmamışlar ondan olabilir mi bizimkilerin hepsi UTF-8 with BOM. Bence sorun o.

### 2. Region,area,subcontinent ve Situation Fetih bölge değişiklikleri:

- steppes_region bölgesi yeni eklediğim docs/maps dosyasından da bakarsın taa kırımın oraları kapsıyor ama sen resurgence visible kısımlarına falan steppes_region eklemişsin zaten ilk situation oralarla alakası yok ki, ben onu değiştirdim oralar subcontinent'e göre yaptım güzel oldu, ve docs/maps/ içine de subcontinentslerin tüm mapi kapsayan resmini koydum ordan da bakıp doğrulamasını yapabilirsin istersen ve başka bu tarz güncellenecek yer varsa güncelleyebilirsin.

- biz neden sadece north_china'yı fetih ediyoruz situationlarımızda neden bütün China regionını(north_china_region,west_china_region ve east_china_region dışarda kalıyor) almıyoruz. Tarihte olduğu gibi, tarihsel gidelim dedik ya, sence onu tüm chinayı almayı 2. situationamı yoksa 3. situationamı eklemeliyiz ve sonrasın da ona göre her şeyi günceller misin mantık hatası olmaması için. Ayrıca şimdi farkettim tibet_region'nınıda da eklememişiz tarihte moğollar orayıda almıştı cengiz han zamanın da diye biliyorum orayı da ekleyelim China bölgesi gibi. Ben Wargoals ksıımlarını biraz düzeltmiştim ama sen yine bak bu son yapacaklarımıza göre düzenle.


#### 3. Diğer ülkere event ile haber gönderimi bilgilendirme ve immersion için:

- Ben bunu Prussian Destiny modumda da yapmıştım immersiokn için çok güzel oluyor. Mantığı şu mesela örnek veriyorum mongol oyuncu veya AI fark etmez situaton başlattı zaman belli yerleri aldığı zaman falan o bölgedekilere o bölgenin bitişinde yakın olan ülkelere de uzakta oklsa da bilgilendirme eventleri gidicek. Mesela o situation bölgesinde olan ve mongolun onu hedefleyeceği kurban ülkelere mesela korku eventi gidecek mesela gibi giib bu tarz immersion için çok güzel eventler ekleyebilirsin her situation için ve çoğu yere bunlara iyice bak ve mantık hatası olmadan bug olmadan ekle. Prussian Destiny Event Örneği: pd_brandenburg.101, pd_brandenburg.102, pd_brandenburg.201 ve pd_brandenburg.202 gibi eventlere bakabilirsin fikir için. 

- Ayrıca şimdi aklıma geldi bu tarz pd_brandenburg.200 gibi ally bozma eventide ekleyebiliriz AI sıkışmasın etrafındakiler için eklemiştim ben situation başlarken PD moduma. Sen bak lazımsa ekle analiz et.

#### 4. Mongol Horde ilk situation gui hatası:

- Mongol resurgence guisinde Mongol Horde MGO hem mr_first_claimant hem de mr_first_rival olarak 2 sindede gözüküyor yani hem first claimant hem de kendisinin rakibi olarak 2 tane ayrı mgo bayrağı gözüküyor guide :D
Bu sanırım tahmini(artık tahmin değil kesin öyle test ettim) şundan dolayı oldu: MGO 1375te spawnlanmadan önce MGO olacak ülke mr_first_rivaldı. Rival olan en güçlü diye MGO oldu, o MGO olunca mr_first_claimanta atandı ve hem mr_first_claimantta hem de mr_first_rivalda kaldı buglandı.

#### 5. MR_the_sleeping_horde Modifier'ının Gereksizliği ve Mantık Hatası:

- Bu modifier situation 1 ile situaton 2 arasında ki geçişte savaş olmasın diye var yazmışsın ama zaten situation 1 bitti zaman situation 2 direk başlıyor çünkü situation 2 nin mr_can_start_imperial kodunda bu var: has_global_variable = mr_phase_one_complete o sebeple bu modifier'ı kaldırabiliriz zaten bence tarihsel olarak moğollara uymuyor ben PD için yapmıştım onu.

#### 6. Rise of Timur situationdaki mantığı yapalım:

- Rise of Timur situationın da Select Core Region diye bir seçenek var situation guisinde main actions kısmında. Onu seçince o the scourge from central asia character modifierı varken timurda, o auto conquer at war ile aldığı yerleri direk o main acitons ile core yapıp, Core Regions adında buff veriyor topraklara. Bizde Mongol Horde için ilk situation da öyle yapabilir miyiz? Eğer yapamazsak olmadı ilk situationda alacağı yerleri direk situation da MGO çıktığı gibi MGO ya core ekleyelim olmadı öylede yapabiliriz hangisini yapabilirsek onu seçelim. 2. situation içinde ekleyebiliriz bu mantığı olmadı.

#### 7. Hala 2. Situationdaki guiyi açınca hata spamlıyor ancak resim portre gelmiş siyah değil artık:

- Hatırlarsan son 2 sessiondır bunu (22.07 #10. maddesi) fixlemeye çalışıyoruz: Bu sefer güzel haberlerim var artık eskisi gibi situation guisini açınca karakter portresi siyah olmuyor o düzelmiş ama hala loga guiyi açtığım an sürekli bu hataları arka arkaya spamlıyor:
- Edit: Aynı şekilde 3. situationda da aynı 2. situation da olduğu gibi bu error loglarını spamlıyor ama portre 3. s3ituationda da düzgün düzelmiş siyah değil yani:

[cw] [error] [pdx_data_localize_helper.cpp:290] FetchData failed for 'Government.GetRegencyInfo'
[cw] [error] [pdx_gui_localize.cpp:140] PdxDataFetchLocalized Data failed for '[Government.GetRegencyInfo]'
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Government' for 'Government.GetRuler' 
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Government' for 'Government.HasRuler' 
[cw] [error] [pdx_gui_data_manager.cpp:233] FetchData failed for 'Government.HasRuler' - gui/character_header.gui:281
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Character' for 'Character.GetReligion' 
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Government' for 'Government.GetActiveRegent' 
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Government' for 'Government.HasActiveRegent' 
[cw] [error] [pdx_gui_data_manager.cpp:233] FetchData failed for 'Government.HasActiveRegent' - gui/character_header.gui:291
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Character' for 'Character.GetReligion' 
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Government' for 'Government.GetRegencyInfo' 
[cw] [error] [pdx_data_localize_helper.cpp:290] FetchData failed for 'Government.GetRegencyInfo'
[cw] [error] [pdx_gui_localize.cpp:140] PdxDataFetchLocalized Data failed for '[Government.GetRegencyInfo]'
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Government' for 'Government.GetRuler' 
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Government' for 'Government.HasRuler' 
[cw] [error] [pdx_gui_data_manager.cpp:233] FetchData failed for 'Government.HasRuler' - gui/character_header.gui:281
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Character' for 'Character.GetReligion' 
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Government' for 'Government.GetActiveRegent' 
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Government' for 'Government.HasActiveRegent' 
[cw] [error] [pdx_gui_data_manager.cpp:233] FetchData failed for 'Government.HasActiveRegent' - gui/character_header.gui:291
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Character' for 'Character.GetReligion'
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Government' for 'Government.GetRegencyInfo' 
[cw] [error] [pdx_data_localize_helper.cpp:290] FetchData failed for 'Government.GetRegencyInfo'
[cw] [error] [pdx_gui_localize.cpp:140] PdxDataFetchLocalizedData failed for '[Government.GetRegencyInfo]'

- Nedense bu error log spam artık 1. situation da gui açınca olmuyor, ama 2. ve 3. situation da guiyi açınca oluyor.

#### 8. Mongol Empire Fulfilled ismi ve Kalıcı Modifierların mantık hatası:

- Bu modifierı 3. situation başlayana kadar veriyorsun ama zaten 2. situation bittiği gibi 3. situation başlıyor, bi anlamı yok bence ya komple kaldıralım ya da 2. situation bittiğin de mongol empire formladığımız için farklı isimle bir modifier da verebilirsin kalıcı olcak şekilde farketmez.

- Ayrıca Modifierı permanent demişiz modifier dosyasında # --- Situation 2 Permanent Reward --- mongol empire formladığımız için. Ama 3. situation yani dominance situationın on_startında kaldırıyoruz # The Phase 2 reward expires here, as its tooltip promises # ("removed upon the start of the 3rd Situation"). remove_country_modifier = MR_empire_fulfilled diyerek neden onu anlamadım.

-  Ayrıca mesela MR_mongol_historical_modifier_2 modifierı vs de permanent olması gerekiyor normalde 1. situation bittiğinde kazanınca ama oda 2. situation başlarken kaldırılıyor bizim situationlar hemen diğeri bitince başladığı için her situation başında kalıcı olanları remove yapmaya gerek yok prussian destiny modundaki gib o sebeple localization dosyasında ki removed upon the start of the 2nd Situation loclarını temizleyip ona göre düzenler misin. Kalıcı olması gerken modifierlar kalıcı kalsın.

#### 9. MGE_f formlanınca harita da çıkan garip ülke ismi:

- MGE_f formlanınca Mongol Empire, Great Mongol Empire veya Yeke Mongol Ulus falan yazmıyor haritada ülke isminde, onun yerine Great Mongol Horde yazıyor dünya haritasında. Sanırım sıkıntı oldu biz MGOya mongol horde demiştik ama mge_f ye ismi taşındı galiba. Ama reqiureiments kısımlarında ya da ülkeyi seçerken ismi Yeke Mongol Ulus olarka gözüküyor ama dünya haritasından direk gözüken ismi Great Mongol Horde olarak gözüküyor.

#### 10. Benim eklediklerim:

1. MGO formlanınca ülke kontluk ve düklük kalabiliyordu onun altına ekledim artık MGO formlanınca kingdom oluyor ve ülkesinin ai personalitysini de agresif yapıyor. Aynısı MGE içinde geçerli MGE formlanınca ülkesini empire değilse empire yapıyor level 4 ile ve ai personalitysini de agresif yapıyor yine.

2. Modifierları biraz düzenledim terminator olanları daha güçlü yaptım historical olanları da biraz güçlendirdim ve khanlara gelen monthly gold income'ı arttırdım ve 2. situationda gelen bufflara army_maintenance_efficiency modifierı ekledim çünkü eğer o bizim eklediğimiz güçlü özel khanlar ölünce ülke bankrupt oluyordu bi anda income'ı düştüğü için.

#### 11. Tarihsellik için isteklerim:

- Benim baktığım kadarıyla moğollar tarihte perslere veya avrupaya gitmeden çinin hepsini veya manchuria korelerin oralarıda girmişlper yani benim senden istediğim TAMAMEN TARİHSEL bir genişleme yapalım ve situationlardaki end requirementları onlara göre düzeltelim olmadı. 24.07:### 2. Region,area,subcontinent ve Situation Fetih bölge değişiklikleri maddesinde de bundan biraz bahsetmiştim, yani lütfen tarihsel yapalım istersen moığollar tarihte nereleri fetih etmiş sıra sıra araştır öyle entegre de edebiliriz fark etmez.
- Ayrıca west_siberia_regionında kalan bursol_area, omsk_area ve kulykol_area bölgelerini de 2. situationda aldırabiliriz borderlar daha güzel gözüksün diye.
- Son olarak 2. situation başarılı bir şekilde bittiğinde ya da 3. situation başladığına bence başkenti akrakorumdan khanbaliqe taşımalıyız tarihsellik olarak düye düşündüm sen ne dersin?

#### 12. any_owned_location veya any-ownable_location kullanımı çok kötü:

- anw_owned_location veya any-ownable_location kullanımı tüm dünyada ki ülkeleri tarıyo toprakları performasnı kötü ve hatalı oluyor çoğu zaman onlar yerine benim prussian destiny modumdaki gibi any_ownable_location_in_area veya region çok daha güvenli ve çalışır durumda onları kullan.

- # MR_scripted_trigger.txt dosyasından Örnek: bu kodu kullanma:

	# The Ilkhanate clause: no power outside the claimant's realm
	# holds a single location in the Persia region. c:TAG links sit
	# behind country_exists guards in the same AND, as everywhere.
	NOT = {
	 	any_country = {
	 		NOR = {
	 			tag = MGE
	 			tag = MGO
	 			AND = {
	 				country_exists = c:MGE
					is_subject_of = c:MGE
				}
	 			AND = {
					country_exists = c:MGO
	 				is_subject_of = c:MGO
	 			}
	 		}
	 		any_ownable_location = {
	 			this.region = region:persia_region
	 		}
	 	}
	 }

	# Bu kodu bu şekilde kullan her zaman daha güvenli ve performans dostu:
	NOT = { 
		region:persia_region = {
			any_ownable_location_in_region = {
				owner ?= {
					NOR = {
						AND = {
							country_exists = c:MGE
							this = c:MGE
							is_subject_of = c:MGE
						}
						AND = {
							country_exists = c:MGO
							this = c:MGO
							is_subject_of = c:MGO
						}
					}
				}
			}
		}
	}


#### 13. ÇOK ÖNEMLİ DÜRÜST CEVAP VER MODUMUN BAŞARIISIYLA VE GELECEĞİYLE İLGİLİ BİR SORU:

- Bildiğin gibi eu5 1337 tarihinde başlıyor. Ben moğolları sevdiğim için Prussian Destiny gibi Mongol railroad modu yaptım senle, modu nerdeyse bitirdik ama şimdi düşündüm mesela bu modda yine taaa irana anadoluya kadar giriyoruz ya bu diğer tarihsel unsurların mesela osmanlı, timur, rusya gibi çıkacak tarihsel ülkelerin gelişimini bozacak bu sefer bu modu kullanan insanlar kendi oynamasa bile diğer ülkelerin tarihselliği de bozulacak. Bizim Mongol Resgurgence modumuz alternatif tarih olsa bile acaba bu modumuzu çıkartmayıp bekletip, ilerde yapmayı planladığım ama çok zor olan total overhaul moduna mı bekletsem?
- Benim amacım Crusader Kings 3 oyunundaki başlangıç tarihlerinden bir EU5 total overhaul'u yapmak çünkü vikingleri ve moğolları çok seviyorum. 867 yılında başlarsak vikingler ile başlıyor 1066 veya 1178 ile başlarsak moğollar var. Crusader Kings'in böyle 3 tane başlangıç tarihi var: 867, 1066 ve 1178 diye 3 tane. Bunlardan birini total overhaul yapmak istiyorum acaba oraya mı saklasam bu mongol modumu yoksa hem EU5'in vanilla 1337 hali için bu modu yayınlayıp, hem de o yapmayı planladığım diğer total overhaul modunda gerçek moğollar için değiştirip 2 tane benzer ama farklı Moğol modumu yapsam, sence ne yapalım ve nasıl ilerlemeliyim?


#### FİNAL NOT: Evet şuan gözüme çarpan ve oyun içinde debug logda ortaya çıkan hatalar bu şekildeydi bunları düzelttikten sonra tekrar bizim ana CLAUDE.md, diğer tüm .md dosyalarımızı ve tüm localization vs. gibi bütün ana mod dosyalarımız da yaptığımız değişikliklerle ve modumuzla ilgili bir içerikte vs. bir mantık hatası ve bug falan olmaması için hepsini güncelleyip elden geçirir misin detaylı bir şekilde. MD dosyalarımız güncel kalsın ki ilerde bu modu kullanıcaksam veya başka sıfırdan bir mod yapacaksam işimize yarasın.






##### 26.07.2026 CLAUDE FIX PASS (24-25.07 maddeleri: 0, 3, 5, 6, 8, 9, 11, 12, 13 + iki yeni bug) #####

Hepsi statik dogrulamadan gecti (verify_mod.py: 24/24 all checks passed). Oyun ici test EDILMEDI â€” TESTING-GUIDE guncellendi, yeni satirlar: 2.10, 2.12, 3.1-3.6, 4.1, 4.3, 4.4, 5.3, 5.9, 5.10 ve YENI Track 5b.

- (KURULUM) ../EU5-Vanilla junction'i BOSTU (klasor var, icerik yok â€” OneDrive yemis). Artik vanilla dogrudan Steam kurulumundan okunuyor: E:\SteamLibrary\steamapps\common\Europa Universalis V\game. CLAUDE.md + 3 skill + verify_mod.py'nin tespit zinciri: MR_VANILLA -> Steam yolu -> junction -> macOS wrapper. Tespit artik klasor degil BILINEN BIR DOSYA yokluyor; bos junction "-d" testini geciyordu ve butun grepler sessizce sifir donerdi.

- (YENI BUG 1 â€” KRITIK) 2. ve 3. situation HIC bitemiyordu. Bolge taramasindaki NOR'un uyeleri tek bir AND'in icine katlanmis: AND = { country_exists = c:MGO  tag = MGO  is_subject_of = c:MGO } â€” bir ulke kendi vassali olamaz, yani AND daima false, NOR daima true, her sahipli lokasyon eslesiyor, disaridaki NOT daima false. Failsafe tum topraklari verse bile faz kapanmiyordu, sadece sure doluyordu. PD'de calismasinin sebebi: orada iki madde AYRI (this = c:PRU / is_subject_of = c:PRU). 10 blokta duzeltildi. Faz 1 dogruydu (tek tag oldugu icin katlanma olmamis) â€” testlerinde P1'in bitip P2/P3'un bitmemesinin sebebi tam olarak buydu.

- (YENI BUG 2) caucasus_region 3. fazin hedefiydi ama HICBIR wargoal onu kapsamiyordu â€” savasla almak yasal olarak imkansizdi. Westward wargoal'a eklendi. Bu, bu oturumdaki degisikliklerden once de vardi ve elle yapilan denetimlerden kacmisti.

- (HARNESS) verify_mod.py'nin 3 kontrolu Windows'ta SIFIR dosya tariyor, sifir problem bildiriyordu ("/events/" in path â€” glob backslash donuyor). Duzeltildi; 233 event loc anahtari, 6 situation, 19 degisken artik gercekten taraniyor (hepsi temiz cikti). Ayrica 2 YENI kontrol eklendi: "goal territory covered by a wargoal" ve "no any_owned_location with a bare geo predicate". Ikisini de bilerek bozup FAIL verdiklerini gordum, sonra geri aldim. 22 -> 24 kontrol.

- (#4 FIXED) MGO'nun hem claimant hem rival gorunmesi: teshisin dogruydu. mr_rival_country sadece on_start'ta bir kez seciliyordu, failsafe banner'i tam da o ulkeye veriyordu. Rival artik her ay yeniden seciliyor (lider + MGO/MGE disarida). Beat 104 ayni on_monthly icinde DAHA SONRA calistigi icin MGO'nun dogdugu ay lider degiskeni hala eski adayi gosteriyor â€” o tek aylik pencereyi NOR = { tag = MGO tag = MGE } kapatiyor.

- (#5 FIXED) MR_the_sleeping_horde komple kaldirildi (4 yer: P1 on_ended verme, P2 on_start kaldirma, modifier tanimi, 2 loc). Hakliydin â€” P2, P1 biter bitmez basliyor, kapatacak bir bosluk yoktu.

- (#8 FIXED) Odul modifierlari artik KALICI: MR_unified_mongol_banner, MR_mongol_historical_modifier_2 (P2 on_start'ta siliniyordu) ve MR_empire_fulfilled (P3 on_start'ta siliniyordu) hic kaldirilmiyor. 3 loc satirindaki "removed upon the start of the Nth Situation" -> "(Permanent.)". Faz BUFF'lari hala kendi fazinin on_ending'inde siliniyor â€” odul/buff ayrimi artik temiz. MR_empire_fulfilled'in ADI degistirilmedi, istersen degistiririz.

- (#9 KABUL) "Great Mongol Horde" bizim hatamiz degil: vanilla harita etiketini rank_empire_horde_prefix ("Great") + MGE_ADJ ("Mongol") + rank_empire_horde ("Horde") diye BIRLESTIRIYOR, ulke adini kullanmiyor. Duzeltmek customizable_localization/country_ranks.txt'i komple override etmeyi gerektirirdi (2000+ satir, uyumluluk borcu). Simdilik kabul edildi.

- (#2 + #11 FIXED â€” TARIHSEL FETIH) Fetih artik gercek Mogol sirasini izliyor. P2: manchuria (Jin 1234) + tibet (Yuan protektorasi 1240'lar) + bursol/omsk/kulykol alanlari eklendi. P3: east/west/south_china (Song 1279) + korea eklendi. KORE VASSAL olarak: ortak clause zaten subject sahiplerini kabul ettigi icin MGE'nin vassali bir Kore kosulu sagliyor, bagimsiz olan saglamiyor â€” ekstra kod gerekmedi (1259 durumunun birebir karsiligi). Her hedef grubu artik TEK bir scripted trigger (mr_p2_*_cleared / mr_p3_*_cleared) ve hem end trigger hem panel skoru AYNI trigger'i cagiriyor â€” eskiden ikisi farkli sekilde yazilmisti, bar 100 gosterirken faz kapanmayabilirdi. Alti yer birlikte guncellendi: hedef trigger, wargoal allowed_locations/subjugation, CB dagitimi, AI hedef secimi + fallback, failsafe devri, tooltip/secondary_map_color. Khorasan ve Tibet'e bilerek add_core VERILMEDI (senin khorasan gerekcen: bedava core AI'i fazla besliyor).

- (#11 FIXED) Baskent P3 on_start'ta Khanbaliq'e (dadu) tasiniyor â€” Kubilay 1272. AI tasiniyor ve haber aliyor (mr_dominance.136), INSAN oyuncuya soruluyor ve reddedebiliyor (.137). Dadu'ya sahip olmak sart, zaten oradaysa atlaniyor.

- (#3 FIXED) Dunyanin tepkisi: 9 yeni event (mr_dominance.20-28), PD'nin 101/102/200/201/202 sekli. Her faz icin IZLEYICI (sahnede cikari var ama hedef toprakta yok), KURBAN (hedef bolgelerde topragi var) ve ITTIFAK BOZMA (claimant'in kendisi â€” every_related_country + remove_relation, boylece railroad'un savas ilani kendi anlasmasina takilmiyor). P1'in ittifak bozmasi on_start'ta DEGIL Beat 104'te, cunku faz acilirken claimant yok. Kimse ayni haberi iki kez almiyor: mr_dominance.10'u alan bozkir gucleri disarida. 27 loc anahtari.

- (#6 FIXED) "Han'in Otlagi" (MR_select_core_region), vanilla rot_select_core_region'in (rise_of_timur.txt:288) alan alan karsiligi. IKI fazda birden calisiyor (P1+P2), claimant tag cifti, ve kapi MR_great_khan KARAKTER modifieri â€” otlak devletin degil Han'in, Han olunce ayricalik olur. Yeni klasorler: common/generic_actions/ ve common/prices/. Yeni location modifieri MR_khans_own_pasture. Vanilla'nin "sonradan aldigin yerler de otomatik core olur" kismi on_location_changed_owner'da yasiyor â€” o on_action effect blokuyla tanimli, ayni isimle yeniden tanimlamak vanilla'nin butun toprak-devri mantigini ezerdi, o yuzden ayni isi situationlarin on_monthly'sinde yapiyorum. (Yazarken prev.prev kullanmistim â€” vanilla'da SIFIR kullanimi oldugunu gorunce save_scope_as ile degistirdim.)

- (#12 FIXED) any_owned_location'in 89 kullanimi TEK bir bolge yukleminden ibaretti, hepsi has_presence_in'e cevrildi (104 cevrim, bu oturumda eklenenler dahil; vanilla'da 108 kullanim). Geriye tek bir tane kalmadi ve harness artik geri gelmesine izin vermiyor. Kalan any_country/ordered_country bloklarina DOKUNULMADI â€” onlar "su ozellikte bir ulke BUL" isi yapiyor, bolge taramasi ulke donduremez. ordered_neighbor_country (20) sadece komsulari, var:...target_country (19) tek ulkeyi geziyor, tarama degiller. Maliyet sirasi CLAUDE.md'ye yazildi.

- (#13 CEVAP) Modu bekletme, cikar. Gerekce: railroad modu kuran oyuncu zaten tarihselligin bukulmesini talep ediyor (PD'de Brandenburg icin yaptigin sey); total overhaul EU5'in 1337 setup agacini sifirdan yazmak demek, yillarca surer; bitmis bir modu ona rehin vermek bitmis isi copetmek olur. 1337 surumunu cikar, tasarimi (uc fazli state machine, failsafe'ler, buff rule) tasinabilir iskelet olarak koru. CK3 baslangici sorusunda: Mogollar merkezdeyse tek mantikli secenek 1178 (Temucin 1162 dogumlu, 1206'da birlestiriyor); 867 Vikingleri verir ama Mogollari tamamen disarida birakir. Istege bagli ek fikir: tarihselligi onemseyenler icin P3'u (bati seferi) kapatan bir game rule.

- (#1 ve #7 â€” GUI, SENDE) BOM hipotezi CURUDU: 6 .gui dosyamizin HICBIRINDE BOM yok, vanilla ile ayni. Ayrica tum .yml/.gui dosyalarinda #l, |l] veya taninmayan tek bir # tag'i yok (byte duzeyinde tarandi). Government.* spami icin onde gelen hipotez: one_country_header_template block "CountryContext"i IKI kez tanimliyor (biri portre, biri datacontext = "[Country.GetGovernment]" tasiyan ruler seridi) ve tek bir blockoverride ikisini birden eziyor. Ama bu vanilla panellerinin de spam yapmasi gerektigi anlamina gelir, senin gozlemin bunu curutuyor â€” yani DOGRULANMADI. Iki ayirt edici test: (a) ayni surumde vanilla Rise of the Ottomans/Rise of Timur panelini ac, loga bak; (b) bizim CountryContext'i degisken yerine sabit bir tag'e ([GetCountry('CHI')]) cevir, spam kesiliyor mu bak. Hangi teori dogru cikarsa ciksin RISKSIZ cozum: P2/P3'u de two_countries_header_template'e alip ikinci portreyi gizlemek (P1 onu kullaniyor ve hic spam yapmiyor).

- (FINAL NOT FIXED) Tum .md dosyalari elden gecirildi: CLAUDE.md (mimari tablosu, failsafe, modifier sayisi, wargoal kapsami, yeni iterator kurali), README.md, MOD-DESIGN-IDEA.md (yeni faz hedefleri, Kore, baskent, action + immersion bolumleri, kalici odul notu), EU5-MODDING-GUIDE.md (yeni iskelet klasorleri, "en ucuz construct" tablosu, duz NOR kurali, generic_action loc konvansiyonu, location modifier kategorisi, harness bolumu 24 kontrol + iki yeni ders), TESTING-GUIDE.md (10 satir guncellendi + YENI Track 5b), FUTURE-DEVELOPMENT.md (bilinen borc listesi, 2 yeni cookbook, definition of done), AUDIT-2026-07-21.md (yeni hata siniflari notu).



##### 26.07.2026 IN-GAME TEST RESULTS + FIX PASS #####

Ilk gercek oyun ici test turu. Dort gercek hata cikti, dordu de duzeltildi. Harness 24 -> 26 kontrol, hepsi yesil.

## CALISTIGI DOGRULANANLAR

- (GUI SPAM COZULDU) 2. ve 3. situation panelini acinca gelen Government.* error spami GITTI. NASIL: one_country_header_template `block "CountryContext"` adini IKI kez tanimliyor â€” biri portre icin bos, digeri ruler seridi icin `datacontext = "[Country.GetGovernment]"` tasiyor. Tek bir blockoverride ikisini birden eziyor, yani seride Government yerine Country itiliyor ve icindeki country_government_character (character_header.gui:260-295) Government isteyince "No context supplied" basiyordu. Cozum: seridi komple gizlemek â€” `blockoverride "one_country_ruler_title_visible" { visible = no }`. Vanilla reformation.gui:88 birebir bunu yapiyor. Gorsel kayip YOK, cunku seritteki her widget [Government.HasRuler] ile korunuyordu ve zaten hicbiri render olmuyordu.
- (END TRIGGER) Scripted trigger'lari ayirip hem end trigger'a hem panel skoruna baglama yapisi calisiyor. custom_tooltip commentlenip bakildiginda mantik dogru gorunuyor.
- (HARITA) Yeni hedef bolgelerin kirmizi cizgileri calisiyor.
- (FAILSAFE) 1545'te P2 failsafe'i tetiklendi, topraklari devretti, ertesi ay situation kapandi ve P3 basladi. Yani A1 duzeltmesi (10 bozuk NOR blogu) ISE YARADI â€” eskiden faz hic kapanmiyordu.
- (AKSIYON) "Claim the Khan's Own Pasture" 2. situation panelinde geliyor, bolge sectirip hem core yapiyor hem MR_khans_own_pasture veriyor.

## DUZELTILEN HATALAR

- (LOC PARSE â€” EN ZARARLISI) `Missing colon (:) separator` x11. Sebep: yazdigim 11 aciklamada `\n\n` dosyaya GERCEK satir sonu olarak dusmus, degerler iki fiziksel satira bolunmus, oyun o 11 girdiyi komple atiyordu. Hepsi birlestirildi. NOT: harness bunu goremiyordu cunku anahtar sayan tarama bozuk satirlari yok sayiyordu â€” YENI KONTROL eklendi (`loc lines are well formed`) ve bilerek bir satir bolunerek yakaladigi kanitlandi.

- (AKSIYONUN UC YAN KAYDI) Bir generic_action eklemek tek basina yetmiyormus; ucu de ayri hata basiyor:
  * `generic_action_ai_list.cpp:82` -> in_game/common/generic_action_ai_lists/MR_actions_list.txt eklendi (sekil: vanilla rise_of_timur_list.txt). AI listesi olmayinca motor aksiyonu gereginden cok sik degerlendiriyor.
  * `price_database.cpp:117` -> main_menu/common/modifier_type_definitions/MR_modifier_types.txt eklendi. Her price icin motor <price_key>_cost_modifier diye bir modifier TIPI turetiyor ve tanimli degilse hata basiyor (sekil: hussite_wars_actions_price_cost_modifier, 00_modifier_types.txt:174).
  * `message_handler.cpp:421` -> main_menu/gui/MR_messagetypes.txt eklendi + 21 loc anahtari. Vanilla'nin 155 situation-tipi aksiyonunun 149'unda bu kayit var, yani pratikte zorunlu. DIKKAT: vanilla hepsini tek bir main_menu/gui/messagetypes.txt icinde tutuyor (1348 girdi) â€” O ISIMLE DOSYA KOYULAMAZ, vanilla'nin tamamini ezerdi. Farkli isimle ayni klasore koyduk. Motor klasoru tariyorsa hata gider; taramiyorsa dosya sessizce yok sayilir (zarar veremez) ve geriye bir log satiri + aksiyon kullanilinca popup cikmamasi kalir. BIR SONRAKI TESTTE BU SATIRIN GIDIP GITMEDIGINE BAK.
  Bu ucu icin de YENI KONTROL eklendi (`generic actions: ai list + message type + price modifier`), AI listesi gecici silinerek yakaladigi kanitlandi.

- ("IMPERIAL PROGRESSION 0" ACIKLANDI VE DUZELTILDI) Bar 0 gosterirken End Requirements'in hepsi yesildi. Sebep: PANEL PROGRESS blogu on_monthly'nin BASINDA, failsafe ise SONUNDA. Failsafe'in calistigi ay bar devir ONCESI degeri gosteriyordu; End Requirements ise panel acilinca canli degerlendigi icin yesildi. Skor artik on_monthly'nin sonunda hesaplaniyor, ikisi ayni tick icinde uyusuyor. (P2 ve P3, ikisinde de.)

- (ISIM + TOOLTIP) MR_empire_fulfilled -> "The Yeke Mongol Ulus Restored", aciklamasi tarihsel bir cumleye cevrildi. mr_dominance_end_tt yedi baslikli okunabilir bir listeye donusturuldu: Koltuklar / Ilhanli / Altin Orda / Yuan / Kore / Bati erisimi â€” Kore'nin VASSAL olarak sayildigi acikca yaziyor.

## KARAR: OLDUGU GIBI BIRAKILDI

- MGE: "Great Mongol Empire" (senin degistirdigin hali) korunuyor. Uyari: vanilla'nin country_names_l_english.yml dosyasinda adinda "Empire" gecen SIFIR ulke var; bu tam olarak 23.07'de `MGE has the name 'empire'` uyarisini ureten degisiklik. Harita etiketi zaten Great + Mongol + Horde diye bilesiyor (rank_empire_horde_prefix + MGE_ADJ + rank_empire_horde), yani bu ad haritada gorunmuyor â€” geri gelen tek sey o uyari. Alternatif hazir duruyor: "Great Mongol State", Yeke Mongol Ulus'un birebir Ingilizce karsiligi, tetikleyici kelimeyi icermiyor.

## HALA ACIK

- `Unknown formatting tag 'l'` â€” vanilla Rise of Timur paneli acilip loga bakilmadi. O tek bakis dosyayi kapatacak.
- messagetypes.txt klasor-birlestirme varsayimi (yukarida).
- has_presence_in â‰¡ any_owned_location { region } esdegerligi: End Requirements satirlari toprak durumuyla uyumlu gorunuyor, yani pratikte dogrulanmis sayilir.



##### 27.07.2026 SCRIPTED GEOGRAPHY REFACTOR + IN-GAME TEST ROUNDS #####

Baska bir yayinlanmis railroad modunu (Legacy of Timur) analiz ettik, oradan ogrendigimiz scripted_geography'yi entegre ettik, ve arka arkaya uc oyun ici test turunda dort gercek hata daha bulundu. Harness 26 -> 29 kontrol, hepsi yesil.

## SCRIPTED GEOGRAPHY (vanilla ozelligi, tamamen kacirmisiz)

Hedef cografya modda 7 dosyada 259 kez yaziliydi; bir hedef degisince ALTI yerin birden dogru degismesi gerekiyordu ve bunlardan sadece BIRININ kontrolu vardi. Artik `in_game/common/scripted_geography/MR_geography.txt` icinde 21 atom var, her bolge adi modda TAM OLARAK BIR KEZ yazili.

Kullanim: ulke scope'unda `has_presence_in = scripted_geography:X`, lokasyon scope'unda `is_in_scripted_geography = scripted_geography:X`, ulkenin baskenti icin `scope:C.capital ?= { is_in_scripted_geography = ... }`, iterasyon icin `scripted_geography:X = { every_location_in_scripted_geography = { ... } }`. Vanilla'nin kendi `scripted_geography.info` dosyasinda belgeli.

IKI KURAL (ikisini de once yanlis yapip ogrendik):
- ATOM ONLY, ASLA BIRLESIM TANIMLAMA. Cografyalar ic ice gecmiyor (vanilla'da sifir ornek), yani "birlesim" tanimi uyelerini ikinci kez yazmak demek â€” kaldirdigin tekrari geri getirir. Cagrilan yerler atomlari OR'lar.
- AYRI AYRI DOGRU OLMASI GEREKEN HER KOSUL ICIN AYRI ATOM, ve her farkli SINIR icin ayri atom. Dogu+bati Gobi'yi tek atoma koymak "ikisi de" hedefini sessizce "ikisinden biri"ne cevirdi. Khorasan xinjiang'dan ayri, cunku P3 failsafe'i khorasan'i TEK BASINA istiyor. Manchuria/tibet Sibirya'dan ayri, cunku biri core aliyor digeri bilerek almiyor. Bir atom yari-bir-sey olamaz.

Her adimda esdegerlik kanitlandi: her atomu definitions.txt'ye gore lokasyon kumesine acan bir dogrulayici yazip eski liste ile yeni cografyayi karsilastirdim. Hepsi EXACT, iki bilincli istisna disinda:
- steppe_unification allowed_subjugation ACIK LISTE KALDI â€” atomlara cevirmek 949 lokasyon eklerdi ve Faz 1'in Horasan/Tibet'i vassallastirmasina izin verirdi ("Too far away for situation 1" yorumun bilincliydi).
- P2 CB dagitimi ve AI hedef secimi GENISLEDI â€” manchuria/tibet/Sibirya alanlarini tutan ulkeye silk-road CB'si hic verilmiyordu, oysa wargoal orayi alinabilir kiliyordu. Caucasus'un aynisi, canli bir acikti; genisleme duzeltme oldu.

## P3 FAILSAFE GENISLETILDI (senin karar verdigin B secenegi)

P3 failsafe'i artik Faz 2 topragini da geri aliyor (xinjiang, manchuria, tibet, Sibirya alanlari). Gerekce: AI 1600'de kotu bir savas kaybederse 1650'de imparatorlugun ortasinda delik kalirdi. Faz 2 iyi gittiyse bedeli SIFIR â€” devir kosulu sadece "sahibi AI, claimant degil, claimant'in tebaasi degil" olan topraga uyuyor. Oyuncunun topragina dokunmuyor. Core politikasi uydurulmadi, Faz 2'den kopyalandi ve programli dogrulandi.

## OYUN ICI TEST TURLARINDA BULUNAN DORT HATA

- (BENIM HATAM, 1a) `is_in_scripted_geography` bir LOKASYON trigger'i; ulke scope'unda `has_presence_in` kullanilmali. 120 cagri yerinde yanlis trigger vardi. Kapsami tahminle degil, her satirin cevresindeki blok yiginini cozerek belirleyip duzelttim. Harness kontrolu eklendi (209 cagri yerini tariyor).
- (BENIM HATAM, 1b/1c) northern_marches'i uce bolerken kullandigim regex `is_in_scripted_geography = ` onekini yutmus, geriye ciplak `scripted_geography:MR_geo_tibet` satirlari kalmisti. 12 satir, uc dosya. Brace sayisi tuttugu icin harness gormedi. DERS: re.sub'da `\S*` bosluk sinirinda kesiliyor ve sonuc sessizce bozuk cikiyor.
- (ESKI HATA) `is_subject_of` sadece DOGRUDAN vassali sayiyor. Uc yerde birden yanlisti: hedef trigger'lari alt-vassalin topragini yabanci sayiyordu (faz uzuyordu â€” senin buldugun), FAILSAFE alt-vassalin topragini ELINDEN ALIYORDU, ve AI kendi alt-vassalina savas acabiliyordu. 46 cagri yeri `top_overlord_or_this` ile duzeltildi (vanilla hundred_years_war.txt:185). Bagimsiz bir ulke icin kendisini dondurdugu icin ayri `tag = MGO` kontrolu de gereksizlesti.
- (ESKI HATA) Koltuk kontrolleri `c:MGO = { owns = location:samarkand }` seklindeydi â€” sadece claimant KENDISI tuttugunda dogru. Vassal Samarkand veya Khanbaliq'i tutunca faz KILITLENIYORDU, ve failsafe de kurtaramiyordu cunku bilerek kendi tebaasinin topragina dokunmuyor. Butun koltuklar ve ayak izleri artik ortak `mr_in_claimant_realm` trigger'indan geciyor (`has_owner = yes` + `top_owner ?= c:MGO/MGE`). Test edildi: Samarkand vassaldayken situation bitiyor.

## GUI: END REQUIREMENTS ARTIK KONTROL LISTESI

P3'un end requirement'i hem tooltip metnini hem altinda ham clause dokumunu gosteriyordu. Sebep: panelin widget'i her `custom_tooltip` icin BIR TIK ciziyor, biz ise 17 clause'un hepsini tek dev tooltip'e sarmistik. Vanilla'nin sekiz situation end-condition tooltip'inin hepsi tek kisa cumle ve HICBIRINDE satir sonu yok (ben P3'unkini yedi paragraf yapmistim).
Artik her gereksinim kendi tooltip'inde: P1 2 tik, P2 4 tik, P3 9 tik. Dokuz hedef trigger'i tooltip'ini kendi icinde tasiyor, end trigger'lar sadece onlarin listesi. Hangi maddenin eksik oldugunu tek bakista goruyorsun.

## MOTOR KAYITLARI: IKISI COZULDU, IKISI KABUL EDILDI

- `generic_action_ai_list.cpp:82` -> COZULDU, ai list dosyasi eklendi.
- `price_database.cpp:117` -> COZULDU, `<price>_cost_modifier` tipi eklendi.
- `message_handler.cpp:421` -> COZULEMEZ, KABUL EDILDI. Motor SADECE `main_menu/gui/messagetypes.txt` dosyasini okuyor (vanilla'nin o klasorunde baska .txt yok). Farkli isimli mod dosyasi sessizce yok sayiliyor â€” Timur modununki de olu, onlar da fark etmemis. Ayni isimli dosya vanilla'nin 1348 girdisini siler. Olu dosyamizi sildim. Bedel: aksiyon kullanilinca bir log satiri ve popup cikmamasi. Aksiyon calisiyor.
- `modifier_type.cpp:1294 Missing Icon` -> KABUL EDILDI. Ikon dosya adiyla araniyor (`gfx/interface/icons/modifier_types/<key>.dds`), tanimda `icon` alani yok. Vanilla kendi `rot_plan_invasion_price_cost_modifier`'i icin de gondermiyor. Istersen 5-6 KB'lik bir .dds koyarsan gider.
- `Unknown formatting tag 'l'` -> KAPANDI. Vanilla situation panellerinde de cikiyor, bizimle alakasi yok (oyun ici dogrulandi).

## TIMUR MODUNDAN OGRENDIKLERIMIZ (analiz, kopyalama yok)

Aldigimiz: `scripted_geography`, `top_owner`.
Almadigimiz ama total overhaul icin kaydedilenler (FUTURE-DEVELOPMENT 5b): `auto_modifiers` (potential_trigger + scales_with â€” kosul dogruyken kendiliginden uygulanan modifier, defter tutma yok, vanilla'da 149 tanim), custom `peace_treaties` + `ai_desire` (hedef topragi BARIS MASASINDA devreden sart â€” failsafe'ten cok daha iyi bir railroad primitifi), `area_preferences` (AI istahini yonlendirme, `TRY_REPLACE:` ile vanilla girdisini ezme), `scripted_effects`, `disasters` (inline modifier + 0-100 sayac + uc farkli son), on_action ailesi (`monthly_country_pulse`, `on_winning_war`/`on_ending_war` + scope:winner/loser/war, agirlikli `random_events`), `situation:X.var:Y`, savas nesnesine baglanan degiskenler.

KARSI DERS: o mod `any_country_in_hierarchy` / `every_country_in_hierarchy` kullaniyor (14 yer) ve vanilla'da bu ikisinin SIFIR kullanimi var â€” hicbir yerde. Populer ve yayinlanmis olmak "attested" demek degil. Citation kurali kaynaktan bagimsiz gecerli.

## HARNESS 26 -> 29

Yeni: `geography trigger matches its scope` (209 cagri yeri), `scripted geographies defined <-> used`, `subjecthood walks the whole chain`.
Yukseltilen: `goal territory covered by a wargoal` artik LOKASYON seviyesinde karsilastiriyor; `regions/areas/locations exist` refactor sirasinda 40'tan 11'e dustu (adlar cografya dosyasina tasindi, kontrol o sozdizimini bilmiyordu) â€” yakalandi ve cografya dosyasini da tarayacak sekilde duzeltildi; `no unguarded c:TAG` artik `owner` ile `top_owner`'i ayiriyor.
Kaldirilan: generic action mesaj-tipi sarti (cozulemez oldugu icin, gerekcesiyle).
Yeni kontrollerin HEPSI known positive'de kanitlandi: cografya adina yazim hatasi, sahipsiz atom, ters cevrilmis trigger, korumasiz top_owner, wargoal'dan cikarilmis atom.



##### 27.07.2026 REFERANS MODLARIN ANALIZI + MOTORUN KENDI DOKUMANTASYONU #####

Bu bolum kod degil BILGI kazanimi. Uc dis kaynak incelendi ve en sonunda motorun kendi script dokumantasyonu repoya girdi. Harness 29 -> 31.

## EN ONEMLISI: docs/EU5-Vanilla-Script-Docs/

Oyun icinde `-debug_mode` ile konsola `script_docs` ve `dump_data_types` yazilarak alindi. Icerik:
- triggers.log  : 1798 trigger, HER BIRI `**Supported Scopes**` beyaniyla
- effects.log   : 1534 effect, ayni sekilde
- event_targets.log : 289 scope baglantisi, Input Scopes -> Output Scopes
- modifiers.log : 2436 modifier tag'i
- on_actions.log: her hook, Expected Scope ile
- data_types/   : 2.9 MB GUI/promote tipleri

BU ARTIK OTORITE. Vanilla'yi grep'lemek sadece birinin ne YAZDIGINI gosteriyordu; bu neyin YASAL oldugunu gosteriyor. CLAUDE.md'nin Verification bolumu buna gore degistirildi: once buraya bak.

Ilk sorgu, bugun bizi isiran seydi:
  is_in_scripted_geography -> location, province_definition, area, region, sub_continent, continent
  has_presence_in          -> country
Oyunun verdigi hata mesaji birebir bu listeyi geri okuyormus. Bu dosya elimizde olsaydi 120 yanlis cagri yeri hic olusmazdi.

Bugun yazdigimiz her sey dogrulandi: top_owner (location->country), top_overlord_or_this (country->country), capital (country->location), owns (country), is_subject_of (country). Ayrica daha temiz bir alternatif bulundu: `is_subject_or_below_of` = "vassali mi ya da vassalinin vassali mi" â€” amaca ozel trigger. Bizimki dogru ve test edildi, degistirilmedi.

Tum mod listeye karsi tarandi: 315 tanimlayicinin hepsi aciklandi, UYDURMA TEK BIR MOTOR CONSTRUCT'I YOK.

## HARNESS 29 -> 31

+ modifier tags exist in engine docs (187 satirimiz, 2436 resmi tag'e karsi)
+ on_action hooks vs engine docs
Ikisi de known positive'de kanitlandi ('disciplin' yazim hatasi yakalandi).

BIR KONTROL DE SILINDI ve sebebi onemli: modifier KATEGORISI karsilastirmasi yazmistim, sonra her tag'in `All` kategorisini de tasidigini gordum â€” yani hic atesleneMEZ. Ustelik kavramsal olarak da yanlis: siege_ability `Unit` kategorisinde ama bizim `category = country` blogumuzda sorunsuz calisiyor; kategori modifier'in NEYI ETKILEDIGINI soyluyor, nerede tanimlanabilecegini degil. Ateslenemeyen kontrol, olmayan kontroldan kotudur â€” sahip olmadigi kapsami ima eder. Bu harness'in var olus sebebi olan tuzagin ta kendisi.

## CANLI HATA DUZELTILDI: modifier ikonu

`modifier_type.cpp:1294` kapandi. Ben "ikon dosya adi konvansiyonuyla araniyor" demistim, EKSIK BILGIYDI. Gercek: `main_menu/common/modifier_icons/`, vanilla'da 4912 girdi, ve yol BASKA BIR MODIFIER'IN ikonuna isaret edebiliyor (vanilla kendisi yapiyor). Hic sanat uretmeden cozuldu. Decoder duzeltildi.

## TOTAL CONVERSION MIMARISI COZULDU

Iki total conversion incelendi (Bronze Era yayinlanmis mod, ve senin 867 test modun). IKISI DE HARITAYI BOYAMIYOR.

Dunya `main_menu/setup/start/` altindaki 25 numarali dosyadan geliyor. Ulke yerlestirmek = VANILLA LOKASYON ADLARINI LISTELEMEK:
  countries = { countries = { NOR = { own_control_core = { bergen oslo nidaros ... } } } }
Hicbir ulkenin sahiplenmedigi yer bos kaliyor â€” "sadece Iskandinavya vardi" etkisi bundan, Location Painter'dan degil.

Uc katman, artan maliyetle:
1. setup/start degistir â€” ZORUNLU, oynanabilir dunya icin YETERLI
2. map_data/location_templates.txt (28.573 satir, her lokasyonun kulturu/dini/kaynagi/arazisi) â€” OPSIYONEL sadakat katmani, tam dosya override'i oldugu icin her yamada birlestirilmeli
3. harita boyama â€” IKISI DE YAPMADI

Takvim `common/defines` ile tasiniyor (START_DATE/END_DATE) ve motor POZITIF yilda tutuluyor; Bronze Era MO tarihleri ulke degiskenleriyle SUNUM katmaninda gosteriyor. Gerekce kendi dokumanlarinda: vanilla timerlari, cooldownlari, AI zamanlamasi, situationlar, institutionlar ve save'ler birkac yerde pozitif takvim varsayiyor.

## TAG KURALIMIZ DUZELTILDI

Vanilla'da 2217 tag'in 2217'si UC HARFLI. Ama Bronze Era'da 531 tag var: 471'i BES harfli, 47'si dort, 13'u uc â€” ve canli kodda kullaniliyorlar (c:ALASI). Yani "3 harf" bir VANILLA KONVANSIYONU, motor siniri degil. Overhaul'da yuzlerce yeni tag gerekince onemli olacak. Harness kontrolu birakildi cunku BU mod vanilla tag'leri kullaniyor.

## CIKARILAMAYAN IKI DERS

- `message_handler.cpp:421` COZULEMEZ. Motor sadece `main_menu/gui/messagetypes.txt` dosyasini okuyor (vanilla'nin o klasorunde baska .txt yok). Farkli isimli mod dosyasi sessizce yok sayiliyor â€” Timur modununki de olu. Ayni isimli dosya vanilla'nin 1348 girdisini siler. Olu dosyamiz silindi.
- `Unknown formatting tag 'l'` VANILLA KAYNAKLI, oyun ici dogrulandi (vanilla panellerinde de cikiyor). Dosya kapandi.

## DIS KAYNAKLARDAN ALINANLAR (FUTURE-DEVELOPMENT 5b/5c/5d)

Timur modu (railroad): scripted_geography, top_owner. Almadiklarimiz ama overhaul icin kaydedilenler: auto_modifiers (kosul dogruyken kendiliginden uygulanan modifier), custom peace_treaties + ai_desire (hedef topragi BARIS MASASINDA devretmek â€” failsafe'ten cok daha iyi bir railroad primitifi), area_preferences, scripted_effects, disasters, on_winning_war/on_ending_war hook ailesi.

HLJSXK/eu5-modding-project (Claude Code ile yurutulen bir mod): CLAUDE.md'leri 140 SATIR ve oyle kaliyor cunku icinde sadece KURAL var; bilgi anti_patterns.yaml + valid_enums.yaml + PROJECT_OVERVIEW.md icinde buyuyup gen_brief.py ile BRIEF.md'ye DERLENIYOR. Bizim 438 satirlik CLAUDE.md sorunumuzun cevabi bu. Ayrica error_log_filter.py + 663 satirlik vanilla_error_filters.txt â€” error.log'dan vanilla gurultusunu ayikliyor; `[l]` meselesine uc kez donmemizin sebebi buydu.

## HER KAYNAGA CITATION KURALI UYGULANIR

Iki dis kaynak da hatali iddialar icerdi:
- Timur modu `any_country_in_hierarchy` kullaniyor â€” vanilla'da SIFIR kullanim, hicbir yerde.
- HLJSXK'in CLAUDE.md'si "location_rank sadece 3 deger alir" diyor â€” vanilla'da DORT var ve eksik olan IKINCI EN COK kullanilan: city 356, megalopolis 279, town 244, rural_settlement 121.
Populer ve yayinlanmis olmak "attested" demek degil.



## NEXT GAME SESSION CHECKLIST (the 2026-07-30 batch — nothing below has in-game evidence yet)

Click tour, ~10 minutes, observer or MGO hands-on:
1. 1372+ as/watching MGO: DHE timeline shows "A Ming embassy demands submission"; taking Defiance leaves a 10-year "Defiance of the South" modifier on the country panel.
2. If TIM exists: "Timur's shadow reaches the steppe" fires (three options incl. the bride price); if TIM never rose, the event correctly never appears.
3. 1370-85: "The Return of Bayan" — after the historical option, a high-adm character named Bayan appears in the court roster. THIS IS A PROBE: create_character without a dynasty line is unobserved.
4. Any winter: "Zud" fires and CAN REPEAT in a later year (no fire_only_once).
5. Paiza event: option a leaves "The Ortoq Partnerships" (+25 gold/month); 3-6 years later "The Ortoq's Bill" arrives (three options incl. the purge).
6. 1430+: "The Karakorum Debate" (fires for MGO or MGE — the multi-tag probe); each option leaves its 20-year modifier.
7. EVERY event window shows the historical-info text (the explicit-field fix — if any is blank, say which).
8. Carried from the audit: KAZ actually spawns in the Great Partition (is_historic probe); mr_yam_riders researchable at the 1437 age boundary; MGE proclamation still works if the AI settled first; the "Great Mongol Empire" map label while still a horde.

##### 30.07.2026 GREAT PARTITION ILK OYUN ICI TEST + FIX PASS #####

Son uc commitlik blok (Great Partition endgame'i, ~1.600 satir) ilk defa oyun
gordu. Yazar uc bulgu bildirdi; ikisi TEK kok nedene indi. Harness 33 -> 34
kontrol, hepsi yesil.

## YAZARIN BULGULARI (TEST RESULTS, 30.07)

1. Mogol AI ulkesi steppe horde'dan cikip monarchy'ye geciyor, levyleri
   cok zayifliyor, Great Chen'i yenemiyor. Sebep olarak steppe_horse_archers
   kaybi tahmin edildi.
2. Great Partition'in end requirement'i situation acilir acilmaz TIKLI
   geliyor (ekran goruntusu: "Any Location in MR_geo_heartland" yesil, ornek
   lokasyon Buir Nuur).
3. Bu yuzden dagilma da aninda oluyor ve halefler eksik/parcali cikiyor
   (Kirim hic gelmiyor).

## KOK NEDEN: SAHIPSIZ ARAZI (#2 ve #3 ayni hata)

Sekiz `mr_ulus_*_held` trigger'i lokasyon uzerinde dogrudan
`NOT = { mr_in_claimant_realm = yes }` soruyordu. O trigger
`has_owner = yes` ile basliyor, dolayisiyla negatiflenince "bunun sahibi
HICBIR ZAMAN olamaz" cumlesi "burayi kaybettik" anlamina geliyor.

OLCULDU (default.map + definitions.txt taranarak): motor 918 `lakes`,
1868 `impassable_mountains` ve 153 `non_ownable` lokasyonu siradan
province -> area -> region agacinin ICINE koyuyor. Sekiz atomun HEPSINDE var:

    MR_geo_heartland         263 lokasyon /  50 sahiplenilemez
    MR_geo_kazakh_steppe     183 /  28
    MR_geo_tarim              88 /  34
    MR_geo_siberian_marches  101 /  34
    MR_geo_dzungaria          48 /  12
    MR_geo_crimean_seat       18 /   4
    MR_geo_nogai_steppe       98 /   3
    MR_geo_bashkiria          28 /   2

Tooltip'te gorunen ornek lokasyon bunun kaniti:
`buir_nuur_province = { buir_nuur barun_xiabaer khalkh tamsabulag lake_buir }`
(definitions.txt:2906) ve `lake_buir` default.map'in lakes blogunda (:1063).

Sonuc zinciri, tek ay icinde: heartland asla "held" okunamiyor ->
`mr_partition_end_trigger` ilk tikte true -> situation acilir acilmaz
kapaniyor; kohezyon 100-30-12-12-12-10-8-8-8 = 0 -> uc esik olayi (85/55/40)
ayni anda; `on_ending`'de alti halefin de ikinci klozu (`NOT = { ..._held }`)
true -> hepsi birakilmaya calisiliyor ama sadece MGE'nin FIILEN sahip oldugu
toprak el degistirdigi icin harita parcali cikiyor ve MGE'nin o an tutmadigi
Kirim'dan hicbir sey dogmuyor.

NEDEN FAZ 1-3 ETKILENMEDI: onlarin hedef trigger'lari (`mr_p2_*_cleared` vb.)
bastan beri `owner ?= { ... }` seklini kullaniyor; `?=` sahipsiz lokasyonu
eslesmez yapiyor. Dosyanin kendi yorumu (satir 939-941) ulus trigger'larinin
da bu sekli kullandigini IDDIA ediyordu ama kod oyle degildi.

## DUZELTMELER

- (#2/#3 KOK) Sekiz `mr_ulus_*_held` trigger'i `owner ?=` sekline gecirildi,
  hedef trigger'larla birebir ayni yapi. `mr_in_claimant_realm` duruyor:
  `on_ending`'in devir limitlerinde ve Faz 1 koltuk klozunda POZITIF
  kullaniliyor, oralarda dogru.

- (#2 TASARIM, yazar karari) `mr_partition_end_trigger` uc kloz oldu:
  tag haritadan silinmis, VEYA `location:karakorum` realm disi, VEYA
  `MR_cohesion_score < 40`. Eski hali "263 heartland lokasyonundan HERHANGI
  biri disarida" idi; duzeltmeden sonra bile tek bir sinir koyu yuzyillik
  endgame'i bitirirdi. Yazarin gerekcesiyle kohezyon klozu eklendi: Karakurum
  Avrupa'dan cok uzak, tek basina birakilirsa imparatorluk ASLA yikilmaz,
  1720'ye kadar bekleyip hayatta kalma odulunu alirdi. `mr_ulus_heartland_held`
  artik end condition degil, sadece 30 puanlik kohezyon girdisi.
  Yeni loc: `mr_partition_cohesion_spent_tt`. `var:` situation scope'unda
  can_end icinde okunuyor (great_pestilence.txt:14-18 birebir bunu yapiyor),
  `has_variable` guard'i ayni scope'ta black_death.txt:158'de attested.

- (#1) Sucluyu vanilla'da bulduk: `generic_actions/government_conversions.txt`
  icindeki `steppe_horde_to_monarchy`, `ai_tick = monthly` +
  `ai_will_do = { value = 100 }` ve vanilla'nin kendi yorumu
  "#They always want to do this". Sartlari: barista olmak, kendi kulturunde
  sehir baskent, %25 home control. Sonra 15 yillik sayac kuruyor,
  `government_conversion_events.10` gelince `change_government_type`.
  Kayip dogrulandi: butun bozkir advance agaci `government = steppe_horde`
  ile kilitli (advances/government_steppe_horde.txt), yani `horse_lords` ve
  onunla `a_steppe_horse_archers`, `a_a_urughs`, `always_allow_army_levies`,
  kurultai binasi ve -0.5 levy maintenance gidiyor. Vanilla bunu kendi
  tooltip'inde soyluyor (warn_about_loss_of_content_tt). MGO_f/MGE_f
  formable'lari SUCSUZ - hicbiri hukumet tipi degistirmiyor.
  COZUM: `in_game/common/generic_action_ai_lists/`
  `zz_MR_government_transition_addon.txt`, `TRY_REPLACE:horde_list`.
  Kapi: is_ai + tag MGO/MGE + NOT mr_railroad_off + NOT mr_railroad_complete
  + NOT mr_railroad_failed. Son kloz sart: rayli yol cokerse
  mr_railroad_complete hic gelmez ve AI sonsuza kadar kilitli kalirdi.
  Insan oyuncunun butonu duruyor - yazarin karari.

- (HARNESS 33 -> 34) Yeni kontrol: `mr_in_claimant_realm never negated in
  place`. Iterator icinde negatiflenmis realm testini yakaliyor ve gonderilen
  hatanin BIREBIR seklini canary olarak tasiyor, boylece pattern sessizce
  bozulursa kontrol vacuous gecemiyor.

- (DOKUMAN) CLAUDE.md: mimari tablosu + Great Partition maddesi guncellendi,
  UC yeni hard rule eklendi (sahipsiz arazi, TRY_REPLACE/TRY_INJECT ile
  vanilla entry duzenleme, vanilla'nin AI hordeyi yerlestirmesi).
  MR_reforms.txt: sabahki "bu gecis serbest" karari revize edildi.

## DOGRULANANLAR (iyi haber)

- (D2 KAPANDI) KAZ haritaya GELDI - ekran goruntusunde "County of Kazakh".
  `is_historic` kimlik blogu olan landless bir tag `change_location_owner`
  ile gercekten instantiate oluyor. Bu, 29.07 denetiminin acik biraktigi
  probu kapatiyor.
- Situation aciliyor, on_ending calisiyor, halefler dogup toprak aliyor,
  end-condition paneli checklist olarak render oluyor.

## HALA ACIK / SONRAKI TESTTE BAKILACAK

- `TRY_REPLACE:` prefix'i olculen klasorler arasinda `generic_action_ai_lists`
  YOK (olcum: advances, prices, laws, generic_actions, static_modifiers,
  building_types). Ayni `in_game/common/` sinifinda oldugu icin calismasi
  bekleniyor ama TEYIT EDILMEDI. TEST: AI Kaghan Faz 3 bitmeden monarchy'ye
  gecerse prefix tutmamistir; o zaman hedef `generic_actions/` altinda
  `TRY_REPLACE:steppe_horde_to_monarchy` olur (REAI'nin call_parliament ile
  birebir kanitladigi klasor) ya da talibe vanilla degiskeni
  `is_about_to_reform_government` kurulur.
- MEVCUT KAYIT YENI TEST ICIN KULLANILAMAZ. `mr_partition_collapsed` global'i
  o save'de zaten set ve `mr_can_start_partition` onu reddediyor - situation
  bir daha acilmaz. Ayrica AI zaten donusum aksiyonunu almissa 15 yillik sayac
  iptal edilemez. Great Partition ve horde kilidi YENI OYUNDA test edilmeli.
- Haleflerin rutbesi/hukumeti: KAZ "County of Kazakh", CHG "Chagatai Tribal
  Kingdom" olarak dogdu. Vanilla setup girdilerinde ne rank ne government var,
  MR de vermiyor. Kozmetik ama dort hanligin ilcelik olarak dogmasi garip
  duruyor - istenirse `set_country_rank_effect` ile duzeltilebilir. KARAR
  BEKLIYOR.
- Kirim'in cikmamasinin sebebi teyit edilmeli: kloz true idi, demek ki MGE o
  an crimea_area'yi tutmuyordu (release sadece Kaghan'in realm'indeki topragi
  aliyor). crimea_area steppes_region icinde, yani Faz 3 hedefiydi - Faz 3
  bittikten sonraki 30+ yilda kaybedilmis olabilir. Sonraki testte MGE'nin
  Kirim'i tutup tutmadigina bakilacak.

##### 30.07.2026 (AYNI GUN, IKINCI TUR) GREAT PARTITION: TARIH GERI GELIYOR #####

Yazarin ekran goruntusu uzerinden iki soru daha cikti ve ikisi de tasarim
duzeyindeydi. Harness 34 -> 34 kontrol (biri genisletildi), hepsi yesil.

## SORU 1: HALEFLERIN TOPRAKLARINDAKI GRI DELIKLER - HATA DEGIL, OLCULDU

Yazar "KAZ ve CHG'nin aldigi topraklarin yarisi bos kalmis, normalde orasi
doluydu" dedi. default.map + definitions.txt + setup/start/10_countries.txt
uzerinden sayildi:

    atom                      toplam  sahiplenilemez  1337'de sahipsiz  gri
    MR_geo_tarim (CHG)            88        34               7         %47
    MR_geo_siberian_marches      101        34               0         %34
    MR_geo_dzungaria (OIR)        48        12               0         %25
    MR_geo_crimean_seat (CRI)     18         4               0         %22
    MR_geo_heartland             263        50               0         %19
    MR_geo_kazakh_steppe (KAZ)   183        28               0         %15
    MR_geo_bashkiria (BSH)        28         2               0          %7
    MR_geo_nogai_steppe (NOG)     98         3               0          %3

Tarim'in neredeyse yarisi Taklamakan, Karakorum/Altun daglari ve Bosten/Lop
golleri; motor bunlari `lakes` / `impassable_mountains` / `non_ownable`
bloklarinda tutuyor (toplam 918 + 1868 + 153 lokasyon) ama definitions.txt
onlari siradan province -> area -> region agacinin ICINE koyuyor. MGE de o
topraklara hicbir zaman sahip degildi; delikler bolunmeden ONCE de oradaydi,
tek renkli devasa mavi blobun icinde goze batmiyorlardi. change_location_owner
her seyi dogru devretti - devredilecek toprak zaten o kadardi.

KIRIM DA CIKMIS. Bir onceki turda "MGE Kirim'i tutmuyordu" diye tahmin
etmistim, yanlis: CRI cikti ama MR_geo_crimean_seat sadece crimea_area, yani
14 sahiplenilebilir lokasyon - listenin en kucugu, tasarim geregi
(cografya dosyasi yedisan_area'yi bilerek disarida birakiyor).

## SORU 2: YERLESIK DUNYA HIC GERI GELMIYORDU - GERCEK EKSIK

Yazar "pers, anadolu falan niye ayrilmiyor, moğol patladiginda cikacak
ulkeler tarihi devam ettirsin" dedi. Haklidiv: halef listesi sadece alti
bozkir tag'iydi. MGE Faz 3 sonunda Persia'yi, Irak'i, Anadolu ayagini, Cin'in
tamamini, Kore'yi, Tibet'i, Mancurya'yi ve Volga'yi tutuyor ve BUNLARIN HEPSI
bolunmeden sonra da MGE'de kaliyordu. "Buyuk Dagilma"dan sonra haritada hala
Siraz'dan Kanton'a uzanan bir imparatorluk duruyordu.

Ustune, olcunce daha kotu bir sey cikti: mevcut haliyle bu situation'da
COGU OYUNDA HICBIR SEY OLMUYOR. Kohezyon sadece Kaghan fiilen toprak
kaybettiginde dusuyor, modda MGE'ye toprak kaybettiren hicbir sey yok (faz
odulleri kalici buff, Faz 3 failsafe'i eksigi tamamliyor). Ve kisir dongu:
Mogollara yonelmis tek koz olan cb_MR_carve_the_ulus kohezyon 55'te
veriliyor, 55'in altina inmek icinse once bes ulus kaybetmis olman lazim.
Imparatorlugu kirmaya yarayan alet, imparatorluk kirildiktan sonra
dagitiliyordu. Sonuc: 1720 timeout -> MR_the_ulus_endures -> harita ayni.

## YAZARIN UC KARARI (30.07)

1. Kapsam: on uc degil, ON DORT tiyatro birden - bozkir alti + yerlesik sekiz.
2. Kopus bicimi: KADEMELI, on_monthly icinde. Imparatorluk gozun onunde erisin.
3. Takvim: yil VEYA gecen sure, hangisi once.

3 numarada bir duzeltme yapmak zorunda kaldim ve yazara bildirildi: yil klozu
GERCEK tarih OLAMAZ. Situation en erken 1600'de aciliyor ve gercek tarihlerin
neredeyse hepsi (Kirim 1441, Kazak 1465, Safevi 1501, Kazan 1552, Nogay 1557,
Joseon 1392) gecmiste kaliyor - hepsi ilk ay patlardi ve yay tek tike
cokerdi. Cozum: SIRA tarihi tasiyor, gecen ay sayaci hizi belirliyor, yil
klozu ise bir BACKSTOP merdiveni (1650 -> 1702, dorder yil) ve sadece gec
acilan bir kampanyanin 1720 penceresini asmasini engelliyor.

## NE YAPILDI

- YENI: `in_game/common/scripted_effects/MR_partition_effects.txt`. Tiyatro
  basina bir scripted effect (mr_return_crimea ... mr_return_tarim), her biri
  kendi `mr_returned_*` global bayragini iceriden kontrol ediyor (idempotent).
  BIR kez yazildi, IKI yerden cagriliyor: on_monthly (takvim) ve on_ending
  (son supurge). Onceki halinde ayni on bir satir alti kez on_ending'in
  icinde kopyalanmisti; on dorde cikinca iki yerde yirmi sekiz kopya olacakti.
  NOT: EU5'te scripted_effects VAR (vanilla 10+ dosya, `$param$` destekli) -
  bu mod bugune kadar hic kullanmamisti.

- Tiyatroler ve mirascilar (hepsi 1650-1700'de o topragi FIILEN tutan guc):
    +4y  Kirim (1441)                  CRI
    +8y  Kazak (1465)                  KAZ
    +12y Safevi Persia (1501) + Kafkas IRA
    +16y Baskurt (1662)                BSH
    +20y Orta Volga (1552/56)          RUS, yoksa MOS
    +24y Nogay (1557)                  NOG
    +28y Kuzeyde Rusya (1582-98)       RUS/MOS  (Sibirya + Ural + Rus topraklari)
    +32y Osmanli (1638 Bagdat)         TUR      (Irak + Anadolu + Ermeni yaylasi)
    +36y Mancurya (1616 Nurhaci)       QNG
    +40y Congar (1634 Erdeni Batur)    OIR
    +44y Tibet (1642 Ganden Podrang)   TIB
    +48y Cin (1644 Qing Pekin'de)      QNG
    +52y Kore (1392 Joseon)            KOR  (once cancel_subject, sonra supurge)
    +56y Tarim (1680 Galdan Kasgar)    CHG

- SIRALAMA YUK TASIYOR: kazan_area, bolghar_area ve bashkiria_area'nin
  ust bolgesi ural_region, yani MR_geo_ural orta Volga'yi VE Baskurdistan'i
  ICERIYOR. Baskurt (+16) ve orta Volga (+20) kuzey supurgesinden (+28) once
  kosuyor; sira bozulursa Rusya Baskurtlari yutuyor. Ayni sebeple
  MR_geo_pontic (steppes+caucasus) ve MR_geo_xinjiang (dzungaria+tarim)
  tiyatro olarak HIC kullanilmiyor - her biri iki halefi iceriyor.

- YENI ATOM (2): `MR_geo_caucasus` ve `MR_geo_middle_volga`. Ihtiyac duyulan
  diger on iki cografya zaten dosyada vardi - atom dosyasinin varlik sebebi
  tam olarak buydu.

- YENI KIMLIK BLOGU (2): IRA (farsi_culture + shia; MZF/INJ ve CHB'den
  attested) ve QNG (jurchen_culture + tungusic_shamanism; SIB'den attested).
  RUS'a gerek yok, cunku sadece country_exists arkasinda adlandiriliyor.
  TUR, TIB, KOR, MOS, MNG, CHI ve alti bozkir tag'i vanilla'da zaten kimlik
  blogu tasiyor.

- YENI GAME RULE: `MR_partition_schedule` (varsayilan ACIK). Kapatan oyuncu
  kesintisiz world conquest yapabiliyor.

- on_ending YENIDEN YAZILDI: cokus dali artik on dort effect'i sirayla
  cagiran tek bir supurge. Ve hayatta kalma dali artik kohezyon >= 70 de
  istiyor - yoksa Karakurum'un uzerinde 45 kohezyonla oturan bir Kaghan
  1720'de timeout'a girip kalici MR_the_ulus_endures odulunu aliyordu.

- on_ended on dort bayragi temizliyor; harita kirmizi cizgisi (tooltip) artik
  on dort tiyatronun hepsini kapsiyor.

- HARNESS: "scripted trigger refs resolve" -> "scripted trigger/effect refs
  resolve". Bir scripted EFFECT ile bir scripted TRIGGER'in cagri sekli
  ikisi de `X = yes` ve metinde ayirt edilemiyor; kontrol iki tanim kumesini
  birden yukluyor, ustune bir de "tanimli ama hic cagrilmayan effect" ters
  yon kontrolu ekledi.

## BEKLENEN KOHEZYON MERDIVENI (tam imparatorluktan)

    100 -> 92 (+4y) -> 80 (+8y, beat 85) -> 72 (+16y) -> 62 (+24y)
        -> 54 (+28y, beat 55 ve carve CB) -> 42 (+40y) -> 30 (+56y,
           beat 40 ve end trigger)

Yani 1600'de acilan bir kampanyada dagilma ~1656'da tamamlaniyor. Situation
artik kendi kendini bitiriyor ve butun ara mekanikleri (esik olaylari,
kurultai, komsulara verilen CB) gercekten devreye giriyor.

## SONRAKI TESTTE BAKILACAKLAR

- Takvim gercekten calisiyor mu: situation acildiktan ~4 yil sonra Kirim,
  ~8 yil sonra Kazak kopmali. Kopmuyorsa ilk suphe var:mr_partition_momentum
  karsilastirmasi.
- IRA ve QNG haritaya geliyor mu (KAZ'in D2 probunun aynisi, iki yeni tag).
- KOR vassal ise cancel_subject calisiyor mu (overlord ?= { cancel_subject =
  prev } - bu modda ilk kullanim).
- Kohezyon merdiveni yukaridaki gibi mi iniyor, esik olaylari ve carve CB'si
  siralamada dogru yerde mi ateşleniyor.
- Halef rutbeleri hala acik: "County of Kazakh", "Chagatai Tribal Kingdom".
  KARAR BEKLIYOR.
- MEVCUT KAYIT YINE KULLANILAMAZ: mr_partition_collapsed o save'de set.

##### 30.07.2026 (UCUNCU TUR) COKUS DEBUFFU, HALEF KORUMASI, RUTBE, SON UC TIYATRO #####

Ultracode workflow: 6 paralel arastirma + her birine ayri bir DUSMAN dogrulayici
+ tek sentez = 13 ajan, 0 hata, ~2.08M token, 799 tool cagrisi. Dogrulayicilar
toplam 58 iddiayi curuttu ve sentez ajani curutulenlerin tarafini tuttu.
Harness 34 -> 34, hepsi yesil.

## ARASTIRMANIN DUZELTTIGI DORT SEY

- `size` CARPANI ILE OLCEKLENEN TEK MODIFIER REDDEDILDI. add_country_modifier
  gercekten `size` aliyor ama "size modifierdaki her degeri carpar" iddiasi
  CIKARIM, effects.log hicbir yerde soylemiyor - yanlis cikarim butun taglari
  ayni anda sessizce bozar. Korumali takas varyantlari da olmuyor: biri sayisal
  `var:X = var:Y` istiyor (vanilla'da SIFIR ornek - uc kullanimin ucu de ULKE
  karsilastiriyor), digeri `set_to_largest_and_extend`, o da sadece SONLU sure
  ile attested. Secilen: UC KADEMELI MERDIVEN, mode = replace ile takas.
- `horde_unity_hit_at_ruler_death` ISARETI TERS. steppe_horde tabani -50
  (government_types/00_default.txt:106) ve motor kaybi sadece TOPLAM sifirin
  altindayken uyguluyor (_hardcoded.txt:3539-3545). Vanilla'nin
  horde_civil_war.txt:68'deki +50'si tam olarak toplami sifira cekip cezayi
  IPTAL ediyor - felaket hafifletmesi. Kaghan'a +50 yazmak veraset gecislerini
  agrisiz yapardi, yani tam tersi. -25 yazildi.
- `ai_months_between_wars` MUTLAK DEGIL, TOPLAMSAL DELTA
  (00_ai_personalities.txt:2-3 acikca soyluyor, :26 -12 yaziyor ki mutlak ay
  sayisi olarak imkansiz). difficulty.txt'deki 60/24/6 kuresel taban, kopyalanacak
  rakam degil. Kademe 2'ye +12 (ai_defensive), kademe 3'e +24 (ai_isolationist).
- IKI KOL OLU CIKTI. `subject_loyalty` MR_unified_mongol_banner'in KALICI +25'i
  ve MR_great_khan'in +100'u yuzunden tavana yapisik - -25 hicbir seyi
  oynatmiyor. `aggressiveness_modifier` de MR_great_khan +1 ve
  MR_imperial_historical_modifier +1'e karsi netleniyor. Ikisi de kullanilmadi;
  yerlerine `ai_months_between_wars` ve `carefulness_modifier`, bunlarin karsi
  agirligi yok.

## YAZILANLAR

- UC KADEMELI COKUS (MR_modifiers.txt): MR_the_centre_cannot_hold (<85),
  MR_the_uluses_drift (<55), MR_khaghan_in_name_only (<40). Mevcut 85/55/40
  esik beat'lerinin ICINDE veriliyor - o bloklar zaten claimant'a scope'lu,
  zaten kendi global bayragiyla korunmus, zaten bir kez atesleniyor; yeni
  aylik tarama YOK. Ucu de on_ending'in EN BASINDA, her iki daldan da once
  kaldiriliyor: bu bir basinc gostergesi, faz odulu degil.
  HICBIRINDE tek bir isyan tag'i yok - monthly_rebel_growth, global_separatism,
  local_unrest, pop_join_rebel_threshold hicbiri. `has_complacency_effects`
  de bilerek yok: o anahtar auto_modifiers/country.txt:456 uzerinden
  pop_join_rebel_threshold = 0.1'e baglaniyor, yani vanilla'nin butun
  gerileme ailesini arka kapidan iceri aliyor.
  56 tag'in hepsi harness'in "modifier tags exist in engine docs" kontrolunden
  gecti (301 item).

- HALEF KORUMASI: MR_ulus_of_its_own, 25 yil, on dort tiyatronun her birinde.
  Sekli vanilla'nin tek gercek "yeni bagimsiz ulke" modifier'i
  sco_independence_from_england (country.txt:5906-5914), 25 yillik verme sekli
  iro_strong_tribal_unity (flavor_IRO.txt:811). SAVUNMACI, saldirgan degil.
  monthly_legitimacy ve monthly_horde_unity BILEREK YOK: o taglar sadece
  government_power o kaynak olan ulkelerde isliyor ve haleflerin hukumet tipi
  hic yazilmamis durumda - evrensel karsiligi da yok (monthly_government_power
  modifiers.log'da 0/2437).
  Bu kol takvimin anlamli olmasini saglayan sey: 14 lokasyonluk bir Kirim'in
  yaninda KALICI faz odulleri tasiyan bir super guc varsa takvim toprak verir,
  AI ertesi ay geri alir.

- RUTBE: vanilla'nin set_country_rank_effect'i (yalnizca-yukselten mandal,
  country_rank_level < N korumali). IRA / TUR / RUS-veya-MOS / QNG(Cin) ->
  empire; KAZ ve QNG'nin ilk Mancurya adimi -> kingdom. CRI, NOG, BSH, OIR,
  CHG, TIB, KOR zaten vanilla setup'inda dogru rutbede - onlara cagri yok.
  KAZ bilerek kingdom: MR_l_english.yml:311 rank_empire_horde'u KURESEL olarak
  "Empire" yapiyor, rank_kingdom_horde'a dokunulmamis, yani kingdom KAZ
  "Kazakh Horde" okunuyor.
  KORE'ye bilerek cagri yok: promote edilse rank_empire_korean cikardi, o da
  1897.

- SON UC TIYATRO (kullanicinin steppes_region tespiti). Uc yeni atom,
  MEVCUT tiyatrolara katlanarak - uc yeni slot merdiveni 17 girise ve 1714'e
  tasirdi, uc yeni bayrak, uc yeni on_ended temizligi ve oyuncuya gorunen kural
  aciklamasinin yeniden yazilmasini isterdi:
    MR_geo_safavid_khorasan  (dogu+bati Khorasan, 96)  -> IRA, slot 3
    MR_geo_kuban_and_yedisan (yedisan+pryazovia+matrega, 64) -> CRI, slot 1
    MR_geo_pontic_frontier   (kursk+sloboda+zaporizhzhia+lower_don+azov, 145)
                                                        -> RUS/MOS, slot 7
  Ve situation'in tooltip blogundaki atom listesine ucu de eklendi - o liste
  CLAUDE.md'nin saydigi altinci tuketici ve en cok atlanan yer.

## SONUC: KAGHAN'IN ELINDE KALAN 379 LOKASYON (bagimsiz olarak iki kez hesaplandi)

    mongolia_region  213   dokuz alanin hepsi, Karakurum icinde
    khorasan_region  166   transoxiana 96 (Semerkant) + khwarazm 32
                           + badakhshan 38
    steppes_region     0

  Yedi raylı-yol koltugundan IKISI kaliyor: Karakurum ve Semerkant. Ucu de
  gercekten Cinggisid: Halha Mogolistan, Buhara (Canogullari 1747'ye kadar) ve
  Hive (Arabsahiler 1740'a kadar). Sarai al-Jadid gidiyor cunku Yeni Sarai
  1395'ten beri harabe ve Karakurum'a 4000 km uzakta 42 lokasyonluk bir eksklav
  tarihsel bir yerlesim degil - Anno 1644 modu da sarai_al_jadid'i Rusya'ya
  veriyor.

  NOT: 379 bir TABAN, kesin rakam degil. 684/379 hesabi ATOM BIRLESIMININ
  artigi; 29 atomun disinda fethedilen her sey (Hindistan, Misir, Avrupa) hic
  geri verilmiyor ve mr_partition_takeable bir INSAN vassalinin topragini
  bilerek hic almiyor.

## BULUNAN CANLI KURAL IHLALI (KARAR BEKLIYOR, DOKUNULMADI)

MR_modifiers.txt:425 -> MR_kurultai_defied icinde `monthly_rebel_growth = 0.005`,
ve TAM USTUNDE 14 satirlik bir yorum (411-424) "bedel bilerek isyan DEGIL...
AI'a %40 sansli bir secenekle isyan buyumesi vermek her seyi ayni anda
bozardi" diyor. Kod yorumun yasakladigi seyi yapiyor. Canli:
MR_partition_events.txt:340'ta ai_chance 40 olan secenege 25 yil veriliyor, ve
o secenegin kendi yorumu da (satir 331) "realm pays for the refusal in unrest"
diyor - yani modun ici iki yorumla kendisiyle celisiyor.
Kardes dort ornek: MR_imperial_failure_ai/_player ve
MR_dominance_failure_ai/_player (+0.0025). Bunlar BASARISIZLIK durumu
modifierlari, yani raylı yol zaten bitmis - savunulabilir, ama ayni ruling
lazim.

## HALA ACIK

- HALEFLERIN HUKUMET TIPI VE BASKENTI YAZILMAMIS. "County of Kazakh"in kok
  sebebi bu; rutbe onu ancak "Sultanate of Kazakh"a tasir. Isim asil hukumet
  tipinden geliyor. Vanilla kendi cozumunu gosteriyor: spawn sonrasi
  set_capital + change_country_type + change_government_type
  (flavor_chi.txt:2543-2550, late_ming_crisis.txt:307-313). MR'in uc partition
  dosyasinda bu ucunden HICBIRI yok, add_core ve set_new_ruler da yok.
- `rank_empire_tribe` = "Tribes" ve butun kultur dallarinin ustunde. Hukumet
  tipi yazilmadigi surece empire'a cikan bir halef "Persian Tribes" okunabilir.
- `horde_unity_hit_at_ruler_death = -25` buyuklugu attested degil (vanilla'da
  sadece -50 taban ve +50 hafifletme var). Veraset kaybi cok sertse -10 yap.
- MR_l_english.yml:311'in kuresel rank_empire_horde -> "Empire" override'i
  vanilla OIR'i de etkiliyor (OIR 10_countries.txt:48920'de rank_empire ile
  basliyor), yani "Oirat Empire" partition hic calismadan once haritada.
  Onceden var olan bir yan etki, bu turun urunu degil. Karar bekliyor.
- QNG'nin arma dosyasi yok, uretilmis arma cizecek (vanilla 280 karali tag'i
  armasiz gonderiyor, hata basmiyor). Isteniyorsa CHI armasi yeniden
  kullanilabilir - vanilla'nin kendi tercihi bu.

##### 30.07.2026 (DORDUNCU TUR) ILK CANLI PARTITION KAYDININ COZULMESI #####

Yazar 1650'de acilan gercek bir kampanyada partition'i izledi ve Object
Inspector'dan degisken degerlerini verdi. Bir ajan yazarin autosave'lerini
acip okudu. Bu turda tahmin yok; her bulgu ya kayittan ya save'den.

## OLCULEN DURUM (momentum 131, sonra 240; yil 1670)

    mr_partition_momentum      131 -> 240
    MR_cohesion_score           80
    mr_partition_concessions    10        <- her seyin anahtari
    mr_leading_country          MGE

## DORT BULGU

1. TAKVIM CALISIYOR ama HER SEYI BACKSTOP TARIHLERI ATESLEDI. Momentum klozu
   bu kampanyada hicbir seyi ateslemedi - dort yillik adimlar merdivenin hep
   gerisinde kaldi. 1670'te tikli olan alti bayrak tam olarak backstop'lari
   1670 ve oncesi olanlar: 1650/1654/1658/1662/1666/1670.

2. PERS TETIKLENDI AMA HICBIR SEY TASIMADI. 1658.2'de calisti, 875 talip
   lokasyonunu supurdu, hicbirini tasimadi. Sebep: 679 MB'lik save'de IRA
   ULKE NESNESI YOK. Konsol: "tag IRA -> country is not valid".
   ULKE VERITABANI KAMPANYA KURULURKEN BIR KEZ BASILIYOR. IRA ve QNG
   bloklari o kampanyadan sonra eklendi, dolayisiyla o kayitta hic var
   olmadilar. KAZ calisiyor cunku onun blogu kampanyadan onceydi - id 2340'ta
   oturuyor, vanilla'nin tam 2339 kimlik blogundan sonraki ilk id.
   BU KAYITTA DUZELTILEMEZ. Yeni kampanya sart.

3. UFA HALA MOGOL, mr_returned_bashkiria SET. Kampanya yasiyla aciklanmiyor:
   BSH vanilla tag'i, id 2253. Sebep BASKA ve gercek: BSH
   country_type = pop. Pop tipi ulkeler (vanilla'da 448 tane) POP sahibi,
   lokasyon sahibi degil; change_location_owner onlara sessizce hicbir sey
   yapmiyor.

4. KOHEZYON GERI YUKSELIYOR. Kurultai'nin iki secenegi concessions'a ekliyordu
   (+25 otonomi, +10 altin) ve skor 100 - kayip + concessions olarak
   hesaplaniyordu. Aritmetik birebir: 100 - 8 (Kirim) - 12 (Kazak) - 10
   (Nogay) + 10 = 80. Momentum 260'ta 100'e donmesi art arda kurultai.
   Ve kurultai'nin KENDI release kodu vardi - takvimden once yazilmis,
   bayrak kurmayan, mr_in_claimant_realm ile sinirli (yani INSAN vassalinin
   topragini alabilen), core vermeyen, on dort tiyatronun sadece altisini
   bilen bir kopya. Nogay'i o birakti, momentum 288 hic gecilmeden.

## YANLIS CIKAN IKI OKUMAM (kayit icin)

- "Nogay zaten haritadaydi, canli vanilla ulkesi" - HAYIR. NOG'un 1337 blogu
  var ama Faz 3 sonunda topraklari Mogol'daydi; onu kurultai birakti.
- "mr_partition_takeable olu olabilir" - HAYIR. Yazar Kuban ve Yedisan'in
  Kirim renginde oldugunu dogruladi, oraya SADECE takvim gidebiliyor.
  Trigger saglam.

## YAZILANLAR

- 22 devir dongusunun hepsine vanilla ucluau: change_location_owner +
  add_core + change_integration_level = core (fall_of_delhi.txt:299-301,
  bir situation'in ardil devlet cikarmasi). Oncesinde add_core sayisi
  dosyada SIFIRDI - her halef integration_conquered seviyesinde,
  ayrilikcilikla doguyordu.
- BSH'ye once change_country_type = location.
- Bayrak artik sadece atomda talip topragi kalmadiysa dusuyor. Sessiz
  basarisizlik bir daha kalici olamaz.
- mr_partition_concessions KOMPLE SILINDI - degisken, seed, temizlik, aylik
  terim, ve onu zapt etmek icin konulan +15 tavani ile 92 tabani. Kohezyon
  artik tam olarak 100 - kayip, mandal, geri ekleyen hicbir sey yok.
- Kurultai kendi release kopyasini birakti, takvimin effect'lerini cagiriyor.
  Uc secenek gercek seyler oduyor: A istikrar+mesruiyet (ulus barisçil
  gidiyor), B modifier'in kendisi, C on yillik sessizlik (cooldown -60).
- Sekiz halefe baskent, uc tanesine hukumet tipi. MOS/RUS, NOG, TUR, TIB,
  KOR'a BILEREK dokunulmadi - yasayan 1337 ulkeleri.
- Hiz: adim 4 -> 3 yil, sira tarihsel capalara gore yeniden kesildi.
  Yay 1652-1691 (onceden 1650-1702). Rusya 1664 ve 1670.
- Partition acilinca Kagan ai_defensive, hayatta kalirsa ai_aggressive.
- Situation harita modunda halefler kendi renklerini koruyor.

## HALA ACIK

- Kalici Faz 1-3 odul modifierlari: strip mi, zayiflat mi, birak mi. Once
  ne verdiklerinin olculmesi lazim.
- OIR (+26y) ve CHG (+41y) hic test edilmedi, ikisi de country_type = army.
- Haleflerin dini/ismi: CRI ortodoks doguyordu, baskent + hukumet tipi
  yazildi ama duzelip duzelmedigi olculmedi.

##### 31.07.2026 YENI KAMPANYA: UC SESSIZ HATANIN KOKU TEK YERDE #####

Yazar yeni bir kampanya kurdu, bookmark init hatalarini ve bir 1667 observer
save'ini Object Inspector'la okudu. Dort paralel Opus ajani (bookmark yagmuru,
spawn-sonrasi kimlik, MCH/QNG/CHI formable semantigi, 1066 modu denetimi)
~790k token. Bu turda tahmin yok: her bulgu ya oyun kaydindan ya vanilla'dan.

## OLCULEN UC SEMPTOM

1. Her kampanya kurulusunda KAZ/IRA/QNG icin 10'ar satir
   initialize_from_bookmark hatasi (hukumet tipi, veraset, dini okul, baskent,
   baskent kesfi, marriage_law, heir_religion_law, toplum degerleri,
   parlamento).
2. IRA ve MCH cag 5-6'da SIFIR advance ve SIFIR harita bilgisiyle dogdu.
   KIRIM'DA OLMADI - yazarin bu ayrimi teshisin anahtari cikti.
3. Kirim ORTODOKS dogdu, Mancu halefi TENGRI dogdu, ikisinin de hukumdari
   rastgele uretildi.

## TEK KOK NEDEN

Kimlik blogu var, BASLANGIC BLOGU YOK. Vanilla'da bu kombinasyon SIFIR kez
geciyor: 2337 gercek tag'in 2337'sinde ikisi de var, sadece motorun rezerve
DUMMY/PIR/MER'inde yok. Hukumet tipi, veraset, baskent, KESIF, yasalar,
toplum degerleri, parlamento, religious_school ve starting_technology_level
hepsi main_menu/setup/start/10_countries.txt'te yasiyor.

Kirim'in duzgun cikmasinin sebebi de bu: CRI'nin 10_countries.txt:4195-4222'de
topraksiz bir baslangic blogu VAR (starting_technology_level = 3 +
include = "expl_mongols"). KAZ/IRA/QNG'de yoktu.

`is_historic = yes` bu on satiri susturmuyor - o sadece :592'yi susturuyor.
12 satirdan 10'a dusmenin aciklamasi tam olarak bu.

## MCH ZINCIRI (yazarin oyun ici olcumleriyle kapandi)

- QNG DIYE BIR TAG YOK. Vanilla'nin Qing'i MCH'nin yeniden adlandirilmisi:
  flavor_MCH.txt:1024-1030 (flavor_mch.17) CHI_f formluyor, sonra QNG'yi
  ISIM/sifat/renk olarak yaziyor.
- Eski kodda QNG kimlik blogu vardi -> spawn oldu -> jurchen kulturu +
  Mancurya'nin tamami MCH_f'in potential'ini sagladi -> AI Later Jin'i
  formladi -> tag MCH oldu. Yazarin gordugu MCH bizim QNG'ydi. 1667
  save'inde: Tag MCH, debug Key 2342 (bizim ucuncu mod tag'imiz),
  Historical Tag CHI, Flag CHI, baskent Dadu, din Tengrism, kultur Jurchen.
- Yazar QNG->MCH degisikligini yapinca 1670'te mr_return_manchuria = yes
  calisti ve HICBIR SEY OLMADI: MCH'nin vanilla'da hicbir kimlik blogu yok
  (46 dosyanin hicbirinde "MCH" gecmiyor; tek kaydi MCH_f formable'i).

## FORM_COUNTRY'NIN GERCEK SEMANTIGI (iki yuzu de ayni kampanyada olculdu)

Hedef tag BOSSA tag'i yaziyor, DOLUYSA yazmiyor - ama form_effect ve sonraki
butun satirlar her iki durumda da calisiyor.
  QNG -> MCH_f : MCH bostu  -> tag MCH oldu
  MCH -> CHI_f : CHI doluydu (Filipinler'de kalinti CHI, `tag CHI` konsolu
                 Qing'e gitmiyor) -> tag MCH kaldi, Historical Tag CHI oldu
Vanilla bunu dort yerde koruyor: LAT_f 793/801, THE_f 985/995,
rise_of_the_ottomans.txt:355 (ve :379'da c:TUR diye hitap ediyor),
red_turban_rebellions.txt:520 (mevcut CHI'yi YUA yapip tag'i BOSALTIYOR).

Vanilla'nin ilani ONCE yapabilmesinin sebebi flavor_mch.17'nin bir event
option'i olmasi ve ARDINDAN ULKEYE TAG'LE HITAP EDEN HICBIR KOD OLMAMASI.
Bizde bes sey vardi. CHI'nin yok edildigi bir kampanyada Cin tiyatrosu
sessizce olurdu.

## YAZILANLAR

- Kimlik blogu QNG -> MCH (color = map_MCH). Bedava gelenler: gercek Mancu
  armasi (pre_scripted_countries.txt:23903), country_MCH.txt'nin alti
  advance'i (has_or_had_tag ile korunuyor, re-tag'den sag cikiyor), 19
  olayllik flavor_MCH zinciri. QNG'nin hic armasi yoktu.
- MR_great_partition.txt'teki olu `tag = QNG` satiri silindi.
- Cin tiyatrosu yeniden siralandi: ONCE toprak, sonra koltuk/rutbe/grace,
  EN SON ilan - ve ilan `c:MCH` yerine `scope:mr_qing` ile yapiliyor.
  Bu ayni zamanda vanilla'nin kendi flavor_mch.17'sine (tag = MCH,
  monthly_chance = 100) karsi da bagisiklik veriyor.
- YENI DOSYA main_menu/setup/start/28_MR_countries.txt (BOM YOK): KAZ, IRA,
  MCH icin topraksiz baslangic bloklari. Sekiller vanilla'dan: KAZ <- TIM
  (:48847), IRA <- FEZ (:19464), MCH <- DNG (:49828). Uc baskentin de
  kendi kesif sablonunun icinde oldugu tek tek dogrulandi (shavgar
  khorasan_region / isfahan persia_region / shenyang manchuria_region).
- Yedi halefe elle kimlik: create_character + set_new_ruler +
  change_religion + change_religion_for_ruler_and_family + change_culture.
  Isimler tarihsel (Haci, Jangir, Abbas, Aldar, Nurhaci, Erdeni, Abdullah),
  hanedanlar vanilla'dan (borjigin, aisin_gioro, choros), `age = 35` ile -
  birth_date degil, cunku partition'in sabit tarihi yok (vanilla'nin 1358
  create_character blogunun 487'si ayni sekilde).
- HARNESS 34 -> 36:
  * BOM kontrolu main_menu/setup/start/ icin TERSINE cevrildi (o klasor tek
    BOM kabul etmeyen agac; BOM'lu dosya sessizce olu sayiliyor).
  * YENI: "land is only handed to registered tags" - change_location_owner =
    c:X cagrilarinda X'in kimlik registry'sinde olup olmadigini bakiyor.
    form_country ile formlanan taglar (MGO) ve define_unique_country_tag ile
    basilanlar muaf, cunku ikisi de yaratmiyor/kayit istemiyor. KIRMA TESTI
    YAPILDI: c:MCH kayitsiz bir tag'e cevrilince kontrol yakaladi.
  * YENI: "mod-registered tags have a start block".

## 1066 MODU DENETIMI (ayni ajan turunda, salt okuma)

Bizim hatayi TASIMIYOR: 2385 kimlik blogu / 2382 baslangic blogu, kimlik-ama-
baslangic-yok olan sadece vanilla'nin DUMMY/MER/PIR'i. Ama kendi hatasi var:
ABS ve FAT butun oyundaki (mod + vanilla) TEK iki karali ulke blogu ki
parliament_type'i yok - 30.07'de yapilan duzeltme sablonun verdigi dort seyin
ucunu tekrar yazip dorduncusunu atlamis. Ayrica dokuz tag'in baskenti kendi
topraginda/iddiasinda degil (vanilla'da da dokuz ayni sinif var, bu yuzden
SUPHELI), ve DUB/ULD sablonun 2'sine karsi 3 teknoloji seviyesi yaziyor.
Bunlar 1066 modunun kendi HANDOFF'una yazilmali - burada degil.

## HALA ACIK

- YENI KAMPANYA SART: setup sadece kampanya kurulurken okunuyor.
- CHG'nin dini: tag'in kendi kaydi tengri, ama 1650'de Yarkand Hanligi
  Muslumandi. Muhafazakar secim yapildi (tag'in kendi kaydi), degistirmek
  tasarim karari.
- Kalici Faz 1-3 odul modifierlari hala olculmedi.
- OIR (+26y) ve CHG (+41y) hic test edilmedi.

## MEKANIZMA NETLESTI (yazarin eski turlardaki gozlemi, 31.07)

Yazar: "Kirim Mogol'un icinden ciktiginda advance'leri etrafindakilerle
AYNIYDI, cikarken yetismisti. Ama Pers ve Mancu/Qing hep gerideydi."

Bu, teknoloji farkinin sebebinin "yetisme" degil VAR OLMA oldugunu gosteriyor:
baslangic blogu olan tag kampanya kurulurken ulke nesnesi olarak yaratiliyor
ve topraksiz da olsa 313 yil boyunca dunyanin cag ilerlemesini yasiyor;
sadece kimlik blogu olan tag ise toprak verilene kadar HIC var olmuyor ve
sifirdan doguyor.

starting_technology_level bu isin kaldiraci DEGIL: motorun kendi yorumu
(0_age_of_traditions.txt:1) "sadece age of traditions'ta gecerli" diyor, 215
advance dosyasinin 6'sinda toplam 25 advance'ta var ve kullanilan degerler
sadece 1/2/3/4. Yani 3 yazmak 1337'deki birkac cag-1 advance'ini belirliyor,
baska hicbir sey yapmiyor.

TEST EDILEBILIR TAHMIN: yeni kampanyada IRA ve MCH de tam olarak CRI gibi
davranacak - ciktiklari anda komsulariyla ayni seviyede. Yanlis cikarsa
mekanizma baska bir seydir ve her halefe elle secilmis research_advance
listesi yazmak gerekir (EU5'in tek advance verme yolu; toplu verme guvenli
degil - dort *_advance_definition iteratorunun vanilla'da sifir kullanimi var
ve caga gore suzecek hicbir trigger yok).

## ILK CANLI GERI BILDIRIM (31.07, yeni kampanya)

    government.cpp:3544  Removing invalid policy 'polygyny' for 'KAZ Kazakh' 2340 at game start

IKI SEY SOYLUYOR:
1. IYI HABER: polygyny yasasi SADECE eurasian_horde_not_present sablonundan
   gelebilir, KAZ da o sablonu sadece bugun yazilan 28_MR_countries.txt
   uzerinden aliyor. Yani DOSYA OKUNUYOR, vanilla'nin 10_countries.txt'siyle
   BIRLESIYOR, ve KAZ artik kampanya kurulusunda var (id 2340).
   Ek dosya (farkli isim) rotasi calisiyor.
2. HATA: polygyny'nin potential'i `is_country_religion_pagan OR hindu OR
   indian culture group` (01_common.txt:1686-1692). KAZ SUNNI, gecmiyor,
   motor yasayi atiyor. Vanilla'nin ayni sablonu kullanan iki Musluman
   ulkesi de tam bu yuzden eziyor: CHB muslim_marriage (10_countries.txt
   :57721), TIM monogamous_marriage (:48857).
   Duzeltildi: KAZ'a laws = { marriage_law = muslim_marriage }.
   muslim_marriage'in potential'i sadece religion.group = muslim (:1656) ve
   modifierleri polygyny ile birebir ayni.

CIKARILAN GENEL KURAL: bir include'dan gelen yasa, o include'u kullanan
ulkeye UYDUGU GARANTI DEGIL. Din/kultur kapili her yasa, ulkenin kendi dinine
gore yeniden yazilmali. IRA (muslim_monarchy_not_present -> muslim_marriage)
ve MCH (jianzhou_tribe_not_present -> polygyny, tungusic_shamanism pagan)
bu yuzden sikayet uretmedi.

DOGRULANDI (31.07, ayni gun ikinci new game): polygyny satiri gitti.
marriage_law = muslim_marriage duzeltmesi calisiyor. Ayrica bu ikinci kez
dogruluyor ki farkli isimli ek dosya main_menu/setup/start/ icinde
BIRLESIYOR ve BOM'suz haliyle okunuyor.

## KAPANDI: BOOKMARK INIT YAGMURU (31.07, olculdu)

Yazar yeni kampanya kurdu ve KAZ/IRA/MCH icin initialize_from_bookmark.cpp
satirlarinin HEPSI gitti. On satirin on tanesi de. Teshis dogruydu ve
duzeltme tamdir:

  kimlik blogu (in_game/setup/countries/)  -> c:TAG cozulur
  baslangic blogu (main_menu/setup/start/) -> hukumet tipi, veraset, baskent,
                                              KESIF, yasalar, toplum
                                              degerleri, parlamento, dini okul
  IKISI BIRDEN sart. Vanilla'da 2337/2337 tag'in ikisi de var.

Bu ayni zamanda su iddiayi da olcmus oluyor: is_historic = yes o on satiri
susturmuyordu, susturan sey baslangic blogu.

## HENUZ OLCULMEDI (sadece 1650'lerde partition acilinca gorunur)

- IRA ve MCH cikarken komsulariyla ayni seviyede mi (tahmin: evet, CRI gibi)
- Kirim Sunni, MCH Tungusik Samanist, IRA Sii mi
- Hukumdarlar isimli mi (Haci, Jangir, Abbas, Aldar, Nurhaci, Erdeni,
  Abdullah)
- "County of Kazakh" gitti mi
- Cin adiminda toprak-once sirasi ve "Qing Empire" + CHI bayragi
- OIR (+26y) ve CHG (+41y) hala hic gorulmedi

## BASKURT TIYATROSU: YAZARIN KARARI + GERI CEKILEN BIR OLCUM (31.07)

YAZARIN KARARI: Baskurtlar kendi slotunu almiyor. Rusya zaten aliyor, cunku
mr_return_north MR_geo_ural'i supuruyor ve ural_region bashkiria_area'yi
ICERIYOR. Harita yine dogru cozuluyor, sadece bir tiyatro sonra ve baska
bir bayrak altinda. Diger tiyatrolarin momentum/backstop tarihleri bos slota
gore yeniden kesilmisti, oyle kaliyor.

GERI CEKILEN OLCUM: "BSH pop tipi oldugu icin spawn edilemiyor" teshisinin
DAYANDIGI KANIT gecersiz. Kanit olarak Ufa'nin Mogol kalmasi gosterilmisti;
ama `ufa` PERM_AREA'da ve MR_geo_bashkiria sadece bashkiria_area. Ufa atomun
icinde hic olmadi, kimseye teklif edilmedi. Pop-ulke YASASI ayakta kaliyor
(vanilla'dan attested: government_conversion_events.10), sadece oyun ici
kaniti geri cekiliyor.

DAHA MUHTEMEL SEBEP (kimse okumamis): BSH'nin kendi baskenti khaiylmysh
khorasan_region / desht_kipchak_area'da - atomun disinda, ural_region'in bile
disinda. Ve vanilla'nin kabile-yerlesme yolu tam buna kapili:
laws/00_tribes.txt:184-195, permanent_settlement_policy ->
allow = { capital = { OR = { owner = root  has_owner = no } } }
sonra on_fully_activated = { change_country_type = location }.
Yani vanilla bir pop ulkesini landholder yapmadan once BASKENTININ kendisinde
ya da sahipsiz olmasini sart kosuyor. Bir gun canlandirilirsa TIP'ten degil
BASKENT'ten baslanacak.

## ILK CANLI PARTITION, YENI KAMPANYA (31.07) - UC DUZELTME BIRDEN DOGRULANDI

Situation 4 acildi. Kirim Mogol'dan ayrildi:
  - hukumdar ISLAM (Islam III Giray, 1644-1654) -> create_character +
    set_new_ruler calisiyor, ve donem-dogru isim tuttu
  - dini SUNNI -> change_religion calisiyor. Onceki turda ORTODOKS
    doguyordu. release-time alan teshisi dogruydu.
  - teknolojileri ARASTIRILMIS geldi
Kazak da geldi:
  - hukumdar JANGIR BORJIGIN -> isim VE hanedan birlikte tuttu
  - dini SUNNI

UC AYRI DUZELTME AYNI ANDA DOGRULANDI: elle yazilan din, elle yazilan
donem-dogru hukumdar, ve hanedan. Kirim'in teknolojisi zaten sorunsuzdu
(baslangic blogu vardi); KAZ'in blogu ise BUGUN eklendi.

## HALA BEKLEYEN - ASIL TEKNOLOJI TESTI

Kirim teknoloji sorununu hic yasamamisti. Tahminin gercek sinavi IRA (1658)
ve MCH (1670): ikisi de bugune kadar HIC baslangic blogu tasimadi ve ikisi de
"0 advance + harita korlugu" ile doguyordu. Onlar da komsulariyla ayni
seviyede gelirse mekanizma ("var olmak yetiyor, yetisme diye bir sey yok")
kapanir. Gelmezlerse elle research_advance listesi gerekir.

Sonrasi: OIR (1673), TIB (1676), MCH'nin Cin adimi (1682, toprak-once sirasi
ve "Qing Empire" + CHI bayragi), KOR (1685), CHG (1688).

## IRA VE MCH DOGRU GELDI - TEKNOLOJI TAHMINI TUTTU (31.07)

Yazar: "duzgun geldiler". Baslangic blogu olmadan doganlar tam olarak bu
ikisiydi (0 advance + harita korlugu). Simdi ikisi de komsulariyla ayni
seviyede geliyor.

MEKANIZMA KAPANDI: "yetisme" diye bir sey yok. Baslangic blogu olan tag
kampanya kurulurken ulke nesnesi olarak yaratiliyor ve topraksiz da olsa
dunyanin cag ilerlemesini yasiyor; sadece kimlik blogu olan tag toprak
verilene kadar HIC var olmuyor. research_advance listesine gerek kalmadi.

## KORE TIYATROSU OLU IDI - YAPISAL, ON DORDUN TEK ISTISNASI

Yazar Kore'nin cikmadigini bildirdi. Sebep kayit degil - KOR vanilla'da
kayitli (east_asia.txt:1; ilk grep'in kacirmasinin sebebi o satirdaki BOM,
bilinen tuzak).

GERCEK SEBEP: mr_return_korea'da SUPURME, lutuf modifieri ve bayrak
kontrolunun HEPSI `country_exists = c:KOR` blogunun icine gomulmustu. Diger
on uc tiyatroda supurme o kontrolun DISINDA, cunku change_location_owner'in
kayitli-ama-topraksiz bir tag'i YARATABILMESI gerekiyor. Faz 3 Kore'yi ya
VASSAL olarak ya da ilhak ederek aliyor; ilhak ettiyse country_exists yanlis
oluyor, supurme hic calismiyor, Kore hic geri gelmiyor - ve bayrak da iceride
oldugu icin her ay bosuna tekrar deniyor.

Duzeltildi: country_exists blogu artik SADECE cancel_subject cagrisini
sariyor (o gercekten ulkenin var olmasini istiyor), geri kalani disarida.

TARAMA YAPILDI: dosyadaki 22 supurmenin hepsi girinti derinligine gore
tarandi. Kore disinda ic ice olan bes tane var (middle_volga ve
mr_return_north'un dordu) ve BESI DE KASITLI: hepsi Rusya tiyatrosu, once
RUS-veya-MOS'u scope:mr_partition_heir'e cozuyor ve ancak biri hayattaysa
supuruyor. RUS'un kimlik blogu YOK, yani sifirdan yaratilmamasi gerekiyor.
Kore tek yanlisti.

## BUTUN TAKVIM CANLI OLARAK GECILDI (31.07, kapanis)

Yazar on dort tiyatronun tamamini yeni kampanyada izledi: "hepsi duzgun".
Kirim, Kazak, Pers, Mancurya, Cungarya, Tibet, Cin, Kore, Tarim - hepsi
kendi tarihinde, dogru din, dogru donem-hukumdari, arastirilmis advance'lar
ve harita bilgisiyle.

BUGUN KAPANAN SORULAR (hepsi oyunda olculdu, hicbiri cikarim degil):
  - bookmark init yagmuru (10 satir x 3 tag) -> baslangic bloklariyla sifir
  - "0 teknoloji + harita korlugu" -> sebep yetisme eksikligi degil, VAR
    OLMAMAKTI; baslangic blogu cozdu
  - Kirim ortodoks / Mancu tengri -> elle change_religion cozdu
  - rastgele hukumdarlar -> elle create_character + set_new_ruler, donem-dogru
    isimler ve hanedanlarla
  - "County of Kazakh" -> hukumet tipi baslangic blogundan geliyor
  - QNG diye bir tag yok -> kimlik blogu MCH'ye tasindi, Qing ilani en sona
    alindi (form_country hedef tag bossa re-tag ediyor)
  - Kore hic cikmiyordu -> supurme country_exists blogunun disina alindi
  - polygyny -> muslim_marriage (include'dan gelen yasa ulkeye uymayabilir)

HALA ACIK (hicbiri bu turun urunu degil):
  - Kalici Faz 1-3 odul modifierlari: strip mi, zayiflat mi, birak mi.
    Once ne verdiklerinin OLCULMESI lazim.
  - CHG'nin dini: tag'in kendi kaydi tengri, 1650'de Yarkand Muslumandi.
    Tasarim karari.
  - horde_unity_hit_at_ruler_death = -25 buyuklugu attested degil.
  - MR_l_english.yml:311'in kuresel rank_empire_horde override'i.
  - Dort kardes rebel-growth satiri (failure modifierlari).
  - Baskurt tiyatrosu yazarin karariyla kapali; Rusya ural_region ile aliyor.
  - MCH'de Kangxi 16 yasinda: regency gozlenmedi, ama gorulurse yas yukseltilir.

##### 31.07.2026 (IKINCI PAKET) CINGGISID BATI: BUHARA VE BADAHSAN #####

Yazar MR_geo_tarim'e badakhshan + transoxiana + khwarazm ekleyerek Kagan'in
elindeki bati topragini Cagatay'a vermisti. Amac dogruydu, ama yontemin iki
sorunu vardi.

## SORUN 1: ATOMUN ALTI TUKETICISI VAR, BIRI ISTEDI

MR_geo_tarim'e eklenen uc alan sessizce sunlari da degistirdi:
  - mr_dzungar_end_hold_tt (MR_scripted_triggers.txt:852) - BAGIMSIZ CUNGAR
    HANLIGI situation'inin bitis sarti. Artik bir Mogol bozkir hordasinin
    Tarim'in yani sira SEMERKANT, BUHARA, HIVE VE BADAHSAN'i da tutmasi
    gerekiyordu. O situation 1634-1650 arasi calisiyor; bu haliyle pratikte
    kazanilamaz.
  - mr_ulus_tarim_held (:1093) - partition'in kohezyon girdilerinden biri.
  - cb_MR_carve_the_ulus wargoal'unun allowed_locations'i (MR_wargoals.txt:198).
Bu, CLAUDE.md'nin "bir atom, alti tuketici" uyarisinin canli ornegi.

## SORUN 2: CAGATAY O TOPRAGIN TARIHSEL SAHIBI DEGIL

1688'de Semerkant ve Buhara Canogullari'nin (Toqay-Timurid Cengizli), Hive
Arabsahilerin. Yarkend Hanligi oralari hic tutmadi.

## ARASTIRMA SONUCU

Vanilla'da Buhara/Hive/Ozbek/Seybani diye TAG YOK - country_names_l_english
.yml'de sifir gecis, o topraga bakan formable da yok. Ama BADAHSAN VAR:
BKH canli bir vanilla tag'i, kendi kimlik blogu (east_asia.txt:3359) ve
baslangic blogu var, baskenti fayzabad ve tam badakhshan_area icinde.

## YAZILANLAR

- MR_geo_tarim tarim_area'ya geri dondu. Iki yeni atom: MR_geo_bukhara
  (transoxiana + khwarazm, ayni halefe ayni tarihte gittikleri icin tek atom)
  ve MR_geo_badakhshan.
- BUK bu modda KAYIT EDILDI (KAZ/IRA/MCH ile ayni yol): kimlik blogu
  (uzbek_culture / sunni, ham rgb renk cunku map_BUK yok), baslangic blogu
  (28_MR_countries.txt, IRA'nin sekli, baskent bukhara - khorasan_region,
  expl_mongols kapsiyor), ve loc anahtarlari BUK / BUK_ADJ.
- BKH'ye hicbir kayit gerekmedi.
- Iki yeni tiyatro efekti, digerlerinin ayni sekli: supurme + core +
  integration, sonra baskent, elle kimlik (din/kultur/hukumdar), 25 yillik
  lutuf, ve is-koruma bayragi.
  Hukumdarlar: BUK Subhan (Subhan Quli Han, 1681-1702), BKH Yarbeg
  (Mir Yar Beg, Yarid mirdomunun kurucusu).
  BUK hanedani borjigin (Canogullari Cuci soyundan Cengizli); BKH'ye hanedan
  YOK (Yarid mirleri Iskender soyu iddia ediyordu).
- BKH'DE BILEREK SAPMA: BKH'nin kimlik blogu mahayana diyor, ama o 1337
  Badahsan'i hakkinda bir ifade. 1694'te mirdom Musluman. sunni yazildi ve
  yorumda tek satirda geri alinabilecegi belirtildi.
- YAZARIN KARARI (tur icinde): iki tiyatro kendi kademesini almadi, NOGAY
  adimina bindirildi (momentum > 168 / 1664). Tarim/Cagatay en son kaliyor.

## SONUC: KAGAN'IN ELINDE ARTIK 213 LOKASYON

mongolia_region ve baska hicbir sey. Yedi rayli-yol koltugundan BIRI kaliyor,
Karakurum. Onceki 379 rakami ve "iki koltuk" ifadesi CLAUDE.md'de guncellendi.

## YAYIN ONCESI IKI KARAR (31.07)

### 1. FAZ 3 FAIL OLURSA HARITA KALICI OLARAK ALTERNATIF KALIYORDU

Yazarin sorusu: insan Pers/Osmanli oynarsa completion failsafe onun topragini
ALAMIYOR (bilerek, insan korumasi), yani Faz 3 fail ile kapanabilir. O zaman?

OLCULEN DURUM: mr_can_start_partition hem mr_railroad_complete istiyordu hem
mr_railroad_failed'i reddediyordu. Sonuc: Kagan Mogolistan + Mancurya + Tibet
+ Kuzey Cin + Sincan + Horasan'i elinde tutarak 1836'ya kadar oylece kaliyordu
ve hicbir sey geri alamiyordu. Bu, situation'in var olma amacinin tam tersi.
Ve nadir bir kose degil: insan korumasi BILEREK var, yani Pers/Anadolu/Ming/
Rusya oynayan her oyuncu bunu sadece hayatta kalarak uretebilir.

KOHEZYON ZATEN KALDIRIYOR: klozlar "tutmuyor VEYA geri verdi" seklinde, yani
hic alinmamis ulus da kayip sayiliyor. Agirliklar heartland 30, sibir 16,
kazak/cungar/tarim 12'ser, nogay 10, kirim 8. Bati bozkiri hic alinmamissa
skor 70'ten basliyor - 40 tabanininn cok ustunde. Pers/Mezopotamya/Anadolu
kohezyon girdisi DEGIL, yani insan Pers skoru bozmuyor.

DUZELTME: kapi artik "rayli yol kazandi mi" degil "dagilacak bir imparatorluk
var mi". mr_can_start_partition mr_railroad_complete yerine
mr_phase_two_complete istiyor, mr_railroad_failed yasagi kalkti, ve
mr_dominance.140 (partition'i 5 yil sonra kuran gecikmeli olay) Faz 3'un
BASARISIZLIK dalindan da atesleniyor.
  Faz 1 fail -> imparatorluk yok  -> partition yok (dogru)
  Faz 2 fail -> sadece bozkir     -> partition yok (kohezyon 30'da acilip
                                     ilk tikta biterdi)
  Faz 3 fail -> imparatorluk var  -> partition aciliyor, kohezyon ~70

### 2. OYUN KURALI ACIKLAMALARI SADECE AI'A GORE YAZILMISTI

Uc buff seceneginin aciklamasi da yalnizca AI durumunu tarif ediyordu; insan
oyuncuya hicbir sey soylemiyordu, ve "Historical (Balanced)" ismi insani
dogal olarak "dengeli olan bu" diye yonlendiriyordu.

OLCULDU: faz buff'larinda is_ai kapisi YOK (MR_mongol_imperial.txt:109-128) -
insan claimant da ayni modifierleri aliyor. is_ai kapisi sadece
MR_mongol_preparing_for_conquest'te var.

Uc aciklamaya da ikinci bir satir eklendi: Vanilla -> oyuncu icin onerilen,
Historical -> AI icin onerilen ama oyuncunun elinde zaten guclu, Terminator ->
oyuncunun elinde meydan okuma degil guc fantezisi.

## YAYIN ONCESI KILITLENME TARAMASI - DORT DUZELTME (31.07)

Ajan raporu: KALICI KILITLENME YOK. MR_mongol_preparing_for_conquest
(savas ilanini bloklayan modifier) uc fazin da her cikisinda, DALDAN ONCE
kaldiriliyor - yazarin en cok korktugu durum hicbir yoldan ulasilabilir degil.
Dort basarisizlik yolunun dordu de terminal kuruyor, yedi situation'in
yedisinde de tarih kacisi var, on alti mr_returned_* bayraginin hepsi eslesiyor.

Bulunan dort gercek hata duzeltildi:

1. ENDGAME'I KAZANAN KAGAN CEZALANDIRILIYORDU. on_ending daldan ONCE
   MR_unified_mongol_banner, MR_empire_fulfilled, MR_mongol_world_order ve
   MR_kurultai_mandate'i soküyordu - yani HAYATTA KALMA dalinda da. Dordunun
   de tooltip'inde "(Permanent.)" yaziyor. Ustelik KURAL KADEMESINE GORE
   ASIMETRIKTI: MR_mongol_historical_modifier_2 (Historical kademesinin Faz 1
   odulu, ve Historical varsayilan) listede yoktu, yani varsayilan kural
   odulunu koruyor Terminator kaybediyordu. Sokme artik COKUS dalinin icinde.

2. CUNGAR SITUATION'I KAGAN'IN USTUNE ACILIYORDU. mr_can_start_dzungar,
   Chahar ve Torghut'un tasidigi MGO/MGE dislama klozunu tasimiyordu. Kagan
   mongol kulturlu, Faz 3 boyunca steppe_horde tutuluyor, ve Faz 2 hedefi
   Sincan'i almasini SART kosuyor - yani ucu de esleşiyordu. Basarili her
   kampanyada 1634'te, Faz 3'un icinde, Cungar situation'i Kagan'i "Cungar"
   sayarak aciliyor, bitis sarti (dzungaria+tarim+zhetysu) zaten saglandigi
   icin neredeyse aninda tamamlaniyor ve MR_dzungar_legacy'yi rayli yol
   claimant'ina odüyordu. Ayni koruma eklendi.

3. KORUMASIZ c:MGE SCOPE ACICI (iki yerde). MGO-fallback yolunda (basarisiz
   ilan - mr_can_start_partition'in acikca tolere ettigi bir yol) her ay hata
   basiyordu, ve modifier MGO'lu Kagan'dan hic kalkmiyordu. every_country
   uzerinden iki tag'e cevrildi.

4. COKUS DALINDA ai_defensive GERI ALINMIYORDU. on_start her Kagan'a
   veriyordu, sadece hayatta kalma dali ai_aggressive'e donuyordu - yani
   cokmus bir kalinti oyunun sonuna kadar +12 ai_months_between_wars ve
   +0.25 carefulness tasiyordu. Cokus dalina da eklendi.

## KARAR BEKLEYENLER (yayini engellemez)

- Faz 1'in cb_MR_steppe_unification'i 25 YIL veriliyor ama faz 1420'ye kadar
  suruyor -> ~1393'te bitiyor. Faz 2 bu hatayi zaten duzeltmis (kendi yorumu
  soyluyor), Faz 1'de kalmis. AI'i etkilemez (PD deseninde declare CB'ye
  sahip olmayi gerektirmiyor) ama INSAN claimant 1393-1420 arasi elle savas
  ilan edemez.
- P2/P3 failsafe'leri claimant'ta at_war = no istiyor, bes yillik pencerede,
  ve rayli yol claimant'i 4-12 ayda bir savasa sokuyor. FAZ 1 BU KAPIYI
  BILEREK KALDIRMIS (kendi yorumu: "sonsuz savas dongusunde sikisan AI
  failsafe'i engeller"), P2/P3'te kalmis.
- Bes DHE olayi (mr_envoys.1/.2, mr_herds.1, mr_paiza.1) ana anahtari
  kontrol etmiyor. Biri bunun bilerek oldugunu yaziyor. Ama CLAUDE.md'nin
  "tum icerik NOT mr_railroad_off kontrol eder" ifadesi bu haliyle YANLIS -
  ya olaylar kapilanmali ya ifade duzeltilmeli.
- cb_MR_carve_the_ulus 80 yil veriliyor, situation'i ~60 yil asiyor - hayatta
  KALAN bir Kagan'a karsi bile.
- Great Partition, alti situation icinde hint_tag'i olmayan tek situation.

## KARAR BEKLEYEN HER SEY KAPATILDI + GAME RULE METIN SINIRI (31.07)

OLCULEN UI SINIRI (yazarin ekran goruntusu): game rule secenek aciklamalari
belli bir uzunluktan sonra "..." ile KESILIYOR. Olculen degerler (renk
etiketleri cikarilmis gorunur karakter):
    262 / 282 / 338  -> tam goruniyor
    435              -> KESILIYOR (Great Partition)
Guvenli butce: ~300 gorunur karakter, en fazla 3 parca. Bes aciklama yeniden
yazildi, hepsi artik 192-239 arasinda.

Great Partition aciklamasinin asil sorunu uzunluk degildi: "Fourteen theatres"
diyordu (artik on alti), "the Bashkirs"i sayiyordu (yazarin karariyla kapali),
ve Buhara ile Badahsan yoktu. On dort tiyatroluk liste metnin yarisiydi ve her
tiyatro eklendiginde bayatlayan kisimdi - liste tamamen cikarildi.

## DORT ACIK MADDE KAPATILDI

1. Faz 1'in cb_MR_steppe_unification'i 25 -> 130 YIL. Faz 1368-1420 arasi
   suruyor, 25 yillik verme ~1393'te bitiyordu. Faz 2 ayni hatayi kendinde
   bulup duzeltmis (kendi yorumu soyluyor), Faz 1'de kalmis. AI'i etkilemiyordu
   ama INSAN claimant fazin son 27 yilinda elle savas ilan edemiyordu.
2. P2 ve P3 failsafe'lerinden at_war = no KAPISI KALDIRILDI. Faz 1 bunu
   BILEREK kaldirmis ("sonsuz savas dongusunde sikisan AI failsafe'i
   engeller"), P2/P3 tutmus - ve rayli yolun kendisi claimant'i 4-12 ayda bir
   savasa sokuyor, pencere ise bes yil. Guvenlik agi tam ihtiyac aninda
   kapaliydi.
3. BES DHE OLAYI KAPILANDI (mr_envoys.1/.2, mr_herds.1, mr_paiza.1). Gerekce:
   ana anahtar KAPALIYKEN de MGO var olabiliyor, cunku vanilla kendi MGO_f
   formable'ini gonderiyor - yani modu kapatmis bir oyuncu bu olaylari
   goruyordu. CLAUDE.md'nin "tum icerik NOT mr_railroad_off kontrol eder"
   ifadesi artik gercekten dogru; o satir da duzeltildi.
4. cb_MR_carve_the_ulus SITUATION'LA BIRLIKTE OLUYOR. 80 yil veriliyordu,
   situation en gec 1720'de bitiyor - komsular partition cozuldukten sonra
   onlarca yil, hatta HAYATTA KALAN bir Kagan'a karsi bile CB tasiyordu.
   on_ending'in en ustunde, her iki daldan da once geri aliniyor
   (remove_casus_belli, vanilla coalition.txt:137 / religious_leagues.txt:151).
5. Great Partition'a hint eklendi - alti situation icinde hint'i olmayan tek
   situation oydu.

## DIS DUNYA ICIN IMMERSION KATMANI (31.07)

Yazarin sorusu: Anadolu'da, Avrupa'da, Hindistan'da oynayan bir oyuncu AI
Mogol'un yukselisini olaylarla gorebiliyor mu, tehlikenin geldigini hissediyor
mu?

## OLCUM: HAYIR, VE BIR DELIK VAR

Great Partition'in UC KATMANLI dinleyici kitlesi zaten var (Kagan / komsular /
uzak seyirciler). Ama imparatorlugun KURULDUGU uc fazda oyle bir katman yok:
  Faz 1 - butun dis olaylari mongolian_group + steppe_horde kapili, yani
          sadece diger bozkir hordalari
  Faz 2 - sadece alti hedef bolgede topragi olanlar
  Faz 3 - persia / pontic / russian_lands / song_china / western_reach
Yani Hindistan 1420-1650 arasi hicbir sey duymuyor, Anadolu ancak 1550'de tek
olay aliyor.

VE ASIL DELIK: mr_partition_is_spectator listesinde western_europe YOKTU.
Fransa/HRE/Iberya/Britanya oyuncusu modun HICBIR olayini, dagilmada bile,
hicbir zaman gormuyordu. north_africa da hicbir yerde yoktu - Memluk Misir'i
Ayn Calut'ta Mogollari YENEN taraf, ve modun hicbir kitlesinde degildi.
south_east_asia ise Faz 3'te vardi ama partition'da yoktu.

## TARIHSEL OLCUT (kim gercekten duydu)

Halka 1, bozkirin kendisi : mongol hordalari, north/central/east asia
Halka 2, istila edilenler : middle_east (Kose Dag 1243, Bagdat 1258),
                            south_asia (Delhi'ye akinlar), eastern_europe
                            (Legnica ve Mohi 1241), south_east_asia (Dai Viet,
                            Champa, Pagan 1287, Java 1293), north_africa
                            (Ayn Calut 1260)
Halka 3, sadece duyanlar  : western_europe - ordu gormediler, her seyi
                            duydular: II. Friedrich'in genelge mektuplari,
                            IX. Louis, 1241 konseyi, Carpini 1245, Rubruck
                            1253, Matthew Paris, ve 1238'de Gotland
                            balikcilarinin denize acilmamasi yuzunden coken
                            Baltik ringa piyasasi
HIC DUYMAYANLAR (bilerek disarida): Sahra alti Afrika, Amerika, Okyanusya

## YAZILANLAR

- mr_partition_is_spectator'a south_east_asia + north_africa + western_europe.
- mr_dominance_visible ve mr_partition_visible ayni sekilde genisletildi.
  Faz 1 ve 2 KASITLI OLARAK dar birakildi: Faz 1 bozkir hordalarinin kendi
  kavgasi, Pers'in batisinda kimse fark etmedi.
- YENI: mr_distant_observer trigger'i - dis halka. Kagan degil, komsusu degil,
  ve yalnizca tarihsel olarak duyan alt kitalar.
- YENI DOSYA in_game/events/situations/MR_distant_events.txt, namespace
  mr_distant, uc olay, haberin gercekte yayildigi sirayla tirmaniyor:
    .1  Faz 2 acilisi   - tuccar soylentisi ("rumour")
    .2  MGE ilani       - Mogol elcisi tabiiyet istiyor. Metin Guyuk Han'in
                          1246'da Papa IV. Innocentius'a verdigi cevaba yakin.
    .3  Faz 3 acilisi   - artik soylenti degil, sinir
  UCUNDE DE MODIFIER YOK. Bunlar haber, odul degil. Uzaktaki bir gucun bir
  imparatorlugun varligini ogrenmesi bir sey hak etmesi anlamina gelmiyor.

## HARNESS IKI HATAYI YAKALADI (ikisi de bilinen sinif)

- Yeni event dosyasinda BOM yoktu.
- Loc degerlerindeki \n gercek satir sonuna donusmustu, yani deger ikiye
  bolunmustu - CLAUDE.md'nin "loc degerleri TEK fiziksel satirda yasar"
  kuralinin tam ornegi. Harness "value opens a quote it never closes" ile
  yakaladi.

## DIS DUNYA KATMANI GENISLETILDI: DORT ISIMLI DARBE (31.07)

Ilk uc olay haberin SEKLIYDI (soylenti / elci / sinir). Bu dordu ICERIGI -
on ucuncu yuzyilin adiyla hatirladigi anlar, bu kampanya ayni yerlere
vardiginda atesleniyor. ZAMANA DEGIL KONUMA bagli: Bagdat'i hic almayan bir
kampanya Bagdat'i hic duymuyor.

  .5  Faz 2, Dadu alininca   - Mandate el degistiriyor (Zhongdu 1215,
                               Hanbalik 1264). Bozkir artik yagmalamiyor,
                               vergi topluyor.
  .4  Faz 3, Bagdat alininca - 1258. Hulagu sehri aliyor, son Abbasi halifesi
                               oldurulyor (halinin icinde, Mogol usulu kan
                               dokmeden), bes yuzyillik hilafet bir haftada
                               bitiyor.
  .6  Faz 3, Rus topraginda  - 1237-40: Ryazan, Vladimir, Kiev. Ardindan
      varlik olunca            1241'de Legnica ve Mohi. PRESENCE ile bagli,
                               fetih ile degil - o bir sinirin kaymasi degil,
                               yakilmis sehirler kampanyasiydi.
  .7  Faz 3 BASARIYLA         - PAX MONGOLICA. Yollar aciliyor.
      bitince

## .7 NEDEN VAR

Bilerek korku degil. Mogol yuzyili sadece terör degildi: Akdeniz'den Pasifik'e
tek yargi alani, tek gumruk, tek yol guvencesi - Rubruck 1254'te Karakurum'a,
Polo 1275'te Hanbalik'a, Ibn Battuta neredeyse tamamini gecti, ve Rabban Bar
Sauma'nin Yuan elciligi 1287'de Roma'ya ve Paris'e ulasti. Uzaktaki oyuncuyu
sadece korkutan bir mod tarihin yarisini anlatir - ve korku, tek nota
olmadiginda daha sert vurur.

HICBIRI MODIFIER VERMIYOR, .7 dahil. Yollarin acilmasi oyuncuya duyurulan bir
FIRSAT, verilen bir hediye degil.

Bayraklar: mr_beat_dadu_fired (Faz 2), mr_beat_baghdad_fired ve
mr_beat_rus_fired (Faz 3), ucu de kendi fazinin on_ended'inda temizleniyor.
