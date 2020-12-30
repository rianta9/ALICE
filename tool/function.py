from numpy import random as rd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import webbrowser as wb
import os
import subprocess
import glob
import urllib.parse as urlparse
import wikipedia as wiki
import json
import smtplib
from pywikihow import WikiHow as wikihow
import goslate
from googletrans import Translator
import datetime

from dao import line_file
from tool import text_tool as TextTool
from util.constant import Constant
import time

#KHỞI TẠO
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
wiki.set_lang('vi')


def chromeDriverInit():
    # Khởi tạo đối tượng dùng chromedriver
    driver = webdriver.Chrome(chrome_options=chrome_options, 
        executable_path = Constant.CHROME_DRIVER)

    return driver


def random(range):
    result = rd.randint(range)
    return result


def getTime():
    result = datetime.datetime.now().strftime("%I:%M %p")
    return result

'''
Trả về kết quả tìm kiếm thông tin từ wikipedia. Nếu không tìm thấy kết quả trả về null.
'''
def wikipedia(text):
    try:
        contents = wiki.summary(text).split('\n')
        return contents[0].split(".")[0]
    except:
        return 'Alice không định nghĩa được từ ' + text
    return None

'''
Mở google bằng trình duyệt với một truy vấn
'''
def searchGoogle(query):
    url = "https://www.google.com/search?q=" + query
    openLink(url)
    return 'Đã tìm kiếm kết quả bằng google cho từ khoá: ' + query


def getResultGG(query):
    driver = chromeDriverInit()
    url = "https://www.google.com/search?q={}".format(query)
    driver.get(url)
    try:
        results = driver.find_elements_by_css_selector("div.g")
        link = results[0].find_element_by_tag_name("a")
        href = link.get_attribute("href")
        rem = linkContent(href)
        if rem is not None and len(rem) > 50:
            return rem
    except Exception as e:
        #print(e)
        pass
    openLink(url)
    return 'Alice sẽ tìm kiếm thông tin này cho master!'


def linkContent(link):
    driver = chromeDriverInit()
    url = link
    driver.get(url)
    try:
        contents = driver.find_elements_by_tag_name('p')
        result = driver.find_element_by_tag_name('title').text + '\n'
        for element in contents:
            result += element.text + '\n'
        return result
    except Exception as e:
        pass
    return None



'''
Cách làm, cách thực hiện một thứ gì đó. Tìm kiếm thông tin từ wikihow. Nếu không tìm thấy kết quả trả về null.
'''
def howTo(text):
    listResult = wikihow.search(text, lang='vn')
    result = ''
    dem = 1
    for how_to in listResult:
        result += TextTool.decode(how_to.title) + '\n'
        result += how_to.intro + '\n'
        for s in how_to.steps:
            result += str(dem) + '. ' + s.summary + '\n'
            dem = dem+1
        break
    return result

'''
Lấy danh sách các bài hát trong một thư mục.
Kết quả trả về trong result: list[BookMark]
'''
def listMusicFolder(result, folder):
    pa = Constant.MUSIC_PATH
    listMusic = glob.glob(os.path.join(pa, '*.mp3')) + glob.glob(os.path.join(pa, '*.flac'))
    return listMusic

'''
Mở một bài hát bất kỳ theo tên bằng trình duyệt.
'''
def openMusicOnline(musicName):
    driver = chromeDriverInit()
    url = "https://www.nhaccuatui.com/tim-kiem?q=" + musicName
    driver.get(url)
    try:
        data = line_file.getLineInCssSelector('lyric')
        if data is None:
            return 'Chức năng lyric hiện không thể hoạt động!'
        selector = data.split('|')
        searchList = driver.find_elements_by_css_selector(selector[0])
        bestResult = searchList[0]
        urlMusic = bestResult.find_element_by_tag_name('a').get_attribute('href')
        print('Url Song:', urlMusic)
        openLink(urlMusic)
        return 'Mở bài hát ' + musicName
    except Exception as e:
        pass
    return 'Mở chức năng mở bài hát online!'

