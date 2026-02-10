import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from fpdf import FPDF
import os
import shutil
from database import CVDatabase
from engine import RecruitmentAgent

st.set_page_config(page_title="AI Talent Scout Pro", layout="wide", page_icon="🚀")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .main-title {
        background: -webkit-linear-gradient(#00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem; font-weight: 800; text-align: center; margin-bottom: 2rem;
    }
    .card {
        background: rgba(255, 255, 255, 0.03);
        padding: 1.5rem; border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 1.5rem;
    }
    .stButton>button { border-radius: 10px; font-weight: bold; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

def save_uploaded_files(uploaded_files):
    upload_path = "./cv_folder"
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    for uploaded_file in uploaded_files:
        with open(os.path.join(upload_path, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
    return len(uploaded_files)

def clear_database():
    if os.path.exists("./cv_folder"):
        shutil.rmtree("./cv_folder")
        os.makedirs("./cv_folder")
    if os.path.exists("./chroma_db"):
        shutil.rmtree("./chroma_db")
    st.session_state.results = None
    st.cache_resource.clear()

def create_pdf(res):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    name = res.get('candidate_name', 'Candidate')
    pdf.cell(200, 10, f"Analysis Report: {name}", ln=True, align='C')
    
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(0, 10, f"Match Score: {res.get('overall_score')}%", ln=True)
    
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Technical Summary:", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 8, res.get('summary', 'N/A'))
    
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Suggested Interview Questions:", ln=True)
    pdf.set_font("Arial", size=11)
    for i, q in enumerate(res.get('interview_questions', [])):
        pdf.multi_cell(0, 8, f"{i+1}. {q}")
    
    return pdf.output(dest='S').encode('latin-1', 'ignore')

with st.sidebar:
    st.markdown("## 📂 CV Boshqaruvi")
    uploaded_files = st.file_uploader("PDF formatidagi CVlarni yuklang", type="pdf", accept_multiple_files=True)
    
    if st.button("🚀 Tanlanganlarni saqlash"):
        if uploaded_files:
            num = save_uploaded_files(uploaded_files)
            st.success(f"{num} ta fayl yuklandi!")
            st.cache_resource.clear()
            st.rerun()
        else:
            st.warning("Fayl tanlanmagan!")

    st.divider()
    
    st.markdown("### 📄 Mavjud fayllar:")
    if os.path.exists("./cv_folder"):
        files = os.listdir("./cv_folder")
        for f in files:
            st.caption(f"✔️ {f}")
            
    st.divider()
    
    if st.button("🗑️ Hamma ma'lumotni o'chirish"):
        clear_database()
        st.success("Baza tozalandi!")
        st.rerun()

st.markdown('<h1 class="main-title">🚀 AI Talent Scout Pro</h1>', unsafe_allow_html=True)

@st.cache_resource
def load_system():
    db = CVDatabase()
    return db.build_or_load()

retriever = load_system()

if 'results' not in st.session_state:
    st.session_state.results = None

col_jd, col_res = st.columns([1, 2.2], gap="large")

with col_jd:
    st.markdown("### 📋 Job Description")
    jd_text = st.text_area("Talablarni kiriting:", height=300, placeholder="E.g. Senior ML Engineer...")
    if st.button("Analizni boshlash ⚡"):
        if jd_text and retriever:
            agent = RecruitmentAgent(retriever)
            with st.spinner("AI nomzodlarni skanerlamoqda..."):
                st.session_state.results = sorted(agent.analyze(jd_text), key=lambda x: x['overall_score'], reverse=True)
        elif not retriever:
            st.error("Baza bo'sh! Sidebar orqali CV yuklang.")
        else:
            st.warning("JD matnini kiriting.")

with col_res:
    if st.session_state.results:
        results = st.session_state.results
    
        if len(results) > 0:
            st.subheader("📊 Nomzodlar malakasi tahlili (Radar Chart)")
            fig = go.Figure()
            colors = ['#00f2fe', '#f200ff', '#4facfe', '#00ff88']
        
            for i, res in enumerate(results[:4]):
                metrics = res.get('metrics', {})
                if metrics:
                    cats = list(metrics.keys())
                    vals = list(metrics.values())
                    vals += vals[:1]
                    cats += cats[:1]
                
                    fig.add_trace(go.Scatterpolar(
                        r=vals, theta=cats, fill='toself',
                        name=res.get('candidate_name', f"Nomzod {i+1}"),
                        line=dict(color=colors[i % len(colors)], width=2),
                        fillcolor=f"rgba{tuple(list(int(colors[i%len(colors)][j:j+2], 16) for j in (1, 3, 5)) + [0.25])}"
                    ))

            fig.update_layout(
                polar=dict(
                    bgcolor="rgba(0,0,0,0)",
                    radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(255,255,255,0.1)", tickfont=dict(color="white")),
                    angularaxis=dict(gridcolor="rgba(255,255,255,0.1)", tickfont=dict(color="white"))
                ),
                showlegend=True, paper_bgcolor="rgba(0,0,0,0)", height=450, legend=dict(font=dict(color="white"))
            )
            st.plotly_chart(fig, use_container_width=True)

        for res in results:
            with st.container():
                name = res.get('candidate_name', 'Unknown')
                st.markdown(f'<div class="card">', unsafe_allow_html=True)
                st.header(f"👤 {name}")
                
                c1, c2 = st.columns([1, 1])
                with c1:
                    st.metric("🏆 Overall Match", f"{res.get('overall_score')}%")
                    st.markdown(f"**AI Verdict:** _{res.get('summary')}_")
                    st.write(f"✅ **Matching:** {', '.join(res.get('matching_skills', []))}")
                    st.write(f"❌ **Missing:** {', '.join(res.get('missing_skills', []))}")

                with c2:
                    st.markdown("#### 🎯 Interview Questions")
                    for q in res.get('interview_questions', []):
                        st.write(f"🔹 {q}")
                    
                    st.divider()
                    btn_col1, btn_col2 = st.columns(2)
                    with btn_col1:
                        pdf_bytes = create_pdf(res)
                        st.download_button("📥 Download Report", pdf_bytes, f"{name}_report.pdf", "application/pdf", key=f"pdf_{name}")
                    with btn_col2:
                        if st.button(f"📧 Draft Email", key=f"email_{name}"):
                            st.code(res.get('interview_email', 'No email generated'), language="markdown")
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("💡 Sidebar orqali CV yuklang va Job Description kiriting.")