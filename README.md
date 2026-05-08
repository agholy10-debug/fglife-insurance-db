# 遠雄人壽保險商品查詢系統

一個便利的保險商品條款查詢系統，收錄遠雄人壽所有現售及停售商品的保單條款 PDF。

## 功能特色

- 📦 **商品分類**：依據商品類型（壽險、健康險、傷害險、年金險、還本險、投資型、團險）分類
- 🔍 **快速搜尋**：支援商品名稱關鍵字搜尋
- 📋 **狀態篩選**：可依現售/停售、主約/附約篩選
- 📄 **PDF 檢視**：直接在瀏覽器中檢視保單條款 PDF
- 📱 **響應式設計**：支援手機、平板、電腦各種裝置

## 已收錄商品

| 類型 | 現售 | 停售 | 小計 |
|------|------|------|------|
| 壽險 | 69 | 175 | 244 |
| 健康險 | 38 | 14 | 52 |
| 傷害險 | 11 | 35 | 46 |
| 年金險 | 10 | 0 | 10 |
| 還本險 | 3 | 2 | 5 |
| **總計** | **131** | **226** | **357** |

## 安裝執行

### 環境需求

- Python 3.8+
- Flask

### 安裝步驟

```bash
# 克隆專案
git clone https://github.com/YOUR_USERNAME/fglife-insurance-db.git
cd fglife-insurance-db

# 建立虛擬環境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate   # Windows

# 安裝依賴
pip install flask

# 執行
python app.py
```

### 環境變數

| 變數 | 說明 | 預設值 |
|------|------|--------|
| `INSURANCE_DB_PATH` | 保險商品資料庫路徑 | `/mnt/c/Users/holya/insurance-db/documents/fglife` |
| `PORT` | 伺服器端口 | `8083` |

### 執行後開啟瀏覽器

```
http://localhost:8083
```

## 資料來源

所有保單條款 PDF 均來自[遠雄人壽官方網站](https://www.fglife.com.tw/)，100% 官方來源，保證資料正確性。

## 專案結構

```
fglife-insurance-db/
├── app.py                 # Flask 伺服器主程式
├── templates/
│   └── index.html         # 前端介面
├── requirements.txt       # Python 依賴
└── README.md             # 本說明文件
```

## 技術棧

- **前端**：HTML5, CSS3, JavaScript (原生)
- **後端**：Flask (Python)
- **PDF**：Browser PDF Viewer

## 注意事項

- 本系統僅收錄民國95年（2006年）之後的停售商品
- PDF 檔案龐大（約 300+ MB），請確保網路頻寬充足
- 部分早期商品可能已下架，無法提供下載

## License

MIT License
