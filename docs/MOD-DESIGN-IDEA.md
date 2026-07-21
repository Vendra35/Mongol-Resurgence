## 2. Mod Tasarımı — Ne Yapmaya Çalışıyoruz

### Konsept
"1368'de Yuan Hanedanı Çin'den kovulduğunda (Kuzey Yuan), Moğol boyları gerçekten birleşseydi ve batıya doğru yeni bir fetih dalgası başlatsaydı?" sorusuna cevap veren, tarihsel zemine bağlı bir alternatif tarih senaryosu.

### 3 Situation (İngilizce isimlerle)
1. **"The Northern Yuan Resurgence"** (~1368-1420) — Moğolistan'ın birleşmesi.
2. **"The Pax Mongolica"** (~1420-1550) — İpek Yolu'na hakimiyet, Ming ile hegemonya savaşı.
3. **"The Silk Empire"** (~1550-1650) — Rusya'ya karşı batıya ilerleme, final formable.

### Tag'ler — DİKKAT: Bunlar wiki'den bulundu ama tekrar teyit gerekiyor (çelişkili bilgi geçmişi var)
| Konsept | Tag (iddia edilen) | Durum |
|---------|---------------------|-------|
| Yuan | CHI (ayrıca YUA diye ayrı bir versiyon da olabilir, netleştir) | Belirsiz, teyit et |
| Chagatai | CHG | Wiki'den teyitli deniyor |
| Ilkhanate | Tek tag değil — HLG (Hüleguids) + İlhanan diye bir International Organization | Wiki'den teyitli deniyor |
| Golden Horde (Jochi) | GLH | Teyitli |
| Oirat | OIR | Teyitli |
| **Mongolia** (Situation 1'in doğuş hedefi) | **MGO** — tier 3 formable | ⚠️ Bir noktada "MGE" ile karıştırıldı, sonra düzeltildi. `00_formable_countries.txt` için önceki AI'lar (DeepSeek/Cline) oluşturmuştu bu dosyayı Mongol modum için ama yapmamıza/oluşturmamıza gerek yok çünkü zaten MGO_f Mongolia formable'ı zaten vanillada oyun dosyalarında var üstüne bi daha yazmamıza gerek yok. Prussian Destiny modunda `00_formable_countries.txt` klasörü var çünkü NGC yani North German Confederation vanillada yok ondan yeni oluşturmuştum o modumda. |
| **Mongol Empire** (Situation 3'ün final formable'ı) | **MGE** — tier 4 formable. | ⚠️ Bir noktada bu "Moghulistan" ile karıştırıldı. Sen bağımsız olarak tekrar doğrula. |

**Bu tag tablosunu ilk iş olarak, sıfırdan, kendi bağımsız araştırmanla doğrula.** Önceki AI'ların (DeepSeek/Cline) birbiriyle çelişen iddiaları var, onlara güvenme.

### Mimari Prensip: Dinamik Doğuş (Sabit Tag Yok)
1337-1368 arası Asya bozkırı çok kaotik olduğu için (Brandenburg/Teutonic Order'ın HRE içinde güvenle hayatta kalmasının aksine), Situation 1'in aktörü **sabit bir tag'e değil, dinamik bir trigger'a** bağlı:

- Vanilla'daki **Timur emergence event'ini** (`flavor_tim.8`, Çağatay'dan Timur'u "doğuran" event) referans al.
- Trigger mantığı: "Kim Karakurum'a sahipse + steppe horde hükümetindeyse + Moğol kültür grubundaysa" → o ülke `create_country_from_cores_in_our_locations` ile MGO'ya dönüşüyor ya da direk dönüştüremezsek `form_country = formable_country:MGO_f` çalıştırılıyor (Prussian Destiny'deki `form_country = formable_country:PRU_f` pattern'inin aynısı).

### İki Katmanlı Failsafe Sistemi
**(a) Doğuş failsafe'i — sadece Situation 1'de:** Eğer ~1370'e kadar (1368'den kısa süre sonra) hiçbir ülke organik olarak trigger şartlarını sağlamazsa, bölgedeki en uygun adayı (en çok Moğolistan/Gobi bölgesi toprağına sahip, steppe horde + Moğol kültürlü ülke) zorla MGO'ya dönüştür.

**(b) Tamamlama failsafe'i — her 3 situation'da da:** Prussian Destiny'deki `PD_brandenburg_rise_auto_conquest_yes/PD_the_prussian_ascension_auto_conquest_yes` mantığının **aynısı**: her situation'ın bitiş tarihinden **5 yıl önce**, hedefler sağlanmamışsa AI'a bedava toprak/vassal/savaş zaferi vererek o son 5 yılda zorla tamamlat. (Prusya modunda bu 1495/1632 gibi tarihlerde uygulanmıştı, aynı 5 yıllık buffer mantığını kullan.)

### Dil Kuralı
**Modun tamamı İngilizce.** Situation isimleri, event başlıkları/açıklamaları, decision isimleri, localisation metinleri, kod içi yorumlar dahil her şey İngilizce. Namespace: `mongol_resurgence`, Prussian Destiny'deki `the_prussian_destiny`/`PD` pattern'ine paralel bir isimlendirme kullan.