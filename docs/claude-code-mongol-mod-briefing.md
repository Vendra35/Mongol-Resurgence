# Claude Code Devir Teslim: Mongol Resurgence (Railroad) Mod Denetimi

> Bu dosyayı olduğu gibi VS Code'da Claude Code'a yapıştır. Workspace'e önce şunları eklemiş olmalısın: (1) EU5 vanilla oyun dosyaları, (2) Prussian Destiny mod klasörün, (3) EU5 Wiki'den PDF'lediğin modding guide'ları (Mod Structure, Situation modding, Event modding vb.), (4) bu dosya.

---

## 1. Rolün ve Genel Durum

Ben Europa Universalis V için "Mongol Resurgence" (bazen "Mongol Railroad" olarak da anılıyor) adında bir mod geliştiriyorum. Bu mod, **Prussian Destiny** adlı (workspace'te duran, çalışan, test edilmiş) başka bir modumun mimarisini örnek alıyor.

**Önemli:** Bu moda ait kod şu ana kadar **Cline + DeepSeek V4 Pro Thinking** ile yazıldı, AMA çok sayıda hata içeriyordu ve hâlâ tam güvenilir değil. Şimdiye kadar bulunan/düzeltilen hata kategorileri:

- Uydurma 4 harfli tag'ler (YUAN, CHAG, ILKH, MOG, TRSX gibi) — EU5'te tag'ler kesinlikle 3 harfli.
- Vanilla'da olmayan situation field'ları uydurulmuş: `title`, `description`, `trigger` (situation seviyesinde), `targets`, `progress`, `completion`, `abort`, `actions`, `left_panel_content`, `ai_weight`, `sort_order`. Bunlar Prussian Destiny'nin gerçek kodunda YOK.
- `set_variable = { name = ... name = ... }` gibi eksik/yanlış parametre kullanımı (ikinci parametre `value` olmalı).
- `exists = c:TAG` yerine `country_exists = c:TAG` kullanılması gerekiyor.
- Yanlış location isimleri (`location:beijing` yerine `location:zhongdu`, `location:sarai` yerine `location:sarai_al_jadid` gibi).
- GFX/GUI referanslarının situation dosyasının içine gömülmesi (ayrı `.gui` dosyalarına çıkarılması gerekiyor).
- Metadata formatı (`version` yerine `supported_game_version`) gibi başka format hataları da bulundu.
- `owns` yerine `controls` kullanımına geçildi ama bu değişikliğin (ownership vs. military control anlam farkı) doğru olup olmadığı **teyit edilmedi** — bunu sen kontrol et.

**Senin görevin:** Bu koda körü körüne güvenme. Her satırı, özellikle syntax'ı ve tag/isim referanslarını, vanilla dosyalarla ve PDF'lediğim wiki guide'larıyla karşılaştırarak denetle. Tahmin etme — emin olmadığın her şeyi vanilla dosyalarında ara, gerekirse `https://eu5.paradoxwikis.com/Modding` `https://eu5.paradoxwikis.com/Europa_Universalis_5_Wiki` `https://eu5.paradoxwikis.com/Category:Country_lists` ve ilgili diğer wiki sayfalarını (WebSearch/WebFetch araçlarınla) kontrol et.

---

## 2. Nasıl İlerlemeni İstiyorum

1. **Önce hiçbir şeyi değiştirme.** Workspace'teki mevcut Mongol mod dosyalarını, Prussian Destiny'yi ve vanilla referans dosyalarını (situations, formable_countries, events, setup/countries) oku.
2. **Tag tablosunu bağımsız olarak doğrula** (yukarıdaki tablo) — Bence önce `https://eu5.paradoxwikis.com/Category:Country_lists` wikisinden veya (WebFetch ile) taglara bak çünkü önce vanilla dosyalarından bulmak zor olabilir. Eğer wikiden bulamazsan sonra EU5 vanilla dosyalarından `Reference EU5 vanilla and Prussian Destiny/Europa Universalis V` bulmaya çalış.
3. **Mevcut kodda yukarıda listelenen hata kategorilerinin gerçekten düzeltilip düzeltilmediğini tek tek denetle.** Grep/metin taramasına güvenme — mantıksal olarak doğru mu diye düşün (örneğin `owns`→`controls` değişikliğinin bizim senaryomuz için doğru olup olmadığını değerlendir).
4. **Bulduğun her sorunu bana raporla, ben onaylamadan dosyalara yazma.** Büyük bir "hepsini düzelttim" raporu yerine, kategorize edilmiş bir bulgular listesi istiyorum: kesin hatalar / şüpheli noktalar / netleştirilmesi gerekenler.
5. Denetim bittikten ve ben onayladıktan sonra, düzeltmelere başla — dosya dosya, her adımda ne yaptığını özetleyerek ilerle, hepsini tek seferde sessizce yapma.

Hazır olduğunda, önce sadece **tag doğrulama** ve **hata kategorisi denetimi** sonuçlarını raporla — kod yazmaya henüz başlama.
