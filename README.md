<div align="center">
<pre>
███████╗████████╗███████╗ ██████╗  █████╗ ███╗   ██╗ ██████╗ 
██╔════╝╚══██╔══╝██╔════╝██╔════╝ ██╔══██╗████╗  ██║██╔═══██╗
███████╗   ██║   █████╗  ██║  ███╗███████║██╔██╗ ██║██║   ██║
╚════██║   ██║   ██╔══╝  ██║   ██║██╔══██║██║╚██╗██║██║   ██║
███████║   ██║   ███████╗╚██████╔╝██║  ██║██║ ╚████║╚██████╔╝
╚══════╝   ╚═╝   ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ 
</pre>
</div>

# 🕵️ Steganography Detector

> Dijital görüntüler (JPG, PNG, BMP) içine gizlenmiş verileri istatistiksel analiz, EOF tespiti ve saf LSB manipülasyonu çıkarımı yöntemleriyle tespit eden forensik aracı.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://python.org)
[![Stdlib](https://img.shields.io/badge/Dep-Stdlib_Only-success)](./)
[![Status](https://img.shields.io/badge/Status-Active-success)](./)

---

## 📈 Proje Hakkında

Bu proje, bir siber güvenlik analisti veya forensik uzmanının dijital dosyalardaki gizli verileri (steganografi) tespit etmesi için geliştirilmiştir.

**Commit Geçmişi:**
| Commit | Açıklama |
|--------|----------|
| `chi square test and eof data detector` | İstatistiksel Shannon Entropisi hesabı ve IEND/FFD9 sonrası gizli veri tespiti. |
| `lsb byte extractor and hidden message string analyzer` | Sıkıştırılmamış dosyalar için Least Significant Bit (LSB) çıkarıcı. |
| `cli interface and forensic report generator` | Argparse CLI, demo modu, terminal renklendirme ve raporlama motoru. |

---

## 🧠 Mimari

```
main.py
  ├── detectors/eof_detector.py  ← JPG ve PNG dosya sonu (EOF) ihlallerini tespit eder
  ├── detectors/chi_square.py    ← Dosyanın byte dağılımını (Chi-Square) ve entropisini ölçer
  └── detectors/lsb_analyzer.py  ← BMP piksel dizilerindeki en önemsiz bitleri birleştirip okur
```

---

## ⚡ Kurulum

```bash
git clone https://github.com/fetihcakmak/steganography-detector.git
cd steganography-detector
python main.py --demo   # Ek bağımlılık gerekmez (yalnızca stdlib)
```

## 🚀 Kullanım

```bash
# Demo modu (simüle edilmiş analizler)
python main.py --demo

# Bir dosyayı taramak
python main.py --scan gizli_resim.jpg
python main.py --scan raw_image.bmp
```

## 🖥️ Örnek Çıktı

```
1. Sahte bir JPG EOF analizi simüle ediliyor...
  [!] UYARI: FF D9'dan sonra 450 bayt gizli veri tespit edildi!
  Önizleme: 'Secret message goes here...'

2. İstatistiksel Analiz (Chi-Square) simüle ediliyor...
  Shannon Entropisi: 7.98 (Çok yüksek, şifrelenmiş veri şüphesi)
  Ortalama Chi-Square: 145.2 (Uniform dağılıma yakın - LSB stego şüphesi)

3. BMP LSB Analizi simüle ediliyor...
  [!] Olası metin bulundu: 'flag{st3g0_1s_aw3s0m3}'
```

## ⚠️ Sınırlamalar

Bu araç yalnızca JPG/PNG EOF-sonrası veri ve sıkıştırılmamış BMP'lerdeki LSB manipülasyonunu tespit eder; F5, OutGuess gibi sofistike/şifreli steganografi algoritmalarını veya sıkıştırılmış PNG'lerdeki gerçek LSB gömme işlemini kapsamaz. Adli/forensik bir vakada kesin sonuç için uzman araçlarla (StegExpose, zsteg, binwalk vb.) çapraz doğrulama yapılmalıdır.

## 📄 Lisans

Bu depo şu an bir lisans dosyası içermiyor. Kullanım koşulları için proje sahibiyle iletişime geçin.

---

*Fetih Çakmak — Cybersecurity Portfolio*
