# -*- coding: utf-8 -*-
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from lxml import etree
import os
from time import sleep
from exams import exams
from exams import test_paper_url
import pymysql
from aip import AipOcr


#client = AipOcr("27050570", "Sljjc2nLRuK4frw3XxMsTpWS", "CFbMkcU40vQEk9FUTaXB1tFq8XrGharW")
# client = AipOcr("26927784", "0HNsy6ms392XDGz7GKhnHqYa", "cEWj4fZi22MeWyn1NBcKjjeUIAtj7v2Y")
client = AipOcr("27051113", "atVcIQeoKkFK9a0QDk2BxeD0", "XolQgtKGQznwCiZxELWbrXDLGMHwenhR")

wd = webdriver.Chrome()
#设置最大等待时长为30秒
wd.implicitly_wait(2)

#从数据库获取用户
def get_user(id):
    db = pymysql.connect(host="127.0.0.1", user="root",
                         password="33333", database="2023new_student", port=3306)
    # 使用cursor（）方法创建一个游标对象cursor
    cursor = db.cursor()
    # 使用execute（）方法执行SQL
    sql = f"select * from user WHERE id ={id};"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            id = row[0]
            username = row[1]
            password = row[2]

            print(f"id={id},user={username},password={password}")
            user_dic = {"username": username, "password": password}
            return user_dic
    except:
        print("Error:找不到")

#进行登录
def login(username, password):
    wd.get("https://www.yooc.me/login")
    wd.find_element(By.NAME, 'email').send_keys(username)
    wd.find_element(By.NAME, 'password').send_keys(password)
    wd.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div[1]/form/div[5]/button').click()
    sleep(4)

    # input("输入任意字母回车继续:")

#获取登录的验证码
def get_login_code():
    # 获取验证码图片
    sleep(1)
    img = wd.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[1]/div[1]/div[3]/div/img")
    sleep(1)
    data = img.screenshot_as_png
    # print(type(data))
    # print(data)
    # 创建一个文件夹
    if not os.path.exists('./picLibs'):
        os.mkdir('./picLibs')
    # 请求图片进行持久化存储, content, 用于读取二进制数据
    img_data=data
    img_name="login.jpg"
     # requests.get(url=img_src,headers=headers).content
    img_path='picLibs/'+img_name
    with open(img_path,'wb') as fp:
        fp.write(img_data)
        print(img_name+'保存成功')

# 为新用户添加到课群
def add_course():
    wd.execute_script("arguments[0].click();", wd.find_element(By.XPATH,
                                                               '/html/body/div[2]/div[2]/table/tbody/tr/td/div[1]/div[1]/span[1]'))
    wd.find_element(By.XPATH,"/html/body/div[2]/div[2]/table/tbody/tr/td/div[1]/div[1]/div/input").send_keys("TQBR4QKB")

    sleep(2)
    wd.execute_script("arguments[0].click();", wd.find_element(By.XPATH,
                                                               '/html/body/div[2]/div[2]/table/tbody/tr/td/div[1]/div[1]/span[2]'))

    try:
        # string1 = wd.find_element(By.XPATH, "/html/body/div[2]/div[2]/table/tbody/tr/td/div[1]/div[4]/div[2]/span[2]").text
        # print(string1)
        #点击加入课群
        sleep(2)
        wd.find_element(By.XPATH, "/html/body/div[2]/div[2]/table/tbody/tr/td/div[1]/div[4]/div[2]/span[2]").click()
    except:
        # 点开考试页面
        # https: // www.yooc.me / group / 7228080 / exams?page = 2
        wd.get("https://www.yooc.me/group/7228080/exams")
        wd.refresh()


