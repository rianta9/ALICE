
# Lấy các dòng dữ liệu từ một file ở trong thư mục train
def getFileInTrain(filename):
    result = []
    file = open('./file/train/' + filename + '.txt', 'r', encoding='utf-8')
    if file is None:
        print('Mở file ' + filename + ' thất bại!')
        return result
    
    for line in file:
        line = line.replace('\n', '')
        result.append(line)
    file.close()
    return result

def getLineInCssSelector(filename):
    result = None
    file = open('./file/cssselector/' + filename + '.txt', 'r', encoding='utf-8')
    if file is None:
        print('Mở file ' + filename + ' thất bại!')
        return result
    result = file.readline()
    file.close()
    return result
