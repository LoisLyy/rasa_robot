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
filename="1.json"
# 根据业务和车险类型选择话术和标签
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

        global filename
        with open(filename,"r",encoding="utf-8") as f:
            domain=json.loads(f.read().splitlines()[0])
            domain=domain["domain"]
            # logging.debug(domain)
            for item in domain:
                intentValue=item["value"]
                if business in intentValue:
                    event1=SlotSet(key = "business", value = intentValue)
                    for item2 in item["entities"]:
                        if "entity" in item2:
                            if item2["entity"]==entity:
                                for item3 in item2["content"]:
                                    if item3["value"]==insurance:
                                        huashu=item3["huashu"]
                                        tag= item3["tag"]
                                        event2=SlotSet(key = "huashu", value = huashu )
                                        event3=SlotSet(key = "tag", value = tag)
                                        if tag!="choose":
                                            return [AllSlotsReset(),event2,event3]
                                        else:
                                            return [event1,event2,event3]
flag=0
# 判断用户选择自助还是人工
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
        if insurance=="非车险" and business=="报案":
            global flag
            if orderNumber=="1":
                if flag==2:
                    event1=SlotSet(key = "huashu", value = "非车险报案自助操作方式已通过短信方式发送到您的手机，请您注意查收。")
                    event2=SlotSet(key = "tag", value = "sendMessage")
                    flag=0 
                    return [AllSlotsReset(),event1,event2]
                else:
                    event1=SlotSet(key = "huashu", value = "为了提升服务体验，现在为您转接人工，请稍等")
                    event2=SlotSet(key = "tag", value = "transfer") 
                    flag=0 
                    return [AllSlotsReset(),event1,event2]
            elif orderNumber=="2":
                if flag==1:
                    event1=SlotSet(key = "huashu", value = "尊敬的客户，现在您可以通过自助渠道进行非车险报案。同意请按^1，转人工请按^2")
                    event2=SlotSet(key = "tag", value = "choose")
                    flag+=1
                    return [event1,event2]    
                elif flag==0:
                    event1=SlotSet(key = "huashu", value = "请问本次事故的受损金额是否已达到或超过人民币3000元？是请按^1，否请按^2")
                    event2=SlotSet(key = "tag", value = "choose")
                    flag+=1 
                    return [event1,event2]                
                elif flag==2:
                    event1=SlotSet(key = "huashu", value = "正在为您转接人工，请稍等。")
                    event2=SlotSet(AllSlotsReset(),key = "tag", value = "transfer")
                    flag=0 
                    return [AllSlotsReset(),event1,event2]
        else:
            if orderNumber=="1":
                event1=SlotSet(key = "huashu", value = insurance+business+"的自助操作方式已通过短信方式发送到您的手机，请您注意查收。")
                event2=SlotSet(key = "tag", value = "sendMessage") 
                return [AllSlotsReset(),event1,event2]
            elif orderNumber=="2":
                event1=SlotSet(key = "huashu", value = "正在为您转接人工，请稍等")
                event2=SlotSet(key = "tag", value = "transfer") 
                return [AllSlotsReset(),event1,event2]
        

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