'''
Mở một bài hát theo tên bằng phần mềm mặc định trên windows
'''
def openMusic(musicName):
    pa = Constant.MUSIC_PATH
    #t = input()
    t = musicName.upper()

    #open file .mp3
    for filename in glob.glob(os.path.join(pa, '*.mp3')):
        #print(filename)
        if len(filename) < 1:
            continue
        rem = TextTool.chuanHoaTenFile(filename)
        # thêm 1 ký tự '\' vào trước tên file để thành ...\\tenFile.mp3
        fn = rem.split('[\]')
        # cắt đường dẫn đang lõi thành 2 phần đường dẫn file_cha và tên_file_nhạc
        fn1 = fn[0].split('\\')
        st = fn1[0]+'/'+fn1[1]  # nối thành đường dẫn hợp lệ
        st1 = str(st)
        tam = st1.split('/')
        x = len(tam)
        temp = fn1[len(fn1) - 1].split('.')  # cắt lấy tên file
        nameSong = temp[0]

        if (t in nameSong.upper()):
            subprocess.call(filename, shell=True)  # mở bài hát đưa về
            return 'Đã mở bài hát ' + musicName

    #open file .raw
    for filename in glob.glob(os.path.join(pa, '*.flac')):

        if len(filename) < 1:
            continue
        rem = TextTool.chuanHoaTenFile(filename)
        # thêm 1 ký tự '\' vào trước tên file để thành ...\\tenFile.mp3
        fn = rem.split('[\]')
        # cắt đường dẫn đang lõi thành 2 phần đường dẫn file_cha và tên_file_nhạc
        fn1 = fn[0].split('\\')
        st = fn1[0]+'/'+fn1[1]  # nối thành đường dẫn hợp lệ
        st1 = str(st)
        tam = st1.split('/')
        x = len(tam)
        temp = fn1[len(fn1) - 1].split('.')  # cắt lấy tên file
        nameSong = temp[0]

        if (t in nameSong.upper()):
            subprocess.call(filename, shell=True)  # mở bài hát đưa về
            return 'Đã mở bài hát ' + musicName

    #open music online
    openMusicOnline(musicName)
    return 'Mở chức năng mở bài hát!'

'''
Mở một bài hát bất kỳ trong thư mục lưu trữ nhạc.
'''
def openRandomMusic():
    pa = Constant.MUSIC_PATH
    listMusic = glob.glob(os.path.join(pa, '*.mp3')) + glob.glob(os.path.join(pa, '*.flac'))
    if listMusic is None or len(listMusic) == 0:
        return 'Không tìm được bài hát nào trong thư mục ' + pa
    rand = random(len(listMusic))
    st = listMusic[rand]
    
    subprocess.call(st, shell=True)  # mở bài hát đưa về
    return 'Mở 1 bài hát ngẫu nhiên!'
    
def lyric(musicName):
    driver = chromeDriverInit()
    url = "https://www.nhaccuatui.com/tim-kiem?q=" + musicName
    driver.get(url)
    try:
        data = line_file.getLineInCssSelector('lyric')
        if data is None:
            return 'Chức năng lyric hiện không thể hoạt động!'
        selector = data.split('|')
        searchList = driver.find_elements_by_css_selector(selector[0])
        bestResult = searchList[0]
        urlMusic = bestResult.find_element_by_tag_name('a').get_attribute('href')
        print('Url Song:', urlMusic)
        lyricDoc = chromeDriverInit()
        lyricDoc.get(urlMusic)
        songName = lyricDoc.find_element_by_css_selector(selector[1])
        composer = lyricDoc.find_element_by_css_selector(selector[2])
        result = "Thông tin:\n" + songName + composer
        lyricElement = lyricDoc.find_element_by_id(selector[3])
        lyric = lyricElement.text
        result += lyric
        return result

    except Exception as e:
        #print(e)
        pass
    searchGoogle('Lời bài hát ' + musicName)
    return 'Tìm kiếm lời bài hát online!'

def musicThemeRandom():
    tags = ["lang-man", "mua", "cafe", "buon", "nho-nhung", "co-don", "fa", "vui-ve", "hung-phan", "thu-gian", "that-tinh", "ngot-ngao"]
    tagsTitle = ["Lãng Mạn", "Mưa", "Cafe", "Buồn", "Nhớ Nhung", "Cô Đơn", "Fa", "Vui Vẻ", "Hưng Phấn", "Thư Giãn", "Thất Tình", "Ngọt Ngào"]
    rand = random(len(tags))
    musicTopic = listMusicTag(tags[rand])
    if musicTopic is not None:
        rand = random(len(musicTopic))
        openLink(musicTopic[rand])
    return 'Mở bài hát theo chủ đề ngẫu nhiên!'


'''
Trả về list playlist theo tag được cập nhật vào hiện tại.
Dữ liệu lấy từ nhaccuatui.com
Dùng để mở random một playlist ngẫu nhiên
'''
def listMusicTag(tag):
    result = []
    for i in range(1,5):
        driver = chromeDriverInit()
        url = "https://www.nhaccuatui.com/playlist/tags/" + tag + "?page=" + str(i)
        driver.get(url)
        playlists = driver.find_elements_by_css_selector('div.list_album.tag > ul > li')
        for playlist in playlists:
            link = playlist.find_element_by_css_selector('div.info_album > h2 > a').get_attribute('href')
            result.append(link)
    return result #list[BookMark]

