import streamlit as st
import json
import os
import pandas as pd

# --- 參數設定 ---
CONFIG_FILE = "money_config.json"
VERSION = "v2.5 (Pastel Colors)"

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
st.set_page_config(page_title="馬尼通訊 工具系統入口", page_icon="📱", layout="wide")

# ==========================================
# 🎨 v2.5 CSS：輕柔粉彩色系 (Pastel)
# ==========================================
st.markdown("""
    <style>
    /* 1. 部門標題 (維持漸層，但稍微調亮一點點以配合粉嫩按鈕) */
    .dept-header {
        padding: 12px;
        border-radius: 12px 12px 0 0;
        color: white;
        text-align: center;
        font-size: 1.6em;
        font-weight: 800;
        letter-spacing: 1px;
        margin-bottom: 0px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }

    /* 2. 卡片容器 */
    .link-card {
        border-radius: 0 0 12px 12px;
        padding: 15px;
        margin-bottom: 15px;
        border-left: 1px solid rgba(0,0,0,0.03);
        border-right: 1px solid rgba(0,0,0,0.03);
        border-bottom: 1px solid rgba(0,0,0,0.03);
        transition: transform 0.2s;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .link-card:hover {
        transform: translateY(-3px);
    }

    /* 3. 色彩定義：更加輕柔的粉彩系 */
    
    /* 行銷部 - 蜜桃粉橘 */
    .header-orange { background: linear-gradient(135deg, #FFB4A2, #E5989B); } /* 標題也變柔和 */
    .bg-orange { background-color: rgba(255, 180, 162, 0.08); } 
    .btn-orange { background-color: #E59E8C; } /* 更淡的陶土色 */

    /* 電商部 - 空氣藍 */
    .header-blue { background: linear-gradient(135deg, #A2D2FF, #8ECAE6); }
    .bg-blue { background-color: rgba(162, 210, 255, 0.08); }
    .btn-blue { background-color: #87A8C9; color: white !important; } /* 更淡的鋼藍色 */

    /* 管理部 - 丁香紫 */
    .header-purple { background: linear-gradient(135deg, #CDB4DB, #B5838D); }
    .bg-purple { background-color: rgba(205, 180, 219, 0.08); }
    .btn-purple { background-color: #A89BC0; } /* 更淡的藕紫色 */
    
    /* 鎖定狀態 */
    .header-gray { background: linear-gradient(135deg, #E0E0E0, #BDBDBD); }
    .bg-gray { background-color: #fdfdfd; }

    /* 4. 文字顏色 (深灰，保持閱讀性) */
    .card-title {
        font-size: 1.15em;
        font-weight: bold;
        color: #555; 
        margin-bottom: 5px;
    }
    .card-desc {
        font-size: 0.9em;
        color: #888;
        margin-bottom: 15px;
        min-height: 40px;
        line-height: 1.4;
    }

    /* 5. 按鈕樣式 */
    .custom-btn {
        display: block;
        width: 100%;
        padding: 8px 10px;
        text-align: center;
        border-radius: 8px;
        text-decoration: none !important;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        color: white !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        border: none;
    }
    .custom-btn:hover {
        transform: translateY(-2px);
        filter: brightness(0.95);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
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
    st.markdown(f"""
        <div class="dept-header header-{theme}">
            {icon} {text}
        </div>
    """, unsafe_allow_html=True)

def render_html_card(link, theme):
    btn_style = f"btn-{theme}"
    html_code = f"""
    <div class="link-card bg-{theme}">
        <div>
            <div class="card-title">{link['name']}</div>
            <div class="card-desc">{link.get('desc', '')}</div>
        </div>
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

# --- 主畫面標題 (更名) ---
st.markdown("# 📱 馬尼通訊 工具系統入口")
st.caption("Money Communications Tools Portal | 整合營運中心")
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
        theme = dept.get('theme', 'purple') if st.session_state.is_manager else 'gray'
        render_styled_header(dept_name, dept['icon'], theme)
        
        if st.session_state.is_manager:
            # === 已登入 ===
            st.markdown(f'<div class="bg-{theme}" style="padding:10px; border-radius:0 0 12px 12px;">', unsafe_allow_html=True)
            for link in dept["links"]:
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
                <div class="card-title" style="text-align:center; color:#888;">🔒 權限鎖定</div>
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
# Excel 式編輯器 (後台管理)
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