# 传入一个url并打开解析试卷，直到答完试卷
def get_one_asw(herf):
    # 打开试卷
    wd.get(herf)
    wd.refresh()
    q_text = wd.page_source
    tree2 = etree.HTML((q_text))
    question_list = tree2.xpath("/html/body/section/section/div[3]/div")
    # https: // www.yooc.me / group / 7228080 / exam / 368141 / detail
    exam_id_url = herf[39:-7]
    for exam in exams:
        exam_id = exam.get("exam_id")
        if exam_id == exam_id_url:
            questions = exam.get("questions")
            for question in questions:
                question_id = question.get("question_id")
                # print(question_id)
                answers = question.get("answers")
                # print(answers)
                for answer in answers:
                    # 题号+1+value  55185700_1_0
                    str =f"{question_id}_{answer}"
                    wd.find_element(By.XPATH, f'//*[@for="{str}"]').click()
                    sleep(0.1)
                    # wd.find_element(By.ID, "submit_paper").click()
            wd.execute_script("arguments[0].click();", wd.find_element(By.ID, 'submit_paper'))
            sleep(1)
            wd.find_element(By.XPATH, f'//*[@id="dlgc-2"]/button').click()
        else:
            pass

#第21套试卷的答题
def exam21():
    # 直接到21套卷子考试界面
    wd.get("https://exam.yooc.me/group/7228080/exam/368118")
    sleep(1)
    # 切到考试的小窗口
    wd.switch_to.window(wd.window_handles[-1])
    try:
        # 尝试找到“考试”、“继续考试”按钮
        start_exam_button = wd.find_element(By.CSS_SELECTOR, 'button[class="jsx-751469096 __ db primary size-l"]')
    except:
        # 找不到说明考过了,回到考试页第三页点击重做
        wd.get("https://www.yooc.me/group/7228080/exams?page=3")
        # 点击重做按钮
        wd.find_element(By.CLASS_NAME, "repeat").click()
        sleep(1)
        # 点击确认
        wd.find_element(By.NAME, "ok").click()
        sleep(1)

    # 点了重做之后再直接回到21套考试页面
    wd.get("https://exam.yooc.me/group/7228080/exam/368118")
    sleep(1)
    # 切窗口
    wd.switch_to.window(wd.window_handles[-1])
    # 重新找到考试按钮

    start_exam_button = wd.find_element(By.CSS_SELECTOR, 'button[class="jsx-751469096 __ db primary size-l"]')
    start_exam_button.click()
    sleep(1)
    # 尝试点击确定,因为继续考试不用确定
    try:
        wd.find_element(By.XPATH, '//*[@id="root"]/div[1]/div[2]/main/article/div[3]/div/div/div[2]/button[2]').click()
    except:
        pass
    sleep(3)
    # input("点击验证码并输入任意字符继续：")

    # 缩小页面
    print("开始考试")
    # print(wd.window_handles[-1])
    # wd.execute_script("document.body.style.zoom='0.8'")
    # print(wd.window_handles[-1])
    # wd.switch_to.window(wd.window_handles[-1])
    # 循环开始
    for i in range(25):
        # 获取题目
        question = wd.find_element(By.XPATH, '/ html / body / div[1] / div[1] / div[2] / main / main / div / div / div / div / h3 / div').text

        # 获取答案个数
        answer_count = len(
            wd.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/main/main/div/div/div/div/div/ul').find_elements(By.XPATH,
                                                                                                                 './li'))
        # 如果只有两个选项,说明是判断题,除了”杀猪盘“都选第二个
        try:
            if answer_count == 2:
                # 杀猪盘选第一项
                if "杀猪盘" in question:
                    wd.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/main/main/div/div/div/div/div/ul/li[1]').click()
                else:
                    wd.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/main/main/div/div/div/div/div/ul/li[2]').click()
            elif '某家贷款公司' in question:
                right=["不合理，陈某是已经被贷款诈骗了"]
                get_asw_list(right)
            elif '小王在网上购买一套衣服' in question:
                right = ["小王将会得到高价赔偿"]
                get_asw_list(right)
            elif '游戏账号挂在网上进行售卖' in question:
                right = ["A.不轻信他人，在正规平台正规交易"]
                get_asw_list(right)
            elif '当你买完飞机票' in question:
                right = ["上网搜索一下相关信息或向航空公司官方客服电话进行核实"]
                get_asw_list(right)
            elif '鉴于您信用良好' in question:
                right = ["不信，这是骗子套路"]
                get_asw_list(right)
            elif '贵人多忘事' in question:
                right = ["是典型的诈骗手段, 应挂断电话"]
                get_asw_list(right)
            elif ' 小鱼正在家里上网聊' in question:
                right = ["刷单的都是骗人的, 忽略"]
                get_asw_list(right)
            elif '小刘发来视频通话请求' in question:
                right = ["直接转账"]
                get_asw_list(right)
            elif '公安局的警官' in question:
                right = ["不相信，因为公安机关办案有严格程序，绝对不会在电话里办案"]
                get_asw_list(right)
            elif '新加坡来的交换生' in question:
                right = ["不轻信他人，找借口迅速离开"]
                get_asw_list(right)
            elif '银行电话称你涉嫌洗钱' in question:
                right = ["警方调查案件不可能通过电话进行",
                            "在调查案件时不会直接通过电话转接",
                            "不管公安机关还是检察机关",
                                "信用卡欠款是银行客服通知的"]
                get_asw_list(right)
            elif '小可同学在QQ上' in question:
                right = ["当面或打电话向张老师核实",
                            "现在QQ盗号诈骗案件很多",
                        "不能把钱款轻易汇入陌生账户"]

                get_asw_list(right)
            elif '接到电话：某某（你的名字' in question:
                right = ["挂掉电话，不在理会",
                        "不经核实不要汇款给任何人"]
                get_asw_list(right)
            elif '你收到一条尾号是' in question:
                right = ["点击短信里的网站链接",
                            "报警或向银行部门官方电话咨询",
                            "置之不理、删除短信"]
                get_asw_list(right)
            elif '你在网购过程中' in question:
                right = ["拨打对方提供的“客服号码”进行咨询",
                            "按照客服要求前往银行",
                            "登录对方提供的网址链接查验订单"]
                get_asw_list(right)
            elif '搭乘飞机回学校' in question:
                right = ["骗子设置的诱饵",
                    "这是人家好心"]
                get_asw_list(right)
            elif '三个凡是' in question:
                right = ["凡是自称行政",
                            "凡是未经认证的网站发布购物",
                            "凡是通过电话"]
                get_asw_list(right)
            elif '一位学生收到老师短信' in question:
                right = ["老师不会做这样的事",
                            "老师为什么考完不久就知道我的成绩",
                            "直接与老师取得联系"]
                get_asw_list(right)
            elif '自称金融公司工作人员' in question:
                right = ["不予理睬",
                            "不点链接",
                            "不注销账户也没有关系"]
                get_asw_list(right)
            elif '小王正在家中玩手机' in question:
                right = ["充值100元试试",
                            "对该返利活动深信不疑",
                            "如果收到返利再继续充值高金额"
                            ]
                get_asw_list(right)
        except:
            print(f"21套卷子第{i + 1}题出现异常,题目如下:")
            print(question)

            wd.find_element(By.XPATH, '//*[@id="root"]/div[1]/div[2]/main/ul/li[4]/button').click()
            continue
        wd.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/main/main/div/ul/li[4]/button').click()
        sleep(0.2)
    else:
        # input("请检查是否异常(输入任意字符提交):")
        # 提交试卷
        wd.find_element(By.XPATH, '//*[@id="root"]/div[1]/div[1]/div[3]/div/button').click()
        wd.find_element(By.XPATH, '//*[@id="root"]/div[1]/div[1]/div[3]/div/div/div/div[2]/button[2]').click()

