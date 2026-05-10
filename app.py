import streamlit as st
import time
import os
import tempfile
import json
import base64
import pickle
import random
from datetime import datetime
from groq import Groq
from questions import get_random_mock, get_random_part, get_all_pools, save_custom_questions, load_custom_questions

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Speaking Mock Test", page_icon="🎙️", layout="centered")

# ─── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif !important; }
.stApp { background: linear-gradient(135deg, #0d0d1a 0%, #1a1a2e 60%, #0d1b2a 100%); }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; max-width: 820px; }

/* ── Cards ── */
.card {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.09);
  border-radius: 18px; padding: 1.75rem; margin: 0.75rem 0;
}
.card-blue {
  background: rgba(102,126,234,0.08);
  border: 1px solid rgba(102,126,234,0.25);
  border-radius: 18px; padding: 1.5rem; margin: 0.75rem 0;
}
.card-admin {
  background: rgba(16,185,129,0.06);
  border: 1px solid rgba(16,185,129,0.2);
  border-radius: 16px; padding: 1.4rem; margin: 0.6rem 0;
}
.card-red {
  background: rgba(239,68,68,0.06);
  border: 1px solid rgba(239,68,68,0.2);
  border-radius: 16px; padding: 1.4rem; margin: 0.6rem 0;
}

/* ── Typography ── */
h1,h2,h3,h4,p,label,div { color: white !important; }
.stMarkdown p { color: rgba(255,255,255,0.82) !important; font-size: 0.97rem; }
.hero { font-size: 2.4rem; font-weight: 800;
  background: linear-gradient(135deg,#667eea,#a78bfa);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  text-align: center; margin-bottom: 0.25rem; line-height: 1.2; }
.sub { color: rgba(255,255,255,0.5) !important; text-align: center;
  font-size: 0.95rem; margin-bottom: 1.5rem; }
.admin-hero { font-size: 2rem; font-weight: 800;
  background: linear-gradient(135deg,#10b981,#34d399);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  text-align: center; margin-bottom: 0.25rem; }

/* ── Buttons ── */
.stButton > button {
  background: linear-gradient(135deg,#667eea,#764ba2) !important;
  color: white !important; border: none !important;
  border-radius: 12px !important; font-weight: 600 !important;
  font-size: 0.95rem !important; transition: all 0.25s !important;
  padding: 0.6rem 1.2rem !important;
}
.stButton > button:hover { transform: translateY(-2px) !important;
  box-shadow: 0 8px 20px rgba(102,126,234,0.4) !important; }

.skip-btn > button {
  background: rgba(255,255,255,0.07) !important;
  border: 1px solid rgba(255,255,255,0.15) !important;
  font-size: 0.82rem !important; padding: 0.4rem 0.9rem !important;
}
.admin-btn > button {
  background: linear-gradient(135deg,#10b981,#059669) !important;
}
.danger-btn > button {
  background: linear-gradient(135deg,#ef4444,#dc2626) !important;
}

/* ── Input ── */
.stTextInput input, .stTextArea textarea, .stSelectbox select, div[data-baseweb="select"] {
  background: rgba(255,255,255,0.07) !important;
  border: 1px solid rgba(255,255,255,0.14) !important;
  border-radius: 12px !important; color: white !important;
}
.stSelectbox div[data-baseweb="select"] > div { background: #1a1a2e !important; }

/* ── Timer ── */
.timer-wrap {
  background: rgba(102,126,234,0.1);
  border: 2px solid rgba(102,126,234,0.4);
  border-radius: 16px; padding: 1.2rem 1.5rem;
  text-align: center; margin: 0.75rem 0;
}
.timer-label { color: rgba(255,255,255,0.5); font-size:0.75rem;
  text-transform: uppercase; letter-spacing: 1.5px; }
.timer-val { font-size: 3.2rem; font-weight: 800; color: #818cf8;
  font-variant-numeric: tabular-nums; line-height: 1.1; }
.timer-speak .timer-val { color: #f87171; }
.timer-speak { border-color: rgba(248,113,113,0.4);
  background: rgba(248,113,113,0.08); }

/* ── Question ── */
.q-box {
  background: rgba(102,126,234,0.07);
  border-left: 4px solid #667eea;
  border-radius: 0 14px 14px 0;
  padding: 1rem 1.3rem; margin: 0.8rem 0;
  font-size: 1.1rem; color: white; font-weight: 500; line-height: 1.6;
}
.q-num { color: #a78bfa; font-size: 0.75rem; font-weight: 700;
  text-transform: uppercase; letter-spacing: 1px; display: block;
  margin-bottom: 0.3rem; }

/* ── Badges ── */
.badge {
  display: inline-block; padding: 0.25rem 0.8rem;
  border-radius: 20px; font-size: 0.75rem; font-weight: 700;
  letter-spacing: 0.5px; margin-right: 6px;
}
.badge-prep { background:rgba(251,191,36,0.15); border:1px solid rgba(251,191,36,0.4); color:#fbbf24; }
.badge-rec  { background:rgba(239,68,68,0.15);  border:1px solid rgba(239,68,68,0.4);  color:#f87171; }
.badge-done { background:rgba(34,197,94,0.15);  border:1px solid rgba(34,197,94,0.4);  color:#4ade80; }
.badge-admin { background:rgba(16,185,129,0.15); border:1px solid rgba(16,185,129,0.4); color:#34d399; }

/* ── Recording dot ── */
.rdot { display:inline-block; width:9px; height:9px; border-radius:50%;
  background:#f87171; animation:rp 1s infinite; margin-right:6px; }
@keyframes rp { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.4;transform:scale(1.3)} }

/* ── EQ bars ── */
.eq-wrap { display:flex; align-items:flex-end; justify-content:center;
  gap:3px; height:52px; margin:0.75rem 0; }
.eq-bar { width:5px; border-radius:3px;
  background:linear-gradient(to top,#667eea,#a78bfa); }

/* ── Part selector ── */
.part-card {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.09);
  border-radius: 14px; padding: 1.2rem;
  cursor: pointer; transition: all 0.2s;
  text-align: center; margin-bottom: 0.5rem;
}
.part-card:hover { border-color: rgba(102,126,234,0.5);
  background: rgba(102,126,234,0.08); }
.part-card-active {
  border-color: #667eea !important;
  background: rgba(102,126,234,0.14) !important;
}
.part-icon { font-size: 1.8rem; margin-bottom: 0.4rem; }
.part-name { font-weight: 700; font-size: 0.95rem; }
.part-desc { color: rgba(255,255,255,0.5) !important; font-size: 0.78rem; }

/* ── Score ── */
.score-big { font-size: 4.5rem; font-weight: 800; text-align: center;
  background: linear-gradient(135deg,#667eea,#a78bfa);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.score-bar-bg { background:rgba(255,255,255,0.08); border-radius:8px; height:10px; overflow:hidden; }
.score-bar-fill { height:100%; border-radius:8px;
  background:linear-gradient(90deg,#667eea,#a78bfa); transition:width 1s ease; }

/* ── Error/Correction boxes ── */
.err-box {
  background: rgba(239,68,68,0.07);
  border: 1px solid rgba(239,68,68,0.2);
  border-radius: 12px; padding: 1rem 1.2rem; margin: 0.5rem 0;
}
.fix-box {
  background: rgba(34,197,94,0.07);
  border: 1px solid rgba(34,197,94,0.2);
  border-radius: 12px; padding: 1rem 1.2rem; margin: 0.5rem 0;
}
.vocab-box {
  background: rgba(251,191,36,0.07);
  border: 1px solid rgba(251,191,36,0.2);
  border-radius: 12px; padding: 1rem 1.2rem; margin: 0.5rem 0;
}
.err-label { font-size:0.72rem; font-weight:700; text-transform:uppercase;
  letter-spacing:1px; margin-bottom:0.4rem; display:block; }
.err-wrong { color:#f87171 !important; text-decoration:line-through;
  font-style:italic; }
.err-right { color:#4ade80 !important; font-weight:600; }
.err-tip   { color:#fbbf24 !important; font-size:0.88rem; }

/* ── Image box ── */
.img-desc {
  background: rgba(167,139,250,0.08);
  border: 1px solid rgba(167,139,250,0.25);
  border-radius: 12px; padding: 1rem 1.2rem; margin: 0.7rem 0;
  font-size: 0.95rem; color: rgba(255,255,255,0.85) !important;
}
.stFileUploader { color: white !important; }
.stFileUploader label { color: rgba(255,255,255,0.7) !important; }
div[data-testid="stFileUploadDropzone"] {
  background: rgba(255,255,255,0.03) !important;
  border: 1px dashed rgba(255,255,255,0.18) !important;
  border-radius: 12px !important;
}

/* ── Admin student card ── */
.student-row {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 12px; padding: 1rem 1.2rem; margin: 0.5rem 0;
  cursor: pointer;
  transition: all 0.2s;
}
.student-row:hover {
  border-color: rgba(102,126,234,0.4);
  background: rgba(102,126,234,0.06);
}
.student-name { font-weight: 700; font-size: 1rem; color: #a78bfa !important; }
.student-score { font-size: 1.3rem; font-weight: 800; }
.add-q-btn > button {
  background: linear-gradient(135deg,#f59e0b,#d97706) !important;
  font-size: 0.88rem !important;
}

/* ── Login Modal ── */
.login-overlay {
  background: rgba(0,0,0,0.8);
  border: 1px solid rgba(102,126,234,0.3);
  border-radius: 20px;
  padding: 2rem;
  max-width: 400px;
  margin: 0 auto;
}

/* ── Admin question image ── */
.admin-q-img {
  max-width: 220px;
  max-height: 160px;
  border-radius: 10px;
  border: 1px solid rgba(255,255,255,0.12);
  margin-top: 0.4rem;
}
</style>
""", unsafe_allow_html=True)

# ─── Data Storage Helpers ───────────────────────────────────────────────────────
RESULTS_FILE = "student_results.pkl"

def load_student_results():
    if os.path.exists(RESULTS_FILE):
        try:
            with open(RESULTS_FILE, "rb") as f:
                return pickle.load(f)
        except:
            return []
    return []

def save_student_result(entry):
    results = load_student_results()
    results.append(entry)
    with open(RESULTS_FILE, "wb") as f:
        pickle.dump(results, f)

def delete_student_result(idx):
    results = load_student_results()
    if 0 <= idx < len(results):
        results.pop(idx)
        with open(RESULTS_FILE, "wb") as f:
            pickle.dump(results, f)

# ─── Session State ─────────────────────────────────────────────────────────────
def init_state():
    defs = {
        "page": "welcome",
        "user_name": "",
        "mode": None,
        "mock_data": None,      # generate qilingan mock (random)
        "part_order": [],
        "current_part_idx": 0,
        "current_q": 0,
        "phase": "prep",
        "timer_start": None,
        "transcripts": {},
        "results": None,
        "skip_flag": False,
        "admin_logged_in": False,
        "show_admin_login": False,
        "admin_tab": "students",
        "audio_files": {},
        "mock_seed": None,
        "pending_audios": {},
    }
    for k, v in defs.items():
        if k not in st.session_state:
            st.session_state[k] = v

# ─── Groq ──────────────────────────────────────────────────────────────────────
@st.cache_resource
def get_groq_client():
      key = st.secrets["GROQ_API_KEY"]
      return Groq(api_key=key) if key else None

def transcribe(audio_bytes: bytes, fname="audio.wav") -> str:
    client = get_groq_client()
    if not client:
        return "[Demo: GROQ_API_KEY not set]"
    try:
        # Format aniqlash
        if fname.endswith(".wav"):
            suffix = ".wav"
            mime = "audio/wav"
        else:
            suffix = ".webm"
            mime = "audio/webm"

        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as f:
            f.write(audio_bytes)
            tmp = f.name
        with open(tmp, "rb") as f:
            r = client.audio.transcriptions.create(
                model="whisper-large-v3",
                file=(fname, f, mime),
                language="en"
            )
        os.unlink(tmp)
        return r.text.strip()
    except Exception as e:
        return f"[Error: {e}]"

def evaluate(transcripts: dict, name: str, mode: str, questions_map: dict) -> dict:
    """
    Barcha savollarga javob tekshiriladi.
    questions_map: {label: question_text} - har bir transcript uchun savol matni
    """
    client = get_groq_client()
    if not client:
        return _demo_result()

    # Savol-javob juftliklari
    qa_pairs = []
    for label, transcript in transcripts.items():
        q_text = questions_map.get(label, "Unknown question")
        qa_pairs.append(f"Q: {q_text}\nA: {transcript}")

    full_text = "\n\n".join(qa_pairs)
    answered_count = sum(1 for v in transcripts.values() if v and "[Audio yuklenmadi]" not in v and "[Error" not in v)
    total_count = len(transcripts)

    prompt = f"""You are an expert IELTS/CEFR speaking examiner. Analyze this speaking test transcript from {name}.

MODE: {mode}
TOTAL QUESTIONS: {total_count}
QUESTIONS ANSWERED: {answered_count}

QUESTION & ANSWER PAIRS:
{full_text}

IMPORTANT SCORING RULES:
1. You MUST evaluate ALL answers, not just one. The score must reflect the overall performance across ALL questions.
2. Check if each answer is ON-TOPIC relative to the question asked. Off-topic answers should significantly lower the score.
3. If the student only answered some questions, reduce scores proportionally.
4. Evaluate based on: Fluency & Coherence, Lexical Resource, Grammatical Range & Accuracy, Pronunciation.
5. Be strict and accurate — do not give inflated scores.

Provide detailed feedback in this EXACT JSON format (no markdown, no extra text):
{{
  "overall": 7.0,
  "vocabulary_score": 6.5,
  "grammar_score": 7.0,
  "fluency_score": 6.5,
  "pronunciation_score": 7.0,
  "topic_relevance_issues": [
    {{"question": "the question text", "issue": "brief explanation of why answer was off-topic"}}
  ],
  "vocab_errors": [
    {{"wrong": "actual word used", "correct": "better word", "tip": "brief explanation"}}
  ],
  "grammar_errors": [
    {{"wrong": "exact phrase with error", "correct": "corrected phrase", "tip": "grammar rule"}}
  ],
  "good_vocab": ["impressive word/phrase 1", "impressive word/phrase 2"],
  "strengths": ["strength 1", "strength 2"],
  "improvements": ["area 1", "area 2"],
  "overall_feedback": "2-3 sentence summary paragraph"
}}

Rules:
- topic_relevance_issues: list any answers that were off-topic or irrelevant to the question (empty array if all on-topic)
- vocab_errors: 3-6 word choice mistakes
- grammar_errors: 3-6 grammatical mistakes from the transcripts
- good_vocab: 3-5 good vocabulary words used correctly
- All scores out of 9.0 (IELTS band scale)
- Be specific and quote actual text"""

    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=2000,
            response_format={"type": "json_object"}
        )
        raw = resp.choices[0].message.content.strip()
        s, e = raw.find("{"), raw.rfind("}") + 1
        return json.loads(raw[s:e])
    except Exception as ex:
        return _demo_result(str(ex))

def _demo_result(err=""):
    return {
        "overall": 6.5, "vocabulary_score": 6.5, "grammar_score": 6.0,
        "fluency_score": 6.5, "pronunciation_score": 6.5,
        "topic_relevance_issues": [],
        "vocab_errors": [{"wrong": "big", "correct": "significant/substantial", "tip": "Use more precise adjectives"}],
        "grammar_errors": [{"wrong": "I am go", "correct": "I am going", "tip": "Use present continuous correctly"}],
        "good_vocab": ["furthermore", "in contrast", "consequently"],
        "strengths": ["Good use of connectors", "Clear structure"],
        "improvements": ["Expand vocabulary range", "Work on complex grammar"],
        "overall_feedback": f"Demo mode (set GROQ_API_KEY). {err}"
    }

# ─── Helpers ───────────────────────────────────────────────────────────────────
def eq_html(n=22):
    import random as _r
    bars = "".join([
        f'<div class="eq-bar" style="height:{_r.randint(15,85)}%;'
        f'animation:eq_{i} {0.3+i*0.04:.2f}s ease infinite alternate;"></div>'
        for i in range(n)])
    kf = "".join([
        f"@keyframes eq_{i}{{0%{{height:{_r.randint(5,20)}%}}"
        f"100%{{height:{_r.randint(40,95)}%}}}}"
        for i in range(n)])
    return f"<style>{kf}</style><div class='eq-wrap'>{bars}</div>"

def fmt_time(s):
    return f"{s//60:02d}:{s%60:02d}"

def get_part_order(mode):
    orders = {
        "part1":   ["part1"],
        "part1_1": ["part1_1"],
        "part2":   ["part2"],
        "part3":   ["part3"],
        "full":    ["part1", "part1_1", "part2", "part3"],
    }
    return orders.get(mode, ["part1"])

def current_part_data():
    mock = st.session_state.mock_data
    idx  = st.session_state.current_part_idx
    key  = st.session_state.part_order[idx]
    return mock[key], key

def get_prep_time_for_question(part_key, q_idx, part_data=None):
    """
    Part 1   : har bir savolga 5 sekund
    Part 1.1 : prep_times listidan olinadi [10, 5, 5] — 1-savolga 10s, qolganlariga 5s
    Part 2/3 : faqat 1-savolda 60s prep, qolganlarida 0 (to'g'ridan gapirish)
    """
    if part_key == "part1":
        return 5
    elif part_key == "part1_1":
        if part_data and "prep_times" in part_data:
            times = part_data["prep_times"]
            return times[q_idx] if q_idx < len(times) else 5
        return 10 if q_idx == 0 else 5
    elif part_key in ("part2", "part3"):
        return 60 if q_idx == 0 else 0
    return 5

# ═══════════════════════════════════════════════════════════════════════════════
# ADMIN LOGIN
# ═══════════════════════════════════════════════════════════════════════════════
def show_admin_login():
    st.markdown('<div class="login-overlay">', unsafe_allow_html=True)
    st.markdown("### 🔐 Admin Login")
    st.markdown('<p style="color:rgba(255,255,255,0.5);font-size:0.85rem;">Admin paneliga kirish uchun ma\'lumotlarni kiriting</p>', unsafe_allow_html=True)

    login_input = st.text_input("Login", placeholder="login", key="admin_login_input")
    password_input = st.text_input("Parol", type="password", placeholder="parol", key="admin_pass_input")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔓 Kirish", use_container_width=True):
            if login_input == "mominxoja" and password_input == "admin5165636":
                st.session_state.admin_logged_in = True
                st.session_state.show_admin_login = False
                st.session_state.page = "admin"
                st.rerun()
            else:
                st.error("❌ Login yoki parol noto'g'ri!")
    with col2:
        if st.button("✖ Bekor qilish", use_container_width=True):
            st.session_state.show_admin_login = False
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: WELCOME
# ═══════════════════════════════════════════════════════════════════════════════
def page_welcome():
    if st.session_state.get("show_admin_login"):
        show_admin_login()
        return

    st.markdown('<div class="hero">🎙️ Speaking Mock Test</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub">AI-powered English Speaking Assessment</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 👋 Ismingizni kiriting")
        name = st.text_input("Full name", placeholder="masalan: Jasur Toshmatov",
                             label_visibility="collapsed")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Davom etish →", use_container_width=True):
                if name.strip():
                    st.session_state.user_name = name.strip()
                    st.session_state.page = "mode_select"
                    st.rerun()
                else:
                    st.error("Iltimos, ismingizni kiriting.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0.6rem;margin-top:0.5rem;">
      <div class="card" style="text-align:center;padding:1rem;">
        <div style="font-size:1.6rem;">📝</div>
        <div style="font-size:0.78rem;color:rgba(255,255,255,0.6)!important;margin-top:0.3rem;">Random Tests</div>
      </div>
      <div class="card" style="text-align:center;padding:1rem;">
        <div style="font-size:1.6rem;">🎯</div>
        <div style="font-size:0.78rem;color:rgba(255,255,255,0.6)!important;margin-top:0.3rem;">4 Parts</div>
      </div>
      <div class="card" style="text-align:center;padding:1rem;">
        <div style="font-size:1.6rem;">🤖</div>
        <div style="font-size:0.78rem;color:rgba(255,255,255,0.6)!important;margin-top:0.3rem;">AI Scoring</div>
      </div>
      <div class="card" style="text-align:center;padding:1rem;">
        <div style="font-size:1.6rem;">📊</div>
        <div style="font-size:0.78rem;color:rgba(255,255,255,0.6)!important;margin-top:0.3rem;">Detailed Feedback</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([3, 1, 3])
    with col2:
        if st.button("⚙️ Admin", use_container_width=True):
            st.session_state.show_admin_login = True
            st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: MODE SELECT
# ═══════════════════════════════════════════════════════════════════════════════
def page_mode_select():
    st.markdown(f'<div class="hero" style="font-size:1.8rem;">Salom, {st.session_state.user_name}! 👋</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub">Mashq turini tanlang</div>', unsafe_allow_html=True)

    # Mode cards — test tanlash yo'q, faqat mode
    st.markdown("### 🎯 Nima uchun tayyorlanmoqchisiz?")
    modes = [
        ("full",    "🏆", "Full Mock Test",  "Barcha 4 qism — random savollar bilan"),
        ("part1",   "📝", "Part 1",     "3 ta qisqa savol — o'zingiz haqingizda"),
        ("part1_1", "🖼️", "Part 1.1",   "Rasm tavsifi va savollarga javob"),
        ("part2",   "📖", "Part 2",     "Uzun monolog — rasmga asoslangan"),
        ("part3",   "🗣️", "Part 3",     "Munozara — FOR va AGAINST"),
    ]
    cols = st.columns(2)
    for ci, (mode_key, icon, name, desc) in enumerate(modes):
        with cols[ci % 2]:
            if st.button(f"{icon} {name}\n{desc}", key=f"mode_{mode_key}",
                         use_container_width=True):
                seed = random.randint(0, 999999)
                st.session_state.mock_seed = seed
                st.session_state.mode = mode_key
                st.session_state.part_order = get_part_order(mode_key)
                st.session_state.current_part_idx = 0
                st.session_state.current_q = 0
                st.session_state.phase = "prep"
                st.session_state.timer_start = time.time()
                st.session_state.transcripts = {}
                st.session_state.results = None
                st.session_state.audio_files = {}
                st.session_state.pending_audios = {}

                # Random mock yaratish
                if mode_key == "full":
                    mock = get_random_mock(seed=seed)
                else:
                    part_data = get_random_part(mode_key, seed=seed)
                    mock = {mode_key: part_data}

                st.session_state.mock_data = mock
                st.session_state.page = "test"
                st.rerun()



# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: TEST
# ═══════════════════════════════════════════════════════════════════════════════
def page_test():
    part, part_key = current_part_data()
    q_idx = st.session_state.current_q
    all_questions = part["questions"]
    total_q = len(all_questions)

    # Taymerni hisoblash
    if st.session_state.timer_start is None:
        st.session_state.timer_start = time.time()
    
    elapsed = time.time() - st.session_state.timer_start
    part_idx = st.session_state.current_part_idx
    total_parts = len(st.session_state.part_order)

    # Part 2 va Part 3 uchun alohida sahifa (agar u yerda ham recorder bo'lsa, uni ham shunday soddalashtiring)
    if part_key in ("part2", "part3"):
        _page_test_all_questions(part, part_key, elapsed, part_idx, total_parts)
        return

    # Tepadagi ma'lumotlar paneli (Header)
    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem;">
      <span style="background:linear-gradient(135deg,#667eea,#a78bfa);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
        font-weight:800;font-size:1.1rem;">{part['title']}</span>
      <span style="color:rgba(255,255,255,0.4);font-size:0.82rem;">
        {st.session_state.user_name} &nbsp;·&nbsp;
        Part {part_idx+1}/{total_parts} &nbsp;·&nbsp;
        Q {q_idx+1}/{total_q}
      </span>
    </div>
    """, unsafe_allow_html=True)

    # Part 1.1 uchun rasm ko'rsatish (savol matnidan OLDIN)
    if part_key == "part1_1":
        img_b64 = part.get("img_b64", "")
        img_desc = part.get("image_description", "")
        if img_b64:
            st.markdown(
                f'<img src="data:image/jpeg;base64,{img_b64}" '
                f'style="width:100%;max-width:620px;border-radius:16px;'
                f'border:1px solid rgba(255,255,255,0.15);margin:0.5rem auto 1rem;display:block;" />',
                unsafe_allow_html=True
            )
        if img_desc:
            st.markdown(
                f'<div class="img-desc">🖼️ <strong>Rasm:</strong> {img_desc}</div>',
                unsafe_allow_html=True
            )

    # Savol matni
    current_q_text = all_questions[q_idx] if q_idx < len(all_questions) else ""
    st.markdown(f"""
    <div class="q-box">
      <span class="q-num">Savol {q_idx + 1}</span>
      {current_q_text}
    </div>""", unsafe_allow_html=True)

    # Vaqt sozlamalari
    prep_time = get_prep_time_for_question(part_key, q_idx, part)
    speak_time = part["speak_time"]

    # ── PHASE: PREP (Tayyorlanish) ──
    if st.session_state.phase == "prep":
        remaining = max(0, prep_time - int(elapsed))
        st.markdown(f'<span class="badge badge-prep">⏳ TAYYORLANISH VAQTI</span>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="timer-wrap">
          <div class="timer-label">Javobingizni tayyorlang</div>
          <div class="timer-val">{fmt_time(remaining)}</div>
        </div>""", unsafe_allow_html=True)

        if st.button("Tayyorman, gapirishni boshlash →", key=f"skip_prep_{part_key}_{q_idx}"):
            st.session_state.phase = "speak"
            st.session_state.timer_start = time.time()
            st.rerun()

        if remaining > 0:
            time.sleep(1)
            st.rerun()
        else:
            st.session_state.phase = "speak"
            st.session_state.timer_start = time.time()
            st.rerun()

    # ── PHASE: SPEAK (Gapirish va Ovoz yozish) ──
    elif st.session_state.phase == "speak":
        remaining = max(0, speak_time - int(elapsed))
        label_id = f"{part_key}_q{q_idx+1}"

        st.markdown(f'<span class="badge badge-rec">🎙️ GAPIRING</span>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="timer-wrap timer-speak">
          <div class="timer-label">⏱ Qolgan vaqt</div>
          <div class="timer-val">{fmt_time(remaining)}</div>
        </div>""", unsafe_allow_html=True)

        # Equalizer olib tashlandi, o'rniga standart va ishonchli audio_input
        audio_val = st.audio_input("Ovozingizni yozing", key=f"mic_{label_id}")

        if audio_val is not None:
            # Audioni o'qib savatga saqlaymiz
            abytes = audio_val.read()
            if abytes:
                st.session_state.pending_audios[label_id] = abytes
            
            # Keyingi savolga o'tish tugmasi (faqat audio yuklangandan keyin chiqadi)
            if st.button("Keyingi savol ➡️", key=f"next_{label_id}"):
                _advance(part, part_key, q_idx, total_q)
        
        else:
            # Agar foydalanuvchi gapira olmasa yoki o'tkazib yubormoqchi bo'lsa
            if st.button("Bu savolni o'tkazib yuborish ⏭"):
                st.session_state.pending_audios[label_id] = None
                _advance(part, part_key, q_idx, total_q)

        # Taymer tugaganda ogohlantirish (avtomatik o'tkazib yubormaymiz, chunki foydalanuvchi stopni bosishi kerak)
        if remaining <= 0:
            st.warning("⚠️ Vaqt tugadi! Iltimos, audioni to'xtatib, keyingi savolga o'ting.")
        else:
            time.sleep(1)
            st.rerun()
# ═══════════════════════════════════════════════════════════════════════════════
# Part 2 / Part 3 uchun: BARCHA SAVOLLAR bitta ekranda, BITTA timer
# ═══════════════════════════════════════════════════════════════════════════════
def _page_test_all_questions(part, part_key, elapsed, part_idx, total_parts):
    all_questions = part["questions"]
    total_q       = len(all_questions)
    prep_time     = part.get("prep_time", 60)
    speak_time    = part.get("speak_time", 120)

    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem;">
      <span style="background:linear-gradient(135deg,#667eea,#a78bfa);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
        font-weight:800;font-size:1.1rem;">{part['title']}</span>
      <span style="color:rgba(255,255,255,0.4);font-size:0.82rem;">
        {st.session_state.user_name} &nbsp;·&nbsp;
        Part {part_idx+1}/{total_parts}
      </span>
    </div>
    """, unsafe_allow_html=True)

    # Instruction
    st.markdown(f'<div class="card-blue" style="font-size:0.88rem;color:rgba(255,255,255,0.7)!important;">'
                f'📋 {part["instruction"]}</div>', unsafe_allow_html=True)

    # Rasm tavsifi
    img_desc = part.get("image_description", "")
    if img_desc:
        st.markdown(f'<div class="img-desc">🖼️ <strong>Rasm:</strong> {img_desc}</div>',
                    unsafe_allow_html=True)

    # Part 3 uchun topic jadval
    topic       = part.get("topic", "")
    for_pts     = part.get("for_points", [])
    against_pts = part.get("against_points", [])
    if part_key == "part3" and topic:
        fp = "".join([f'<div style="color:rgba(255,255,255,0.78);font-size:0.85rem;margin-bottom:4px;">✅ {p}</div>' for p in for_pts])
        ap = "".join([f'<div style="color:rgba(255,255,255,0.78);font-size:0.85rem;margin-bottom:4px;">❌ {p}</div>' for p in against_pts])
        st.markdown(f"""
        <div style="background:rgba(102,126,234,0.07);border:1px solid rgba(102,126,234,0.2);
          border-radius:14px;padding:1.2rem;margin:0.7rem 0;">
          <div style="color:#a78bfa;font-weight:700;font-size:0.95rem;margin-bottom:0.8rem;">
            📋 {topic}
          </div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;">
            <div><div style="color:#4ade80;font-weight:700;margin-bottom:6px;font-size:0.82rem;">FOR</div>{fp}</div>
            <div><div style="color:#f87171;font-weight:700;margin-bottom:6px;font-size:0.82rem;">AGAINST</div>{ap}</div>
          </div>
        </div>""", unsafe_allow_html=True)

    # Barcha savollarni ko'rsatish
    qs_html = "".join([
        f'<div class="q-box" style="margin-bottom:0.6rem;">'
        f'<span class="q-num">Savol {i+1}</span>{q}</div>'
        for i, q in enumerate(all_questions)
    ])
    st.markdown(qs_html, unsafe_allow_html=True)

    phase = st.session_state.phase

    # ── PHASE: PREP (faqat bir marta, barcha savollar uchun birgalikda) ──
    if phase == "prep":
        remaining = max(0, prep_time - int(elapsed))
        st.markdown('<span class="badge badge-prep">⏳ TAYYORLANISH VAQTI</span>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="timer-wrap">
          <div class="timer-label">Barcha savollarga tayyorlaning</div>
          <div class="timer-val">{fmt_time(remaining)}</div>
        </div>""", unsafe_allow_html=True)

        c1, c2, c3 = st.columns([2, 1, 2])
        with c2:
            st.markdown('<div class="skip-btn">', unsafe_allow_html=True)
            if st.button("O'tkazish →", key=f"skip_prep_{part_key}_all"):
                st.session_state.phase = "speak"
                st.session_state.timer_start = time.time()
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        if remaining > 0:
            time.sleep(0.8)
            st.rerun()
        else:
            st.session_state.phase = "speak"
            st.session_state.timer_start = time.time()
            st.rerun()

    # ── PHASE: SPEAK (barcha savollar uchun bitta timer) ──
    elif phase == "speak":
        remaining = max(0, speak_time - int(elapsed))
        label_id  = f"{part_key}_all"

        st.markdown(
            '<span class="badge badge-rec"><span class="rdot"></span>' +
            f'🎙️ GAPIRING — barcha savollarga javob bering</span>',
            unsafe_allow_html=True
        )
        st.markdown(f"""
        <div class="timer-wrap timer-speak">
          <div class="timer-label">⏱ Gapirish vaqti</div>
          <div class="timer-val">{fmt_time(max(0,remaining))}</div>
        </div>""", unsafe_allow_html=True)

        st.markdown(eq_html(24), unsafe_allow_html=True)
        st.markdown(
            '<div style="text-align:center;color:rgba(255,255,255,0.6);font-size:0.85rem;margin:0.5rem 0;">' +
            '🎙️ Barcha savollarga ketma-ket javob bering, tugagach yuklang</div>',
            unsafe_allow_html=True
        )

        audio_val = st.audio_input(" ", key=f"mic_{label_id}", label_visibility="collapsed")

        if audio_val is not None:
            abytes = audio_val.read()
            if abytes:
                st.session_state.pending_audios[label_id] = abytes
            else:
                st.session_state.pending_audios[label_id] = None
            _advance_part(part_key)
        else:
            if remaining <= 0:
                st.warning("⏱ Vaqt tugadi. Audiongizni yuboring yoki o'tkazish tugmasini bosing.")
            c1, c2, c3 = st.columns([2, 1, 2])
            with c2:
                st.markdown('<div class="skip-btn">', unsafe_allow_html=True)
                if st.button("O'tkazish ⏭", key=f"skip_{part_key}_all"):
                    st.session_state.pending_audios[label_id] = None
                    _advance_part(part_key)
                st.markdown('</div>', unsafe_allow_html=True)
            if remaining > 0:
                time.sleep(0.8)
                st.rerun()
def _advance_part(part_key):
    """Part 2 / Part 3 tugagandan keyin keyingi partga o'tish yoki finish."""
    nxt = st.session_state.current_part_idx + 1
    if nxt < len(st.session_state.part_order):
        st.session_state.current_part_idx = nxt
        st.session_state.current_q = 0
        st.session_state.phase = "prep"
        st.session_state.timer_start = time.time()
    else:
        _finish()
    st.rerun()


def _advance(part, part_key, q_idx, total_q):
    if q_idx + 1 < total_q:
        st.session_state.current_q = q_idx + 1
        st.session_state.phase = "prep"
        st.session_state.timer_start = time.time()
    else:
        nxt = st.session_state.current_part_idx + 1
        if nxt < len(st.session_state.part_order):
            st.session_state.current_part_idx = nxt
            st.session_state.current_q = 0
            st.session_state.phase = "prep"
            st.session_state.timer_start = time.time()
        else:
            _finish()
    st.rerun()


def _finish():
    mock    = st.session_state.mock_data
    pending = st.session_state.get("pending_audios", {})

    # Questions map
    questions_map = {}
    for pk in st.session_state.part_order:
        for i, q in enumerate(mock.get(pk, {}).get("questions", [])):
            questions_map[f"{pk}_q{i+1}"] = q

    # Batch transcribe
    transcripts = {}
    items = []
    for pk in st.session_state.part_order:
        n_q = len(mock.get(pk, {}).get("questions", []))
        if pk in ("part2", "part3"):
            items.append((f"{pk}_all", True, pk, n_q))
        else:
            for i in range(n_q):
                items.append((f"{pk}_q{i+1}", False, pk, n_q))

    bar = st.progress(0, text="🎙️ Ovozlar tahlil qilinmoqda…")
    for idx, (lbl, is_all, pk, n_q) in enumerate(items):
        bar.progress(idx / max(len(items), 1), text=f"🎙️ Tahlil: {idx+1}/{len(items)}")
        abytes = pending.get(lbl)
        txt = _do_transcribe(abytes, f"{lbl}.webm") if abytes else "[Ovoz kiritilmadi]"
        if is_all:
            for i in range(n_q):
                transcripts[f"{pk}_q{i+1}"] = txt
        else:
            transcripts[lbl] = txt

    bar.progress(0.95, text="🤖 AI baholayapti…")
    results = evaluate(
        transcripts,
        st.session_state.user_name,
        st.session_state.get("mode", "full"),
        questions_map
    )
    bar.empty()

    st.session_state.transcripts = transcripts
    st.session_state.results     = results

    pool_ids = {pk: mock[pk]["pool_id"] for pk in st.session_state.part_order if "pool_id" in mock.get(pk, {})}
    save_student_result({
        "name":          st.session_state.user_name,
        "date":          datetime.now().strftime("%Y-%m-%d %H:%M"),
        "mode":          st.session_state.get("mode", "full"),
        "pool_ids":      pool_ids,
        "transcripts":   transcripts,
        "questions_map": questions_map,
        "results":       results,
        "audio_files":   {},
    })
    st.session_state.page = "results"
    st.rerun()


def _do_transcribe(audio_bytes: bytes, fname: str) -> str:
    try:
        txt = transcribe(audio_bytes, fname)
        return txt.strip() if txt else "[Bo'sh javob]"
    except Exception as ex:
        return f"[Xato: {ex}]"


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def page_results():
    r = st.session_state.results or {}
    name = st.session_state.user_name

    st.markdown('<div class="hero">📊 Natijalaringiz</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub">Ajoyib, {name}! Bu sizning to\'liq baholashingiz.</div>',
                unsafe_allow_html=True)

    overall = float(r.get("overall", 0) or 0)
    color = "#4ade80" if overall >= 7 else "#fbbf24" if overall >= 5.5 else "#f87171"
    st.markdown(f"""
    <div class="card" style="text-align:center;padding:2rem;">
      <div style="color:rgba(255,255,255,0.45);font-size:0.72rem;text-transform:uppercase;
        letter-spacing:2px;margin-bottom:0.5rem;">Umumiy Band Score</div>
      <div style="font-size:5.5rem;font-weight:800;color:{color};line-height:1;">{overall}</div>
      <div style="color:rgba(255,255,255,0.35);font-size:0.85rem;margin-top:0.3rem;">9.0 dan</div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📈 Batafsil Baholar")
    criteria = [
        ("🗣️ Ravonlik va Izchillik",      r.get("fluency_score", 0)),
        ("📚 Lug'at (Leksik Boylik)", r.get("vocabulary_score", 0)),
        ("📝 Grammatika Doirasi va Aniqligi",  r.get("grammar_score", 0)),
        ("🔊 Talaffuz",             r.get("pronunciation_score", 0)),
    ]
for cname, score in criteria:
        try:
            # Kelgan qiymatni songa aylantirishga harakat qilamiz
            score = float(score) if score is not None else 0.0
        except (ValueError, TypeError):
            # Agar xato bo'lsa (masalan score "N/A" bo'lsa), 0.0 deb olamiz
            score = 0.0
        
        # Bu qatorlar endi try-except blokidan tashqarida, lekin 'for' tsikli ichida:
        pct = int((score / 9) * 100)
        c = "#4ade80" if score >= 7 else "#fbbf24" if score >= 5.5 else "#f87171"
        
        # Stilizatsiya qilingan natijani chiqarish kodi shu yerdan davom etadi...
        st.markdown(f"""
            <div style="margin-bottom:1rem;">
                <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                    <span style="font-weight:600; color:rgba(255,255,255,0.85);">{cname}</span>
                    <span style="font-weight:700; color:{c};">{score} / 9</span>
                </div>
                <div style="background:rgba(255,255,255,0.05); border-radius:10px; height:8px; overflow:hidden;">
                    <div style="background:{c}; width:{pct}%; height:100%; border-radius:10px;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Topic relevance issues
    topic_issues = r.get("topic_relevance_issues", [])
    if topic_issues:
        st.markdown('<div class="card-red">', unsafe_allow_html=True)
        st.markdown("### ⚠️ Mavzudan Chetlashish")
        for ti in topic_issues:
            st.markdown(f"""
            <div class="err-box">
              <span class="err-label" style="color:#fbbf24!important;">📌 Savol</span>
              <div style="color:rgba(255,255,255,0.85);margin-bottom:6px;">"{ti.get('question','')}"</div>
              <span class="err-label" style="color:#f87171!important;">⚠️ Muammo</span>
              <div style="color:rgba(255,255,255,0.7);">{ti.get('issue','')}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    vocab_errors = r.get("vocab_errors", [])
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"### 📚 Lug'at — Baho: {r.get('vocabulary_score', 0)}/9.0")
    if vocab_errors:
        st.markdown("**❌ Lug'at Xatolari va Tuzatishlar:**")
        for ve in vocab_errors:
            st.markdown(f"""
            <div class="err-box">
              <span class="err-label" style="color:#f87171!important;">Noto'g'ri ishlatish</span>
              <div style="margin-bottom:6px;"><span class="err-wrong">"{ve.get('wrong','')}"</span></div>
              <span class="err-label" style="color:#4ade80!important;">✅ Yaxshiroq variant</span>
              <div style="margin-bottom:6px;"><span class="err-right">"{ve.get('correct','')}"</span></div>
              <span class="err-tip">💡 {ve.get('tip','')}</span>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown('<div class="fix-box">✅ Muhim lug\'at xatolari topilmadi!</div>', unsafe_allow_html=True)

    good_vocab = r.get("good_vocab", [])
    if good_vocab:
        st.markdown("**✅ Yaxshi ishlatilgan so'zlar:**")
        items = "".join([f'<span style="background:rgba(34,197,94,0.15);border:1px solid rgba(34,197,94,0.3);'
                         f'border-radius:8px;padding:3px 10px;margin:3px;display:inline-block;'
                         f'color:#4ade80;font-size:0.88rem;">🌟 {w}</span>' for w in good_vocab])
        st.markdown(f'<div style="margin:0.5rem 0;">{items}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    grammar_errors = r.get("grammar_errors", [])
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"### 📝 Grammatika — Baho: {r.get('grammar_score', 0)}/9.0")
    if grammar_errors:
        st.markdown("**❌ Grammatika Xatolari va Tuzatishlar:**")
        for ge in grammar_errors:
            st.markdown(f"""
            <div class="err-box">
              <span class="err-label" style="color:#f87171!important;">Noto'g'ri</span>
              <div style="margin-bottom:6px;"><span class="err-wrong">"{ge.get('wrong','')}"</span></div>
              <span class="err-label" style="color:#4ade80!important;">✅ To'g'ri shakl</span>
              <div style="margin-bottom:6px;"><span class="err-right">"{ge.get('correct','')}"</span></div>
              <span class="err-tip">📖 {ge.get('tip','')}</span>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown('<div class="fix-box">✅ Muhim grammatika xatolari topilmadi!</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 💬 Examiner Fikr-Mulohazasi")
    st.markdown(f'<p style="line-height:1.75;">{r.get("overall_feedback","")}</p>', unsafe_allow_html=True)
    strengths = r.get("strengths", [])
    improvements = r.get("improvements", [])
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**✅ Kuchli tomonlar:**")
        for s in strengths:
            st.markdown(f'<div style="color:#4ade80;font-size:0.88rem;margin-bottom:4px;">• {s}</div>', unsafe_allow_html=True)
    with col2:
        st.markdown("**🎯 Yaxshilash kerak:**")
        for im in improvements:
            st.markdown(f'<div style="color:#fbbf24;font-size:0.88rem;margin-bottom:4px;">• {im}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📄 To'liq Matn")
    tr_text = ""
    for lbl, txt in st.session_state.transcripts.items():
        tr_text += f"[{lbl.upper()}]\n{txt}\n\n"
    st.markdown(f"""<div style="background:rgba(0,0,0,0.35);border:1px solid rgba(255,255,255,0.07);
      border-radius:12px;padding:1.2rem;white-space:pre-wrap;font-size:0.88rem;
      color:rgba(255,255,255,0.78)!important;line-height:1.7;font-family:monospace;">
      {tr_text or "Matn yozilmadi."}</div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Yangi Test", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()
    with col2:
        if st.button("🏠 Bosh Menyu", use_container_width=True):
            st.session_state.page = "mode_select"
            st.session_state.transcripts = {}
            st.session_state.results = None
            st.session_state.mock_data = None
            st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# ADMIN: STUDENTS PAGE
# ═══════════════════════════════════════════════════════════════════════════════
def page_admin_students():
    # ─── 1. ARROW RIGHT XATOSINI YO'QOTISH UCHUN CSS ───
    st.markdown("""
    <style>
        /* Expander sarlavhasidagi noto'g'ri render bo'layotgan ikonkani butunlay yashirish */
        [data-testid="stExpander"] [data-testid="stIconMaterial"] {
            display: none !important;
        }
        /* Sarlavha matni va chetidagi ortiqcha belgilarni tozalash */
        .st-emotion-cache-p5m613 { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

    results = load_student_results()

    if not results:
        st.markdown('<div class="card" style="text-align:center;padding:2rem;">'
                    '<div style="font-size:3rem;">👀</div>'
                    '<p>Hali hech qanday student test topshirmagan</p></div>', unsafe_allow_html=True)
        return

    st.markdown(f"### 👥 Jami studentlar: **{len(results)}** ta")

    for i, entry in enumerate(reversed(results)):
        real_idx = len(results) - 1 - i
        r = entry.get("results", {})
        overall = float(r.get("overall", 0) or 0)
        color = "#4ade80" if overall >= 7 else "#fbbf24" if overall >= 5.5 else "#f87171"
        date_str = entry.get("date", "N/A")
        mode_str = entry.get("mode", "full")
        name_str = entry.get("name", "?")

        # ─── 2. VIZUAL QATOR (Grid ko'rinishida, expander ustida) ───
        # Bu qism student ismini chiroyli ko'rsatadi va orasini ochadi
        st.markdown(f"""
        <div style="display: grid; grid-template-columns: 2fr 1fr 1.5fr 1fr; padding: 12px 20px; 
                    background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); 
                    border-radius: 12px; margin-top: 10px; align-items: center;">
            <div style="font-weight: 700; color: #a78bfa;">👤 {name_str.upper()}</div>
            <div style="text-align: center; font-weight: 800; color: {color}; font-size: 1.1rem;">{overall}</div>
            <div style="text-align: center; color: rgba(255,255,255,0.5); font-size: 0.85rem;">📅 {date_str.split(' ')[0]}</div>
            <div style="text-align: right;"><span class="badge badge-admin">{mode_str.upper()}</span></div>
        </div>
        """, unsafe_allow_html=True)

        # ─── 3. EXPENDER (Faqat ochish vazifasini bajaradi) ───
        # Sarlavhada murakkab belgilar yo'qligi va yuqoridagi CSS arrow chiqishini to'xtatadi
        with st.expander("Batafsil hisobot va audiolarni ko'rish 👇"):
            
            # Top row — asosiy statistika (Sizning kodingiz o'zgarishsiz)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f'<div style="text-align:center;">'
                            f'<div style="color:rgba(255,255,255,0.5);font-size:0.7rem;text-transform:uppercase;letter-spacing:1px;">UMUMIY</div>'
                            f'<div style="font-size:2.5rem;font-weight:800;color:{color};">{overall}</div>'
                            f'<div style="font-size:0.7rem;color:rgba(255,255,255,0.3);">/ 9.0</div>'
                            f'</div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div style="font-size:0.85rem;color:rgba(255,255,255,0.6);">'
                            f'🎯 Mode: {mode_str}<br>📅 {date_str}</div>',
                            unsafe_allow_html=True)
            with col3:
                st.markdown(f'<div style="font-size:0.82rem;">'
                            f'🗣️ Fluency: {r.get("fluency_score",0)}<br>'
                            f'📚 Vocab: {r.get("vocabulary_score",0)}<br>'
                            f'📝 Grammar: {r.get("grammar_score",0)}<br>'
                            f'🔊 Pronunciation: {r.get("pronunciation_score",0)}</div>',
                            unsafe_allow_html=True)
            with col4:
                st.markdown('<div class="danger-btn">', unsafe_allow_html=True)
                if st.button("🗑️ O'chirish", key=f"del_{real_idx}"):
                    delete_student_result(real_idx)
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("---")

            # Questions & Answers
            st.markdown("**📝 Savol va javoblar:**")
            transcripts  = entry.get("transcripts", {})
            questions_map = entry.get("questions_map", {})

            if transcripts:
                for label, transcript in transcripts.items():
                    q_text = questions_map.get(label, "Savol topilmadi")
                    st.markdown(f"""
                    <div style="background:rgba(102,126,234,0.07);border-left:3px solid #667eea;
                      border-radius:0 10px 10px 0;padding:0.8rem 1rem;margin:0.5rem 0;">
                      <div style="color:#a78bfa;font-size:0.72rem;font-weight:700;text-transform:uppercase;
                        letter-spacing:1px;margin-bottom:4px;">{label.upper()}</div>
                      <div style="color:rgba(255,255,255,0.9);font-size:0.9rem;margin-bottom:6px;">
                        ❓ <strong>{q_text}</strong></div>
                      <div style="color:rgba(255,255,255,0.65);font-size:0.85rem;
                        border-top:1px solid rgba(255,255,255,0.08);padding-top:6px;margin-top:6px;">
                        🗣️ {transcript}</div>
                    </div>""", unsafe_allow_html=True)

            # Audio files
            audio_data = entry.get("audio_files", {})
            if audio_data:
                st.markdown("**🎵 Audio fayllar:**")
                for label, audio_b64 in audio_data.items():
                    try:
                        audio_bytes = base64.b64decode(audio_b64)
                        st.markdown(f'<div style="color:rgba(255,255,255,0.6);font-size:0.8rem;">🎙️ {label}</div>',
                                    unsafe_allow_html=True)
                        st.audio(audio_bytes, format="audio/wav")
                    except:
                        pass

            # Topic relevance issues
            topic_issues = r.get("topic_relevance_issues", [])
            if topic_issues:
                st.markdown("**⚠️ Mavzudan Chetlashish:**")
                for ti in topic_issues:
                    st.markdown(f'<div style="background:rgba(239,68,68,0.07);border:1px solid rgba(239,68,68,0.2);'
                                f'border-radius:10px;padding:0.6rem 0.9rem;margin:0.3rem 0;font-size:0.85rem;">'
                                f'<span style="color:#fbbf24;">📌 {ti.get("question","")}</span><br>'
                                f'<span style="color:#f87171;">⚠️ {ti.get("issue","")}</span></div>',
                                unsafe_allow_html=True)

            # Feedback
            st.markdown("**💬 AI Feedback:**")
            st.markdown(f'<div style="background:rgba(0,0,0,0.2);border-radius:10px;padding:1rem;'
                        f'font-size:0.88rem;color:rgba(255,255,255,0.8);">'
                        f'{r.get("overall_feedback","N/A")}</div>', unsafe_allow_html=True)

            strengths    = r.get("strengths", [])
            improvements = r.get("improvements", [])
            if strengths or improvements:
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**✅ Kuchli tomonlar:**")
                    for s in strengths:
                        st.markdown(f'<div style="color:#4ade80;font-size:0.85rem;">• {s}</div>',
                                    unsafe_allow_html=True)
                with c2:
                    st.markdown("**🎯 Yaxshilash kerak:**")
                    for im in improvements:
                        st.markdown(f'<div style="color:#fbbf24;font-size:0.85rem;">• {im}</div>',
                                    unsafe_allow_html=True)
# ═══════════════════════════════════════════════════════════════════════════════
# ADMIN: ADD QUESTION
# ═══════════════════════════════════════════════════════════════════════════════
def page_admin_add_question():
    st.markdown("### ➕ Yangi Savol Qo'shish")
    st.markdown('<p style="color:rgba(255,255,255,0.5);font-size:0.88rem;">Har qanday partga savol qo\'shish mumkin — keyingi testlarda random tanlanadi</p>',
                unsafe_allow_html=True)

    part_choice = st.selectbox("🎯 Part tanlang",
                               options=["part1", "part1_1", "part2", "part3"],
                               format_func=lambda x: {
                                   "part1":   "Part 1 — Shaxsiy savollar",
                                   "part1_1": "Part 1.1 — Rasm tasviri",
                                   "part2":   "Part 2 — Uzun monolog",
                                   "part3":   "Part 3 — Munozara"
                               }.get(x, x),
                               key="admin_part_choice")

    st.markdown("---")

    question_text = st.text_area("❓ Savol matni", placeholder="Savolni kiriting...", key="new_q_text", height=80)

    # Image upload
    st.markdown("**🖼️ Rasm qo'shish (ixtiyoriy):**")
    uploaded_img = st.file_uploader("Rasm yuklang (JPG, PNG)", type=["jpg","jpeg","png","webp"],
                                    key="admin_img_upload", label_visibility="collapsed")
    img_preview_b64 = None
    if uploaded_img:
        img_bytes = uploaded_img.read()
        img_preview_b64 = base64.b64encode(img_bytes).decode()
        st.image(uploaded_img, caption="Ko'rinish", width=220)

    # Part 3 specific
    topic_text = ""
    for_text   = ""
    against_text = ""
    image_desc_text = ""

    if part_choice == "part3":
        st.markdown("**📋 Part 3 uchun qo'shimcha ma'lumot:**")
        topic_text = st.text_input("Mavzu (Topic)", placeholder="masalan: Electric cars should replace gasoline cars.", key="new_topic")
        st.markdown("**✅ FOR nuqtalari (har birini yangi qatorda):**")
        for_text = st.text_area("FOR nuqtalari", placeholder="Birinchi nuqta\nIkkinchi nuqta\nUchinchi nuqta",
                                key="new_for", height=80)
        st.markdown("**❌ AGAINST nuqtalari (har birini yangi qatorda):**")
        against_text = st.text_area("AGAINST nuqtalari", placeholder="Birinchi nuqta\nIkkinchi nuqta\nUchinchi nuqta",
                                    key="new_against", height=80)
    elif part_choice in ("part1_1", "part2"):
        image_desc_text = st.text_input("🖼️ Rasm tavsifi (image_description)",
                                        placeholder="masalan: 🏌️ Golf (left) and 🏀 Basketball (right)",
                                        key="new_img_desc")

    col1, col2 = st.columns(2)
    with col1:
        prep_time = st.number_input("⏱️ Tayyorlanish vaqti (soniya)", min_value=0, max_value=300,
                                    value=5 if part_choice in ("part1","part1_1") else 60, key="new_prep_time")
    with col2:
        speak_time = st.number_input("🎙️ Gapirish vaqti (soniya)", min_value=10, max_value=600,
                                     value=30 if part_choice in ("part1","part1_1") else 120, key="new_speak_time")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("✅ Savolni Qo'shish", use_container_width=True):
        if not question_text.strip():
            st.error("❌ Savol matni bo'sh bo'lmasligi kerak!")
        else:
            custom_qs = load_custom_questions()
            key = f"custom_{part_choice}"
            if key not in custom_qs:
                custom_qs[key] = {"questions": [], "images": {}}

            q_idx = len(custom_qs[key]["questions"])
            custom_qs[key]["questions"].append(question_text.strip())

            if img_preview_b64:
                custom_qs[key]["images"][q_idx] = img_preview_b64

            if part_choice == "part3":
                custom_qs[key]["topic"]          = topic_text.strip()
                custom_qs[key]["for_points"]     = [x.strip() for x in for_text.strip().split("\n") if x.strip()]
                custom_qs[key]["against_points"] = [x.strip() for x in against_text.strip().split("\n") if x.strip()]
            elif part_choice in ("part1_1", "part2"):
                custom_qs[key]["image_description"] = image_desc_text.strip()

            custom_qs[key]["prep_time"]  = int(prep_time)
            custom_qs[key]["speak_time"] = int(speak_time)

            save_custom_questions(custom_qs)
            st.success(f"✅ Savol muvaffaqiyatli qo'shildi! ({part_choice})")
            st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# ADMIN: VIEW ALL QUESTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def page_admin_view_questions():
    st.markdown("### 📋 Barcha Savollar")

    all_pools = get_all_pools()
    custom_qs = load_custom_questions()

    part_labels = {
        "part1": "Part 1 — Shaxsiy savollar",
        "part1_1": "Part 1.1 — Rasm tasviri",
        "part2": "Part 2 — Uzun monolog",
        "part3": "Part 3 — Munozara"
    }

    for part_key, pool in all_pools.items():
        with st.expander(f"🎯 {part_labels.get(part_key, part_key)}  ({len(pool)} to'plam)"):
            for item in pool:
                pid = item.get("id", "?")
                st.markdown(f'<div style="color:#a78bfa;font-weight:700;margin:0.8rem 0 0.4rem;">'
                            f'📦 To\'plam #{pid}</div>', unsafe_allow_html=True)

                # Image description
                if "image_description" in item:
                    st.markdown(f'<div class="img-desc" style="font-size:0.82rem;padding:0.6rem 0.9rem;">'
                                f'🖼️ {item["image_description"]}</div>', unsafe_allow_html=True)

                # Part3 topic
                if "topic" in item:
                    st.markdown(f'<div style="background:rgba(102,126,234,0.07);border:1px solid rgba(102,126,234,0.15);'
                                f'border-radius:10px;padding:0.6rem 1rem;margin:0.3rem 0;font-size:0.85rem;">'
                                f'<span style="color:#a78bfa;font-weight:700;">📋 Mavzu:</span> {item["topic"]}</div>',
                                unsafe_allow_html=True)

                for j, q in enumerate(item.get("questions", [])):
                    st.markdown(f'<div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);'
                                f'border-radius:10px;padding:0.6rem 1rem;margin:0.25rem 0;font-size:0.88rem;">'
                                f'<span style="color:rgba(255,255,255,0.4);margin-right:6px;">{j+1}.</span>'
                                f'{q}</div>', unsafe_allow_html=True)

                st.markdown("---")

            # Custom (admin qo'shgan) savollar
            ckey = f"custom_{part_key}"
            if ckey in custom_qs:
                custom_part = custom_qs[ckey]
                extra_qs    = custom_part.get("questions", [])
                extra_imgs  = custom_part.get("images", {})
                if extra_qs:
                    st.markdown(f'<div style="color:#34d399;font-weight:700;margin:0.8rem 0 0.4rem;">'
                                f'➕ Admin Qo\'shgan Savollar ({len(extra_qs)} ta)</div>', unsafe_allow_html=True)
                    for j, q in enumerate(extra_qs):
                        st.markdown(f'<div style="background:rgba(16,185,129,0.06);border:1px solid rgba(16,185,129,0.2);'
                                    f'border-radius:10px;padding:0.6rem 1rem;margin:0.25rem 0;font-size:0.88rem;">'
                                    f'<span style="color:rgba(255,255,255,0.4);margin-right:6px;">{j+1}.</span>'
                                    f'{q} <span style="background:rgba(16,185,129,0.15);border:1px solid rgba(16,185,129,0.3);'
                                    f'border-radius:6px;padding:2px 6px;font-size:0.65rem;color:#34d399;margin-left:6px;">ADMIN</span>'
                                    f'</div>', unsafe_allow_html=True)

                        if j in extra_imgs:
                            try:
                                img_bytes = base64.b64decode(extra_imgs[j])
                                # Kichik o'lchamda ko'rsatish
                                st.markdown(
                                    f'<img src="data:image/jpeg;base64,{extra_imgs[j]}" class="admin-q-img" />',
                                    unsafe_allow_html=True
                                )
                            except:
                                pass

                        if st.button(f"🗑️ O'chirish", key=f"del_q_{part_key}_{j}"):
                            custom_qs[ckey]["questions"].pop(j)
                            if j in custom_qs[ckey]["images"]:
                                del custom_qs[ckey]["images"][j]
                            save_custom_questions(custom_qs)
                            st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: ADMIN PANEL
# ═══════════════════════════════════════════════════════════════════════════════
def page_admin():
    if not st.session_state.get("admin_logged_in"):
        st.session_state.page = "welcome"
        st.rerun()
        return

    st.markdown('<div class="admin-hero">🛠️ Admin Panel</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub">Barcha huquqlar mavjud</div>', unsafe_allow_html=True)

    tabs = st.tabs(["👥 Studentlar", "➕ Savol Qo'shish", "📋 Barcha Savollar"])

    with tabs[0]:
        page_admin_students()
    with tabs[1]:
        page_admin_add_question()
    with tabs[2]:
        page_admin_view_questions()

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([3, 1, 3])
    with col2:
        if st.button("🚪 Chiqish", use_container_width=True):
            st.session_state.admin_logged_in = False
            st.session_state.page = "welcome"
            st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    init_state()
    p = st.session_state.page

    if p == "welcome":
        page_welcome()
    elif p == "admin":
        page_admin()
    elif p == "mode_select":
        page_mode_select()
    elif p == "test":
        page_test()
    elif p == "results":
        page_results()

if __name__ == "__main__":
    main()
