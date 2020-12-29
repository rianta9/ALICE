from dao.logic_reply_dao import LogicReplyDao
from bean.logic_reply import LogicReply
from bean.list_logic_data import ListLogicData
from tool import text_tool as TextTool

class LogicReplyBo:
    def __init__(self):
        self.dao = LogicReplyDao()
        self.dao.load() #load dữ liệu từ file
    
    def saveAll(self):
        self.dao.saveAll()
    
    # Thêm một reply vào list và cập nhật file data
    def addData(self, reply):
        self.dao.addData(reply)
    
    # Tìm kiếm câu trả lời từ danh sách reply
    def search(self, message):
        return self.dao.search(message)
        