#用于获取第21套试卷的答案，需要一个参数，
# 传入正确答案，遍历答案列表进行点击
def get_asw_list(rights):
    answer_count = len(
        wd.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/main/main/div/div/div/div/div/ul').find_elements(
            By.XPATH,
            './li'))

    # 获取答案列表
    asw_list = []
    i = 0
    # 正确答案列表
    as_right = rights

    # 获得li列表
    li_list = wd.find_elements(By.XPATH, '/html/body/div[1]/div[1]/div[2]/main/main/div/div/div/div/div/ul/li')

    # 获取li列表中的每一个li
    for li in li_list:
        # 遍历li获取答案列表
        s = li.find_element(By.XPATH, "./div[2]").text
        # print(s)
        asw_list.append(s)
        for right in as_right:
            if right in s:
                li.find_element(By.XPATH, "./div[1]").click()
                sleep(0.1)
            else:
                pass



#获取字母验证码，用于提交到输入框
def get_submit_code():
    # 获取验证码图片
    sleep(1)
    img = wd.find_element(By.XPATH, "/html/body/section/section/form/div[2]/div[2]/img")
    sleep(1)
    data = img.screenshot_as_png
    # print(type(data))
    # print(data)
    # 创建一个文件夹
    if not os.path.exists('./picLibs'):
        os.mkdir('./picLibs')
    # 请求图片进行持久化存储, content, 用于读取二进制数据
    img_data=data

    result = client.basicGeneral(data)
    verificationCode = result["words_result"][0]["words"]
    img_name="验证码2.jpg"
     # requests.get(url=img_src,headers=headers).content
    img_path='picLibs/'+img_name
    with open(img_path,'wb') as fp:
        fp.write(img_data)
        print(img_name+'保存成功')
    return  verificationCode

