import streamlit as st
import openai
import json

# 初始化OpenAI API

example = '''{'Title : 短袖上衣, Category : ADSAA01、ADSAB02、ADSAC02、ADSAE02、ADSAG06、ADSAG08、ADSAG19、ADSAH01、CNYtest, Brand : adidas ,Description : 辨識度極高的三條線圖案上衣自 1973 年推出後就迅速成為經典單品，本季 adidas 利用街頭感元素重新設計，使風格煥然一新。這款修身的男性棉質上衣配有拉克蘭袖，搭配撞色三條線，胸口電繡 Originals Logo。靈感來自 70 年代服裝的三條線設計棉質上衣|國際尺寸|羅紋圓領|拉克蘭袖|羅紋袖口|胸口電繡 Originals Logo；肩膀和衣袖三條線設計|我們與瑞士良好棉花發展協會（Better Cotton Initiative）合作，協助改善全球的棉花種植業。包覆曲線的修身版型，打造俐落線條|100% 棉質單面針織布' : { "goods": "上衣",   "feature": ["修身", "拉克蘭袖"],   "brand": "Originals",   "material": "100% 棉",   "pattern": ["撞色", "三條線"],   "gender": "男",   "neckline": "圓領",   "sleeve_length": "短袖",   "color": "黑色" }  \n 'Title : 個性挖破休閒男友牛仔褲(附腰帶) S-XXL Category : J系列、人氣推薦>-5KG激瘦最強系列、主題企劃>牛仔丹寧、下著>長褲 Brand : Mando蔓朵 Description :視覺上打造出清夏高階感 最流行的夏日色系淺刷色牛仔&奶油色 絕對會成為妳今夏的好夥伴💛 >直筒搭配九分版型修飾腿型一流 >任何缺點都可以偷偷藏起來 >刷破提升穿搭魅力 毫不費力的百搭單品快拿下!  商品為Free Size 詳細平量尺寸在頁面最下方 ♥️（模特兒身高163體重43）  貼心提醒: 色彩因濾鏡關係會有些許落差，介意色差的買家請謹慎思考再下標。賣場不接受色差或與想像中不符而退換貨。 。MANDO蔓朵-個性挖破休閒男友牛仔褲(附腰帶)-視覺上打造出清夏高階感。最流行的夏日色系淺刷色牛仔&奶油色  絕對會成為妳今夏的好夥伴💛 >直筒搭配九分版型修飾腿型一流 >任何缺點都可以偷偷藏起來 >刷破提升穿搭魅力  毫不費力的百搭單品快拿下!。男友褲,牛仔長褲,牛仔寬鬆,休閒牛仔褲,挖破牛仔褲,蔓朵,Mando,Mando蔓朵,服飾,女裝,韓系,韓國,': { "goods": "牛仔褲",   "feature": ["刷色", "附腰帶", "直筒", "刷破"],   "material": "牛仔",   "clothes_length": "九分",   "color": ["杏色", "藍色"],   "style": ["顯瘦穿搭", "休閒", "個性"] }  \n Title : 完全是我的菜：麂皮口袋上衣+短褲套裝 兩色 Category : 多睡五分鐘 ♥ 洋裝套裝系列>A/W 洋裝 / 連身褲 / 套裝、In Stock ➠ 現貨專區、NEW IN 2023>【January.一月號】 Brand : Mando蔓朵 "Description : Color - 溫柔杏/性感黑  兩件式套裝組 出遊、約會都不用想要怎麼搭配～  分開搭配也合適 溫柔的麂皮總是和你一樣止不住心動💓 最喜歡大大的口袋 大腿開岔增添一點小性感 又甜又辣！我這個周末就要穿這件啦 貼心提醒: 色彩因濾鏡關係會有些許落差，介意色差的買家請謹慎思考再下標。賣場不接受色差或與想像中不符而退換貨。 ♥️模特兒身高163體重43 MANDO蔓朵-完全是我的菜：麂皮口袋上衣+短褲套裝 兩色-又甜又辣！ 我這個周末就要穿這件啦。 - Color - 溫柔杏/性感黑 兩件式套裝組 出遊、約會都不用想要怎麼搭配～ 分開搭配也合適 溫柔的麂皮總是和你一樣止不住心動💓  最喜歡大大的口袋 大腿開岔增添一點小性感 又甜又辣！我這個周末就要穿這件啦。 秋冬必備,約會套裝,無害,麂皮,套裝,韓系,短褲,日常單品,蔓朵,Mando,Mando蔓朵,服飾,女裝,韓系,韓國': { "goods": ["短褲", "上衣"],   "feature": ["套裝", "口袋", "兩件式", "開岔"],   "material": "麂皮",   "occasion": "約會",   "color": ["黑色", "杏色"],   "style": ["性感", "溫柔"] }}'''

