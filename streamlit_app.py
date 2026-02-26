# import streamlit as st
# import requests
# import pandas as pd

# # Page config
# st.set_page_config(
#     page_title="DataBot",
#     page_icon="🧠",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # Custom CSS for modern look based on the reference design
# st.markdown("""
# <style>
#     /* Global Background and Fonts */
#     [data-testid="stAppViewContainer"] {
#         background-color: #F8F9FC;
#         font-family: 'Inter', sans-serif;
#     }
#     [data-testid="stHeader"] {
#         background-color: transparent;
#     }
    
#     /* Hide top padding and default header elements */
#     .block-container {
#         padding-top: 2rem !important;
#         padding-bottom: 2rem !important;
#         max-width: 1000px !important;
#     }
    
#     /* Top Bar Branding */
#     .top-bar {
#         display: flex;
#         align-items: center;
#         gap: 15px;
#         padding-bottom: 20px;
#     }
#     .brand-icon {
#         background-color: #4C6FFF;
#         color: white;
#         border-radius: 8px;
#         width: 32px;
#         height: 32px;
#         display: flex;
#         align-items: center;
#         justify-content: center;
#         font-size: 18px;
#         box-shadow: 0 4px 6px rgba(76, 111, 255, 0.2);
#     }
#     .brand-name {
#         font-weight: 700;
#         font-size: 24px;
#         color: #1E2330;
#     }
    
#     /* Hero Typography */
#     .hero-title {
#         text-align: center;
#         font-size: 38px;
#         font-weight: 800;
#         color: #1A1C29;
#         margin-top: 15px;
#         margin-bottom: 10px;
#         letter-spacing: -0.5px;
#     }
#     .hero-subtitle {
#         text-align: center;
#         color: #717A8B;
#         font-size: 18px;
#         max-width: 600px;
#         margin: 0 auto 30px auto;
#         line-height: 1.5;
#     }

#     /* Suggestion Pills (Secondary Buttons) */
#     div[data-testid="stButton"] button[kind="secondary"] {
#         background-color: white !important;
#         color: #636D82 !important;
#         border: 1px solid #E2E8F0 !important;
#         border-radius: 20px !important;
#         padding: 5px 20px !important;
#         font-size: 14px !important;
#         transition: all 0.2s ease;
#         box-shadow: 0 1px 2px rgba(0,0,0,0.02) !important;
#         white-space: nowrap !important;
#     }
#     div[data-testid="stButton"] button[kind="secondary"] p {
#         font-size: 14px !important;
#     }
#     div[data-testid="stButton"] button[kind="secondary"]:hover {
#         border-color: #4C6FFF !important;
#         color: #4C6FFF !important;
#         background-color: #F8F9FC !important;
#     }

#     /* Input Styling */
#     div[data-testid="stTextInput"] > div > div > input {
#         background-color: white !important;
#         color: #1E2330 !important;
#         border-radius: 12px !important;
#         border: 2px solid #C4D2FF !important;
#         padding: 16px 20px !important;
#         font-size: 16px !important;
#         box-shadow: 0 4px 15px rgba(196, 210, 255, 0.4) !important;
#         transition: all 0.2s ease;
#     }
#     div[data-testid="stTextInput"] > div > div > input:focus {
#         border-color: #4C6FFF !important;
#         box-shadow: 0 44px 15px rgba(76, 111, 255, 0.3) !important;
#     }

#     /* Primary Search Button Styling */
#     div[data-testid="stButton"] button[kind="primary"] {
#         background-color: #5575FF !important;
#         color: white !important;
#         border-radius: 12px !important;
#         border: none !important;
#         padding: 10px 30px !important;
#         font-weight: 600 !important;
#         font-size: 16px !important;
#         box-shadow: 0 4px 10px rgba(85, 117, 255, 0.3) !important;
#         transition: transform 0.1s ease, background-color 0.2s ease !important;
#     }
#     div[data-testid="stButton"] button[kind="primary"] p {
#         font-size: 16px !important;
#         color: white !important;
#     }
#     div[data-testid="stButton"] button[kind="primary"]:hover {
#         background-color: #4562E6 !important;
#         transform: translateY(-1px) !important;
#     }
    
#     /* Results Labels */
#     .db-label {
#         font-weight: 700;
#         font-size: 14px;
#         color: #5A6A85;
#         display: flex;
#         align-items: center;
#         gap: 8px;
#         margin-bottom: 20px;
#         letter-spacing: 0.5px;
#         text-transform: uppercase;
#     }
#     .db-icon {
#         background: #EEF2FF;
#         color: #5575FF;
#         padding: 6px;
#         border-radius: 8px;
#         display: inline-flex;
#     }
#     .db-icon.yellow { color: #F59E0B; background: #FEF3C7; }
# </style>
# """, unsafe_allow_html=True)

