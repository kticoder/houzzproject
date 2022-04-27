import requests
from asyncio  import run, ensure_future, gather
from aiohttp   import ClientSession
from bs4 import BeautifulSoup
from parsel    import Selector
import aiofiles
import os
from Robot import konsol
import pyuser_agent
import time
# class houzzkategoriresim:
#     def __init__(self,kategorilinki) -> None:
#         self.kategorilinki = kategorilinki
#     def resimurlgetir(self):
#         self.cekilecekresimurl = []
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0',
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
#             'Accept-Language': 'tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3',
#             # 'Accept-Encoding': 'gzip, deflate, br',
#             'Connection': 'keep-alive',
#             # Requests sorts cookies= alphabetically
#             # 'Cookie': 'v=1650313544_a0a009dc-b8e6-4f0b-bcd8-62afdd86cbe7_9620fa983798795b3669d2bb94a9ac7b; vct=en-US-vxlIyV1iSBxIyV1iCR9IyV1iAh5IyV1i4R1IyV1i4h1IyV1i; _csrf=NuQkW8f2EePS1XkaxY-a0uPp; ns=2; jsq=; jdv=t7WOzUb2vHLZtWVUHSk%2FXJAbN7ua9zR%2BVkXobdRfXESxgRJNwu%2BreeHk6ZisQQO8WOImJsfwFlzxEEl3dW21jNrysoge; prf=generalFilter%7C%7D17%7C%7DisGfOverride%7C%7D0; documentWidth=1020; browseResultSetGridWidth=1136; documentHeight=987; fstest=8; G_ENABLED_IDPS=google; kcan=0; kucan=0',
#             'Upgrade-Insecure-Requests': '1',
#             'Sec-Fetch-Dest': 'document',
#             'Sec-Fetch-Mode': 'navigate',
#             'Sec-Fetch-Site': 'none',
#             'Sec-Fetch-User': '?1',
#             # Requests doesn't support trailers
#             # 'TE': 'trailers',
#         }
#         response = requests.get(self.kategorilinki, headers=headers)
#         soup = BeautifulSoup(response.text, "html.parser")
#         sayfaici = soup.find_all("a", {"class": "hz-photo-card__ratio-box"})
#         for i in sayfaici:
#             resimurl = i["href"]
#             if "hznb" in resimurl:
#                 continue
#             self.cekilecekresimurl.append(resimurl)
#             print(resimurl)
#         return self.cekilecekresimurl
#     def resimindir(self):
#         self.resimindir = []
#         for i in self.resimurlgetir():
#             response = requests.get(i)
#             soup = BeautifulSoup(response.text, "html.parser")
#             resimindir = soup.find("div", {"class": "view-photo-image-pane"}).find("img")["src"]
#             self.resimindir.append(resimindir)
#             print(resimindir)
#             return 
#     def resimindirdekiindir():
#         for i in self.resimindir:
            

# _basla = time()
# houzzkategoriresimleri = houzzkategoriresim("https://www.houzz.com/photos/bathroom-ideas-phbr0-bp~t_712?pg=1")
# houzzkategoriresimleri.resimindir()
# print(f"\n{time() - _basla:.4f} saniye\n")

class houzzkategoriresimasync:
    def __init__(self,kategorilinki,aralik) -> None:
        self.ua = pyuser_agent.UA()
        self.sayfasayisi = 0
        self.kategorilinki = kategorilinki
        self.resimsayisi = 0
        self.resimbasi = int(aralik.split("-")[0])
        if self.resimbasi == 0:
            self.resimbasi = 1
        self.resimson = int(aralik.split("-")[1]) + 1
    def resimurlgetir(self):
        self.cekilecekresimurl = []
        for i in range(self.resimbasi,self.resimson):
            headers = {
                # 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3',
                # 'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                # Requests sorts cookies= alphabetically
                # 'Cookie': 'v=1650313544_a0a009dc-b8e6-4f0b-bcd8-62afdd86cbe7_9620fa983798795b3669d2bb94a9ac7b; vct=en-US-vxlIyV1iSBxIyV1iCR9IyV1iAh5IyV1i4R1IyV1i4h1IyV1i; _csrf=NuQkW8f2EePS1XkaxY-a0uPp; ns=2; jsq=; jdv=t7WOzUb2vHLZtWVUHSk%2FXJAbN7ua9zR%2BVkXobdRfXESxgRJNwu%2BreeHk6ZisQQO8WOImJsfwFlzxEEl3dW21jNrysoge; prf=generalFilter%7C%7D17%7C%7DisGfOverride%7C%7D0; documentWidth=1020; browseResultSetGridWidth=1136; documentHeight=987; fstest=8; G_ENABLED_IDPS=google; kcan=0; kucan=0',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                # Requests doesn't support trailers
                # 'TE': 'trailers',
            }
            response = requests.get(f"{self.kategorilinki}?pg={i}", headers=headers)
            konsol.print(f"[bold red] {self.kategorilinki}?pg={i} sayfası indiriliyor. [/]")
            soup = BeautifulSoup(response.text, "html.parser")
            sayfaici = soup.find_all("a", {"class": "hz-photo-card__ratio-box"})
            for urller in sayfaici:
                cekilresimurl = urller["href"]
                # if "hznb" in cekilresimurl:
                #     continue
                self.cekilecekresimurl.append(cekilresimurl)
                self.sayfasayisi += 1
                konsol.print(f"[bold] Sayfa Alındı! {cekilresimurl}[/bold]")
                
        time.sleep(0.5)
        return self.cekilecekresimurl
    async def get_link(self,session, url):
        async with session.get(url) as resp:
            return await resp.text()
    async def image_downloader(self,session,resimindir):
        for i in resimindir:
            async with session.get(i) as resp:
                self.resimsayisi += 1
                f = await aiofiles.open(f'{os.getcwd()}/HouzzKategoriResim/resim{self.resimsayisi}.jpg', mode='wb')
                await f.write(await resp.read())
                await f.close()
                konsol.print(f"[bold] {i} dosyası indirildi. [/]")
    async def print_response(self,session, url):
        resmiindir = []
        istek = await self.get_link(session, url)
        soup =  BeautifulSoup(istek, "html.parser")
        try:
            resim = soup.find("div", {"class": "view-photo-image-pane"}).find("img")["src"]
            resmiindir.append(resim)
        except:
            pass
        await self.image_downloader(session,resmiindir)
    async def main(self):
        async with ClientSession() as session:
            tasks = (ensure_future(self.print_response(session, link)) for link in self.resimurlgetir())
            await gather(*tasks)
    def calistir(self):
        run(self.main())