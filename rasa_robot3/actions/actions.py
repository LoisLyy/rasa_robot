# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
from typing import Dict, Text, Any, List
from rasa_sdk import Tracker, Action
from rasa_sdk.events import UserUtteranceReverted, Restarted, SlotSet,AllSlotsReset,ConversationPaused,ConversationResumed
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
# import rasa_sdk.events
import random
import logging
import json
logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.DEBUG)
from requests import (
    ConnectionError,
    HTTPError,
    TooManyRedirects,
    Timeout
)
filename="huashu.json"
businessList=["报案","救援","保单信息查询","理赔进度查询","退保"]
with open(filename,"r",encoding="utf-8") as f:
    jsonText=json.loads(f.read().splitlines()[0])
# 根据业务和车险类型选择话术和标签(正常的业务类型)
class ActionactionHandleBusinessAbountInsurance(Action):    
    def name(self) -> Text:
        return "action_handle_businessAbountInsurance"
    def run(self,
            dispatcher:CollectingDispatcher,
            tracker:Tracker,
            domain:Dict[Text,Any])->List[Dict[Text,Any]]:
        insurance=tracker.get_slot('insurance')
        business=tracker.get_slot('business')
        entity="insurance"
        global filename,jsonText        
        domain=jsonText["domain"]
        logging.debug(tracker)
        for item in domain:
            intentValue=item["value"]
            if business in intentValue:
                event1=SlotSet(key = "business", value = intentValue)
                # 根据用户现在发起的业务，决定该业务完成时应该为用户返回的话术
                otherBusiness=[]
                global businessList
                for item1 in businessList:
                    if item1!=intentValue:
                        otherBusiness.append(item1)
                event2=SlotSet(key = "otherBusiness", value =','.join(otherBusiness) )
                #   选择现在要返回给用户的话术
                for item2 in item["entities"]:
                    if "entity" in item2:
                        if item2["entity"]==entity:
                            for item3 in item2["content"]:
                                if item3["value"]==insurance:
                                    huashu=item3["huashu"]
                                    tag= item3["tag"]
                                    event3=SlotSet(key = "huashu", value = huashu )
                                    event4=SlotSet(key = "tag", value = tag)
                                    event5=SlotSet(key = "businesstoIvr", value = insurance+intentValue)
                                    return [event1,event2,event3,event4,event5]
                                       
flag=0
# 用户输入数字时，判断用户的选择
class ActionHandleChoose(Action):    
    def name(self) -> Text:
        return "action_handle_choose"
    def run(self,
            dispatcher:CollectingDispatcher,
            tracker:Tracker,
            domain:Dict[Text,Any])->List[Dict[Text,Any]]:   
        orderNumber=tracker.get_slot('orderNumber')
        insurance=tracker.get_slot('insurance')
        business=tracker.get_slot('business')
        # 非车险报案用户输入数字
        if insurance=="非车险" and business=="报案":
            event=SlotSet(key = "businesstoIvr", value = "非车险报案") 
            global flag
            if orderNumber=="1":
                if flag==2:
                    event1=SlotSet(key = "huashu", value = "非车险报案自助操作方式已通过短信方式发送到您的手机，请您注意查收。")
                    event2=SlotSet(key = "tag", value = "sendMessage")
                    flag=0 
                    return [event1,event2,event]
                    # return [AllSlotsReset(),event1,event2]
                else:
                    event1=SlotSet(key = "huashu", value = "为了提升服务体验，现在为您转接人工，请稍等")
                    event2=SlotSet(key = "tag", value = "transfer") 
                    flag=0 
                    return [event1,event2]
                    # return [AllSlotsReset(),event1,event2]
            elif orderNumber=="2":
                if flag==1:
                    event1=SlotSet(key = "huashu", value = "尊敬的客户，现在您可以通过自助渠道进行非车险报案。同意请按^1，转人工请按^2")
                    event2=SlotSet(key = "tag", value = "choose")
                    flag+=1
                    return [event1,event2]    
                elif flag==0:
                    event1=SlotSet(key = "huashu", value = "请问本次事故的受损金额是否已达到或超过人民币3000元？是请按^1，否请按^2")
                    event2=SlotSet(key = "tag", value = "chooseMoney")
                    flag+=1 
                    return [event1,event2]                
                elif flag==2:
                    event1=SlotSet(key = "huashu", value = "正在为您转接人工，请稍等。")
                    event2=SlotSet(key = "tag", value = "transfer")
                    flag=0 
                    return [event1,event2]
                    # return [AllSlotsReset(),event1,event2]
        # 判断用户选择的是自助服务还是人工服务
        else:
            if orderNumber=="1":
                event1=SlotSet(key = "huashu", value = insurance+business+"的自助操作方式已通过短信方式发送到您的手机，请您注意查收。")
                event2=SlotSet(key = "tag", value = "sendMessage") 
                event3=SlotSet(key = "businesstoIvr", value = insurance+business) 
                return [event1,event2,event3]
                # return [AllSlotsReset(),event1,event2]
            elif orderNumber=="2":
                event1=SlotSet(key = "huashu", value = "正在为您转接人工，请稍等")
                event2=SlotSet(key = "tag", value = "transfer") 
                # return [AllSlotsReset(),event1,event2]
                return [event1,event2]