def convert_to_json(input, tag):
    # 調用GPT API
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "請你作為一名專業分類人員，根據給定的產品資訊，以及不同標籤進行分類。"},
        {"role": "user", "content": f"每個分類可以有多個標籤，我會告知你需求的欄位。請將每個指定欄位進行詳細分類，並僅以json格式返回，請最大化 prompt 效果。以下是範例：```{example}```, 請分類以下內容：```{input}```。  \n 不要出現複雜或過長的詞彙。  \n Provide them in JSON format with the following keys:{tag}"}
    ],
    temperature=0.3  # 創意程度
)
    
    # 從API回應中獲取轉換後的內容
    converted_content = response.choices[0].message['content'].strip()
    
    # 直接返回回應的內容
    return converted_content

# Streamlit界面
st.title('產品資訊轉換器')

# 輸入框
if 'input' not in st.session_state:
    st.session_state['input'] = ''
st.session_state['input'] = st.text_area('請輸入產品資訊', value=st.session_state['input'], height = 200)
tag_input = st.text_area('請輸入你要的json格式，每行一個不用逗點', 
                         height = 200,
                         help = '每行輸入一個標籤名稱，例如 good、feature、color 等等。')

# 將不同行的內容轉換成逗點分隔
tag = ', '.join(tag_input.split('\n'))



# 創建一個空的按鈕區塊
button2 = st.empty()

# 送出按鈕
if st.button('送出'):
    # 初始化 output1 為一個空列表
    output1 = []
    # 創建進度條
    progress_bar = st.progress(0)
    for i in range(3):
        # 執行轉換，每次傳入不同的參數
        result = convert_to_json(st.session_state['input'] + " ", tag)
        # 檢查結果是否為json格式
        if result.startswith('{') and result.endswith('}'):
            # 將結果轉換成字串並在前後加入```
            result = f"```\n{result}\n```"
            # 顯示結果
            st.markdown(result, unsafe_allow_html=True)
        else:
            # 如果結果不是json格式，則直接輸出原始結果
            st.write(result)
        # 更新進度條
        progress_bar.progress((i + 1) / 3)
        # 將結果添加到 output1 列表中
        output1.append(result)
    # 儲存所有的結果
    st.session_state['output1'] = output1

# 第一次的結果出現後，顯示第二個按鈕
if button2.button('進行二次檢查！'):
    # 將 output1 的內容轉換成一個字串
    st.session_state['output1_str'] = '\n'.join(st.session_state['output1'])
    st.write(f"['input']")
    st.write(f"output1: {st.session_state['output1_str']}")
    # 執行第二次的轉換
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "請你作為一名專業分類人員，根據給定的產品資訊，以及不同標籤進行分類。"},
            {"role": "user", "content": f"產品資訊：```{st.session_state['input']}```  \n 產品資訊對應的3個分類json：```{st.session_state['output1_str']}```  \n 請問哪個json是分類最準確、沒有錯誤資訊的？僅給我json即可。不要有任何一個文字說明，一個都不要。"}
        ],
        temperature=0  # 創意程度
    )
    print(response)
    # 儲存 response 的內容
    st.session_state['response'] = response

    # 顯示 response 的內容
    st.write(st.session_state['response'])

    # 從API回應中獲取轉換後的內容
    st.session_state['converted_content'] = st.session_state['response'].choices[0].message['content'].strip()

    # 直接輸出原始結果
    st.write(st.session_state['converted_content'])