# # Top Bar
# st.markdown("""
# <div class="top-bar">
#     <div class="brand-icon">🧠</div>
#     <div class="brand-name">DataBot</div>
# </div>
# """, unsafe_allow_html=True)

# # Center Icon
# st.markdown("""
# <div style='display: flex; justify-content: center; margin-top: 10px;'>
#     <div style='background-color: #EEF2FF; border-radius: 12px; color: #5575FF; font-size: 20px; width: 44px; height: 44px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 10px rgba(85,117,255,0.15);'>
#         🔍
#     </div>
# </div>
# """, unsafe_allow_html=True)

# # Hero Section
# st.markdown("<h1 class='hero-title'>Hello! Ask me anything about jobs & industries</h1>", unsafe_allow_html=True)
# st.markdown("<p class='hero-subtitle'>I'll search multiple databases and find the best matches for you — from skills and locations to companies and roles.</p>", unsafe_allow_html=True)

# # Suggestion Pills Setup
# if "search_query" not in st.session_state:
#     st.session_state.search_query = ""

# def set_query(q):
#     st.session_state.search_query = q

# col1, col2, col3, col4, col5 = st.columns([1, 2, 2.5, 2, 1])
# with col2: st.button("Software Engineer in NYC", on_click=set_query, args=("Software Engineer in NYC",), use_container_width=True)
# with col3: st.button("Marketing roles with leadership skills", on_click=set_query, args=("Marketing roles with leadership skills",), use_container_width=True)
# with col4: st.button("Remote data analyst jobs", on_click=set_query, args=("Remote data analyst jobs",), use_container_width=True)

# # Spacing manually
# st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# # Search Input Area
# search_col1, search_col2, search_col3 = st.columns([1.5, 7, 1.5])
# with search_col2:
#     inner_col1, inner_col2 = st.columns([5, 1.5])
#     with inner_col1:
#         user_query = st.text_input(
#             label="Search Query", 
#             label_visibility="collapsed", 
#             placeholder="e.g. software engineers",
#             value=st.session_state.search_query,
#             key="search_input"
#         )
#     with inner_col2:
#         st.markdown("<div style='margin-top: 1px;'></div>", unsafe_allow_html=True)
#         search_button = st.button("🔍 Search", type="primary", use_container_width=True)

# # Bottom spacer
# st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

# # Execution block
# if search_button and user_query:
#     with st.spinner("🤖 Consulting DataBot..."):
#         try:
#             response = requests.get(f"http://localhost:8000/search?q={user_query}")
#             response.raise_for_status()
#             data = response.json()
            
#             extracted = data["extracted_params"]
#             merged_data = data["results"]["merged"]
#             pg_data = data["results"]["postgres"]
#             es_data = data["results"]["elasticsearch"]
            
#             # Show reasoning info
#             with st.expander("🧠 Agent Reasoning & Parameters", expanded=False):
#                 st.write(f"**Reasoning:** {extracted.get('reasoning', 'Extracted structural parameters for search.')}")
#                 st.write(f"**Parameters:** " + ", ".join([f"{k}: {v}" for k, v in extracted.items() if k != 'reasoning' and v]))
            
#             st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
            
#             # Formulate the "Why it was fetched" summary
#             active_params = [f"{k.capitalize()}: {v}" for k, v in extracted.items() if k != 'reasoning' and v]
#             reason_msg = "Fetching all active records"
#             if active_params:
#                 reason_msg = f"Fetching records matching {', '.join(active_params)} across all databases."
                
#             # --- MERGED RESULTS SECTION ---
#             st.markdown(f"### 🤝 Merged Results")
#             st.info(f"**Why these results appear:** {reason_msg}")
            
#             if merged_data["duplicates_removed"] > 0:
#                 st.warning(f"🧹 Omitted {merged_data['duplicates_removed']} duplicate records across combined datasets.")
                
#             if merged_data["data"] and "error" not in merged_data["data"][0]:
#                 st.caption(f"Showing {merged_data['total_found']} unique absolute results")
#                 st.dataframe(pd.DataFrame(merged_data["data"]), use_container_width=True, hide_index=True)
#             else:
#                 st.info("No matching records found across any database.")
                
#             st.divider()
            
#             # --- INDIVIDUAL DB DATABASES ---
#             res_col1, res_col2 = st.columns(2)
            
#             with res_col1:
#                 st.markdown("""
#                 <div class="db-label es">
#                     <div class="db-icon yellow">⚡</div> ELASTICSEARCH
#                 </div>
#                 """, unsafe_allow_html=True)
                
