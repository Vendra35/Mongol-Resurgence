#### 1. Variables set but never used: MR_dominance_events.txt in game error logs

- Variable `mr_history_babur` is set but never used.
- Variable `mr_history_ilkhanate_fragmanted` is set but never used.
- Variable `mr_history_oirat_challenge` is set but never used.
- Variable `mr_history_delhi_sacked` is set but never used.
- Variable `mr_history_chagatai_schism` is set but never used.
- Variable `mr_history_yuan_decline` is set but never used.
- Variable `mr_history_tokhtamysh` is set but never used.

Bu variableları set etmişsin ama hiç kullanmamışsın ya kaldıralım ya da kullanalım ama nasıl kullanıcan zor gibi belki event yollayarak kullanabilirsin: Mesela delhi sacked olur eğer bizim main mongol ülkesi bi situationı tamamlayınca  veya delhiyle savaşırsa o event hem bize gelir delhiyi sackedladık diye, hem de delhiye veya delhi toprağını elinde kim tutuyorsa ona gider bizi sacked yaptılar gibi. Ama sen anladın yani eğer tarihsel güzel akıcı bir hikaye kurabilceksen variableları tut ve uygula eğer kurulmaz dersen komple kaldırabiliriz mantığı bu şekilde boşu boşuna kodlar kalmasın orda error verip oyunu çöktürmüyor ama boşuna duruyor diye in game logda uyarı verdi.

#### 2. Army balance support for AI support Events:

Bunu eklememişsin asker basma eventine ve manpower basma bina eventini ben biraz steppe advancelerine göre biraz düzenledim bu şekilde:

MR_dominance_event.txt içine ki 996 ve 995. eventler için kodlar düzenlendi ve dğeiştirildi cost multipler reasonvs eklendi ve dediğim gibi steppeye özel advance binaları kurultai gibi manpower binası ve Steppe Horse Archers gibi unit birimler eklendi ordu basma(AI support) kısmı için.

#### 3. mr_dominance.997 gibi AI railroad: declare the unification war eventlerindeki problem:

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

#### 4. MR_mongol_preparing_for_conquest modifierının yanlış kullanılması ve anlaşılmaması:

Sen sanırım bu modifierı daha mantığın anlamamışsın neden yaptığımızı hemen anlatayım:
- Bu modifierın amacı her farklı situation başladığında o situation sahibi ülkeye mesela benim Prussian Destiny modumda bu perparing_for_conquest modifierını Prussiaya veya Brandenburga veriyorduk çünkü AI için bu tamamen. Situation başladığı zaman AI kendi kafasına göre savaş açmasını engelleyelim ki bizim savaş açma komutumuz railroad kodumuz (AI RAILROAD: FIND A TARGET) ile savaş açılsın. AI kendisi savaş açıp kendini bitirmesin hem de o railroad kodumuzu engellemesin (çünkü at_war = no koyduk) çalıştırsın bizim istediğimiz kişilere saldırsın. Ana mantığı bu ve önemli!

#### 5. Modu test edicem o nedenle tam olarak situationlarda ve kodda ne oluyor anlatır mısın:

Kodu güzel bir plan ile test etmem gerek yani mesela situationlar ne zaman oluyor situationlarda ne olacak veya olması planlandı onları sıra sıra düzgün test edeyim birbiriyle bağlantılı şeyleri birlikte test edeyim ki karışmasın. Kod testi yaparken çok kod var çünkü bana güzel bir modu test etme rehberi lazım. "Şunlara bak şurda şu olması gerekiyor bak oluyor mu falan gibi" rehber lazım dediğimi anladın umarım. Daha iyi bir fikrin varsa o şekilde de yapabiliriz yeter ki modu komple düzgün bir şekilde test edebileyim.

#### 6. Kullanılmayan Game Rules Locları ve Ayrı Localization Dosyaları:

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

#### 8. MR_on_actions.txt dosyasındaki invalid right side hatası:

- Böyle bir hata geldi bu sanırım on_actionda biz OR = {this = c:MGO this = c:MGE} böyle yazmışız önceden tag = MGO yerine this:MGO şeklinde yazdığımız için olmuş bu hatu sanırım. Baktım Prussian Destinyde de öyle yapmamışız tag = BRA olarak yapmışız on_actionstaki kodlarımızda o sebeple bu hatayı düzelttim ben kendim ama sen yinede bir kontrol et. on_action.txt dışındaki dosyalarda this = c:MGO kullanı mı error logda hata vermiyor gözüküyor bilgin olsun. Aynı zamanda Mongol_resurgence situationı başladığı an direk bu hatalarıda verdi oyun çökmüyor tabi ki çalışıyor ama debug.logunda gördüm oyun içinde ki:

## Gelmiş olan hata ilk hata benim düzelttiğim fixledim sadece bilgi al diye attım:
[game] [error] [jomini_script_system.cpp:252] Script system error! Error: Invalid right side during comparison 'c'
Script location:
common/on_action/MR_on_actions.txt:38

## Gelmiş olan 2. hata ben fixleyemedim sana bıraktım:
[game] [error] [jomini_script_system.cpp:252] Script system error! Error: Invalid right side during comparison 'c'
Script location:
common/situations/MR_mongol_resurgence.txt:592

- Acaba o ülke var olmadığı için olabilir mi çünkü c:MGO diye arıyor bulamıyor biz MGO yu 1368de situation başlıyor ama hala mevcut değil. Biz mongol_resurgence situationun da 1375e kadar kimse claim almadıysa ondan sonra oluşturuyoruz MGO yu çıkartıyoruz ama claim alma nasıl oluyor tam anlamadım yani bağlantı da bir sıkıntı var mı yoksa doğru mu onuda bir teyit eder misin. Çünkü bu 2. hatadan 100bin tane falan atıyor logda situation başladığı için her ay bakmaya çalışıyor ve sürekli spamlıyor bu hatayı logda.
- Edit: Evet ülke var olmadığı içinmiş 1375 te MGO çıkınca error logları gitti ama ondan önce dediğim gibi çok fazla hata atıyor ona bir çözüm bulmak lazım.