# 完整範例 example = '''{'Title : 短袖上衣, Category : ADSAA01、ADSAB02、ADSAC02、ADSAE02、ADSAG06、ADSAG08、ADSAG19、ADSAH01、CNYtest, Brand : adidas ,Description : 辨識度極高的三條線圖案上衣自 1973 年推出後就迅速成為經典單品，本季 adidas 利用街頭感元素重新設計，使風格煥然一新。這款修身的男性棉質上衣配有拉克蘭袖，搭配撞色三條線，胸口電繡 Originals Logo。靈感來自 70 年代服裝的三條線設計棉質上衣|國際尺寸|羅紋圓領|拉克蘭袖|羅紋袖口|胸口電繡 Originals Logo；肩膀和衣袖三條線設計|我們與瑞士良好棉花發展協會（Better Cotton Initiative）合作，協助改善全球的棉花種植業。包覆曲線的修身版型，打造俐落線條|100% 棉質單面針織布' : { "goods": "上衣",   "feature": ["修身", "拉克蘭袖"],   "brand": "Originals",   "material": "100% 棉",   "pattern": ["撞色", "三條線"],   "gender": "男",   "neckline": "圓領",   "sleeve_length": "短袖",   "color": "黑色" }  \n 'Title : 個性挖破休閒男友牛仔褲(附腰帶) S-XXL Category : J系列、人氣推薦>-5KG激瘦最強系列、主題企劃>牛仔丹寧、下著>長褲 Brand : Mando蔓朵 Description :視覺上打造出清夏高階感 最流行的夏日色系淺刷色牛仔&奶油色 絕對會成為妳今夏的好夥伴💛 >直筒搭配九分版型修飾腿型一流 >任何缺點都可以偷偷藏起來 >刷破提升穿搭魅力 毫不費力的百搭單品快拿下!  商品為Free Size 詳細平量尺寸在頁面最下方 ♥️（模特兒身高163體重43）  貼心提醒: 色彩因濾鏡關係會有些許落差，介意色差的買家請謹慎思考再下標。賣場不接受色差或與想像中不符而退換貨。 。MANDO蔓朵-個性挖破休閒男友牛仔褲(附腰帶)-視覺上打造出清夏高階感。最流行的夏日色系淺刷色牛仔&奶油色  絕對會成為妳今夏的好夥伴💛 >直筒搭配九分版型修飾腿型一流 >任何缺點都可以偷偷藏起來 >刷破提升穿搭魅力  毫不費力的百搭單品快拿下!。男友褲,牛仔長褲,牛仔寬鬆,休閒牛仔褲,挖破牛仔褲,蔓朵,Mando,Mando蔓朵,服飾,女裝,韓系,韓國,': { "goods": "牛仔褲",   "feature": ["刷色", "附腰帶", "直筒", "刷破"],   "material": "牛仔",   "clothes_length": "九分",   "color": ["杏色", "藍色"],   "style": ["顯瘦穿搭", "休閒", "個性"] }  \n Title : 完全是我的菜：麂皮口袋上衣+短褲套裝 兩色 Category : 多睡五分鐘 ♥ 洋裝套裝系列>A/W 洋裝 / 連身褲 / 套裝、In Stock ➠ 現貨專區、NEW IN 2023>【January.一月號】 Brand : Mando蔓朵 "Description : Color - 溫柔杏/性感黑  兩件式套裝組 出遊、約會都不用想要怎麼搭配～  分開搭配也合適 溫柔的麂皮總是和你一樣止不住心動💓 最喜歡大大的口袋 大腿開岔增添一點小性感 又甜又辣！我這個周末就要穿這件啦 貼心提醒: 色彩因濾鏡關係會有些許落差，介意色差的買家請謹慎思考再下標。賣場不接受色差或與想像中不符而退換貨。 ♥️模特兒身高163體重43 MANDO蔓朵-完全是我的菜：麂皮口袋上衣+短褲套裝 兩色-又甜又辣！ 我這個周末就要穿這件啦。 - Color - 溫柔杏/性感黑 兩件式套裝組 出遊、約會都不用想要怎麼搭配～ 分開搭配也合適 溫柔的麂皮總是和你一樣止不住心動💓  最喜歡大大的口袋 大腿開岔增添一點小性感 又甜又辣！我這個周末就要穿這件啦。 秋冬必備,約會套裝,無害,麂皮,套裝,韓系,短褲,日常單品,蔓朵,Mando,Mando蔓朵,服飾,女裝,韓系,韓國': { "goods": ["短褲", "上衣"],   "feature": ["套裝", "口袋", "兩件式", "開岔"],   "material": "麂皮",   "occasion": "約會",   "color": ["黑色", "杏色"],   "style": ["性感", "溫柔"] }}'''

