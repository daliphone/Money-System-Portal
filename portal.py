import streamlit as st
import json
import os
import pandas as pd

# --- 參數設定 (維持 v2.0 不變) ---
CONFIG_FILE = "money_config.json"
VERSION = "v2.1 (Visual Upgrade)"

# --- 預設設定檔 ---
DEFAULT_CONFIG = {
    "admin_password": "0526",
    "departments": {
        "行銷部": {
            "icon": "📢",
            "theme": "orange", # 新增主題色標記
            "protected": False,
            "links": [
                {"name": "馬尼行銷活動進程", "url": "https://money-marketing-room.streamlit.app/", "desc": "活動排程與進度"},
                {"name": "馬尼活動發想規劃", "url": "https://moneyweb.streamlit.app/", "desc": "活動的提案與設定"}
            ]
        },
        "電商部": {
            "icon": "🛒",
            "theme": "blue", # 新增主題色標記
            "protected": False,
            "links": [
                {"name": "蝦皮試算", "url": "https://shopee-money.streamlit.app/", "desc": "獲利試算"},
                {"name": "鮮拾試算", "url": "https://10mart-calculator.streamlit.app/", "desc": "獲利試算"},
                {"name": "奇摩拍賣", "url": "https://money-yahoo-auction-calculator.streamlit.app/", "desc": "獲利試算"},
                {"name": "Friday購物", "url": "https://fridayshop-calculator.streamlit.app/", "desc": "獲利試算"}
            ]
        },
        "管理部": {
            "icon": "💰",
            "theme": "purple", # 新增主題色標記
            "protected": True,
            "links": [
                {"name": "業績戰情室", "url": "https://money-real-timesalesperformancereport.streamlit.app/", "desc": "每月業績"},
                {"name": "人員評核", "url": "https://hqkpiapp.streamlit.app/", "desc": "績效評分"}
            ]
        }
    }
}

# --- 頁面設定 ---
st.set_page_config(page_title="馬尼通訊系統入口", page_icon="📱", layout="wide")

