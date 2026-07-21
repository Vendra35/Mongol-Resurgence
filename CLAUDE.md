# CLAUDE.md — Mongol Resurgence (EU5 Mod)

## Proje
EU5 için "Mongol Resurgence" mod'u. Prussian Destiny (Reference EU5 vanilla and Prussian Destiny/The Prussian Destiny/)
mimarisini temel alıyor. Referans klasörlerine (Reference EU5 vanilla and Prussian Destiny/) ASLA yazma, sadece oku. Sadece kendi mod klasörüne (Mongol Resurgence/) yaz.

## Kesin kurallar
- Tag'ler her zaman 3 harfli. 4 harfli tag önerme/kullanma.
- Situation field'larını UYDURMA. Sadece Reference EU5 vanilla and Prussian Destiny/ içinde
  gerçekten var olan field'ları kullan. Emin değilsen bana sor, tahmin etme.
- `exists = c:TAG` değil `country_exists = c:TAG`.
- Location isimlerini vanilla dosyasından (Reference EU5 vanilla and Prussian Destiny/Europa Universalis V) teyit etmeden kullanma.
- GFX/GUI referanslarını situation dosyasının içine gömme, ayrı .gui dosyasına çıkar.
- Başka Paradox oyunlarının (Victoria 3, CK3, HOI4, Stellaris, EU4) syntax'ını EU5'e taşıma/pattern-match yapma. EU5'in kendi syntax'ı farklı olabilir, her zaman bu projedeki (Reference EU5 vanilla and Prussian Destiny/) gerçek örneklerden doğrula.

## Çalışma akışı
- Hiçbir şeyi ben onaylamadan dosyaya yazma.
- Mod tasarımının tam detayları (tag tablosu, failsafe sistemi, situation timeline) için Mongol Resurgence/docs/MOD-DESIGN-IDEA.md'ye bak — her göreve başlamadan önce oku.
- Bulguları kategorize et: kesin hata / şüpheli / netleştirilmesi gereken.
- Emin olmadığın her tag/isim/field için vanilla dosyada ara; hâlâ emin.
  değilsen `https://eu5.paradoxwikis.com/Europa_Universalis_5_Wiki`'dan kontrol et veya Mongol Resurgence/docs/ altındaki wiki PDF'lerineden kontrol et, tahmin etme.

## Dil
Tüm kod, localisation, yorum satırları İngilizce.