#!/usr/bin/env python3
"""
Steganography Detector - Ana CLI Modülü
Kullanım: python main.py --scan image.jpg
"""
import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from detectors.eof_detector import detect_eof_data
from detectors.chi_square import analyze_anomalies
from detectors.lsb_analyzer import analyze_bmp_lsb

# --- ANSI Renk Kodları ---
RED    = "\033[91m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
CYAN   = "\033[96m"
MAGENTA= "\033[95m"
BOLD   = "\033[1m"
RESET  = "\033[0m"
GRAY   = "\033[90m"

BANNER = f"""{BOLD}{GREEN}
███████╗████████╗███████╗ ██████╗  █████╗ ███╗   ██╗ ██████╗ 
██╔════╝╚══██╔══╝██╔════╝██╔════╝ ██╔══██╗████╗  ██║██╔═══██╗
███████╗   ██║   █████╗  ██║  ███╗███████║██╔██╗ ██║██║   ██║
╚════██║   ██║   ██╔══╝  ██║   ██║██╔══██║██║╚██╗██║██║   ██║
███████║   ██║   ███████╗╚██████╔╝██║  ██║██║ ╚████║╚██████╔╝
╚══════╝   ╚═╝   ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ 
        STEGANOGRAPHY DETECTOR v1.0{RESET}
"""

def print_section(title: str):
    print(f"\n{BOLD}{CYAN}[*] {title}{RESET}")

def main():
    parser = argparse.ArgumentParser(
        description='Steganography Detector - Resimlerde gizli veri tespiti'
    )
    parser.add_argument('--scan', help='Taranacak dosyanın yolu')
    parser.add_argument('--demo', action='store_true', help='Demo modunda çalıştır')
    
    args = parser.parse_args()
    print(BANNER)
    
    if not (args.scan or args.demo):
        print(f"{YELLOW}Kullanım örnekleri:{RESET}")
        print("  python main.py --demo")
        print("  python main.py --scan image.png")
        sys.exit(0)

    if args.demo:
        print_section("DEMO MODU AKTİF")
        print(f"{GRAY}1. Sahte bir JPG EOF analizi simüle ediliyor...{RESET}")
        print(f"  {RED}[!] UYARI: FF D9'dan sonra 450 bayt gizli veri tespit edildi!{RESET}")
        print(f"  {YELLOW}Önizleme: 'Secret message goes here...'{RESET}\n")
        
        print(f"{GRAY}2. İstatistiksel Analiz (Chi-Square) simüle ediliyor...{RESET}")
        print(f"  {CYAN}Shannon Entropisi:{RESET} 7.98 (Çok yüksek, şifrelenmiş veri şüphesi)")
        print(f"  {CYAN}Ortalama Chi-Square:{RESET} 145.2 (Uniform dağılıma yakın - LSB stego şüphesi)\n")
        
        print(f"{GRAY}3. BMP LSB Analizi simüle ediliyor...{RESET}")
        print(f"  {RED}[!] Olası metin bulundu:{RESET} 'flag{{st3g0_1s_aw3s0m3}}'")
        sys.exit(0)

    if args.scan:
        filepath = args.scan
        if not os.path.exists(filepath):
            print(f"{RED}Hata: Dosya bulunamadı -> {filepath}{RESET}")
            sys.exit(1)
            
        print_section(f"Analiz Ediliyor: {filepath}")
        
        # 1. EOF Analysis
        has_eof, size, data = detect_eof_data(filepath)
        if has_eof:
            print(f"  {RED}[!] EOF UYARISI: Dosya sonunda {size} bayt eklenmiş veri bulundu!{RESET}")
            try:
                print(f"  {YELLOW}Önizleme:{RESET} {data[:50].decode('ascii', errors='replace')}")
            except:
                print(f"  {YELLOW}Önizleme (Hex):{RESET} {data[:20].hex()}")
        else:
            print(f"  {GREEN}[+] EOF: Temiz. Dosya sonunda ek veri yok.{RESET}")
            
        # 2. Statistical Analysis
        try:
            with open(filepath, 'rb') as f:
                file_bytes = f.read()
            entropy, avg_chi, is_suspicious = analyze_anomalies(file_bytes)
            print(f"  {CYAN}Shannon Entropisi:{RESET} {entropy:.2f}")
            print(f"  {CYAN}Ortalama Chi-Square:{RESET} {avg_chi:.2f}")
            if is_suspicious:
                print(f"  {RED}[!] İSTATİSTİKSEL UYARI: Dosya yapısı steganografi şüphesi taşıyor.{RESET}")
            else:
                print(f"  {GREEN}[+] İstatistiksel yapı normal görünüyor.{RESET}")
        except Exception as e:
            print(f"  {RED}İstatistiksel analiz hatası: {e}{RESET}")
            
        # 3. LSB Analysis (BMP only)
        if filepath.lower().endswith('.bmp'):
            print_section("BMP LSB Analizi Başlıyor")
            found, msg, ext_bytes = analyze_bmp_lsb(filepath)
            if found:
                print(f"  {RED}[!] LSB UYARISI:{RESET} {msg}")
            else:
                print(f"  {GREEN}[+] LSB:{RESET} {msg}")

    print()

if __name__ == '__main__':
    main()
