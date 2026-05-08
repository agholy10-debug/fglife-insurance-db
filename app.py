#!/usr/bin/env python3
"""
遠雄人壽保險商品查詢系統 - Flask 伺服器
"""

from flask import Flask, request, jsonify, render_template, send_file, abort
import os
import json
from pathlib import Path

app = Flask(__name__, template_folder='templates')

# 路徑設定 - 使用環境變數或預設路徑
BASE_DIR = Path(os.environ.get('INSURANCE_DB_PATH', '/mnt/c/Users/holya/insurance-db/documents/fglife'))
現售_DIR = BASE_DIR / "現售"
停售_DIR = BASE_DIR / "停售"

def classify_product(filename, status):
    """根據商品名稱或代碼分類商品"""
    name_lower = filename.lower()
    
    # 副約判斷
    rider_markers = [
        "_ha", "_hb", "_he", "_hf", "_hg", "_hh", "_hi", "_hj", "_hl", "_hn", "_ho", "_hp", "_hr",
        "_qa", "_qb", "_rda", "_rdb", "_rdw", "_rdx", "_rtl", "_rwa", "_rwl", "_tr", "_spwlr",
        "_fe1", "_fe2", "_fe3", "_ier", "_ilr", "_ioabc", "_ntr", "_otl", "_qtl", "_qdb",
        "_adb", "_aeab", "_aec", "_aiab", "_apa", "_apb", "_atl", "_awa", "_odbl",
        "_raa", "_ra", "_rar", "_rda", "_reab", "_rec", "_riab", "_rpa", "_rpb",
        "_tlr", "_xdb", "_xtl", "_spwlr"
    ]
    is_rider = any(m in name_lower for m in rider_markers) or "附約" in filename
    
    # 商品類型判斷
    if any(x in filename for x in ["年金", "_ga", "_gb", "_gc", "_gd", "_ge", "_gf", "_gg", "_gh", "_gi", "_gj", "_gk", "_gl", "_gm", "_gn"]):
        category = "年金險"
    elif any(x in filename for x in ["投資", "_ia", "_ib", "_ic", "_id", "_ie", "_if", "_ig", "_ih", "_ii", "_ij", "_ik", "_il", "_im"]):
        category = "投資型"
    elif any(x in name_lower for x in ["_ha", "_hb", "_he", "_hf", "_hg", "_hh", "_hi", "_hj", "_hl", "_hn", "_ho", "_hp", "_hr"]):
        if any(x in filename for x in ["醫療", "健康", "溫馨", "好心"]):
            category = "健康險"
        else:
            category = "傷害險"
    elif any(x in filename for x in ["還本", "_ja", "_jb", "_jd", "_je", "_jf", "_jg", "_jh", "_ji", "_jj", "_jk", "_jl", "_jm", "_fv", "_fwa", "_fwb", "_fwc", "_fwd", "_fwe", "_fwg", "_fwh", "_fwm", "_fwn", "_fwo", "_fwp", "_fwq", "_fwr", "_fws", "_fwt", "_fwu", "_fwv", "_fww", "_fwx", "_fwy", "_fwzs"]):
        category = "還本險"
    elif any(x in filename for x in ["醫療", "健康", "癌症", "特定傷病", "重大疾病", "_ce4", "_ci4", "_cj2", "_co1", "_cp1", "_cq1", "_cr1", "_csd", "_cu1", "_cv1", "_cw1", "_cx1", "_cy1", "_ha4", "_hb4", "_he6", "_hf1", "_hg6", "_hh5", "_hi6", "_hj5", "_hl6", "_hn4", "_ho6", "_rsl", "_rsm", "_rsn", "_hq1"]):
        category = "健康險"
    elif "團" in filename or "_gpk" in name_lower:
        category = "團險"
    else:
        category = "壽險"
    
    return {
        "category": category,
        "is_rider": is_rider,
        "type": "附約" if is_rider else "主約",
        "status": status,
        "filename": filename
    }

def build_index():
    """建立商品索引"""
    products = []
    
    for status, directory in [("現售", 現售_DIR), ("停售", 停售_DIR)]:
        if directory.exists():
            for f in sorted(directory.glob("*.pdf")):
                info = classify_product(f.name, status)
                info['filepath'] = str(f)
                info['filesize'] = f.stat().st_size
                products.append(info)
    
    return products

def get_stats():
    """取得統計資料"""
    products = build_index()
    categories = {}
    
    for p in products:
        cat = p['category']
        if cat not in categories:
            categories[cat] = {"現售": {"主約": 0, "附約": 0}, "停售": {"主約": 0, "附約": 0}}
        categories[cat][p['status']][p['type']] += 1
    
    return categories, len(products)

@app.route('/')
def index():
    """首頁"""
    stats, total = get_stats()
    return render_template('index.html', stats=stats, total=total)

@app.route('/api/products')
def api_products():
    """取得商品列表"""
    category = request.args.get('category', '')
    status = request.args.get('status', '')
    search = request.args.get('search', '')
    products = build_index()
    
    if category:
        products = [p for p in products if p['category'] == category]
    if status:
        products = [p for p in products if p['status'] == status]
    if search:
        search_lower = search.lower()
        products = [p for p in products if search_lower in p['filename'].lower()]
    
    return jsonify(products)

@app.route('/api/categories')
def api_categories():
    """取得分類統計"""
    stats, total = get_stats()
    return jsonify({"stats": stats, "total": total})

@app.route('/pdf/<path:filename>')
def serve_pdf(filename):
    """提供 PDF 下載"""
    # 安全檢查
    if '..' in filename or '/' not in filename:
        abort(403)
    
    # 嘗試兩個目錄
    path1 = 現售_DIR / filename
    path2 = 停售_DIR / filename
    
    if path1.exists():
        return send_file(path1, mimetype='application/pdf')
    elif path2.exists():
        return send_file(path2, mimetype='application/pdf')
    else:
        abort(404)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8083))
    app.run(host='0.0.0.0', port=port, debug=False)