#import libraries
import os
import playsound
import speech_recognition as sr
import time
import sys
import ctypes
import wikipedia
import datetime
import json
import re
import webbrowser
import smtplib
import requests
import urllib
import urllib.request as urllib2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from time import strftime
from gtts import gTTS
from youtube_search import YoutubeSearch


#import libraries
from tool import text_tool
from bean.reply import Reply
from bo.reply_bo import ReplyBo
from bo.logic_reply_bo import LogicReplyBo
from dao.word_dao import WordDao
from dao import line_file
from speak import speak as alice
from tool import text_tool as TextTool
from core.master_info import Master
from core import message_analysis as MessageAnalysis
from tool import function as Function
from util.constant import Constant

# Khởi tạo
wikipedia.set_lang('vi')
language = 'vi'
path = ChromeDriverManager().install()



class AliceSystem:
    getInputType = 10
    rememberReply = None
    defaultReplyList = None
    def __init__(self):
        print('Alice System Init')
        self.replyBo = ReplyBo()
        self.logicReplyBo = LogicReplyBo()
        WordDao.load()
        AliceSystem.defaultReplyList = line_file.getFileInTrain('default_ans')
    
    


    def run(self):
        alice.speak('Hello ' + Master.name)
        time.sleep(1)
        AliceSystem.getInputType = 10
        while True:
            text = ''

            # lấy tin nhắn
            if AliceSystem.getInputType < 3: 
                text = alice.listen()
                time.sleep(2)

            elif AliceSystem.getInputType == 3:
                alice.speak('Tự động chuyển sang chế độ nhập tin nhắn!')
                AliceSystem.getInputType = 10
                text = alice.get_text()
            
            else: 
                text = alice.get_text()
            
            # kiểm tra tin nhắn
            if not text:
                AliceSystem.getInputType += 1
                alice.speak('Alice không nghe rõ...')
                time.sleep(3)
            
            else:
                if AliceSystem.getInputType < 3:
                    AliceSystem.getInputType = 0 #reset
                text = text.lower().strip()
                if len(text) == 0:
                    continue
                #print('Text:['+ text+']')
                if text == 'bye' or text == 'tạm biệt' or text == 'bye bye' or text == 'goodbye':
                    alice.stop()
                    break
                
                elif text == 'mở nhận dạng giọng nói':
                    AliceSystem.getInputType = 0
                    alice.speak('Đã chuyển sang chế độ nhận dạng giọng nói!')
                
                elif text == 'tắt nhận dạng giọng nói':
                    AliceSystem.getInputType = 10
                    alice.speak('Đã chuyển sang chế độ nhập tin nhắn!')
                
                elif text == 'help':
                    print(Constant.HELP)

                else:
                    if AliceSystem.rememberReply is not None: # đang yêu cầu train thêm dữ liệu
                        if text.startswith('trả lời'): # master đang train dữ liệu
                            text = text.replace('trả lời ', '')
                            text = text.replace(' hoặc ', '|') # phân tách thành các câu trả lời riêng biệt
                            AliceSystem.rememberReply.addAnswer(text) # train thêm câu trả lời 
                            firstChar = AliceSystem.rememberReply.message[0]
                            self.replyBo.saveListMess(TextTool.getUnsignedChar(firstChar))
                            alice.speak('Cảm ơn master. Alice sẽ ghi nhớ!')
                            AliceSystem.rememberReply = None # reset rememberReply
                        else: # xem như một tin nhắn thông thường
                            AliceSystem.rememberReply = None # reset rememberReply cũ
                            replyMessage = self.answer(text) # tìm câu trả lời
                            if replyMessage is None:
                                alice.speak('Alice nên trả lời như thế nào ạ?')
                            else:
                                alice.speak(replyMessage)
                    else:
                        replyMessage = self.answer(text) # tìm câu trả lời
                        if replyMessage is None:
                            alice.speak('Alice nên trả lời như thế nào ạ?')
                        else:
                            alice.speak(replyMessage)

                        
    
    def answer(self, message):
        # type 1: trả lời mặc định
        #TODO: viết code

        # type 2: yêu cầu chức năng
        #print('Trả lời cho tin nhắn: ' + message)
        #print('Kiểm tra có phải là tin nhắn yêu cầu chức năng không!')
        result = MessageAnalysis.functionLogic(message)
        if result is not None:
            #print('Tìm thấy chức năng trùng khớp!')
            return result
        #print('Không phải yêu cầu chức năng!')

        #type 3: trả lời bằng data

        # chuẩn hoá tin nhắn
        message = TextTool.standardMessageForTraining(message)
        message = message.strip()
        #print('Kết quả chuẩn hoá tin nhắn:[' + message + ']')

        #print('Tìm kiếm trong reply_bo!')
        reply = self.findAnswerInReplyData(message) #object type: Reply
        if reply is not None:
            #print('Tìm thấy reply trùng khớp!')
            if Function.random(29) == 12: 
                #print('Lựa chọn train thêm dữ liệu!')
                AliceSystem.rememberReply = reply # lưu vào rememberReply
                return None
            else:
                result = reply.chooseAnswer()
                return result
        else:
            #print('Không tìm thấy reply trùng khớp!')
            if Function.random(12) == 2:
                #print('Lựa chọn train thêm dữ liệu!')
                reply = Reply(message, []) # Tạo mới một Reply
                self.replyBo.addData(reply) # Lưu vào replyBo
                AliceSystem.rememberReply = reply # lưu lại reply để train
                return None
            else:
                # Tìm kiếm theo từ khoá
                #print('Tìm kiếm câu trả lời theo từ khoá!')
                logicAnswer = self.findAnswerInLogicReplyData(message) # type: LogicReply
                if logicAnswer is not None: # Tìm thấy kết quả theo từ khoá
                    #print('Tìm thấy logic reply trùng khớp!')
                    return logicAnswer.chooseAnswer()
                # Không tìm thấy kết quả theo từ khoá
                #print('Không tìm thấy logic reply trùng khớp!')
                if Function.random(6) != 2:
                    #print('Trả lời ngẫu nhiên từ dữ liệu mặc định!')
                    defaultListSize = len(AliceSystem.defaultReplyList)
                    if defaultListSize > 0: # Nếu list rep mặc định không rỗng
                        pos = Function.random(defaultListSize)
                        return AliceSystem.defaultReplyList[pos] # Chọn một câu trả lời ngẫu nhiên để phản hồi
                # Xui thì vào đây train thêm dữ liệu...hhh
                #print('Yêu cầu train thêm dữ liệu')
                reply = Reply(message, []) # Tạo mới một Reply
                self.replyBo.addData(reply) # Lưu vào replyBo
                AliceSystem.rememberReply = reply # lưu lại reply để train
                return None


    '''
    Tìm kiếm trong reply list.
    Giới hạn độ dài tìm kiếm là 20 từ. Nếu quá trả về None.
    Trả về 1 Reply hoặc None
    '''
    def findAnswerInReplyData(self, message):
        if len(message.split(' ')) > 20:
            return None 
        
        # tìm kiếm dữ liệu từ replyBo
        result = self.replyBo.search(message)
        return result


    '''
    Tìm kiếm trong logicreply list.
    Giới hạn độ dài tìm kiếm là 20 từ. Nếu quá trả về None.
    Trả về 1 LogicReply hoặc None
    '''
    def findAnswerInLogicReplyData(self, message):
        if len(message.split(' ')) > 20:
            return None 
        
        # tìm kiếm dữ liệu từ logicReplyBo
        result = self.logicReplyBo.search(message)
        return result