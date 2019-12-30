# coding=utf-8
import requests,json


'''
将接口封装,request接口自动化基础库封装
excel数据驱动和反射，改造关键字，写入实际结果和异常信息
'''
class HTTP:

    def __init__(self,writer):
        # session管理,实例函数，定义实例变量
        self.session = requests.session()
        #基础的host地址：
        self.url = ''
        #结果解析
        self.result = None
        self.jsonres = None
        #关联保存参数的字典
        self.relations={}
        #写入excel文件的Excel.Writer对象
        self.writer = writer
        #记录当前需要写入的列
        self.row = 0


    def seturl(self,url):
        """
        设置基本url地址
        :param url:
        :return:
        """
        self.url = url
        self.__writer_excel('PASS','地址设置成功：'+str(url))

    def post(self,path,params):
        """
        发送post请求
        :param path:请求的路径
        :param params:请求的参数
        :return:无
        """
        params = self.__get_relations(params)
        self.result = self.session.post(self.url+'/'+path,data=self.__getdata(params))
        # print(self.result)
        try:
            self.jsonres = json.loads(self.result.text)
        except Exception as e:
            self.jsonres = None
        # print(self.jsonres)
        self.__writer_excel('PASS', self.result.text)

    def addheader(self,key,value):
        """
        在session上添加头
        :param key:头的键
        :param value:头的值
        :return:无
        """
        value = self.__get_relations(value)
        self.session.headers[key] = value
        # print(self.session.headers)
        self.__writer_excel('PASS','添加成功：'+str(self.session.headers))


    def removeheader(self,key):
        """
        删除头
        :param key:头的键
        :return:无
        """
        try:
            self.session.headers.pop(key)
        except Exception as e:
            pass
        self.__writer_excel('PASS', '删除成功：' + str(self.session.headers))

    def __getdata(self,params):
        """
        将标准的url参数转换为字典
        :param params: url参数字符串
        :return: 转换后的字典
        """

        if params is None or params =='':
            #如果是空或者空字符串，都返回None
            return None
        else:
            param_dict = {}
            #分割url字符串的键值对
            list_params = params.split('&')
            # 遍历键值对
            for items in list_params:
                # 如果键值对里有‘=’，取左边为键，右边为值

                if items.find('=') >= 0:

                    param_dict[items[0:items.find('=')]] = items[items.find('=') + 1:]
                else:
                    # 如果没有‘=’，处理为键，值为空
                    param_dict[items] = None
            # print(param_dict)
            return param_dict

    # def test(self,x, y):
    #     z = x + y
    #     print(z)
    #     return z
    def savejson(self,key,param_name):
        """
        保存关联的参数
        :param key: 需要保存的json结果里的键
        :param param_name: 保存后参数的名字
        :return: 无
        """
        try:
            self.relations[param_name]=self.jsonres[key]
            self.__writer_excel('PASS', self.relations)
        except Exception as e:
            self.relations[param_name]= ''
            self.__writer_excel('FAIL',self.relations)
        # print(self.relations)

    def __get_relations(self,params):
        """
        将参数里用到关联的地方，替换为关联后的值
        :param params: 关联前的参数
        :return: 关联后的结果
        """
        if params is None or params == '':
            return ''
        else:
            for keys in self.relations:
                """
                遍历当前保存后的参数字典
                把凡是符合{keys}这种形式的字符串，都替换为relations这个字典里keys这个键的值
                """

                params =params.replace('{'+keys+'}',self.relations[keys])
                # print(params)
                print(self.relations)

        return params

    def assertequals(self,key,value):
        """
        判断json结果里某个键的值是否和期望值value相等
        :param key:json结果的键
        :param value:期望值
        :return:是否相等
        """
        res = None
        try:
            res = str(self.jsonres[key])

        except Exception as e:
            pass
        #value添加关联
        value = self.__get_relations(value)
        if str(res) == str(value):
            self.__writer_excel('PASS',res)
            return True
        else:
            print('Fail')
            self.__writer_excel('FAIL', res)
            return False

    def __writer_excel(self,status,msg):
        """
        写入Excel
        :param status: 写入执行状态
        :param msg: 写入结果信息
        :return: 无
        """
        self.writer.write(self.row,7,status)
        self.writer.write(self.row,8,str(msg))