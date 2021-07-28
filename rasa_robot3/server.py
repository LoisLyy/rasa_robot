from flask import Flask, jsonify
from flask import request
import requests
import json
import logging

app = Flask(__name__)


@app.route('/ai', methods=['GET', 'POST'])
def webToBot():
    """
    前端调用接口
        路径：/ai
        请求方式：GET、POST
        请求参数：content
    :return: response rasa响应数据
    """
    content = request.values.get('content')
    id = request.values.get('id')
    if id is None:
        return 'empty id'
    if content is None:
        return 'empty input'
    response = requestRasabotServer(id,content)
    # return response.text
    # utf-8转中文
    return response.text.encode('utf-8').decode("unicode-escape")


def requestRasabotServer(userid,content):
    """
        访问rasa服务
    :param userid: 用户id
    :param content: 自然语言文本
    :return:  json格式响应数据
    """
    params = {'sender': userid,'message': content}
    botIp = '127.0.0.1'
    botPort = '5005'
    # https://rasa.com/docs/rasa/user-guide/connectors/your-own-website/#rest-channels
    # POST /webhooks/rest/webhook
    rasaUrl = "http://{0}:{1}/webhooks/rest/webhook".format(botIp, botPort)
    return requests.post(
        rasaUrl,
        data=json.dumps(params),
        headers={'Content-Type': 'application/json'}
    )


if __name__ == '__main__':

    webIp = '127.0.0.1'
    webPort = '8088'
    app.run(
        host=webIp,
        port=int(webPort),
        threaded=True,
        debug=True
    )
    

