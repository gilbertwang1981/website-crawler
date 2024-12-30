## 项目背景

##### 1. 前置项目为一个1688搜图的模块，业务通过图像搜索找到相关性较强的品，然后勾选商品，进行批量首次话术沟通，通过阿里旺旺IM工具；

##### 2. 1688-阿里旺旺群发消息接口，为该项目提供后置服务；

##### 3. Python实现发送/接收消息和添加/更新Cookie的接口；

##### 4. 实现了海外电商独立站的商品资料爬虫，主要是迪拜站点；

| 编号     | 站点                            |
|--------| ------------------------------- |
| 1      | https://saifalfares.com/        |
| 2      | https://jubilee.ae/     |
| 3      | https://www.fakhruddinsouq.com/ |
| 4      | https://hajsabbagh.ae/ |
| 5      | https://victorwatch.com/ |
| 6      | https://salmansaffron.com |
| 7      | https://hajsabbagh.ae/ |
| 8      | https://www.jamshidramin.com/ |
| 9      | https://shop.atcacar.com/ |
| 10     | https://www.riiffsperfumes.com/ |
| 11     | http://www.rippleorbit.com/ |
| 12     | https://afs.ae/ |
| 13     | https://maat.ae/ |
| 14     | https://royalford.ae/ |
| 15     | https://sevenwonder.ae/ |
| 16     | https://rbwtoy.com |
 | 17     | https://oveisgharan.ae/ |
 | 18     | https://www.titastar.com/ |
 | 19     | https://atcacar.com/ |
 | 20     | https://stargoldworld.com/ |
 | 21     | https://citylineuae.com/ |
 | 22     | https://nddauto.com/ |
 | 23     | https://lutfitrading.com/ |
 | 24     | https://www.mebashi.com/ |
 | 25     | https://www.gracekitchenequip.com/ |
 | 26     | https://www.farookonline.com/ |
 | 27     | https://murexgeneraltrading.com/ |
 | 28     | http://www.copexsolar.com/  | 
 | 29     | http://www.nicewaylighting.com/products.php |
 | 30     | http://www.platoled.com/ |
 | 31     | http://www.shannylighting.com/ |
 | 32     | https://www.ghstorchlight.com/ | 
 | 33     | https://www.marjanalsahra.com/ |
 | 34     | http://sanfordworld.com/ |
 | 35     | https://www.dolphinstationery.com/ | 

##### 5. 实现爬取1688指定类目商品的供应商联系电话；

## 【附】部分模块编译/部署方法

#### 1. 通过下列命令打包镜像；

#####

    docker build -f Dockerfile.chat -t 1688-chat-service:1.0 .

#### 2. 通过以下命令启动服务；

#####

    docker run -itd -p 10019:10015 1688-chat-service:1.0 /bin/sh

#### 3. 通过以下命令查看服务是否正常；

#####

    docker logs -f container_id

## 测试

#### 1. 先增加cookie；

#####

    METHOD: POST

#####

    URL:http://ip:10019/aliWangWang/cookie/update/{loginAccount}

#####

    BODY: cookie string

#### 2. 发送消息；

#####

    METHOD: POST

#####

    URL:http://ip:10019/aliWangWang/tx

#####

    BODY:
    {
    	"offerId": "679618131020",
    	"chatList": [
    		"你好!",
    		"请问商品的价格可以便宜点吗？"
    	],
    	"userName": "loginAccount"
    }

#### 3. 接收消息；

#####

    METHOD: POST

#####

    URL:http://ip:10019/aliWangWang/rx

##### BODY:

    {
    	"offerId": "679618131020",
    	"userName": "loginAccount"
    }

#### 4. 获取商品详情；

#####

    METHOD: POST

#####

    URL:http://ip:10019/aliWangWang/getDetail

#####

    BODY:
    {
    	"offerId": "679618131020",
    	"userName": "loginAccount"
    }

