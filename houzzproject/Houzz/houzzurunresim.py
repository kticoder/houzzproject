import requests
from asyncio  import run, ensure_future, gather
from aiohttp   import ClientSession
from bs4 import BeautifulSoup
from parsel    import Selector
import aiofiles
import os
from Robot import konsol


class houzzurunresimasync:
    def __init__(self,kategorilinki,aralik) -> None:
        self.kategorilinki = kategorilinki
        self.resimsayisi = 0
        self.resimbasi = int(aralik.split("-")[0])
        self.resimson = int(aralik.split("-")[1]) + 1
    def resimurlgetir(self):
        self.cekilecekurunurl = []
        for i in range(self.resimbasi,self.resimson):
            sayfa = i*36
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
            response = requests.get(f"{self.kategorilinki}/p/{sayfa}/", headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
            sayfaici = soup.find_all("a", {"class": "hz-product-card__link"})
            konsol.print(f"[bold green]{self.kategorilinki}/p/{sayfa}/ sayfası indiriliyor...[/]")
            for i in sayfaici:
                cekilurunurl = i["href"]
                self.cekilecekurunurl.append(cekilurunurl)
                konsol.print(cekilurunurl)
        return self.cekilecekurunurl
    async def get_link(self,session, url):
        async with session.get(url) as resp:
            return await resp.text()
    async def image_downloader(self,session,resimindir,resimadi):
        resimsayisi = 0
        for i in resimindir:
            resimsayisi += 1
            async with session.get(i) as resp:
                f = await aiofiles.open(f'{os.getcwd()}/HouzzUrunResim/{resimadi}{resimsayisi}.jpg', mode='wb')
                await f.write(await resp.read())
                await f.close()
                konsol.print(f"[bold] {i} dosyası indirildi. [/]")
    async def print_response(self,session, url):
        resmiindir = []
        istek = await self.get_link(session, url)
        soup = BeautifulSoup(istek, "html.parser")
        resimler = soup.find("div", {"class": "view-product-image__container prxl"}).find_all("img", {"width": "44"})
        resimadi = url.split("-prvw")[0].split("/")[-1]
        for i in resimler:
            resim = i["src"]
            if "fimgs" in resim:
                resim = resim.replace("fimgs", "simgs").split("-w44")[0] + "/home-design.jpg"
                resim = resim.replace("_", "_9-")
            if ".jpg" not in resim:
                continue
            if resim in resmiindir:
                continue
            resmiindir.append(resim)
        await self.image_downloader(session,resmiindir,resimadi)
    async def main(self):
        async with ClientSession() as session:
            tasks = (ensure_future(self.print_response(session, link)) for link in self.resimurlgetir())
            await gather(*tasks)
    def calistir(self):
        run(self.main())