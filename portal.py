import streamlit as st
import json
import os
import pandas as pd

# --- 參數設定 ---
CONFIG_FILE = "money_config.json"
VERSION = "v2.2 (UI Polish)"

# --- 預設設定檔 ---
DEFAULT_CONFIG = {
    "admin_password": "0526",
    "departments": {
        "行銷部": {
            "icon": "📢",
            "theme": "orange",
            "protected": False,
            "links": [
                {"name": "馬尼行銷活動進程", "url": "https://money-marketing-room.streamlit.app/", "desc": "活動排程與進度"},
                {"name": "馬尼活動發想規劃", "url": "https://moneyweb.streamlit.app/", "desc": "活動的提案與設定"}
            ]
        },
        "電商部": {
            "icon": "🛒",
            "theme": "blue",
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
            "theme": "purple",
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
# 🎨 v2.2 CSS 魔法：背景色、大標題、按鈕特效
# ==========================================
st.markdown("""
    <style>
    /* 1. 部門標題放大與美化 */
    .dept-header {
        padding: 12px;
        border-radius: 12px 12px 0 0;
        color: white;
        text-align: center;
        font-size: 1.6em; /* 字體放大 */
        font-weight: 800; /* 加粗 */
        letter-spacing: 1px;
        margin-bottom: 0px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* 2. 卡片容器：加上淡淡背景色 */
    .link-card {
        border-radius: 0 0 12px 12px; /* 下方圓角 */
        padding: 15px;
        margin-bottom: 15px;
        border-left: 1px solid rgba(0,0,0,0.05);
        border-right: 1px solid rgba(0,0,0,0.05);
        border-bottom: 1px solid rgba(0,0,0,0.05);
        transition: transform 0.2s;
    }
    .link-card:hover {
        transform: translateY(-3px); /* 卡片懸浮效果 */
    }

    /* 3. 主題色定義 (標題背景 + 卡片淡色背景) */
    /* 行銷部 - 橘色 */
    .header-orange { background: linear-gradient(135deg, #FF9966, #FF5E62); }
    .bg-orange { background-color: rgba(255, 153, 102, 0.08); } /* 8% 透明度 */
    .btn-orange { background-color: #FF5E62; }

    /* 電商部 - 藍色 */
    .header-blue { background: linear-gradient(135deg, #4facfe, #00f2fe); }
    .bg-blue { background-color: rgba(79, 172, 254, 0.08); }
    .btn-blue { background-color: #00f2fe; color: #005bea !important; }

    /* 管理部 - 紫色 */
    .header-purple { background: linear-gradient(135deg, #667eea, #764ba2); }
    .bg-purple { background-color: rgba(102, 126, 234, 0.08); }
    .btn-purple { background-color: #764ba2; }
    
    /* 鎖定狀態 - 灰色 */
    .header-gray { background: linear-gradient(135deg, #bdc3c7, #2c3e50); }
    .bg-gray { background-color: #f8f9fa; }

    /* 4. 卡片內容排版 */
    .card-title {
        font-size: 1.15em;
        font-weight: bold;
        color: #333;
        margin-bottom: 5px;
    }
    .card-desc {
        font-size: 0.9em;
        color: #666;
        margin-bottom: 15px;
        min-height: 40px;
        line-height: 1.4;
    }

    /* 5. 客製化按鈕 (取代 Streamlit 原生按鈕以獲得更多特效) */
    .custom-btn {
        display: block;
        width: 100%;
        padding: 8px 10px;
        text-align: center;
        border-radius: 8px;
        text-decoration: none !important; /* 去除底線 */
        font-weight: bold;
        transition: all 0.3s ease;
        color: white !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .custom-btn:hover {
        transform: scale(1.02); /* 放大 */
        box-shadow: 0 5px 15px rgba(0,0,0,0.2); /* 陰影加深 */
        filter: brightness(1.1); /* 變亮 */
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
    """渲染大標題"""
    st.markdown(f"""
        <div class="dept-header header-{theme}">
            {icon} {text}
        </div>
    """, unsafe_allow_html=True)

def render_html_card(link, theme):
    """
    渲染帶有背景色與特效的 HTML 卡片
    (為了達到背景色需求，我們這裡改用 HTML 渲染而非 st.container)
    """
    # 針對藍色主題的按鈕文字做一點深色調整，避免看不清楚
    btn_style = f"btn-{theme}"
    
    html_code = f"""
    <div class="link-card bg-{theme}">
        <div class="card-title">{link['name']}</div>
        <div class="card-desc">{link.get('desc', '')}</div>
        <a href="{link['url']}" target="_blank" class="custom-btn {btn_style}">
            前往系統 🚀
        </a>
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)

# --- 初始化 ---
if "config" not in st.session_state:
    st.session_state.config = load_config()
if "is_manager" not in st.session_state:
    st.session_state.is_manager = False

config = st.session_state.config

# --- 主畫面標題 ---
st.markdown("# 📱 馬尼通訊：智慧運營入口")
st.caption("Money Communications System Portal | 整合營運中心")
st.markdown("---")

# ==========================================
# 核心版面配置
# ==========================================
col1, col2, col3 = st.columns(3, gap="medium")

# --- 1. 左欄：行銷部 ---
with col1:
    dept_name = "行銷部"
    dept = config["departments"].get(dept_name)
    if dept:
        theme = dept.get('theme', 'orange')
        render_styled_header(dept_name, dept['icon'], theme)
        for link in dept["links"]:
            render_html_card(link, theme)

# --- 2. 中欄：電商部 ---
with col2:
    dept_name = "電商部"
    dept = config["departments"].get(dept_name)
    if dept:
        theme = dept.get('theme', 'blue')
        render_styled_header(dept_name, dept['icon'], theme)
        for link in dept["links"]:
            render_html_card(link, theme)

# --- 3. 右欄：管理部 ---
with col3:
    dept_name = "管理部"
    dept = config["departments"].get(dept_name)
    if dept:
        # 判斷主題色
        theme = dept.get('theme', 'purple') if st.session_state.is_manager else 'gray'
        render_styled_header(dept_name, dept['icon'], theme)
        
        if st.session_state.is_manager:
            # === 已登入 ===
            # 包裹一個容器來畫背景 (模擬卡片區)
            st.markdown(f'<div class="bg-{theme}" style="padding:10px; border-radius:0 0 12px 12px;">', unsafe_allow_html=True)
            for link in dept["links"]:
                # 這裡為了不要雙重背景，我們微調一下傳入的 theme
                # 但為了保持一致性，我們還是用 render_html_card，只是 HTML 結構會自動堆疊
                # 簡單來說：直接呼叫即可
                render_html_card(link, 'purple') 
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.write("")
            if st.button("登出系統 🔒", type="secondary"):
                st.session_state.is_manager = False
                st.rerun()
        else:
            # === 未登入 ===
            st.markdown(f"""
            <div class="link-card bg-gray">
                <div class="card-title" style="text-align:center;">🔒 權限鎖定</div>
                <div class="card-desc" style="text-align:center;">此區域僅限管理層存取</div>
            </div>
            """, unsafe_allow_html=True)
            
            pwd = st.text_input("請輸入密碼解鎖", type="password")
            if pwd:
                if pwd == config.get("admin_password", "0526"):
                    st.session_state.is_manager = True
                    st.rerun()
                else:
                    st.error("❌ 密碼錯誤")

st.markdown("---")

# ==========================================
# Excel 式編輯器 (功能維持，僅優化顯示)
# ==========================================
if st.session_state.is_manager:
    with st.expander("⚙️ 系統參數設定 (後台管理)"):
        st.info("💡 操作說明：編輯完畢請務必點擊「💾 儲存變更設定」按鈕。")
        
        dept_options = list(config["departments"].keys())
        col_a, col_b = st.columns([1, 3])
        with col_a:
            selected_dept = st.selectbox("選擇編輯部門", dept_options)
        
        current_links = config["departments"][selected_dept]["links"]
        if not current_links:
            current_links = [{"name": "範例", "url": "https://", "desc": "說明"}]
        df = pd.DataFrame(current_links)
        
        with col_b:
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
