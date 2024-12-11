import json
import os
import aliWangWangConfig


def updateCookie(userName, cookie):
    cookiePath = aliWangWangConfig.aliWangWangConfig['aliWangWang']['cookieDir']
    cookieFile = cookiePath + userName + '.cookie'

    if os.path.exists(cookieFile):
        os.remove(cookieFile)

    with open(cookieFile, 'w') as file:
        file.write(json.dumps(cookie))

    return "OK"

