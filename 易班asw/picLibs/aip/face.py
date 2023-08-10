
# -*- coding: utf-8 -*-

"""
人脸识别
"""

import re
import sys
import math
import time
from .base import AipBase
from .base import base64
from .base import json
from .base import urlencode
from .base import quote

class AipFace(AipBase):

    """
    人脸识别
    """

    __detectUrl = 'https://aip.baidubce.com/rest/2.0/face/v3/detect'

    __searchUrl = 'https://aip.baidubce.com/rest/2.0/face/v3/search'

    __multiSearchUrl = 'https://aip.baidubce.com/rest/2.0/face/v3/multi-search'

    __userAddUrl = 'https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/add'

    __userUpdateUrl = 'https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/update'

    __faceDeleteUrl = 'https://aip.baidubce.com/rest/2.0/face/v3/faceset/face/delete'

    __userGetUrl = 'https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/get'

    __faceGetlistUrl = 'https://aip.baidubce.com/rest/2.0/face/v3/faceset/face/getlist'

    __groupGetusersUrl = 'https://aip.baidubce.com/rest/2.0/face/v3/faceset/group/getusers'

    __userCopyUrl = 'https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/copy'

    __userDeleteUrl = 'https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/delete'

    __groupAddUrl = 'https://aip.baidubce.com/rest/2.0/face/v3/faceset/group/add'

    __groupDeleteUrl = 'https://aip.baidubce.com/rest/2.0/face/v3/faceset/group/delete'

    __groupGetlistUrl = 'https://aip.baidubce.com/rest/2.0/face/v3/faceset/group/getlist'

    __personVerifyUrl = 'https://aip.baidubce.com/rest/2.0/face/v3/person/verify'

    __videoSessioncodeUrl = 'https://aip.baidubce.com/rest/2.0/face/v1/faceliveness/sessioncode'

    __verifyUrl = "https://aip.baidubce.com/rest/2.0/face/v4/mingjing/verify"

    __faceMatchUrlV4 = 'https://aip.baidubce.com/rest/2.0/face/v4/mingjing/match'

    __onlinePictureLiveV4 = 'https://aip.baidubce.com/rest/2.0/face/v4/faceverify'


    def detect(self, image, image_type, options=None):
        """
            人脸检测
        """
        options = options or {}

        data = {}
        data['image'] = image
        data['image_type'] = image_type

        data.update(options)
        return self._request(self.__detectUrl, json.dumps(data, ensure_ascii=False), {
            'Content-Type': 'application/json',
        })
    
    def search(self, image, image_type, group_id_list, options=None):
        """
            人脸搜索
        """
        options = options or {}

        data = {}
        data['image'] = image
        data['image_type'] = image_type
        data['group_id_list'] = group_id_list

        data.update(options)
        return self._request(self.__searchUrl, json.dumps(data, ensure_ascii=False), {
            'Content-Type': 'application/json',
        })
    
    def multiSearch(self, image, image_type, group_id_list, options=None):
        """
            人脸搜索 M:N 识别
        """
        options = options or {}

        data = {}
        data['image'] = image
        data['image_type'] = image_type
        data['group_id_list'] = group_id_list

        data.update(options)
        return self._request(self.__multiSearchUrl, json.dumps(data, ensure_ascii=False), {
            'Content-Type': 'application/json',
        })
    
    def addUser(self, image, image_type, group_id, user_id, options=None):
        """
            人脸注册
        """
        options = options or {}

        data = {}
        data['image'] = image
        data['image_type'] = image_type
        data['group_id'] = group_id
        data['user_id'] = user_id

        data.update(options)
        return self._request(self.__userAddUrl, json.dumps(data, ensure_ascii=False), {
            'Content-Type': 'application/json',
        })
    
    def updateUser(self, image, image_type, group_id, user_id, options=None):
        """
            人脸更新
        """
        options = options or {}

        data = {}
        data['image'] = image
        data['image_type'] = image_type
        data['group_id'] = group_id
        data['user_id'] = user_id

        data.update(options)
        return self._request(self.__userUpdateUrl, json.dumps(data, ensure_ascii=False), {
            'Content-Type': 'application/json',
        })
    
    def faceDelete(self, user_id, group_id, face_token, options=None):
        """
            人脸删除
        """
        options = options or {}

        data = {}
        data['user_id'] = user_id
        data['group_id'] = group_id
        data['face_token'] = face_token

        data.update(options)
        return self._request(self.__faceDeleteUrl, json.dumps(data, ensure_ascii=False), {
            'Content-Type': 'application/json',
        })
    
    def getUser(self, user_id, group_id, options=None):
        """
            用户信息查询
        """
        options = options or {}

        data = {}
        data['user_id'] = user_id
        data['group_id'] = group_id

        data.update(options)
        return self._request(self.__userGetUrl, json.dumps(data, ensure_ascii=False), {
            'Content-Type': 'application/json',
        })
    
    def faceGetlist(self, user_id, group_id, options=None):
        """
            获取用户人脸列表
        """
        options = options or {}

        data = {}
        data['user_id'] = user_id
        data['group_id'] = group_id

        data.update(options)
        return self._request(self.__faceGetlistUrl, json.dumps(data, ensure_ascii=False), {
            'Content-Type': 'application/json',
        })
    
    def getGroupUsers(self, group_id, options=None):
        """
            获取用户列表
        """
        options = options or {}

        data = {}
        data['group_id'] = group_id

        data.update(options)
        return self._request(self.__groupGetusersUrl, json.dumps(data, ensure_ascii=False), {
            'Content-Type': 'application/json',
        })
    
    def userCopy(self, user_id, options=None):
        """
            复制用户
        """
        options = options or {}

        data = {}
        data['user_id'] = user_id

        data.update(options)
        return self._request(self.__userCopyUrl, json.dumps(data, ensure_ascii=False), {
            'Content-Type': 'application/json',
        })
    
    def deleteUser(self, group_id, user_id, options=None):
        """
            删除用户
        """
        options = options or {}

        data = {}
        data['group_id'] = group_id
        data['user_id'] = user_id

        data.update(options)
        return self._request(self.__userDeleteUrl, json.dumps(data, ensure_ascii=False), {
            'Content-Type': 'application/json',
        })
    
    def groupAdd(self, group_id, options=None):
        """
            创建用户组
        """
        options = options or {}

        data = {}
        data['group_id'] = group_id

        data.update(options)
        return self._request(self.__groupAddUrl, json.dumps(data, ensure_ascii=False), {
            'Content-Type': 'application/json',
        })
    
    def groupDelete(self, group_id, options=None):
        """
            删除用户组
        """
        options = options or {}

        data = {}
        data['group_id'] = group_id

        data.update(options)
        return self._request(self.__groupDeleteUrl, json.dumps(data, ensure_ascii=False), {
            'Content-Type': 'application/json',
        })
    
    def getGroupList(self, options=None):
        """
            组列表查询
        """
        options = options or {}

        data = {}

        data.update(options)
        return self._request(self.__groupGetlistUrl, json.dumps(data, ensure_ascii=False), {
            'Content-Type': 'application/json',
        })
    
    def personVerify(self, image, image_type, id_card_number, name, options=None):
        """
            身份验证
        """
        options = options or {}

        data = {}
        data['image'] = image
        data['image_type'] = image_type
        data['id_card_number'] = id_card_number
        data['name'] = name

        data.update(options)
        return self._request(self.__personVerifyUrl, json.dumps(data, ensure_ascii=False), {
            'Content-Type': 'application/json',
        })
    
    def videoSessioncode(self, options=None):
        """
            语音校验码接口
        """
        options = options or {}

        data = {}

        data.update(options)
        return self._request(self.__videoSessioncodeUrl, json.dumps(data, ensure_ascii=False), {
            'Content-Type': 'application/json',
        })
    

    __faceverifyUrl = 'https://aip.baidubce.com/rest/2.0/face/v3/faceverify'

    def faceverify(self, images):
        """
            在线活体检测
        """

        return self._request(self.__faceverifyUrl, json.dumps(images, ensure_ascii=False), {
            'Content-Type': 'application/json',
        })

    __matchUrl = 'https://aip.baidubce.com/rest/2.0/face/v3/match'

    def match(self, images):
        """
            人脸比对
        """

        return self._request(self.__matchUrl, json.dumps(images, ensure_ascii=False), {
            'Content-Type': 'application/json',
        })

    def faceMingJingVerify(self, id_card_number, name, image, options=None):
        """
            人脸 - 人脸实名认证V4
        """
        options = options or {}

        data = {}
        data['id_card_number'] = id_card_number
        data['name'] = name
        data['image'] = image

        data.update(options)
        return self._request(self.__verifyUrl, json.dumps(data, ensure_ascii=False),
                             {'Content-Type': 'application/json;charset=utf-8'})

    def faceMingJingMatch(self, image, imageType, registerImage, registerImageType, options=None):
        """
            人脸 - 人脸对比V4
        """
        options = options or {}

        data = {}
        data['image'] = image
        data['image_type'] = imageType
        data['register_image'] = registerImage
        data['register_image_type'] = registerImageType

        data.update(options)
        return self._request(self.__faceMatchUrlV4, json.dumps(data, ensure_ascii=False),
                             {'Content-Type': 'application/json;charset=utf-8'})

    def onlinePictureLiveV4(self, sdkVersion, options=None):
        """
            人脸 - 在线图片活体V4
        """
        options = options or {}

        data = {}
        data['sdk_version'] = sdkVersion

        data.update(options)
        return self._request(self.__onlinePictureLiveV4, json.dumps(data, ensure_ascii=False),
                             {'Content-Type': 'application/json;charset=utf-8'})



