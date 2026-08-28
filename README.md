# 📺 PHTV - Localhost Smart TV & Yönlendirme Sistemi

PHTV, Akıllı Televizyonlar (Smart TV), bilgisayarlar ve mobil cihazlar için tasarlanmış; ulusal ücretsiz canlı TV kanallarını izlemenizi sağlayan, aynı zamanda tek tıkla özel bir adrese yönlendirme yapabilen hafif, bağımlılıksız bir yerel medya sunucusudur.

Türksat 5B uydusu veya harici TV kutusu olmayan cihazlarda, TV web tarayıcısı üzerinden kesintisiz ve kumanda uyumlu bir TV deneyimi sunar.
ooof of Beşiktaş ne vardı adam gibi bir kanalda versen maçı iki saat uğraştırdın TV100 kurulmuyor televizyona diye oluşturdum tüm bu projeyi
---

## ✨ Özellikler

- 📺 **Canlı TV Oynatıcısı (HLS.js)**: TV100, TRT 1, ATV, Show TV, Kanal D, Star TV, TV8, HaberTürk, NTV, CNN Türk, Sözcü TV, Halk TV gibi 20'den fazla ücretsiz ulusal kanal.
- 🔗 **Tek Tıkla Yönlendirme**: `hedef.txt` belgesine yazdığınız herhangi bir web sitesine (YouTube, Netflix, özel web siteleri vb.) TV'nizden anında yönlendirme.
- 🎮 **Smart TV & Kumanda Uyumlu (10-Foot UI)**: TV kumandasının ok tuşları (D-Pad), Enter ve Geri tuşları ile tam entegre çalışan büyük arayüz.
- ⚡ **Sıfır Bağımlılık (Zero-Dependency)**: Harici hiçbir Python paketi (`pip install`) gerektirmez. Standart Python kütüphaneleri ile çalışır.
- 🌐 **Yerel Ağ Erişimi**: Aynı Wi-Fi/Ağa bağlı TV, Telefon, Tablet veya PC üzerinden sorunsuz erişim.

---

## 📁 Proje Yapısı

```text
phtv/
├── server.py             # Python HTTP web sunucusu (Port 9901)
├── start_server.bat       # Windows için tek tıkla başlatıcı script
├── hedef.txt              # Yönlendir butonu için hedef URL
├── channels.json          # TV kanalları ve HLS yayın adresleri kataloğu
└── static/
    ├── index.html         # Ana sayfa (Yönlendir & Canlı TV butonları)
    └── tv.html            # HLS.js tam ekran canlı TV player arayüzü
```

---

## 🚀 Kurulum ve Çalıştırma

### Gereksinimler
- **Python 3.x** (Sisteminizde Python yüklü olması yeterlidir).

### Çalıştırma

1. Projeyi indirin veya klonlayın:
   ```bash
   git clone https://github.com/PratikHackTR/freeiptvandrouterforsmartTV.git
   cd phtv
   ```

2. Sunucuyu başlatın:
   - **Windows**: `start_server.bat` dosyasına çift tıklayın.
   - **Terminal / Komut Satırı**:
     ```bash
     python server.py
     ```

3. Ekranınızda sunucunun çalıştığı adresler gösterilecektir:
   - **Bilgisayardan erişim**: `http://localhost:9901`
   - **Smart TV / Ağdaki cihazlardan erişim**: `http://<BILGISAYAR_IP_ADRESI>:9901` (Örn: `http://192.168.1.105:9901`)

---

## ⚙️ Kullanım ve Özelleştirme

### 1. Yönlendirme Adresini Değiştirme
[hedef.txt](hedef.txt) dosyasını açıp içerisine TV'nizden gitmek istediğiniz web sitesinin URL'sini yazıp kaydedin:
```text
https://www.youtube.com
```
TV arayüzünden **Yönlendir** butonuna bastığınızda tarayıcınız doğrudan bu adrese gidecektir.

### 2. Kanal Ekleme / Düzenleme
[channels.json](channels.json) dosyasını açarak yeni canlı TV kanalları veya özel `.m3u8` akış adresleri ekleyebilirsiniz:
```json
{
  "id": "kanal-id",
  "name": "Kanal Adı",
  "category": "Kategori",
  "logo": "https://logo-url-adresi.png",
  "url": "https://yayin-adresi.m3u8"
}
```

---

## 🎮 TV Kumandası Kısayolları

- **Yön Tuşları (Ok Tuşları)**: Butonlar ve kanal listesi arasında gezinme.
- **Enter / OK**: Seçili butona tıklama veya kanalı açma.
- **Sağ / Sol Tuşları**: Canlı TV oynatıcısında kanal listesini açma/kapatma.
- **ESC / Backspace (Geri Tuşu)**: Ana sayfaya veya kanal listesine dönme.

---

## ⚠️ Sorumluluk Reddi (Disclaimer)

Bu proje yalnızca kişisel kullanım amacıyla geliştirilmiş açık kaynaklı bir medya oynatıcı arayüzüdür. Proje içerisinde sunulan kanal yayın adresleri internet üzerinde halka açık olarak paylaşılan resmi HLS/M3U8 yayın bağlantılarıdır. PHTV hiçbir video içeriği barındırmaz veya depolamaz.

Ayrıca hedef.txt dosyasına bazı kaçak yayın linkleri bırakıp uygulama içerisinden yönlendirme yapmak kesinlikle tavsiye edilmez ve yasadışıdır kaçak yayına karşı olduğumun altını çizerim yayınları lütfen TV'de uydunuzun çekmediği veya frekans desteği bulunmayan kanalların halka açık olarak paylaşılan resmi HLS/M3U8 yayın bağlantılarını kullanarak izleyin
---