#话题的编写和提交
def write():
    title="树木树人"
    article="""
    西南林业大学是我国西部地区唯一独立设置的林业高校，经过多年发展，构建了从本科生教育、硕士研究生教育到博士研究生教育以及博士后研究的人才培养体系，形成了以林学、林业工程、风景园林等涉林学科为特色，林理融合、林工融合、林文融合，多学科协调发展的学科与专业格局，是国家卓越农林人才教育培养计划、卓越工程师教育培养计划高校、中西部高校基础能力建设工程支持院校。
    学校办学起源于1938年云南大学森林系，建校于1958年昆明农林学院，1973年与南迁昆明的北京林学院合并办学，成立云南林业学院。1978年北京林学院迁回北京办学后，学校更名为云南林学院，直属原国家林业部管理。1983年更名为西南林学院，2000年由原国家林业局直属高校调整为中央与地方共建，以省为主管理。2010年更名为西南林业大学。
    学校主动适应经济社会发展需要，不断调整优化学院架构，现设有林学院（亚太林学院）、材料与化学工程学院、园林园艺学院、生命科学学院、生态与环境学院、土木工程学院、生物多样性保护学院、大数据与智能工程学院、机械与交通学院、地理与生态旅游学院、湿地学院、数理学院、马克思主义学院、文法学院、经济管理学院、会计学院、外国语学院、艺术与设计学院·艺术博物馆、体育学院、继续教育学院（职业技术学院、农林干部学院）、国际学院等21个教学单位。
    学校现有全日制在校本科生24958人，硕士研究生3798人，博士研究生189人。有教职工1700余人。学校现有国家、省部级以上人才共249人次。国家百千万人才1人，国家高层次人才特殊支持计划科技创新领军人才1人，全国优秀教师2人，国家有突出贡献中青年专家1人，享受国务院特殊津贴专家3人，教育部原新世纪优秀人才2人。云南省“兴滇英才”支持计划122人，其中，科技领军人才1人、云岭学者5人、高端外国专家1人、创业人才1人、产业创新人才11人、教学名师9人、文化名家4人、青年人才90人。云南省有突出贡献优秀专业技术人才5人，享受云南省政府特殊津贴专家14人，省委联系专家13人，国家林草局教学名师3人，
    国家林业和草原科技创新领军人才3人，国家林业和草原青年拔尖人才2人，云南省中青年学术和技术带头人33人，云南省技术创新人才7人。
    学校高度重视教学工作，现设有本科专业83个，中外合作专业1个，第二学士学位专业10个，其中国家级第一类特色专业3个、国家卓越农林人才培养计划专业4个、国家卓越工程师培养计划专业3个、省级特色专业5个，国家一流专业建设点8个，省级一流专业建设点24个。获国家级教学成果二等奖1项，省级教学成果奖一等奖7项，二等奖19项。获批省部级质量工程项目500余项（含产学研项目52项），获省部级实践教学示范中心12个。“林学类专业基础实验教学中心”获批为国家级实验教学示范中心，“西南林业大学——楚雄市林业局紫金山林场理科综合实践教育基地”获批为国家级大学生校外实践教育基地。有国家级精品课程1门，
    国家级精品资源共享课1门，省级精品课程19门，省级精品视频公开课2门，省级精品资源共享课11门，国家级一流本科课程3门，省级一流本科课程35门，省级课程思政示范课程3门，省级课程思政教改项目3项。有全国高校黄大年式教师团队1个、省级高校黄大年式教师团队1个，获批教育部新农科研究与改革实践项目3项、新工科研究与实践项目2项（含参与1项）。云南省首批省级新文科研究与改革实践项目1项，云南省首批新工科研究与实践项目1项。学生在“互联网+”大学生创新创业大赛、
    全国大学生结构设计竞赛、全国大学生数学建模竞赛等比赛中取得优异成绩，学校创业园被评为省级青年创业示范园，林科类校园创业平台被认定为省级校园创业平台，是大学生KAB创业教育基地。学校被评为云南省省级创新创业学院、云南省高校毕业生创新创业典型经验高校、云南省深化创新创业教育改革示范高校、云南省大学生自主创业先进集体、云南省高校毕业生就业创业工作先进单位，全国普通高等学校毕业生就业工作先进集体。
    学校是国务院批准的首批硕士学位授予单位，具有博士学位授予权，有林学、林业工程、风景园林学、农林经济管理4个博士后科研流动站，是推荐优秀应届本科毕业生免试攻读研究生高校。现有一级学科博士点4个、一级学科硕士点15个、专业硕士学位点15个，国家林业和草原局重点学科6个、培育学科1个，省级重点学科5个、省级优势特色重点建设学科2个，省院省校合作咨询共建学科2个，A类高峰学科1个、B类高峰学科2个、B类高峰学科优势特色研究方向1个，A类高原学科2个。2022年获批云南省重点支持建设一流学科3个、特色学科建设计划4个、新学科培育计划1个。学校植物与动物科学进入ESI全球排名前1
    学校获批成立林业生物质资源高效利用技术国家地方联合工程研究中心、生物质材料国际联合研究中心、西南山地森林资源保育与利用教育部重点实验室、国家高原湿地研究中心、云南生物多样性研究院、云南森林资源资产管理及林权制度研究基地。有国家林业和草原长期科研基地3个，国家林业和草原局重点实验室3个、工程技术研究中心2个、检验检测中心1个、生态系统定位研究站3个、创新联盟3个。
    有省级工程实验室1个、省级工程研究中心4个、省级重点实验室4个、省级工程技术研究中心1个、省级野外科学观测研究站 1个、省级国际联合研究中心2个、省级国际科技合作基地1个、省级面向南亚东南亚科技创新中心2个。有院士工作站5个、专家工作站10个。有协同创新中心1个、
    省高校重点实验室13个、省高校工程研究中心6个、昆明市工程技术研究中心2个、昆明市国际研发中心1个。设有中国林学会国家公园分会、中国林学会古树名木分会、云南省生态文明建设研究与发展促进会。有各级各类自然科学类创新团队22个，省级哲学社会科学创新团队4个、研究基地1个、智库2个，社科普及基地2个。
    2010年至今先后荣获云南省哲学社会科学成果奖二等奖1项，三等奖40项。2023年荣获云南省社会科学奖二等奖1项，三等奖3项。先后获国家科技进步奖二等奖2项、全国创新争先奖1项、教育部高等学校科学研究科技进步奖一等奖1项、云南省“科学技术杰出贡献奖”1项、云南省科学技术奖一等奖8项、梁希林业科学技术奖一等奖1项、何梁何利奖1项。办有《西南林业大学学报（自然科学）》《西南林业大学学报（社会科学）》。
    学校现有林业调查规划设计甲B级资质证书、木材与木竹制品质量检验检测计量认证资质证书、生产建设项目水土保持方案编制乙级资格证书、生产建设项目水土保持监测乙级资格证书、风景园林工程设计专项乙级、建筑行业建筑工程丙级资质、旅游规划设计乙级资质证书，发挥区域、行业和学科优势，主动参与服务经济社会发展，在生物多样性与自然保护区管理、森林培育、森林保护、竹藤研究、木质科学与技术、高原湿地等方面在国内有一定优势，
    一些领域居于国内同类研究前沿；在园林规划设计、生态旅游等领域具有明显的区域特色；在蚁类、鸟类、鱼类等方面研究取得突出成绩，社会影响日益扩大，受到国家林业和草原局及云南省委、省政府多次表彰和奖励。
    学校立足特色学科、发挥区位优势，不断加强国际合作与交流。学校与21个国家和地区的60余所高校和研究机构签署合作协议；在非洲马里共建孔子学院及孔子课堂各1所，孔子课堂获全球先进孔子课堂奖，孔子课堂外方负责人获首批“孔子学院院长纪念奖章”。获批与俄罗斯南乌拉尔国立大学合作举办机械电子工程专业本科教育项目；与不列颠哥伦比亚大学（UBC）林学院合作共建亚太林学院；
    通过各类留学项目选派优秀师生赴外学习深造，培养高素质国际化人才。学校外籍专家曾获得中国政府“友谊奖”、云南省政府“彩云奖”及云南省科学技术合作奖。入选国家“高等学校学科创新引智计划”地方高校新建基地。留学生生源国覆盖五大洲20余国，涵盖本科、硕士和博士学历留学生及非学历留学生。学校与国家林业和草原局共建的亚太森林组织昆明中心，
    连续数年面向南亚、东南亚、南太平洋岛国等27个经济体举办国际培训班，培训林业中高级官员和科研人员百余名。与北京林业大学、中国林科院、普洱市等签订战略合作协议，服务经济社会发展能力和水平不断提升。
    学校占地2500余亩，馆藏纸质图书194.78万册，电子图书近82万册，中外文数据库23个。标本馆藏有各类标本50余万份，是云南省“科学普及教育基地”、国家高原湿地研究中心“公众教育基地”、中国野生动物保护协会“全国野生动物保护科普教育基地”和“云南会泽黑颈鹤国家级自然保护区宣传教育基地”、云南省社科联“云南省社会科学普及示范基地”、云南省林草科普基地。
    先后荣获全国绿化先进集体、全国绿化模范单位、全国五四红旗团委、全国大学生暑期实践十佳大学、云南省文明学校、云南省平安校园等多项荣誉称号。
    学校坚持以党的政治建设为统领，落实立德树人根本任务，坚定不移地走以高质量为核心的内涵发展和特色发展道路，全力推进“双一流”建设。凝心聚力、对标一流、抢抓机遇、追求卓越，坚定不移加快推进学校高质量发展，为全面建设社会主义现代化国家、全面推进中华民族伟大复兴，为云南高质量跨越式发展作出西南林业大学新的更大的贡献。（数据更新至2023年3月底）
    """

    List =random.sample(range(1, len(article)), 2)

    if List[0]>List[1]:
        num1=List[0]
        List[0]=List[1]
        List[1]=num1


    values=article[List[0]:List[1]]
    wd.get("https://www.yooc.me/group/7228080/topics")
    # wd.find_element(By.XPATH,"/html/body/section/section/div[2]/div[1]/a").click()

    wd.execute_script("arguments[0].click();", wd.find_element(By.XPATH,"/html/body/section/section/div[2]/div[1]/a"))
    wd.find_element(By.XPATH,"/html/body/section/section/form/input[2]").send_keys(title)
    wd.switch_to.frame("content_ifr")
    wd.find_element(By.ID,"tinymce").send_keys(values)

    wd.switch_to.default_content()
    code=get_submit_code()
    wd.find_element(By.XPATH,"/html/body/section/section/form/div[2]/input[1]").send_keys(code)
    try:
        input("检查验证码：")
        wd.find_element(By.XPATH,"/html/body/section/section/form/div[2]/input[3]").click()
    except:
        input("请手动输入验证码，并输入任意字符继续：")
        wd.find_element(By.XPATH, "/html/body/section/section/form/div[2]/input[3]").click()

