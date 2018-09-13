import requests
from bs4 import BeautifulSoup

class GetSong:


    def getSongList(self,url,match="artist"):
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        if match == "artist":
            num = soup.select_one("""#search_result > div.s_result.clearfix > div.s_re_left > span:nth-of-type(3)""").text
        else:
            num = soup.select_one("#search_result > div.s_result.clearfix > div.s_re_left > span:nth-of-type(4)").text


        if num.count("201-"):
            num = int(num.replace("201-",""))
        elif num.count("401-"):
            num = int(num.replace("401-",""))
        else:
            num = int(num.replace("1-",""))


        if match == "artist":
            tag = "#artist"
        elif match == "search":
            tag = "#ichiran"
        else:
            print("引数エラー")
        songlist = []
        tbnum = int(((num-50)/30) + 2)
        for tb in range(3,tbnum+1):
            for i in range(1,31):
                body = soup.select("""{} > div:nth-of-type({}) > table > tbody > tr:nth-of-type({}) > td.side.td1 > a""".format(tag,tb,i))
                for elem in body:
                    if elem.get('href').count("song"):
                        songlist.append(elem.get('href'))
        for i in range(1,57):
            body = soup.select("""{} > div.result_table.last > table > tbody > tr:nth-of-type({}) > td.side.td1 > a:nth-of-type(1)""".format(tag,i))
            for elem in body:
                if elem.get('href').count("song"):
                    songlist.append(elem.get('href'))
        url = elem.get('href')

        for slist in songlist:
            yield slist

    def getWordofsong(self,url):
            utaNeturl = "https://www.uta-net.com" + url
            r = requests.get(utaNeturl)
            soup = BeautifulSoup(r.content, "html.parser")
            title = soup.select_one("#view_kashi > div > div.title > h2").text
            data = str(soup.select_one("#kashi_area"))
            data = data.replace("<br/>","\n").replace("<br>","\n").replace("""<div id="kashi_area" itemprop="text">""","").replace("""</br></br></div>""","")
            title = soup.select_one("#view_kashi > div > div.title > h2").text
            if title.count("/"):
                title = title.replace("/","／")
            return title,data

if __name__ == '__main__':
    a = GetSong()
    Input_url = input("urlを入力:")
    print(Input_url)
    kashiList = a.getSongList(str(Input_url),match="search")
    num = 0
    utaNeturl = "https://www.uta-net.com"
    for kashi in kashiList:
        title,data = a.getWordofsong(utaNeturl+kashi)
        print(title)
