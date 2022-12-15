from Tabanım.taban import Amil
vezir = Amil(
    baslik   = "Houzzİ",
    aciklama = "Houzzİ",
    banner   = "Houzzİ",
    girinti  = 3
)
konsol = vezir.konsol

import os
from dotenv import load_dotenv

load_dotenv("ayar.env")

if AYAR_KONTROL := os.environ.get(
    "___________LUTFEN_______BU_____SATIRI_____SILIN__________", None
):
    hata("\n\tLütfen ayar.env dosyanızı düzenlediğinize emin olun /veya\n\tilk hashtag'de belirtilen satırı kaldırın..\n")
    quit(1)
