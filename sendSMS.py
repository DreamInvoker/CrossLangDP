"""
    使用Twilio官网提供的免费的信息服务，每个月15美元的额度
    使用前请安装twilio：pip install twilio
    每条短信0.028美元，每个月可以发500多条短信，所以尽量只在需要的时候调用该接口发送短信。
"""
from twilio.rest import Client


def send(msg='No Content.', to="+8618813092702"):
    """
        发送短信
    :param msg: 短信内容
    :param to: 接收号码
    :return:
    """
    account_sid = 'AC6211336838c38a445b7c5c7b237b4510'
    auth_token = 'ab0b9ab3911d4f87a2d26628ead3d6ca'
    from_number = '+19786366084'

    client = Client(account_sid, auth_token)
    try:
        client.messages.create(to=to, from_=from_number, body=msg)
        # print('短信已经发送：\nfrom:\t{}\nto:\t{}\ncontent:\t\t{}\n'.format(from_number,to.split('+86')[1],msg))
    except Exception as e:
        # print('短信发送失败，账号欠费或者未被验证！')
        return e