#                 if es_data["data"] and "error" in es_data["data"][0]:
#                     st.error(f"❌ {es_data['data'][0]['error']}")
#                 else:
#                     st.caption(f"Found {es_data['total_found']} results (Omitted {es_data['duplicates_removed']} duplicates)")
#                     if es_data["data"]:
#                         st.dataframe(pd.DataFrame(es_data["data"]), use_container_width=True, hide_index=True)
#                     else:
#                         st.info("No matching records found in Elasticsearch.")
            
#             with res_col2:
#                 st.markdown("""
#                 <div class="db-label pg">
#                     <div class="db-icon">🛢</div> POSTGRESQL
#                 </div>
#                 """, unsafe_allow_html=True)
                
#                 if pg_data["data"] and "error" in pg_data["data"][0]:
#                     st.error(f"❌ {pg_data['data'][0]['error']}")
#                 else:
#                     st.caption(f"Found {pg_data['total_found']} results (Omitted {pg_data['duplicates_removed']} duplicates)")
#                     if pg_data["data"]:
#                         st.dataframe(pd.DataFrame(pg_data["data"]), use_container_width=True, hide_index=True)
#                     else:
#                         st.info("No matching records found in PostgreSQL.")
                    
#         except Exception as e:
#             st.error(f"Error fetching results: {e}")
#             st.info("Make sure the FastAPI backend is running on http://localhost:8000")