#播放视频
def playvideo():

    #进入课程学习的页面
    wd.get("https://www.yooc.me/group/7228080/courses")

    wd.refresh()
    page_text = wd.page_source
    tree = etree.HTML(page_text)

    div_list1 = tree.xpath("/html/body/section/section/div[2]/div")
    div_list=div_list1[1:len(div_list1)]
    # 定义答题的url列表

    div_url=wd.find_elements(By.CLASS_NAME,"detail-holder")
    print(len(div_url))

    #每一个模块的入口
    div_link = []

    for li in div_list:
        herf = li.xpath("./div/div[3]/a/@href")[0]
        div_link.append(herf)

    print(div_link)

   #获取每一个连接并进入
    for url in div_link:
        i=0
        wd.get(url)
        if i==1:
            wd.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/a")  # 点击报名，或者点击开始学习
            try:
                wd.refresh()
                sleep(1)
                wd.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/a")
            except:
                print("已经报名过了!!")
        else:
            wd.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/div/a")#点击报名，或者点击开始学习
            try:
                wd.refresh()
                sleep(1)
                wd.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/a")
            except:
                print("已经报名过了!!")
        i=i+1


def repeat(i):
    #第一页的试卷目录URL
    pag_url = "https://www.yooc.me/group/7228080/exams",
    num=i
    if i>10:
        # 第二页试卷的url
        pag_url="https://www.yooc.me/group/7228080/exams?page=2"
        num=i-10