'''
Trả về list chủ đề âm nhạc được cập nhật vào hiện tại
Dữ liệu lấy từ nhaccuatui.com
'''
def listMusicTopic():
    result = []
    driver = chromeDriverInit()
    url = "https://www.nhaccuatui.com/chu-de.html"
    driver.get(url)
    topicList = driver.find_elements_by_css_selector('div.topic_more > div.fram_select > ul > li')
    for topic in topicList:
        title = topic.find_element_by_css_selector('div.box-info-detail > h3').text
        title = title.replace('-', '')
        link = topic.find_element_by_css_selector('a.box_absolute').get_attribute('href')
        bookmark = {'title': title.lower(), 'link':link}
        result.append(bookmark)
    return result #list[BookMark]

'''
Mở 1 playlist nhạc online theo 1 chủ đề được yêu cầu.
Dữ liệu lấy từ nhaccuatui.com
'''
def musicTheme(topic):
    musicTopic = listMusicTopic()
    for i in musicTopic:
        if(i['title'] == topic):
            openLink(i['link'])
            return 'Mở chủ đề ' + i['title']
    
    #Nếu không tìm thấy chủ đề có sẵn. Tìm kiếm chủ đề theo tag
    tags = ["lang-man", "mua", "cafe", "buon", "nho-nhung", "co-don", "fa", "vui-ve", "hung-phan", "thu-gian", "that-tinh", "ngot-ngao"]
    tagsTitle = ["Lãng Mạn", "Mưa", "Cafe", "Buồn", "Nhớ Nhung", "Cô Đơn", "Fa", "Vui Vẻ", "Hưng Phấn", "Thư Giãn", "Thất Tình", "Ngọt Ngào"]
    size = len(tags)
    fl = False
    for i in range(0, size):
        if topic == tagsTitle[i].lower():
            musicTopic = listMusicTag(tags[i])
            if musicTopic is not None and len(musicTopic) > 0:
                rand = random(len(musicTopic))
                openLink(musicTopic[rand])
                fl = True
            break
    if(fl == False):
        return 'Chủ đề không có sẵn!'
    return 'Mở bài hát theo chủ đề ' + topic


'''
Lịch chiếu phim
'''
def showtimes(query):
    driver = chromeDriverInit()
    url = "https://www.google.com/search?q={}".format(query)
    driver.get(url)  
    #time.sleep(5)
    selector = line_file.getLineInCssSelector('showtime')
    list = selector.split('|')
    elements0 = driver.find_elements_by_css_selector(list[0]+">span")
    storyUrls0 = [el.text for el in elements0]
    result = ''
    if  storyUrls0:
        el = driver.find_element_by_css_selector("div.MXl0lf")
    #option 1: regular click
        el.click()
        li0 = storyUrls0
        result += "{}".format(li0) + '\n\t'
 
        elements1 = driver.find_elements_by_css_selector(list[1])
        li1 = [el.text for el in elements1]
        result += "Ngày chiếu:{}".format(li1) + '\n\t'
 
        elements2 = driver.find_elements_by_css_selector(list[2])
        li2 = [el.text for el in elements2]
        result += "Thời điểm:{}".format(li2) + '\n'
 
        elements3 = driver.find_elements_by_css_selector(list[3])
 
        elements4 = elements3[0].find_elements_by_css_selector(list[4])
        for i in elements4:
            movie = i.find_elements_by_css_selector(list[5])
            time1 = i.find_elements_by_css_selector(list[6])
            rmovie = [el.text for el in movie]
            rtime = [el.text for el in time1]
            result +='\tPhim: ' + str(rmovie[0]) + '\n\t  Khung giờ phim: '
            i=0
            y=5
            while(y <= len(rtime[0])): 
                result += str(rtime[0][i:y]) + ' '
                if y == len(rtime[0]):
                    result += '\n\t'
                i=i+5
                y=y+5
 
        return result
 
 
    elif not storyUrls0 and "cinestar huế" and "hôm nay" in query:
        link1 = "https://c...content-available-to-author-only...m.vn/lichchieu"
        openLink(link1)
    elif not storyUrls0 and "cinestar huế" and "ngày mai" in query:
        openLink("https://c...content-available-to-author-only...m.vn/lichchieu")
    elif not storyUrls0 and "starlight huế" and "ngày mai" in query:
        link1 = "https://r...content-available-to-author-only...m.com/lich-chieu"
        openLink(link1)
    elif not storyUrls0 and "starlight huế" and "hôm nay" in query:
        link1 = "https://r...content-available-to-author-only...m.com/lich-chieu"
        openLink(link1)
    else:
        searchGoogle(query)
    return 'Mở chức năng tìm kiếm lịch chiếu phim!'


