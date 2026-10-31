import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO

st.set_page_config(page_title="ATLAS | Research Command", page_icon="🧠", layout="wide")

BUSINESSES = [
    ("AI receptionist service", "Monthly subscription", "Local services, clinics, salons"),
    ("Real estate lead automation", "Setup + monthly retainer", "Real estate agencies"),
    ("Social media content agency", "Monthly packages", "SMEs and local brands"),
    ("Resume and job assistance", "Per order / subscription", "Job seekers"),
    ("AI customer support service", "Monthly subscription", "E-commerce and SMEs"),
    ("Appointment booking automation", "Setup + monthly fee", "Clinics and service businesses"),
    ("WhatsApp business automation", "Setup + monthly fee", "Retailers and service providers"),
    ("E-commerce operations automation", "Monthly retainer", "Online sellers"),
    ("Lead generation service", "Per qualified lead / retainer", "B2B and local businesses"),
    ("AI website and landing-page service", "Project fee + maintenance", "Small businesses"),
    ("Online courses and training", "Course sales", "Students and professionals"),
    ("Digital products and templates", "Per-sale income", "Creators and small businesses"),
    ("Automated reporting service", "Monthly subscription", "SMEs and agencies"),
    ("Recruitment workflow automation", "Placement / subscription", "Recruiters and employers"),
    ("Email marketing automation", "Monthly retainer", "SMEs and online stores"),
    ("Bookkeeping workflow support", "Monthly subscription", "Small businesses"),
    ("Online review management", "Monthly subscription", "Local businesses"),
    ("Customer reminder automation", "Monthly subscription", "Clinics and appointment businesses"),
    ("Market research service", "Project fee", "Startups and SMEs"),
    ("AI workflow consulting", "Setup + maintenance", "SMEs across sectors"),
]

if "missions" not in st.session_state:
    st.session_state.missions = []
if "candidates" not in st.session_state:
    st.session_state.candidates = pd.DataFrame([
        {"Business": n, "Revenue model": r, "Target customers": c,
         "Demand evidence": "Not researched", "Competitor evidence": "Not researched",
         "Startup cost (₹)": None, "Monthly revenue (₹)": None,
         "Automation score / 10": None, "Evidence status": "Pending"}
        for n, r, c in BUSINESSES
    ])

st.markdown("""
<style>
.block-container {padding-top: 1.4rem; padding-bottom: 2rem;}
.atlas-sub {color:#8b95a5; font-size:0.92rem;}
div[data-testid="stMetric"] {background:rgba(120,120,120,.07); padding:12px; border-radius:12px;}
</style>
""", unsafe_allow_html=True)

st.title("🧠 PROJECT ATLAS")
st.caption("Research Command Centre · Mission 001")
st.markdown('<p class="atlas-sub">One mission interface for research planning, specialist work allocation and evidence-led business decisions.</p>', unsafe_allow_html=True)

with st.sidebar:
    st.header("Mission settings")
    region = st.selectbox("Primary market", ["India", "India + international comparison", "Global"])
    currency = st.selectbox("Currency", ["INR (₹)", "USD ($)"])
    depth = st.selectbox("Research depth", ["Standard", "Deep research", "Due-diligence level"], index=2)
    st.divider()
    st.caption("Build status")
    st.success("Dashboard foundation ready")
    st.warning("Live web research connector: not configured")
    st.info("No API keys are stored in this starter version.")

tab1, tab2, tab3, tab4 = st.tabs(["🎯 Mission control", "🧩 Specialist teams", "📊 Business workspace", "📘 Setup guide"])

