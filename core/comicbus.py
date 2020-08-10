from typing import List, Union
from .manga_site import MangaSite
from .manga_site_enum import MangaSiteEnum
from .manga import Manga, MangaIndexTypeEnum
import re
import json
import base64
from urllib.parse import quote


def decode_to_big5(s: str):
    s = s.strip().encode("unicode-escape").decode()    
    idx = 0
    result = []
    
    while idx < len(s):
        if s[idx:(idx+2)] == "\\x":
            b = bytes.fromhex(s[idx + 2:(idx+4)])
            idx += 4
            
            result.append(b[0])            
        elif s[idx:(idx + 2)].startswith('\\u'):
            result.extend(s[idx:(idx + 6)].encode().decode('unicode-escape').encode('big5'))
            idx += 6
        else:
            result.append(ord(s[idx]))
            idx += 1
    return bytearray(result).decode('big5')


def lc(l: str) -> Union[str, int]:
    if len(l) != 2:
        return l

    az = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    a = l[0:1]
    b = l[1:2]
    b_idx = az.find(b)
    if a == "Z":
        return 8000 + az.find(b)
    else:
        return az.find(a) * 52 + b_idx


def su(a, b, c): return str(a)[b:(b+c)]
def mm(p): return (int((p-1)/10) % 10) + (((p-1) % 10)*3)


def get_urls(s: str, ch: int, manga_id: int,  y: int = 46) -> List[str]:
    match = re.search("var cs='([a-zA-Z0-9]+)';(.*)spp", s)
    cs = match.group(1)
    s = match.group(2)
    loop_num = int(re.search("for\(var i=0;i<(\d+);i\+\+\)", s).group(1))
    ps_str = re.search(";ps=(\w+);", s).group(1)
    ch_str = re.search("if\((\w+)== ch", s).group(1)
    first_str = re.search("'//img'\+su\((\w+)", s).group(1)
    last_str = re.search("(\w+),mm\(p\),3\)\+'\.jpg'", s).group(1)

    d = {}
    for match in re.finditer("var (\w+)=\ ?lc\(su\(cs,i\*y\+(\d+),(\d+)", s):
        d[match.group(1)] = [int(match.group(2)), int(match.group(3))]
    result = []
    for i in range(loop_num):
        tmp_dict = {
            key: lc(su(cs, i * y + value[0], value[1])) for key, value in d.items()}
        if tmp_dict[ch_str] == ch:            
            num_page = tmp_dict[ps_str]
            for page_i in range(1, num_page + 1):
                url = f"https://img{su(tmp_dict[first_str], 0, 1)}.8comic.com/{su(tmp_dict[first_str], 1, 1)}/{manga_id}/{ch}/{str(page_i).zfill(3)}_{su(tmp_dict[last_str], mm(page_i), 3)}.jpg"
                result.append(url)
            break
    return result


class ComicBus(MangaSite):
    def __init__(self):
        super(ComicBus, self).__init__(
            '無限動漫', 'https://www.comicbus.com/'
        )
        self.site = MangaSiteEnum.ComicBus

    async def search_manga(self, keyword) -> List[Manga]:

        def handle_td(td) -> Manga:
            name = td.find('b').find("font", {"color": "#0099CC"}).text.strip()
            url = td.find('a').get('href')
            if not url.startswith('http'):
                url = self.url + url.strip('/') + "/"

            manga = self.get_manga(self.site, name, url)
            return manga

        search_url = f'{self.url}member/search.aspx?k={quote(keyword.encode("big5"))}'
        soup = await self.downloader.get_soup(search_url)
        table = soup.find("table", {"style": "margin-top:8px;"})
        tds = table.find_all("td", {
                             "style": "border-bottom:1px dotted #cccccc; line-height:18px; padding-left:5px "})

        result = [handle_td(td) for td in tds]
        return result

    def get_meta_data(self, soup):
        last_update = soup.find('div', {"class": "button_div"}).find_parent(
            'tr').find_all("td")[1].text.strip()
        finished_text = decode_to_big5(soup.find(
            'a', {'href': '#Comic'}).text)
        finished = decode_to_big5(soup.find(
            'a', {'href': '#Comic'}).text).endswith("完")
        thum_img = soup.find(
            'img', {'style': "border:#CCCCCC solid 1px;width:240px;"}).get('src')

        if not thum_img.startswith('http'):
            thum_img = self.url + thum_img.lstrip('/')

        return {'last_update': last_update, 'finished': finished, 'thum_img': thum_img}

    async def get_index_page(self, page: str) -> Manga:

        manga = self.get_manga(self.site, None, page)

        if manga is not None and manga.idx_retrieved:
            return manga
        print(page)
        soup = await self.downloader.get_byte_soup(page)

        name = decode_to_big5(soup.find(
            'font', {"style": "font-size:10pt; letter-spacing:1px"}).text)
        
        manga = self.get_manga(self.site, name, page)

        for m_type, table_id in zip([MangaIndexTypeEnum.VOLUME, MangaIndexTypeEnum.CHAPTER], ["rp_ctl04_0_dl_0", "rp_ctl05_0_dl_0"]):
            table = soup.find("table", id=table_id)
            class_name = "Vol" if m_type == MangaIndexTypeEnum.VOLUME else "Ch"

            a_list = table.find_all("a", {"class": class_name})
            for a in a_list:
                url = a.get('onclick').split("'")[1]
                url = url.replace(".html", "").replace("-", ".html?ch=")
                if not url.startswith('http'):
                    url = f'https://comicbus.live/online/a-{url}'
                title = decode_to_big5(a.text)
                
                manga.add_chapter(m_type=m_type, title=title, page_url=url)

        meta_dict = self.get_meta_data(soup)
        thum_img_b = await self.downloader.get_img(meta_dict['thum_img'])
        meta_dict['thum_img'] = base64.b64encode(thum_img_b).decode("utf-8")

        manga.set_meta_data(meta_dict)
        manga.retreived_idx_page()
        return manga

    async def get_page_urls(self, manga: Manga, m_type: MangaIndexTypeEnum, idx: int) -> List[str]:
        chapter = manga.get_chapter(m_type, idx)

        manga_id = int(manga.url.split('/')[-2].split('.')[0])
        ch = int(chapter.page_url.split('=')[-1])
        soup = await self.downloader.get_byte_soup(chapter.page_url)
        for script in soup.find_all('script'):
            if len(script.contents) == 0:
                continue
            if script.contents[0].strip().startswith('function request'):
                urls = get_urls(script.contents[0], ch, manga_id)
                print(urls)
                return urls
        return []