#### 9. Modifierlar ve Karakter yaratılması hakkında 

- 1. Mongol Horde yani MGO 1375te çıktıktan sonra ona giden modifierları gördüm mesela mongol warrior spirit(terminator) diye bir modifier gitmiş ama terminator game rule'u yok ki bizde mesela neye göre neden gitti bu? Ayrıca bu modifierlar doğru zamanda kaldırılmıyordu oyun sonuna kadar kalıyor onlarıda Prussian Destinydeki gibi situation bitince kaldırmamız gerekiyor ayrıca MR_mongol_preparing_for_conquest: "Mongol War Preparations" modifierın locları STATIC_MODIFIER_NAME_MR_mongol_preparing_for_conquest olarak gözüküyor Mongol War Preparations olarak gözükmesi gerekirken, yani loclar çalışmamış neden bilmiyorum ama mongol warrior spirit(terminator) ün locları çalışıyor. Başka böyle sorunlu modifierda varsa düzelt lütfen.

- 2. Birde şu özelliği eklesek çok güzel olur vanilla timurdaki gibi: Vanilla timur da timur ülkesi spawnlandığı zaman eventle timur ülkenin başına geliyor ve emir timurda yani sadece ülkeye değil karakterin kendisine de bufflar geliyor Conquerer's Vitaly ismin de Character life expentacy buffu ve The Scourge From Central Asia ismin de diye baya detaylı bir buff alıyor bizde bu tarz bir şey yapabiliriz ve bizim mgo ülkemiz çıktığı anda Borjigin hanedanından mı sence bir karakter oluşturmak güzel olur mu Borjigin den bir karakter ya da bizim modumuza göre tarihsel en iyi hangisi ne şekilde olursa öyle yapalım.

#### 10. Mongol Imperial situation GUI sindeki sorunlar

- 1. GUI de karakter portresi böyle simsiyah boş gözüküyor sanki karakter yok gibi ilk situationda yani mongol resurgence de doğru gözüküyorda ama bu 2. mongol imperial situationında bozuk gözüküyor. Loglara baktım loglarda böyle diyor yine çok fazla bu hataları spawnlıyor logda bide:

[cw] [error] [pdx_data_localize_helper.cpp:290] FetchData failed for 'Character.Get Court Country.GetName'
[cw] [error] [pdx_gui_localize.cpp:140] PdxDataFetchLocalized Data failed for 'EVENT_CHARACTER_FOREIGN'
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Character' for 'Character.GetRoleName'
[cw] [error] [pdx_gui_data_manager.cpp:233] FetchData failed for 'EqualTo_string(Character.GetRoleName, "')' - gui/shared/cards.gui:1073
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Character' for 'Character.GetCourt Country.GetName' [cw] [error] [pdx_data_localize_helper.cpp:290] FetchData failed for 'Character.GetCourt Country.GetName'
[cw] [error] [pdx_gui_localize.cpp:140] PdxDataFetchLocalized Data failed for 'EVENT_CHARACTER_FOREIGN_NO_ROLE'
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Character' for 'Character.GetCourt Country'
[cw] [error] [pdx_data_callstack.cpp:17] No context supplied (Use SetDataContext), wanted context of type 'Character' for 'Character.GetNameToFit('(int32)22', '(bool)yes')' 
[cw] [error] [pdx_data_localize_helper.cpp:290] FetchData failed for 'Character.GetNameToFit('(int32)22', '(bool)yes')'
[cw] [error] [pdx_gui_localize.cpp:140] PdxDataFetch Localized Data failed for '[Character.GetNameToFit('(int32)22', '(bool)yes')]'
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

- 2. Aynı zamanda Imperial expansion progress sekmesi boş gözüküyor hiç bir şey gözükmüyor. Aynı zamanda o sekme neden vardı bide bilmiyorum açıklarsan iyi olur.
- 3. mongol imperial situationında hedefler olarak khorasan region ve north_china regionları kırmızı çizgi olarak situation haritasında gözüküyor ama khorasan ile arada boşluk kalıyor o sebeple o aradaki xinjiang_region diye bir region var onuda ekleyelim bu situation için birleşik olsun hedefler yoksa khorasan_reigon uzakta kalıyor. Ayrıca şunu fark ettim end requirementları mesela sadece dadu ve samarkandı elinde tutsun diyor ama bence tüm o kırmızı ile çizilen regionları alana kadar davem etsin daha iyi olmaz mı sınırlar daha iyi gözükür Prussian Destinyde de hep öyle yapmıştım area ve regionları hedef olarak koyuyorduk. Bu mantığı diğer situationlar içindeöyle değiştirebilirsen çok sevinirim region isimlerini bilemezsen ben de verebilirim ya da palceholder yap ben kendim yazarım çok sorun değil o.




#### FİNAL NOT: Event şuan gözüme çarpan ve oyun içinde debug logda ortaya çıkan hatalar bu şekildeydi bunları düzelttikten sonra tekrar bizim ana CLAUDE.md ve diğer tüm md dosyalarımızı bunlarla ilgili bir içerik rehber falan varsa onlarıda güncelleyip elden geçirir msiin detaylı bir şekilde. MD dosyalarımız güncel kalsın ki ilerde bu modu kullanıcaksam veya başka sıfırdan bir mod yapacaksam işimize yarasın.