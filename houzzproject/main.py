from Houzz.houzzkategoriresim import houzzkategoriresimasync
from Houzz.houzzurunresim import houzzurunresimasync
from Houzz.houzzararesim import houzzararesimasync
from time import time
from Robot import konsol, vezir


def job():
    secenek = vezir.option("str","Ürün,Kategori,Arama")
    if secenek == "Kategori":
        link = vezir.option("str", "Houzz kategori linkini giriniz.")
        _basla = time()
        aralik = vezir.option("str", "Houzz kategori resimlerini indirme aralığını giriniz.")
        houzzkategoriresimleri = houzzkategoriresimasync(link,aralik)
        houzzkategoriresimleri.calistir()
        konsol.print(f"\n [bold green] İşlem {time() - _basla:.4f} saniyede bitti....\n")
    if secenek == "Ürün":
        link = vezir.option("str", "Houzz ürün linkini giriniz.")
        _basla = time()
        aralik = vezir.option("str", "Houzz ürün resimlerini indirme aralığını giriniz.")
        houzzurunresimleri = houzzurunresimasync(link,aralik)
        houzzurunresimleri.calistir()
        konsol.print(f"\n [bold green] İşlem {time() - _basla:.4f} saniyede bitti....\n")
    if secenek == "Arama":
        link = vezir.option("str", "Houzz arama linkini giriniz.")
        _basla = time()
        aralik = vezir.option("str", "Houzz arama resimlerini indirme aralığını giriniz.")
        houzzararesimleri = houzzararesimasync(link,aralik)
        houzzararesimleri.calistir()
        konsol.print(f"\n [bold green] İşlem {time() - _basla:.4f} saniyede bitti....\n")


if __name__ == "__main__":
    job()



