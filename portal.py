import streamlit as st
import json
import os
import pandas as pd

# --- 參數設定 ---
CONFIG_FILE = "money_config.json"
VERSION = "v2.0"

# --- 預設設定檔 (如果找不到檔案時會自動建立) ---
DEFAULT_CONFIG = {
    "admin_password": "0526",
    "departments": {
        "行銷部": {
            "icon": "📢",
            "protected": False,
            "links": [
                {"name": "馬尼行銷活動進程", "url": "https://money-marketing-room.streamlit.app/", "desc": "活動排程與進度"},
                {"name": "馬尼活動發想規劃", "url": "https://moneyweb.streamlit.app/", "desc": "活動的提案與設定"}
            ]
        },
        "電商部": {
            "icon": "🛒",
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
            "protected": True,
            "links": [
                {"name": "業績戰情室", "url": "https://money-real-timesalesperformancereport.streamlit.app/", "desc": "每月業績"},
                {"name": "人員評核", "url": "https://hqkpiapp.streamlit.app/", "desc": "績效評分"}
            ]
        }
    }
}

# --- 頁面設定 (寬螢幕模式) ---
st.set_page_config(page_title="馬尼通訊系統入口", page_icon="📱", layout="wide")

# --- CSS 優化 (讓按鈕與卡片整齊) ---
st.markdown("""
    <style>
    .stButton button {width: 100%;}
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

def render_card(link):
    """渲染單一連結卡片"""
    st.info(f"**{link['name']}**")
    st.caption(link.get('desc', '-'))
    st.link_button("前往 🚀", link['url'], use_container_width=True)
    st.write("")

# --- 初始化 ---
if "config" not in st.session_state:
    st.session_state.config = load_config()
if "is_manager" not in st.session_state:
    st.session_state.is_manager = False

config = st.session_state.config

# --- 主畫面標題 ---
st.title(f"📱 馬尼通訊系統入口")
st.markdown("---")

# ==========================================
# 核心版面配置：左(行銷) / 中(電商) / 右(管理)
# ==========================================
col1, col2, col3 = st.columns(3)

# --- 1. 左欄：行銷部 (固定) ---
with col1:
    dept_name = "行銷部"
    dept = config["departments"].get(dept_name)
    if dept:
        st.subheader(f"{dept['icon']} {dept_name}")
        st.markdown("---")
        for link in dept["links"]:
            render_card(link)

# --- 2. 中欄：電商部 (固定) ---
with col2:
    dept_name = "電商部"
    dept = config["departments"].get(dept_name)
    if dept:
        st.subheader(f"{dept['icon']} {dept_name}")
        st.markdown("---")
        for link in dept["links"]:
            render_card(link)

# --- 3. 右欄：管理部 (含登入邏輯) ---
with col3:
    dept_name = "管理部"
    dept = config["departments"].get(dept_name)
    if dept:
        st.subheader(f"{dept['icon']} {dept_name}")
        st.markdown("---")
        
        if st.session_state.is_manager:
            # === 已登入 ===
            for link in dept["links"]:
                render_card(link)
                
            st.markdown("---")
            if st.button("登出系統", type="secondary"):
                st.session_state.is_manager = False
                st.rerun()
        else:
            # === 未登入 (顯示密碼框) ===
            st.warning("🔒 管理專區")
            pwd = st.text_input("輸入密碼 (Enter)", type="password")
            if pwd:
                if pwd == config.get("admin_password", "0526"):
                    st.session_state.is_manager = True
                    st.rerun()
                else:
                    st.error("❌ 密碼錯誤")

st.markdown("---")

# ==========================================
# v2.0 重點功能：Excel 式編輯器 (僅管理員可見)
# ==========================================
if st.session_state.is_manager:
    with st.expander("⚙️ 系統參數設定 (圖形化編輯版)"):
        st.info("💡 操作說明：直接在表格中點擊修改，支援新增列與刪除。修改完畢請記得按「儲存」。")
        
        # 1. 選擇要編輯的部門
        dept_options = list(config["departments"].keys())
        selected_dept = st.selectbox("請選擇要編輯的部門", dept_options)
        
        # 2. 將資料轉為表格 (DataFrame) 以便編輯
        current_links = config["departments"][selected_dept]["links"]
        # 確保有資料，避免 DataFrame 報錯
        if not current_links:
            current_links = [{"name": "範例按鈕", "url": "https://", "desc": "說明"}]
            
        df = pd.DataFrame(current_links)
        
        # 3. 顯示可編輯表格 (Data Editor)
        edited_df = st.data_editor(
            df, 
            num_rows="dynamic", # 允許新增刪除列
            use_container_width=True,
            column_config={
                "name": st.column_config.TextColumn("按鈕名稱", required=True),
                "url": st.column_config.LinkColumn("連結網址", required=True),
                "desc": st.column_config.TextColumn("功能描述")
            },
            key=f"editor_{selected_dept}"
        )
        
        # 4. 儲存按鈕
        if st.button("💾 儲存變更"):
            # 將表格轉回清單格式
            new_links = edited_df.to_dict(orient="records")
            
            # 更新設定到記憶體
            config["departments"][selected_dept]["links"] = new_links
            
            # 寫入檔案
            save_config(config)
            st.session_state.config = config
            
            st.success(f"✅ {selected_dept} 設定已更新！")
            st.rerun()

# --- 頁尾 ---
st.caption(f"© 2026 Money Communications System {VERSION}")
