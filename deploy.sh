#!/bin/bash
# 部署到 GitHub 的腳本

echo "=========================================="
echo "  遠雄人壽保險商品查詢系統 - GitHub 部署"
echo "=========================================="
echo ""

# 檢查 git 是否存在
if ! command -v git &> /dev/null; then
    echo "❌ git 未安裝"
    exit 1
fi

# 檢查 gh 是否已認證
if command -v gh &> /dev/null && gh auth status &> /dev/null; then
    echo "✅ gh 已認證"
    GH_CMD="gh"
else
    echo "⚠️  gh 未認證或未安裝"
    echo ""
    echo "選項："
    echo "1. 使用 GitHub Token (需自行建立)"
    echo "2. 稍後手動上傳"
    echo ""
    read -p "請選擇 (1/2): " choice
    
    if [ "$choice" = "1" ]; then
        read -p "請輸入 GitHub Personal Access Token: " TOKEN
        export GITHUB_TOKEN="$TOKEN"
        GH_CMD="curl"
    else
        echo ""
        echo "手動部署說明："
        echo "1. 前往 https://github.com/new 建立新倉庫"
        echo "2. 倉庫名稱：fglife-insurance-db"
        echo "3. 選擇 Public 或 Private"
        echo "4. 建立後複製倉庫 URL"
        echo "5. 在終端執行："
        echo "   cd /home/holya/insurance-db-web"
        echo "   git remote add origin <你的倉庫URL>"
        echo "   git push -u origin master"
        echo ""
        exit 0
    fi
fi

# 建立 GitHub 倉庫
REPO_NAME="fglife-insurance-db"
DESCRIPTION="遠雄人壽保險商品查詢系統 - 收錄所有現售及停售保單條款 PDF"

if [ "$GH_CMD" = "gh" ]; then
    gh repo create "$REPO_NAME" --public --description "$DESCRIPTION" --clone=false
else
    # 使用 curl 建立倉庫
    RESP=$(curl -s -X POST \
        -H "Authorization: token $GITHUB_TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        https://api.github.com/user/repos \
        -d "{\"name\":\"$REPO_NAME\",\"description\":\"$DESCRIPTION\",\"private\":false}")
    
    if echo "$RESP" | grep -q "html_url"; then
        echo "✅ 倉庫建立成功"
        echo "$RESP" | grep -o '"html_url": "[^"]*"' | cut -d'"' -f4
    else
        echo "❌ 建立失敗: $RESP"
        exit 1
    fi
fi

# 添加 remote 並推送
cd /home/holya/insurance-db-web

# 嘗試获取默認 remote URL
if [ "$GH_CMD" = "gh" ]; then
    REMOTE_URL=$(gh api user --jq '.login' | xargs -I{} echo "https://github.com/{}/$REPO_NAME.git")
else
    GH_USER=$(curl -s -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user | python3 -c "import sys,json; print(json.load(sys.stdin)['login'])")
    REMOTE_URL="https://github.com/$GH_USER/$REPO_NAME.git"
fi

git remote add origin "$REMOTE_URL" 2>/dev/null || git remote set-url origin "$REMOTE_URL"

echo ""
echo "正在推送..."
git push -u origin master

echo ""
echo "=========================================="
echo "✅ 部署完成！"
echo "=========================================="
echo ""
echo "你的倉庫：$REMOTE_URL"
echo ""
echo "啟動本地伺服器："
echo "  cd /home/holya/insurance-db-web"
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""
echo "然後在瀏覽器開啟：http://localhost:8083"
