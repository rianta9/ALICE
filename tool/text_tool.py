from urllib.parse import unquote

from dao import line_file
from core.alice_info import Alice


# các đại từ ngôi 1: bản thân master
def isPronounType1Master(text):
    list = ['t', 'tau', 'tao', 'tôi', 'tớ', 'tui', 'mình', 'i', 'ck', 'chuỵ', 'chụy']
    for i in list:
        if text == i:
            return True
    return False

# các đại từ ngôi 2: gọi alice
def isPronounType2Master(text):
    list = ['em', 'e', 'mi', 'm', 'mày', 'mầy', 'cậu', 'you', 'cưng', 'kưng', 'vk', 'vợ', 'bạn']
    for i in list:
        if text == i:
            return True
    return False

# các đại từ ngôi 1: bản thân alice
def isPronounType1Alice(text):
    list = ['t', 'tau', 'tao', 'tôi', 'tớ', 'tui', 'mình', 'i', 'chuỵ', 'chụy', 'e', 'em']
    for i in list:
        if text == i:
            return True
    return False

# các đại từ ngôi 2: gọi master
def isPronounType2Alice(text):
    list = ['mi', 'm', 'mày', 'mầy', 'cậu', 'you', 'cưng', 'kưng', 'bạn']
    for i in list:
        if text == i:
            return True
    return False

def standardMessageForTraining(text):
    text = text.lower()
    text = text.strip()
    text = std1(text) # chuẩn hoá từ địa phương
    text = getOrigin(text) # xoá ký tự đặc biệt

    if text is None or not text:
        return None
    words = text.split(' ')
    result = ''
    for word in words:
        if isPronounType1Master(word):
            result += 'master '
        elif isPronounType2Master(word):
            result += 'alice '
        else:
            result += word + ' '
    return result


'''
Chuẩn hoá replyMessage trước khi add vào 1 Reply.
replyMessage cần được chuẩn hoá các từ ngữ xưng hô, thay thế bằng alice hoặc master.
'''
def standardReplyForTraining(text):
    text = text.lower()
    text = text.strip()

    if text is None or not text:
        return None
    words = text.split(' ')
    result = ''
    for word in words:
        if isPronounType1Alice(word):
            result += 'alice '
        elif isPronounType2Alice(word):
            result += 'master '
        else:
            result += word + ' '
    return result

'''
Tạo ra các đoạn text tương tự với đoạn text ban đầu
'''
def similarTextList(text, gender):
    result = []
    result.append(text)
    if 'alice' in text:
        result.append(text.replace('alice', 'em'))
    if 'master' in text:
        if(gender == 'male'):
            result.append(text.replace('master', 'anh'))
        else:
            result.append(text.replace('master', 'chị'))
            result.append(text.replace('master', 'chụy'))
            result.append(text.replace('master', 'chị bé'))
            
    #TODO: tạo worddao để làm công việc này


# lấy giá trị không dấu của một ký tự
def getUnsignedChar(c):
    vni = ["àáạảãăằắặẳẵâầấậẩẫ", "èéẻẹẽêếềểễệ", "đ", "ìíỉĩị", "òóỏõọôồốổỗộơờớợởỡ", "ùúụủũưừứựửữ", "ỳýỵỷỹ"]
    ascii = ["a", "e", "d", "i", "o", "u", "y"]

    for i in range(0, 7):
        if vni[i].find(c) != -1:
            return ascii[i]
    
    return c

def getOrigin(text):
    #TODO: 
    return text

def isQuestion(text):
    listQuestionKey = line_file.getFileInTrain('question_keyword')
    for key in listQuestionKey:
        if key in text:
            return True
    # một số cái khác    
    anotherKey = [' à', ' á', 'gì', 'chi', ' ai', 'ruk', 'rứa', 'chứ', ' ừ', ' ư', ' sao', 'vậy', ' rag', ' răng', ' ak', 'nhỉ']
    for key in anotherKey:
        if(text.endswith(key)):
            return True
    
    return False

# Chỉnh sửa từ địa phương
def std1(text):
    listStd1 = line_file.getFileInTrain('std1')
    for key in listStd1:
        rem = key.split('|')
        if len(rem) == 2:
            text = text.replace(rem[0], rem[1])
    return text.strip()

'''
Kiểm tra từ đầu câu có phải là từ xưng hô(cho người) hay không.
 Vd: anh, mày, tao, mình, ikaros, boss, master...v.v
Mẫu: ikaros là ai
Dùng để loại bỏ các câu dễ bị nhầm lẫn là câu yêu cầu chức năng.
Dùng để phân tích câu
'''
def cauXungHo(text):
    xungho = [
        "t ", "tau", "tao", "tôi", "tui"
        , "mày", "mầy", "mi ", "m "
        , "anh", "a "
        , "em", "e ", "iêm"
        , "chị", "chụy"
        , "bạn ", "cậu", "tớ "
        , "ck ", "chồng"
        , "vk ", "vợ ", "zợ "
        , "mình", "chúng mình", "chúng ta", "chúng tôi"
        , "chúng mày", "bọn bay"
        , "chúng nó"
        , "những đứa", "những người", "những tên", "những thằng"
        , "mấy đứa", "mấy người", "mấy thằng"
        , "họ ", "ta "
        , "hắn ", "tên kia", "tên đó", "tên này"
        , "ô ", "ông", "ôn "
        , "bà ", "mệ "
        , "honey", "my love"
        , "con của", "con ni", "con này", "con đó", "con kia", "thằng"
        , "kon "
        , "bố", "cha", "tía", "má", "mẹ"
        , "cô ", "chú ", "thím", "bác", "dì", "dượng"
        , "alice", "boss", "master", "angeltown"
	]
    for i in Alice.alias:
        xungho.append(i)
    
    for word in xungho:
        if text.startswith(word):
            return True
    return False

'''
Kiểm tra từ đầu câu có phải là từ xưng hô(cho vật) hay không.
	 * Vd: cái này, chuyện này, vật này, thứ đó...v.v
	 * Mẫu câu: [...] là gì.
	 * Dùng để loại bỏ các câu dễ bị nhầm lẫn là câu yêu cầu chức năng.
	 * Dùng để phân tích câu.
'''

def cauXungHo2(text):
    xungho = [
        "cái này", "cái kia", "cái đó", "cái ni"
        , "chuyện này", "chuyện kia", "chuyện đó", "chuyện ni"
        , "việc này", "việc đó", "việc kia", "việc ni"
        , "câu chuyện này", "câu chuyện đó", "câu chuyện kia"
        , "điều này", "điều đó"
        , "câu này", "câu đó", "câu kia"
        , "cuốn sách này"
        , "vật này", "vật đó", "vật kia"
        , "con vật này", "con vật đó", "con vật kia"
        , "con này", "con đó", "con kia", "con ni"
        , "thứ đó", "thứ này", "thứ kia"
        , "cây này", "cây kia", "cây đó"
    ]
    
    for word in xungho:
        if word in text:
            return True
    
    return False

def chuanHoaTenFile(nameFile):
	temp = nameFile.replace('-', ' ')
	st = temp.replace('_', ' ')
	return st

def decode(text):
    return unquote(text, encoding='utf-8')