'''
Thời tiết
'''
def weather(query):
    driver = chromeDriverInit()
    url = "https://www.google.com/search?q={}".format(query)
    driver.get(url)  
    time.sleep(3)
    elements0 = driver.find_elements_by_css_selector("#wob_loc")
    position = [el.text for el in elements0]
    if position:
        # vt = position[0].split("[,]")
        # if len(vt) <= 2:
        location = position
        # else: location = "Vị trí:" + vt[1] +","+vt[2]
        elements1 = driver.find_elements_by_css_selector("#wob_dts")
        dateOfWeek=[el.text for el in elements1]

        elements2 = driver.find_elements_by_css_selector("#wob_tm")
        temperature=[el.text for el in elements2]

        elements3 = driver.find_elements_by_css_selector("#wob_dc")
        status =[el.text for el in elements3]

        elements4 = driver.find_elements_by_css_selector("#wob_pp")
        precipitation =[el.text for el in elements4]

        elements5 = driver.find_elements_by_css_selector("#wob_hm")
        humidity =[el.text for el in elements5]

        elements6 = driver.find_elements_by_css_selector("#wob_ws")
        windspeed=[el.text for el in elements6]
        content = """
        Thông tin thời tiết:
        Vị trí {location}
        Thời điểm {dateOfWeek}
        Nhiệt độ{temperature}
        Dự báo {status}
        Khả năng có mưa {precipitation}
        Độ ẩm {humidity}
        Sức gió {windspeed}""".format(location=location,dateOfWeek=dateOfWeek,temperature=temperature,status=status,
                                precipitation=precipitation,humidity=humidity,windspeed=windspeed)
        return content
    elif not position:
        openLink("https://www.google.com/search?q={}".format(query))
        return "Alice không thể truy xuất nhanh thông tin thời tiết vào hiện tại. Alice sẽ mở trình duyệt giúp Master!\n"
        


'''
Lấy thông tin tóm tắt của một chủ đề từ google
'''
def quickInformation(text):
    driver = chromeDriverInit()
    return None

def openNotepad():
    os.system("start Notepad")
    return 'Mở chức năng open notepad'

def openPaint():
    os.system("start mspaint")
    return 'Mở chức năng open paint'

def openCalculator():
    os.system('start calc')
    return 'Mở calculator'

def openFileExplorer():
    os.system('start explorer')
    return 'Mở file explorer'

def openChrome():
    os.system('start chrome')
    return 'Mở chrome'

def openEdge():
    os.system("start msedge")
    return 'Mở Edge'

def openVLC():
    os.system("start VLC")
    return 'Mở VLC'

def openIllustrator():
    os.system("start illustrator")
    return 'Mở Illustrator'

def openPhotoshop():
    os.system("start photoshop")
    return 'Mở Photoshop'

def openTaskManager():
    os.system("start taskmgr")
    return 'Mở chức năng mở task manager!'

def openPowerPoint():
    os.system("start powerpnt")
    return 'Mở chức năng mở powerpoint'

def openWord():
    os.system("start winword")
    return 'Mở chức năng mở word'

def openCMD():
    os.system('start cmd')
    return 'Mở chức năng mở cmd'

def openExcel():
    os.system("start excel")
    return 'Mở chức năng open excel'

def openMap():
    openLink('https://www.google.com/maps')
    return 'Mở chức năng open map'

def openMail():
    openLink('https://mail.google.com/mail/u/0/#inbox')
    return 'Mở chức năng open mail'

'''
Mở một bookmark được cài sẵn
file danh sách bookmark nằm trong file/adress/bookmark.txt
'''
def openBookMark(title):
    listBookmark = line_file.getBookmarkInAddress('bookmark')
    if listBookmark is None:
        return None
    for bookmark in listBookmark:
        if bookmark['title'].lower() == title:
            openLink(bookmark['link'])
            return 'Mở ' + bookmark['title']
    return None

'''
Mở link bằng trình duyệt mặc định
'''
def openLink(link):
    wb.open(link, new=2)
    return 'Đã mở link: {}'.format(link)

'''
Mở một loại file bất kỳ nằng phần mềm mặc định trên desktop.
'''
def openFileType(pathname):
    os.startfile(pathname)
    return 'Đã mở file theo yêu cầu!'


def sendMail(mailto, subject, content):
    try:
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        mail.login(Constant.MAIL_ADDRESS, Constant.MAIL_PASS) # Username + Password
        mail.sendmail(Constant.MAIL_ADDRESS, 
                        mailto, content.encode('utf-8')) # mailto là địa chỉ người nhận
        mail.close()
        return 'Đã gửi mail có nội dung ' + content + ' đến ' + mailto
    except:
        return 'Chức năng gửi mail tạm thời không hoạt động!'

'''
sl: ngôn ngữ cần dịch
tl: ngôn ngữ trả về
'''
def translateG(text, sl, tl):
    result = ''
    try:
        translator = goslate.Goslate()
        result = translator.translate(text, tl)
    except Exception as e:
        result = 'Hiện không thể sử dụng chức năng dịch!'
    
    return result