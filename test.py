from dao.reply_dao import ReplyDao
from dao.word_dao import WordDao
from tool import text_tool
from bean.list_data import ListData
from bean.reply import Reply
from bean.logic_reply import LogicReply
from bean.list_logic_data import ListLogicData


'''
Test list_data & reply
'''

a = ListData()
a.addData(Reply('master là ai', ['bạn là master','bạn là master chứ ai nữa','bạn là master của tôi']))
a.addData(Reply('alice là ai', ['tôi là alice','tôi là trợ lý ảo alice','tôi là alice...trợ lý ảo của bạn']))
a.addData(Reply('alice ăn cơm chưa', ['tôi không biết ăn cơm','tôi không cần ăn cơm','tôi không thể ăn cơm']))
print(a.size())

result = a.search('Bạn Ăn cơm chưa')
if result is not None:
    print(result.chooseAnswer())
    print(result.toString())
else:
    print('Xin lỗi master. tôi không hiểu câu này!')


'''
Test logic_reply & list_logic_data
'''

# a = LogicReply('ăn&cơm', ['alice không biết ăn', 'master biết nấu ăn không'])
# a.addAnswer('alice làm gì biết nấu cơm|alice chịu thôi, ko biết nấu cơm')
# b = LogicReply('đi|go', ['đi đâu', 'đi đâu đây'])
# b.addAnswer('alice nên đi đâu đây')
# listLogic = ListLogicData()
# listLogic.addData(a)
# listLogic.addData(b)
# print(listLogic.size())
# result = listLogic.search('Em ăn cơm chưa')
# if result is not None:
#     print(result.chooseAnswer())
#     print(result.toString())
# else:
#     print('Xin lỗi master. tôi không hiểu câu này!')

'''
Test word_dao
'''
# text = 'Như vẬy thì phải làm sao? sao không nghĩ ra được nhỉ?Chắc là do ý trời rồi'
# text = text.lower()
# WordDao.load() # load dữ liệu
# result = WordDao.similarMessages(text)
# for i in result:
#     print(i)