import streamlit as st
import requests
import pandas as pd

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="DataBot AI | Intelligence Engine",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. BLUE THEME & ANIMATION CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');

    [data-testid="stAppViewContainer"] {
        background-color: #F8F9FC;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .nav-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 40px;
        background: white;
        border-radius: 0 0 25px 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
        margin-bottom: 60px;
    }

    .hero-title {
        text-align: center;
        font-size: 56px !important;
        font-weight: 800;
        color: #1E293B;
        letter-spacing: -1.5px;
        margin-bottom: 5px;
    }

    .animated-word {
        background: linear-gradient(90deg, #6366F1, #9333EA, #6366F1);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
    }

    @keyframes shine { to { background-position: 200% center; } }

    div[data-testid="stTextInput"] > div > div > input {
        border-radius: 14px !important;
        padding: 16px 22px !important;
        border: 1px solid #E2E8F0 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04) !important;
    }

    .res-card {
        background: white;
        border-radius: 18px;
        padding: 20px;
        border: 1px solid #F1F5F9;
        box-shadow: 0 8px 20px rgba(0,0,0,0.02);
    }
</style>
""", unsafe_allow_html=True)

# 3. NAVIGATION BAR
st.markdown("""
<div class="nav-bar">
    <div style="display: flex; align-items: center; gap: 12px;">
        <span style="font-size: 24px;">🧠</span>
        <span style="font-weight: 800; font-size: 22px; color: #1E293B;">DataBot<span style="color: #6366F1;">.ai</span></span>
    </div>
    <div style="color: #94A3B8; font-weight: 600; font-size: 13px;">v2.0 Professional Edition</div>
</div>
""", unsafe_allow_html=True)

# 4. HERO SECTION
st.markdown("<h1 class='hero-title'>Discover <span class='animated-word'>Opportunities</span> in Seconds</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748B; font-size: 18px; margin-bottom: 40px;'>The most powerful cross-database search engine for the modern job market.</p>", unsafe_allow_html=True)

# 5. SUGGESTION PILLS (ERROR FIXED)
if "search_query" not in st.session_state:
    st.session_state.search_query = ""

def set_query(q):
    st.session_state.search_query = q

pills = st.columns([1, 2, 2, 2, 1])
# Removed 'kind' argument to ensure compatibility with your Streamlit version
with pills[1]: st.button("📍 Software in NYC", on_click=set_query, args=("Software Engineer in NYC",), use_container_width=True)
with pills[2]: st.button("🚀 Marketing Leadership", on_click=set_query, args=("Marketing Leadership",), use_container_width=True)
with pills[3]: st.button("🏠 Remote Analyst", on_click=set_query, args=("Remote Analyst",), use_container_width=True)

st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

# 6. SEARCH INPUT
sc1, sc2, sc3 = st.columns([1.5, 7, 1.5])
with sc2:
    search_box, search_btn = st.columns([5, 1.2])
    with search_box:
        user_query = st.text_input("Query", label_visibility="collapsed", placeholder="Search by role, skill, or location...", value=st.session_state.search_query)
    with search_btn:
        search_button = st.button("Search", type="primary", use_container_width=True)

        # 7. BACKEND INTEGRATION LOGIC
if search_button and user_query:
    with st.status("🔍 Searching Databases...", expanded=True) as status:
        try:
            # API Request to your FastAPI backend
            response = requests.get(f"http://localhost:8000/search?q={user_query}")
            response.raise_for_status()
            data = response.json()
            
            # Map response data
            extracted = data["extracted_params"]
            v_res = data["results"]["verified"]
            i_res = data["results"]["inferred"]
            
            status.update(label="✅ Search Complete!", state="complete", expanded=False)

            # Display Extraction/Reasoning
            with st.expander("🛠 Extraction Logic & NLP Analysis", expanded=False):
                col_ex1, col_ex2 = st.columns([3, 1])
                with col_ex1:
                    st.json(extracted)
                with col_ex2:
                    st.markdown(f"""<div class="res-card" style="text-align:center;">
                        <div style="font-size:10px; color:#64748B; font-weight:700;">VERIFIED RECORDS</div>
                        <div style="font-size:28px; font-weight:800; color:#4C6FFF;">{v_res['total_found']}</div>
                    </div>""", unsafe_allow_html=True)
                st.info(f"**Analysis:** {extracted.get('reasoning', 'Extracted parameters for optimized search.')}")

            # SECTION 1: VERIFIED RESULTS
            st.markdown("""
            <div style="margin-top: 20px; padding: 15px; border-left: 5px solid #3B82F6; background: #EFF6FF; border-radius: 8px;">
                <h3 style="margin: 0; color: #1E3A8A; font-size: 20px;">🛡️ Verified Database Results</h3>
                <p style="margin: 5px 0 0 0; color: #3B82F6; font-size: 14px;">Extracted strictly from explicit query terms. No semantic assumptions applied.</p>
            </div>
            """, unsafe_allow_html=True)
            
            if v_res["duplicates_removed"] > 0 or v_res["total_found"] > 0:
                m1, m2, m3 = st.columns(3)
                with m1:
                    st.metric("Total Unique Records", v_res["total_found"])
                with m2:
                    total_raw = len(v_res.get("postgres_data", [])) + len(v_res.get("elastic_data", []))
                    st.metric("Total Records Found", total_raw)
                with m3:
                    st.metric("Duplicates Removed", v_res["duplicates_removed"])

            if v_res["data"]:
                st.dataframe(pd.DataFrame(v_res["data"]), use_container_width=True, hide_index=True)
            else:
                st.info("No matching verified records found across your ecosystem.")


            # SECTION 3: SOURCE DATA BREAKDOWN
            st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
            st.markdown("### 🔍 Individual Source Data (Deduplicated)")
            
            def get_unique_records(records):
                seen = set()
                unique = []
                for r in records:
                    key = (r.get("occupation"), r.get("field"), r.get("city"), r.get("country"))
                    if key not in seen:
                        seen.add(key)
                        unique.append(r)
                return unique

            s_col1, s_col2 = st.columns(2)
            
            with s_col1:
                pg_raw = v_res.get("postgres_data", [])
                pg_unique = get_unique_records(pg_raw)
                st.markdown(f"""<div style="padding:10px; background:#F1F5F9; border-radius:8px; margin-bottom:10px; display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight:700; color:#475569;">🛢 PostgreSQL Source</span>
                    <span style="background:#3B82F6; color:white; padding:2px 8px; border-radius:12px; font-size:12px;">{len(pg_unique)} unique / {len(pg_raw)} total</span>
                </div>""", unsafe_allow_html=True)
                if pg_unique:
                    st.dataframe(pd.DataFrame(pg_unique), use_container_width=True, hide_index=True)
                else:
                    st.info("No records found in PostgreSQL.")
            
            with s_col2:
                es_raw = v_res.get("elastic_data", [])
                es_unique = get_unique_records(es_raw)
                st.markdown(f"""<div style="padding:10px; background:#F1F5F9; border-radius:8px; margin-bottom:10px; display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight:700; color:#475569;">⚡ Elasticsearch Source</span>
                    <span style="background:#F59E0B; color:white; padding:2px 8px; border-radius:12px; font-size:12px;">{len(es_unique)} unique / {len(es_raw)} total</span>
                </div>""", unsafe_allow_html=True)
                if es_unique:
                    st.dataframe(pd.DataFrame(es_unique), use_container_width=True, hide_index=True)
                else:
                    st.info("No records found in Elasticsearch.")
                    
        except Exception as e:
            st.error(f"Search Engine Error: {e}")

# 8. FOOTER
st.markdown("<div style='text-align: center; color: #CBD5E1; font-size: 11px; margin-top: 50px;'>Built with ❤️ for Data Engineering | © 2026 DataBot AI</div>", unsafe_allow_html=True)