# 打开试卷页
    wd.get(pag_url)
    wd.refresh()

    #获取打开的页面的试卷列表，返回一个列表
    lis=wd.find_elements(By.XPATH,"/html/body/section/section/div[2]/div[3]/ul/li")

    #获取传入的值（试卷号），减一后获得该试卷的定位的地方
    li=lis[num-1]
    # print(li)

    # 获取分数
    garden = li.find_element(By.XPATH, "./div[2]/p[2]").text
     # print(num)
    print(f"成绩是：{garden}")

    #如果成绩是100分就跳过，不再重新考试
    if garden=="100":
        pass

    # 如果成绩不是100就进行重新考试
    else:
        #点击重新考试
        li.find_element(By.XPATH, ".//div[2]/a[2]").click()
        #点击确定
        wd.find_element(By.XPATH,"/html/body/div[12]/div[3]/div/div[1]/button").click()
        wd.refresh()
        sleep(1)
        #获取当前打开的试卷的URL
        currentPageUrl =wd.current_url
        print(currentPageUrl)
        sleep(1)
        # 对该试卷重新答题
        get_one_asw(currentPageUrl)

def one_20():
    # 1--20套
    wd.get("https://www.yooc.me/group/7228080/exams")
    i = 1
    for urls in test_paper_url:
        for url in urls:
            try:
                get_one_asw(url)
            except:
                print(f"试卷{url}出现异常;第{i}套,正在尝试重做")
            i = i + 1




if __name__ == '__main__':
    dict_u=get_user(1)
    username=dict_u["username"]
    password=dict_u["password"]

    # username="13529393416"
    # password="CM204428"
    #登录
    # login("15894263886","108427222wrt")
    login(username,password)

    # 获取登录验证码图片
    # get_login_code()
    try:
        wd.get("https://www.yooc.me/group/7228080/exams")
    except:
        #添加课群
        add_course()

    # 以下是答题部分
    one_20()
    # 解答第21题
    exam21()


    # # 对不是满分的试卷进行检查
    # pagnum=1
    # while pagnum <=20:
    #     repeat(pagnum)
    #     pagnum=pagnum+1

    # 发表话题
    write()


    # 成绩查询页
    wd.get("https://www.yooc.me/group/7228080/grade")
    sleep(5)
    # 进入课程学习的页面
    wd.get("https://www.yooc.me/group/7228080/courses")

    # 视频学习
    # playvideo()




