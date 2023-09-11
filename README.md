# 產品資訊轉換器

這個程式是一個產品資訊轉換器，使用了 Streamlit 和 OpenAI 的 GPT-3.5 Turbo 模型。目的是將非結構化的產品資訊轉換為結構化的 JSON 格式，以便更容易地進行處理和分析。

## 如何使用

1. 在上方的"請輸入產品資訊"文字框中輸入你的產品資訊。這些資訊應該是一個文字描述，可以是產品的特性、描述、顏色等等。

2. 在"請輸入你要的 JSON 格式，每行一個不用逗點"文字框中，輸入你想要的 JSON 格式的標籤。每個標籤應該是一行，例如 "goods"、"feature"、"color" 等等。

3. 點選"送出"按鈕，程式將使用 GPT-3.5 Turbo 模型將你的產品資訊轉換為 JSON 格式。

4. 接著再點擊「進行二次檢查！」，程式會把這三個產出的 JOSN 餵給 GPT-3.5-turbo 的模型來判斷哪個是最佳 JSON 並返回結果。

## 訓練方式

**使用 3 個輸入輸出範例讓 GPT 學習如何分類。**

### 範例一

輸入：
```
Title : 短袖上衣,
Category : ADSAA01、ADSAB02、ADSAC02、ADSAE02、ADSAG06、ADSAG08、ADSAG19、ADSAH01、CNYtest,
Brand : adidas ,
Description : 辨識度極高的三條線圖案上衣自 1973 年推出後就迅速成為經典單品，本季 adidas 利用街頭感元素重新設計，使風格煥然一新。這款修身的男性棉質上衣配有拉克蘭袖，搭配撞色三條線，胸口電繡 Originals Logo。靈感來自 70 年代服裝的三條線設計棉質上衣|國際尺寸|羅紋圓領|拉克蘭袖|羅紋袖口|胸口電繡 Originals Logo；肩膀和衣袖三條線設計|我們與瑞士良好棉花發展協會（Better Cotton Initiative）合作，協助改善全球的棉花種植業。包覆曲線的修身版型，打造俐落線條|100% 棉質單面針織布
```

輸出：
```
{
  "goods": "上衣",
  "feature": ["修身", "拉克蘭袖"],
  "brand": "Originals",
  "material": "100% 棉",
  "pattern": ["撞色", "三條線"],
  "gender": "男",
  "neckline": "圓領",
  "sleeve_length": "短袖",
  "color": "黑色"
} 
```

### 範例二

輸入：
```
Title : 個性挖破休閒男友牛仔褲(附腰帶) S-XXL
Category : J系列、人氣推薦>-5KG激瘦最強系列、主題企劃>牛仔丹寧、下著>長褲
Brand : Mando蔓朵
Description :視覺上打造出清夏高階感 最流行的夏日色系淺刷色牛仔&奶油色 絕對會成為妳今夏的好夥伴💛 >直筒搭配九分版型修飾腿型一流 >任何缺點都可以偷偷藏起來 >刷破提升穿搭魅力 毫不費力的百搭單品快拿下!
商品為Free Size 詳細平量尺寸在頁面最下方 ♥️（模特兒身高163體重43）  貼心提醒: 色彩因濾鏡關係會有些許落差，介意色差的買家請謹慎思考再下標。賣場不接受色差或與想像中不符而退換貨。MANDO蔓朵-個性挖破休閒男友牛仔褲(附腰帶)-視覺上打造出清夏高階感。最流行的夏日色系淺刷色牛仔&奶油色  絕對會成為妳今夏的好夥伴💛 >直筒搭配九分版型修飾腿型一流 >任何缺點都可以偷偷藏起來 >刷破提升穿搭魅力  毫不費力的百搭單品快拿下!。男友褲,牛仔長褲,牛仔寬鬆,休閒牛仔褲,挖破牛仔褲,蔓朵,Mando,Mando蔓朵,服飾,女裝,韓系,韓國,
```

輸出：
```
{
  "goods": "牛仔褲",
  "feature": ["刷色", "附腰帶", "直筒", "刷破"],
  "material": "牛仔",
  "clothes_length": "九分",
  "color": ["杏色", "藍色"],
  "style": ["顯瘦穿搭", "休閒", "個性"]
}
```

### 範例三

輸入：
```
Title : 完全是我的菜：麂皮口袋上衣+短褲套裝 兩色
Category : 多睡五分鐘 ♥ 洋裝套裝系列>A/W 洋裝 / 連身褲 / 套裝、In Stock ➠ 現貨專區、NEW IN 2023>【January.一月號】 B
rand : Mando蔓朵 
Description : Color - 溫柔杏/性感黑  兩件式套裝組 出遊、約會都不用想要怎麼搭配～  分開搭配也合適 溫柔的麂皮總是和你一樣止不住心動💓 最喜歡大大的口袋 大腿開岔增添一點小性感 又甜又辣！我這個周末就要穿這件啦 貼心提醒: 色彩因濾鏡關係會有些許落差，介意色差的買家請謹慎思考再下標。賣場不接受色差或與想像中不符而退換貨。 ♥️模特兒身高163體重43 MANDO蔓朵-完全是我的菜：麂皮口袋上衣+短褲套裝 兩色-又甜又辣！ 我這個周末就要穿這件啦。
Color - 溫柔杏/性感黑 兩件式套裝組 出遊、約會都不用想要怎麼搭配～ 分開搭配也合適 溫柔的麂皮總是和你一樣止不住心動💓  最喜歡大大的口袋 大腿開岔增添一點小性感 又甜又辣！我這個周末就要穿這件啦。
秋冬必備,約會套裝,無害,麂皮,套裝,韓系,短褲,日常單品,蔓朵,Mando,Mando蔓朵,服飾,女裝,韓系,韓國
```
輸出：
```
{
  "goods": ["短褲", "上衣"],
  "feature": ["套裝", "口袋", "兩件式", "開岔"],
  "material": "麂皮",   "occasion": "約會",
  "color": ["黑色", "杏色"],
  "style": ["性感", "溫柔"]
}
```