# ==========================================
# 🎨 v2.1 美化核心：自訂 CSS 樣式
# ==========================================
st.markdown("""
    <style>
    /* 讓按鈕充滿寬度，並增加一點圓角和陰影 */
    .stButton button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* 自訂部門標題樣式 */
    .dept-header {
        padding: 10px;
        border-radius: 8px 8px 0 0;
        color: white;
        text-align: center;
        font-size: 1.2em;
        font-weight: bold;
        margin-bottom: 15px;
    }
    /* 定義不同部門的顏色 */
    .theme-orange { background: linear-gradient(135deg, #ff9a44, #fc6076); }
    .theme-blue { background: linear-gradient(135deg, #4facfe, #00f2fe); }
    .theme-purple { background: linear-gradient(135deg, #667eea, #764ba2); }
    .theme-gray { background: linear-gradient(135deg, #bdc3c7, #2c3e50); }
    
    /* 調整連結卡片內的文字間距 */
    .link-card-title {
        font-size: 1.1em;
        font-weight: 600;
        margin-bottom: 0px;
    }
    .link-card-desc {
        font-size: 0.9em;
        color: #666;
        margin-bottom: 10px;
        height: 40px; /* 固定高度讓排版整齊 */
        overflow: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# --- 函式庫 ---
def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_CONFIG

def save_config(new_config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(new_config, f, ensure_ascii=False, indent=4)

def render_styled_header(text, icon, theme):
    """渲染帶有主題色的漂亮標題"""
    st.markdown(f"""
        <div class="dept-header theme-{theme}">
            {icon} {text}
        </div>
    """, unsafe_allow_html=True)

def render_card(link):
    """渲染單一連結卡片 (使用 container 增加邊框感)"""
    # 使用 st.container(border=True) 創造卡片效果
    with st.container(border=True):
        st.markdown(f'<div class="link-card-title">{link["name"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="link-card-desc">{link.get("desc", "")}</div>', unsafe_allow_html=True)
        st.link_button("前往系統 🚀", link['url'], use_container_width=True)

# --- 初始化 ---
if "config" not in st.session_state:
    st.session_state.config = load_config()
if "is_manager" not in st.session_state:
    st.session_state.is_manager = False

config = st.session_state.config

# --- 主畫面標題 ---
# 使用 markdown 讓標題更大氣
st.markdown("# 📱 馬尼通訊：智慧運營入口")
st.caption("Money Communications System Portal | 整合營運中心")
st.markdown("---")

# ==========================================
# 核心版面配置 (維持三欄，但加入美化)
# ==========================================
col1, col2, col3 = st.columns(3, gap="medium") # 增加欄位間距

# --- 1. 左欄：行銷部 ---
with col1:
    dept_name = "行銷部"
    dept = config["departments"].get(dept_name)
    if dept:
        # 使用新的美化標題函式
        render_styled_header(dept_name, dept['icon'], dept.get('theme', 'orange'))
        for link in dept["links"]:
            render_card(link)

# --- 2. 中欄：電商部 ---
with col2:
    dept_name = "電商部"
    dept = config["departments"].get(dept_name)
    if dept:
        render_styled_header(dept_name, dept['icon'], dept.get('theme', 'blue'))
        for link in dept["links"]:
            render_card(link)

# --- 3. 右欄：管理部 ---
with col3:
    dept_name = "管理部"
    dept = config["departments"].get(dept_name)
    if dept:
        # 根據是否登入顯示不同主題色
        header_theme = dept.get('theme', 'purple') if st.session_state.is_manager else 'gray'
        render_styled_header(dept_name, dept['icon'], header_theme)
        
        if st.session_state.is_manager:
            # === 已登入 ===
            for link in dept["links"]:
                render_card(link)
            st.markdown("---")
            if st.button("登出系統 🔒", type="secondary"):
                st.session_state.is_manager = False
                st.rerun()
        else:
            # === 未登入 ===
            with st.container(border=True):
                st.info("此區域需要管理權限")
                pwd = st.text_input("請輸入密碼解鎖", type="password")
                if pwd:
                    if pwd == config.get("admin_password", "0526"):
                        st.session_state.is_manager = True
                        st.rerun()
                    else:
                        st.error("❌ 密碼錯誤")

st.markdown("---")

# ==========================================
# Excel 式編輯器 (維持 v2.0 功能，僅微調樣式)
# ==========================================
if st.session_state.is_manager:
    with st.expander("⚙️ 系統參數設定 (後台管理)"):
        st.info("💡 操作說明：直接在表格中修改。新增請點擊表格下方 `+`。修改完畢請按「儲存」。")
        
        dept_options = list(config["departments"].keys())
        col_a, col_b = st.columns([1, 3])
        with col_a:
            selected_dept = st.selectbox("選擇編輯部門", dept_options)
        
        # 將資料轉為表格
        current_links = config["departments"][selected_dept]["links"]
        if not current_links:
            current_links = [{"name": "範例按鈕", "url": "https://", "desc": "說明"}]
        df = pd.DataFrame(current_links)
        
        with col_b:
            # 顯示可編輯表格
            edited_df = st.data_editor(
                df, 
                num_rows="dynamic",
                use_container_width=True,
                column_config={
                    "name": st.column_config.TextColumn("按鈕名稱", required=True),
                    "url": st.column_config.LinkColumn("連結網址", required=True),
                    "desc": st.column_config.TextColumn("功能描述")
                },
                key=f"editor_{selected_dept}"
            )
            
            if st.button("💾 儲存變更設定", type="primary"):
                new_links = edited_df.to_dict(orient="records")
                config["departments"][selected_dept]["links"] = new_links
                save_config(config)
                st.session_state.config = config
                st.success(f"✅ {selected_dept} 設定已更新！")
                st.rerun()

# --- 頁尾 ---
st.caption(f"© 2026 Money Communications System {VERSION}")
