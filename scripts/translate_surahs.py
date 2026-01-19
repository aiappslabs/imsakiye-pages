import json
import os

SURAH_NAMES_TR = {
    1: "Fatiha", 2: "Bakara", 3: "Âl-i İmrân", 4: "Nisâ", 5: "Mâide",
    6: "En'âm", 7: "A'râf", 8: "Enfâl", 9: "Tevbe", 10: "Yûnus",
    11: "Hûd", 12: "Yûsuf", 13: "Ra'd", 14: "İbrâhîm", 15: "Hicr",
    16: "Nahl", 17: "İsrâ", 18: "Kehf", 19: "Meryem", 20: "Tâhâ",
    21: "Enbiyâ", 22: "Hac", 23: "Mü'minûn", 24: "Nûr", 25: "Furkân",
    26: "Şuarâ", 27: "Neml", 28: "Kasas", 29: "Ankebût", 30: "Rûm",
    31: "Lokmân", 32: "Secde", 33: "Ahzâb", 34: "Sebe'", 35: "Fâtır",
    36: "Yâsîn", 37: "Saffât", 38: "Sâd", 39: "Zümer", 40: "Mü'min (Gāfir)",
    41: "Fussilet", 42: "Şûrâ", 43: "Zuhruf", 44: "Duhân", 45: "Câsiye",
    46: "Ahkâf", 47: "Muhammed", 48: "Fetih", 49: "Hucurât", 50: "Kâf",
    51: "Zâriyât", 52: "Tûr", 53: "Necm", 54: "Kamer", 55: "Rahmân",
    56: "Vâkıa", 57: "Hadîd", 58: "Mücâdele", 59: "Haşr", 60: "Mümtehine",
    61: "Saff", 62: "Cuma", 63: "Münâfikûn", 64: "Tegābün", 65: "Talâk",
    66: "Tahrîm", 67: "Mülk", 68: "Kalem", 69: "Hâkka", 70: "Meâric",
    71: "Nûh", 72: "Cin", 73: "Müzemmil", 74: "Müddessir", 75: "Kıyâmet",
    76: "İnsân", 77: "Mürselât", 78: "Nebe'", 79: "Nâziât", 80: "Abese",
    81: "Tekvîr", 82: "İnfitâr", 83: "Mutaffifîn", 84: "İnşikâk", 85: "Burûc",
    86: "Târık", 87: "A'lâ", 88: "Gāşiye", 89: "Fecr", 90: "Beled",
    91: "Şems", 92: "Leyl", 93: "Duhâ", 94: "İnşirah", 95: "Tîn",
    96: "Alak", 97: "Kadir", 98: "Beyyine", 99: "Zilzâl", 100: "Âdiyât",
    101: "Kāria", 102: "Tekâsür", 103: "Asr", 104: "Hümeze", 105: "Fîl",
    106: "Kureyş", 107: "Mâûn", 108: "Kevser", 109: "Kâfirûn", 110: "Nasr",
    111: "Tebbet (Mesed)", 112: "İhlâs", 113: "Felak", 114: "Nâs"
}

