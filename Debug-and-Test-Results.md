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