with tab1:
    st.subheader("Create a research mission")
    with st.form("mission_form"):
        mission_name = st.text_input("Mission name", "Mission 001 — 20 Automated Business Opportunities")
        objective = st.text_area(
            "What should ATLAS accomplish?",
            "Research 20 businesses that can be automated in India. Compare demand, competitors, startup investment, operating costs, revenue potential, automation feasibility and risks. Rank the best opportunities and recommend the top three.",
            height=125
        )
        deliverables = st.multiselect(
            "Required deliverables",
            ["20-business comparison", "Competitor analysis", "Investment model", "12-month projections",
             "Automation architecture", "Customer acquisition plan", "Risk assessment", "Top-three recommendation"],
            default=["20-business comparison", "Competitor analysis", "Investment model",
                     "12-month projections", "Automation architecture", "Top-three recommendation"]
        )
        submitted = st.form_submit_button("＋ Create mission", type="primary", use_container_width=True)

    if submitted:
        if not objective.strip():
            st.error("Please enter a mission objective.")
        else:
            item = {
                "id": f"ATLAS-{len(st.session_state.missions)+1:03d}",
                "name": mission_name.strip(),
                "objective": objective.strip(),
                "market": region,
                "currency": currency,
                "depth": depth,
                "deliverables": deliverables,
                "status": "Planned — awaiting research connector",
                "created": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            st.session_state.missions.insert(0, item)
            st.success(f"{item['id']} created. The dashboard has recorded the mission plan.")
            st.info("This starter version creates and tracks the mission specification. It does not yet claim to have searched the live internet or completed the research.")

    st.divider()
    st.subheader("Mission queue")
    if not st.session_state.missions:
        st.info("No missions created in this session yet. Submit the form above to create Mission 001.")
    else:
        for m in st.session_state.missions:
            with st.container(border=True):
                c1, c2 = st.columns([3, 1])
                c1.markdown(f"**{m['id']} · {m['name']}**")
                c2.warning(m["status"])
                st.caption(f"Created {m['created']} · Market: {m['market']} · Depth: {m['depth']}")
                st.write(m["objective"])
                st.caption("Deliverables: " + ", ".join(m["deliverables"]))

with tab2:
    st.subheader("Specialist workforce")
    st.write("The 100 roles are logical specialist roles. The first implementation groups them into 10 departments; they are not 100 independently running paid models.")
    teams = [
        ("Research & source discovery", "10 roles", "Find relevant sources, extract facts, compare evidence, record publication dates."),
        ("Market & customer analysis", "10 roles", "Assess customer segments, demand signals, buying problems and willingness-to-pay evidence."),
        ("Competitor intelligence", "10 roles", "Find providers, compare public offers, pricing and positioning."),
        ("Business model design", "10 roles", "Define service packages, revenue models, delivery scope and recurring income."),
        ("Financial modelling", "10 roles", "Estimate startup costs, monthly expenses, revenue scenarios, margins and break-even."),
        ("Automation architecture", "10 roles", "Map tasks, tools, integrations, human handoffs and operating workflows."),
        ("Sales & marketing", "10 roles", "Develop acquisition channels, offers, outreach plans and conversion assumptions."),
        ("Risk & compliance", "10 roles", "Identify privacy, consumer, sector-specific, platform and operational risks."),
        ("Quality assurance", "10 roles", "Cross-check sources, flag contradictions, test calculations and mark unsupported claims."),
        ("Master orchestration", "10 roles", "Plan tasks, delegate work, track dependencies and assemble final reports."),
    ]
    for i in range(0, len(teams), 2):
        cols = st.columns(2)
        for col, team in zip(cols, teams[i:i+2]):
            with col:
                with st.container(border=True):
                    st.markdown(f"**{team[0]}**")
                    st.caption(team[1])
                    st.write(team[2])

with tab3:
    st.subheader("20-business research workspace")
    st.caption("Initial candidate register. Evidence and financial fields remain blank until research is run and verified.")
    edited = st.data_editor(
        st.session_state.candidates,
        use_container_width=True,
        hide_index=True,
        disabled=["Business", "Revenue model", "Target customers"],
        column_config={
            "Startup cost (₹)": st.column_config.NumberColumn(format="₹%d"),
            "Monthly revenue (₹)": st.column_config.NumberColumn(format="₹%d"),
            "Automation score / 10": st.column_config.NumberColumn(min_value=0, max_value=10, step=1),
        }
    )
    st.session_state.candidates = edited
    csv = edited.to_csv(index=False).encode("utf-8-sig")
    st.download_button("⬇ Download candidate register (CSV)", csv, "atlas_20_business_candidates.csv", "text/csv")
    st.metric("Business candidates", len(edited))
    st.warning("Do not treat blank financial fields or candidate names as verified market findings.")

with tab4:
    st.subheader("What is working now — and what comes next")
    st.markdown("""
**Working in this starter build**
- Interactive mission creation and session queue.
- Market, currency and research-depth settings.
- Ten specialist department definitions.
- Editable 20-business candidate register.
- CSV export of the candidate register.

**Not connected yet**
- Live web search and source extraction.
- AI model / agent orchestration.
- Persistent database across sessions.
- Automated financial estimates and source verification.
- PDF report generation and user login.

**Next build step:** connect a web research provider and an AI model through protected API secrets. ATLAS will then gather source-backed evidence for each business, retain URLs and dates, and mark estimates separately from verified facts.
""")
    st.markdown("Deployment guide: [Streamlit Community Cloud](https://docs.streamlit.io/deploy/streamlit-community-cloud) · [Secrets management](https://docs.streamlit.io/deploy/concepts/secrets)")

st.divider()
st.caption("ATLAS starter build · Mission planning workspace · Research results are not generated until live research integrations are configured.")