SURAH_TRANSLATIONS_TR = {
    1: "Açılış", 2: "Sığır", 3: "İmrân Ailesi", 4: "Kadınlar", 5: "Sofra",
    6: "En'âm", 7: "Yüksek Yerler", 8: "Ganimetler", 9: "Tevbe", 10: "Yûnus",
    11: "Hûd", 12: "Yûsuf", 13: "Gök Gürültüsü", 14: "İbrâhîm", 15: "Hicr",
    16: "Arı", 17: "Gece Yürüyüşü", 18: "Mağara", 19: "Meryem", 20: "Tâhâ",
    21: "Peygamberler", 22: "Hac", 23: "Mü'minler", 24: "Nûr", 25: "Farkı Belirten",
    26: "Şairler", 27: "Karınca", 28: "Kasas", 29: "Örümcek", 30: "Romalılar",
    31: "Lokmân", 32: "Secde", 33: "Gruplar", 34: "Sebe'", 35: "Yaratan",
    36: "Yâsîn", 37: "Saf Tutanlar", 38: "Sâd", 39: "Zümreler", 40: "Affeden",
    41: "Uzun Uzadıya Açıklanan", 42: "Şûrâ", 43: "Süsler", 44: "Duman", 45: "Diz Çöken",
    46: "Kum Tepeleri", 47: "Muhammed", 48: "Fetih", 49: "Hücreler", 50: "Kâf",
    51: "Rüzgarlar", 52: "Tûr Dağı", 53: "Yıldız", 54: "Ay", 55: "Rahmân",
    56: "Vâkıa", 57: "Demir", 58: "Mücâdele", 59: "Haşr", 60: "İmtihan Edilen",
    61: "Saflar", 62: "Cuma", 63: "Münâfiklar", 64: "Kayıp ve Kazanç", 65: "Boşanma",
    66: "Haram Kılma", 67: "Hükümranlık", 68: "Kalem", 69: "Gerçekleşecek Olan", 70: "Yükseliş Yolları",
    71: "Nûh", 72: "Cin", 73: "Örtünüp Bürünen", 74: "Gizlenen", 75: "Kıyâmet",
    76: "İnsân", 77: "Gönderilenler", 78: "Haber", 79: "Çekip Çıkaranlar", 80: "Surat Astı",
    81: "Gök Dürüldüğü Zaman", 82: "Gök Yarıldığı Zaman", 83: "Ölçüde Hile Yapanlar", 84: "Gök Parçalandığı Zaman", 85: "Burçlar",
    86: "Târık", 87: "En Yüce", 88: "Kuşatan", 89: "Tan Yerinin Ağarması", 90: "Şehir",
    91: "Güneş", 92: "Gece", 93: "Kuşluk Vakti", 94: "İnşirah", 95: "İncir",
    96: "Alak", 97: "Kadir Gecesi", 98: "Beyyine", 99: "Deprem", 100: "Âdiyât",
    101: "Kāria", 102: "Çoğaltma Yarışı", 103: "Zaman", 104: "Hümeze", 105: "Fîl",
    106: "Kureyş", 107: "Mâûn", 108: "Kevser", 109: "Kâfirler", 110: "Yardım",
    111: "Kurusun", 112: "İhlâs", 113: "Felak", 114: "Nâs"
}

def translate_surahs():
    data_dir = "/Users/hursit.topal/expo/imsakiye-pages/api/tr/quran"
    
    # 1. Translate surahs.json (list)
    path = os.path.join(data_dir, "surahs.json")
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            surahs = json.load(f)
        
        for s in surahs:
            num = s['number']
            if num in SURAH_NAMES_TR:
                s['englishName'] = SURAH_NAMES_TR[num]
            if num in SURAH_TRANSLATIONS_TR:
                s['englishNameTranslation'] = SURAH_TRANSLATIONS_TR[num]
            if s['revelationType'] == 'Meccan':
                s['revelationType'] = 'Mekki'
            elif s['revelationType'] == 'Medinan':
                s['revelationType'] = 'Medeni'
                
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(surahs, f, ensure_ascii=False, indent=2)
        print(f"Translated surahs.json")

    # 2. Translate individual surah_*.json files
    for i in range(1, 115):
        surah_path = os.path.join(data_dir, f"surah_{i}.json")
        if os.path.exists(surah_path):
            with open(surah_path, 'r', encoding='utf-8') as f:
                surah = json.load(f)
            
            num = surah['number']
            if num in SURAH_NAMES_TR:
                surah['englishName'] = SURAH_NAMES_TR[num]
            if num in SURAH_TRANSLATIONS_TR:
                surah['englishNameTranslation'] = SURAH_TRANSLATIONS_TR[num]
            if surah['revelationType'] == 'Meccan':
                surah['revelationType'] = 'Mekki'
            elif surah['revelationType'] == 'Medinan':
                surah['revelationType'] = 'Medeni'
                
            with open(surah_path, 'w', encoding='utf-8') as f:
                json.dump(surah, f, ensure_ascii=False, indent=2)
            if i % 20 == 0 or i == 114:
                print(f"Translated up to surah_{i}.json")

if __name__ == "__main__":
    translate_surahs()