# 异议处理
class ActionHandleObjection(Action):    
    def name(self) -> Text:
        return "action_handle_objection"
    def run(self,
            dispatcher:CollectingDispatcher,
            tracker:Tracker,
            domain:Dict[Text,Any])->List[Dict[Text,Any]]:
        objection=tracker.get_intent_of_latest_message()
        global filename,jsonText,businessList        
        domain=jsonText["domain"]
        # logging.debug(domain)
        for item in domain:
            intent=item["intent"]
            if objection==intent:
                huashu=item["huashu"]
                intentValue=item["value"]
                tag= item["tag"]
                event1=SlotSet(key = "huashu", value = huashu )
                event2=SlotSet(key = "tag", value = tag)
                event3=SlotSet(key = "otherBusiness", value =','.join(businessList) )
                event4=SlotSet(key = "businesstoIvr", value = intentValue) 
                if tag=="voice" or tag=="sendMessage" :
                    event5=SlotSet(key = "ifEnd", value = "1")
                    return [AllSlotsReset(),event1,event2,event3,event4,event5]
                else:
                    return [AllSlotsReset(),event1,event2,event3,event4]

# 判断tag的值，来判断该业务是否已完成(异议处理)
class ActionJudgeTag2(Action):    
    def name(self) -> Text:
        return "action_judge_tag2"
    def run(self,
            dispatcher:CollectingDispatcher,
            tracker:Tracker,
            domain:Dict[Text,Any])->List[Dict[Text,Any]]:  
        ifEnd=tracker.get_slot('ifEnd')
        # 判断是否询问用户的其他需求
        if ifEnd=="1":
            dispatcher.utter_message(response = "utter_anything_else")
        return []

# 判断tag的值，来判断该业务是否已完成（正常业务）
class ActionJudgeTag(Action):    
    def name(self) -> Text:
        return "action_judge_tag"
    def run(self,
            dispatcher:CollectingDispatcher,
            tracker:Tracker,
            domain:Dict[Text,Any])->List[Dict[Text,Any]]:  
        huashu=tracker.get_slot('huashu')
        tag=tracker.get_slot('tag')
        otherBusiness=tracker.get_slot('otherBusiness')
        # 正常业务处理流程已结束，且需要询问客户其他需求，设置一个值标识业务完成
        if tag=="sendMessage":
            dispatcher.utter_message(response = "utter_anything_else")
            event1=SlotSet(key = "huashu", value = huashu)
            event2=SlotSet(key = "tag", value = tag)
            event3=SlotSet(key = "ifEnd", value = "1")
            event4=SlotSet(key = "otherBusiness", value = otherBusiness)
            return [AllSlotsReset(),event1,event2,event3,event4]
        elif tag=="transfer":
            return [AllSlotsReset()]
        else:
            return []

# 客户要求再说一遍，此时要判断ifEnd的值，如果为1要将tag改为voice
class ActionJudgeIfEnd(Action):    
    def name(self) -> Text:
        return "action_judge_ifEnd"
    def run(self,
            dispatcher:CollectingDispatcher,
            tracker:Tracker,
            domain:Dict[Text,Any])->List[Dict[Text,Any]]:  
        ifEnd=tracker.get_slot('ifEnd')
        if ifEnd=="1":
            tag="voice"
            event1=SlotSet(key = "tag", value = tag)
            return [event1] 
        else:
            return []

# 客户要求再说一遍，此时要判断ifEnd的值，如果为1要播放是否有其他需求的话术
class ActionJudgeIfEnd2(Action):    
    def name(self) -> Text:
        return "action_judge_ifEnd2"
    def run(self,
            dispatcher:CollectingDispatcher,
            tracker:Tracker,
            domain:Dict[Text,Any])->List[Dict[Text,Any]]:  
        ifEnd=tracker.get_slot('ifEnd')
        if ifEnd=="1":
            dispatcher.utter_message(response = "utter_anything_else") 
        return [] 

# 询问需求
# class ActionAnythingElse(Action):    
#     def name(self) -> Text:
#         return "action_anything_else"
#     def run(self,
#             dispatcher:CollectingDispatcher,
#             tracker:Tracker,
#             domain:Dict[Text,Any])->List[Dict[Text,Any]]:  
#         business=tracker.get_slot('business')
#         otherBusiness=[]
#         global businessList
#         if business!=None:
#             for item in businessList:
#                 if item!=business:
#                     otherBusiness.append(item)
#             event=SlotSet(key = "otherBusiness", value =','.join(otherBusiness) )
#             # dispatcher.utter_message(response = "utter_to_ivr") 
#             return [event]
#         else:
#             event=SlotSet(key = "otherBusiness", value =','.join(businessList) )
#             # dispatcher.utter_message(response = "utter_to_ivr") 
#             return [event]


# 重启对话
class ActionRestart(Action):    
    def name(self) -> Text:
        return "action_restart"
    def run(self,
            dispatcher:CollectingDispatcher,
            tracker:Tracker,
            domain:Dict[Text,Any])->List[Dict[Text,Any]]:   
        # dispatcher.utter_message(response = "utter_to_ivr") 
        return [Restarted()]

# 重置槽值
class ActionRestart(Action):    
    def name(self) -> Text:
        return "action_resetSlot"
    def run(self,
            dispatcher:CollectingDispatcher,
            tracker:Tracker,
            domain:Dict[Text,Any])->List[Dict[Text,Any]]:   
        # dispatcher.utter_message(response = "utter_to_ivr") 
        return [AllSlotsReset()]