# 只有 json 的範例 example = '''{'Title : 短袖上衣, Category : ADSAA01、ADSAB02、ADSAC02、ADSAE02、ADSAG06、ADSAG08、ADSAG19、ADSAH01、CNYtest, Brand : adidas ,Description : 辨識度極高的三條線圖案上衣自 1973 年推出後就迅速成為經典單品，本季 adidas 利用街頭感元素重新設計，使風格煥然一新。這款修身的男性棉質上衣配有拉克蘭袖，搭配撞色三條線，胸口電繡 Originals Logo。靈感來自 70 年代服裝的三條線設計棉質上衣|國際尺寸|羅紋圓領|拉克蘭袖|羅紋袖口|胸口電繡 Originals Logo；肩膀和衣袖三條線設計|我們與瑞士良好棉花發展協會（Better Cotton Initiative）合作，協助改善全球的棉花種植業。包覆曲線的修身版型，打造俐落線條|100% 棉質單面針織布' : { "goods": "上衣",   "feature": ["修身", "拉克蘭袖"],   "brand": "Originals",   "material": "100% 棉",   "pattern": ["撞色", "三條線"],   "gender": "男",   "neckline": "圓領",   "sleeve_length": "短袖",   "color": "黑色" }  \n 'Title : 個性挖破休閒男友牛仔褲(附腰帶) S-XXL Category : J系列、人氣推薦>-5KG激瘦最強系列、主題企劃>牛仔丹寧、下著>長褲 Brand : Mando蔓朵 Description :視覺上打造出清夏高階感 最流行的夏日色系淺刷色牛仔&奶油色 絕對會成為妳今夏的好夥伴💛 >直筒搭配九分版型修飾腿型一流 >任何缺點都可以偷偷藏起來 >刷破提升穿搭魅力 毫不費力的百搭單品快拿下!  商品為Free Size 詳細平量尺寸在頁面最下方 ♥️（模特兒身高163體重43）  貼心提醒: 色彩因濾鏡關係會有些許落差，介意色差的買家請謹慎思考再下標。賣場不接受色差或與想像中不符而退換貨。 。MANDO蔓朵-個性挖破休閒男友牛仔褲(附腰帶)-視覺上打造出清夏高階感。最流行的夏日色系淺刷色牛仔&奶油色  絕對會成為妳今夏的好夥伴💛 >直筒搭配九分版型修飾腿型一流 >任何缺點都可以偷偷藏起來 >刷破提升穿搭魅力  毫不費力的百搭單品快拿下!。男友褲,牛仔長褲,牛仔寬鬆,休閒牛仔褲,挖破牛仔褲,蔓朵,Mando,Mando蔓朵,服飾,女裝,韓系,韓國,': { "goods": "牛仔褲",   "feature": ["刷色", "附腰帶", "直筒", "刷破"],   "material": "牛仔",   "clothes_length": "九分",   "color": ["杏色", "藍色"],   "style": ["顯瘦穿搭", "休閒", "個性"] }  \n Title : 完全是我的菜：麂皮口袋上衣+短褲套裝 兩色 Category : 多睡五分鐘 ♥ 洋裝套裝系列>A/W 洋裝 / 連身褲 / 套裝、In Stock ➠ 現貨專區、NEW IN 2023>【January.一月號】 Brand : Mando蔓朵 "Description : Color - 溫柔杏/性感黑  兩件式套裝組 出遊、約會都不用想要怎麼搭配～  分開搭配也合適 溫柔的麂皮總是和你一樣止不住心動💓 最喜歡大大的口袋 大腿開岔增添一點小性感 又甜又辣！我這個周末就要穿這件啦 貼心提醒: 色彩因濾鏡關係會有些許落差，介意色差的買家請謹慎思考再下標。賣場不接受色差或與想像中不符而退換貨。 ♥️模特兒身高163體重43 MANDO蔓朵-完全是我的菜：麂皮口袋上衣+短褲套裝 兩色-又甜又辣！ 我這個周末就要穿這件啦。 - Color - 溫柔杏/性感黑 兩件式套裝組 出遊、約會都不用想要怎麼搭配～ 分開搭配也合適 溫柔的麂皮總是和你一樣止不住心動💓  最喜歡大大的口袋 大腿開岔增添一點小性感 又甜又辣！我這個周末就要穿這件啦。 秋冬必備,約會套裝,無害,麂皮,套裝,韓系,短褲,日常單品,蔓朵,Mando,Mando蔓朵,服飾,女裝,韓系,韓國': { "goods": ["短褲", "上衣"],   "feature": ["套裝", "口袋", "兩件式", "開岔"],   "material": "麂皮",   "occasion": "約會",   "color": ["黑色", "杏色"],   "style": ["性感", "溫柔"] }}'''
