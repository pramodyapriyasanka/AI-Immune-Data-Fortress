import streamlit as st
import boto3
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
from dotenv import load_dotenv
import time
from datetime import datetime

load_dotenv()

s3 = boto3.client('s3')
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

st.set_page_config(page_title="Data Fortress Console", layout="wide")


st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; color: #1e293b; }
    
    /* Header Bar change the color */
    .header-bar {
        background-color: #f1f5f9; 
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        color: #0f172a;
        margin-bottom: 25px;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .header-bar h1 { color: #0f172a !important; margin: 0; font-size: 28px; }
    
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

def get_stats():
    try:
        res_t = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix='trusted/')
        res_q = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix='quarantine/')
        t_count = res_t.get('KeyCount', 0)
        q_count = res_q.get('KeyCount', 0)
        
        t_list = [obj['Key'].split('/')[-1] for obj in res_t.get('Contents', []) if not obj['Key'].endswith('/')][-5:]
        q_list = [obj['Key'].split('/')[-1] for obj in res_q.get('Contents', []) if not obj['Key'].endswith('/')][-5:]
        
        return t_count, q_count, t_list, q_list
    except:
        return 0, 0, [], []


st.markdown(f'''
    <div class="header-bar">
        <span style="font-size: 40px;">🛡️</span>
        <div>
            <h1>AI-Immune Data Fortress | Security Console</h1>
            <p style="margin:0; color:#64748b;">Autonomous Security Monitoring & Real-time Audit Stream</p>
        </div>
    </div>
''', unsafe_allow_html=True)

placeholder = st.empty()


traffic_history = []

while True:
    t_cnt, q_cnt, t_list, q_list = get_stats()
    total = t_cnt + q_cnt
    success_rate = (t_cnt / total * 100) if total > 0 else 0
    
    
    traffic_history.append({'Time': datetime.now().strftime('%H:%M:%S'), 'Count': total})
    if len(traffic_history) > 10: traffic_history.pop(0)

    with placeholder.container():
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Audited", total)
        m2.metric("✅ Trusted Records", t_cnt)
        m3.metric("🚨 Quarantined", q_cnt)
        m4.metric("📊 Reliability Score", f"{round(success_rate, 1)}%")

        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns([1.2, 0.8])
        
        with c1:
            st.markdown("### 📈 Live Data Ingestion Traffic")
            traffic_df = pd.DataFrame(traffic_history)
            fig_line = px.line(traffic_df, x='Time', y='Count', markers=True, 
                               line_shape='spline', render_mode='svg')
            fig_line.update_traces(line_color='#3b82f6')
            fig_line.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=350)
            st.plotly_chart(fig_line, use_container_width=True)

        with c2:
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = success_rate,
                number = {'suffix': "%", 'font': {'color': "#0f172a"}},
                title = {'text': "Integrity Score", 'font': {'size': 18, 'color': '#64748b'}},
                gauge = {
                    'axis': {'range': [None, 100], 'tickcolor': "#64748b"},
                    'bar': {'color': "#3b82f6"},
                    'bgcolor': "#f1f5f9",
                    'steps': [{'range': [0, 60], 'color': '#fee2e2'}, {'range': [60, 100], 'color': '#dcfce7'}]}
            ))
            fig_gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", height=350)
            st.plotly_chart(fig_gauge, use_container_width=True)

        st.markdown("### 📥 Recent System Logs")
        log_data = []
        for item in reversed(t_list): log_data.append({"Record": item, "Status": "✅ PASS"})
        for item in reversed(q_list): log_data.append({"Record": item, "Status": "❌ FAIL"})
        
        if log_data:
            df = pd.DataFrame(log_data)
            st.dataframe(df, use_container_width=True) 
        else:
            st.info("Waiting for data stream...")

        time.sleep(5)
        st.rerun()