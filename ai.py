#encoding=utf-8
import tool
import time

tool.getChats()
tool.saySomething()
time.sleep(30)
while True:
    tool.getChats()
    if u'系統' == tool.chats[tool.chats_key[-1]]['name']:
        time.sleep(60*10)
    else:
        tool.saySomething()
        time.sleep(60*4)
