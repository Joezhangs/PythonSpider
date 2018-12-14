## 采集七麦网-爬虫文档-更新于2018/11/21
### 1. 采集需求
#### 采集网站：七麦网
https://www.qimai.cn

#### 采集范围：
采集APP和公众号基本信息及排名数据；
采集分类榜单：每个榜单的前200名
https://www.qimai.cn/rank/index/brand/free/country/cn/genre/6005/device/iphone

##### 应用详情——iOS版：

- url：https://www.qimai.cn/app/baseinfo/appid/414478124/country/cn
- 版本：iOS
- 基本信息：Logo、应用名称、开发商、开发商ID（乐职etid）、App ID、分类、价格（免费/付费）、应用截图、应用描述 ---> 一级页面，   二级A1
- 网站：支持网站、开发者网站、内容评级 ---> 二级页面
- 榜单排名：iPhone实时排名-总榜、应用榜、社交榜；iPad实时排名-总榜、应用榜、社交榜
- 评论统计：应用市场、平均评分、评论人数
- 同开发商应用：数据库关联即可，无需采集
- 移动端版本关联：关联同一个应用的iOS版和安卓版，便于核实开发商的英文名称


- ##### 应用详情——安卓版：
- url：https://www.qimai.cn/andapp/baseinfo/appid/335517
- 版本：安卓
- 基本信息：Logo、应用名称、开发商、开发商ID（乐职etid）、分类、Bundel id、应用截图、应用描述
- 评论统计：应用市场、平均评分、评论人数
- 榜单排名：电子市场、市场分类、实时排名、排名统计时间
- 移动端版本关联：关联同一个应用的iOS版和安卓版

### 2. 爬虫介绍：
使用的是selenium采集七麦网的数据


- python版本：python3

- 编译工具：pycharm

- 数据存储：mysql

#### 爬虫思路：
1. 使用selenium驱动浏览器进入网站
2. 驱动浏览器进入相应的网址，获取对应网址的页面
3. 将页面数据传递给解析函数进行解析
4. 将解析的数据传回主函数，并存储到数据库中

#### 页面分级：
将页面标注，以及对于页面所能获取的信息
- 一级页面：（初始页面）
- 二级页面A： （ios app详情页面）
    - 二级页面A1:    
     Logo、应用名称、开发商、App ID、分类、价格（免费/付费）、应用截图、应用描述、支持网站、内容评级
    - 二级页面A3：    
    应用市场（ App Store）、平均评分、评论人数
    - 二级页面A7：       
    iPhone实时排名-总榜、应用榜、分类榜；iPad实时排名-总榜、应用榜、分类榜
- 二级页面B：（安卓 app详情页面）    
    - 二级页面B1：    
    Logo、应用名称、开发商、分类、Bundel id、应用截图、应用描述
    - 二级页面B3:     
    应用市场、平均评分、评论人数
    - 二级页面B5：电子市场、市场分类、实时排名、排名统计时间
- 二级页面C：（公司页面） ：开发者网站


#### 所建的表：

##### 表ios_android_ID：ios和安卓版本的关联库
1. id
2. ios_id
3. android_id

##### 表ios_main:ios主要信息库
1. id
2. ios_id
3. app_name/应用名称
4. caiji_url/采集源url
5. 开发商/developer
6. logo_url
6. 分类/class
7. 价格/price
8. 应用截图url/screenshot_url
9. 应用描述/app_desc
10. 支持网站/support_website
11. 内容评级/content_rating
12. 应用市场/app_market
13. 平均评分/average_rating
14. 评论人数/comments_num
15. 开发者网站/developer_website


##### android_main：安卓主要信息库

1. id
2. android_id
3. app_name/应用名称...
4. caiji_url/采集源url
5. Logo_url...
7. 开发商...
8. 分类...
9. Bundle id
10. 应用截图...
11. 应用描述...


##### 表ios_Leaderboardl：ios排行榜：
1. id
2. ios_id
3. leaderboardl


##### 表android_Leaderboardl：安卓排行榜：
1. id
2. android_id
3. leaderboardl

##### 表android_rating：安卓评分
1. id
2. android_id
3. 应用市场/app_market
4. 平均评分/average_rating
5. 评论人数/comments_num




---

---





### 3. 过程记录：

**这里是写爬虫的过程中的一些情况记录，并没有太多的逻辑性，仅供参考**

1. 之前准备熟悉fiddler工具，发现不是很友好，改用charles，并熟悉相关操作
2. 已经获取到初始页面的要获取的ajax数据信息，数据url为：https://api.qimai.cn/rank/index?analysis=L1tzFH4xL0M7DHNda24OFFh3XEE7MgoKcBMYS1cPXhwIX1YGSCZCBFZSDwAID1FbAQglF1A%3D&brand=free&country=cn&genre=6005&device=iphone
3. 使用python3编程
4. 此网站有提供api接口，各个需要采集的信息api应该是有规律的，尝试去寻找规律，先从开始页面寻找
5. 在初始页面：

	全部应用：5000
	商务到购物：6000~6024
	儿童：6061

6. 七麦网站虽然是使用了ajax，单纯的ajax不难，但是这里的有个analysis参数做了js加密，不会解（这个貌似和淘宝很像，使用了ajax，但是多接口都做了加密）
7. 这里有一个七麦的请求加密破解的教程，看了一下不是很懂，留存之后待用: [https://lengyue.me/index.php/2018/10/15/qimai/](https://lengyue.me/index.php/2018/10/15/qimai/)
8. 尝试使用selenium来获取数据
9. 已经使用selenium可以获取到全部初始页面的数据
10. 基本上已经完成了对HTML的爬取，之后就需要将HTML的信息提取出来
11. 出现错误，访问限制了
12. 可能在网站自动点击的时候，可能需要到能点击的页面部分，之后估计要处理
13. 对数据的解析同时处理
14. 点击元素




