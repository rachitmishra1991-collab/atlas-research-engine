
import streamlit as st
import pandas as pd
import json
import re
import time
from io import BytesIO
from google import genai
from google.genai import types

st.set_page_config(
    page_title="ATLAS Research Engine",
    page_icon="🌐",
    layout="wide"
)

BUSINESSES = [
    "AI receptionist service",
    "Real estate lead automation",
    "Social media content agency",
    "Resume and job assistance",
    "AI customer support service",
    "Appointment booking automation",
    "WhatsApp business automation",
    "E-commerce operations automation",
    "Lead generation service",
    "AI website and landing-page service",
    "Online courses and training",
    "Digital products and templates",
    "Automated reporting service",
    "Recruitment workflow automation",
    "Email marketing automation",
    "Bookkeeping workflow support",
    "Virtual assistant automation",
    "Invoice processing automation",
    "Local SEO and reputation management",
    "Inventory management automation"
]

st.title("🌐 ATLAS — AI Business Research Engine")
st.caption("Mission 001 | India | 20 Automated Business Opportunities")

st.sidebar.header("Research Configuration")

api_key = st.sidebar.text_input(
    "Google Gemini API Key",
    type="password",
    help="Enter your Gemini API key. It is not saved in this repository."
)

model_name = "gemini-3.8-flash"

if "results" not in st.session_state:
    st.session_state.results = []

if "completed" not in st.session_state:
    st.session_state.completed = False

st.sidebar.metric("Businesses", len(BUSINESSES))
st.sidebar.metric("Research completed", len(st.session_state.results))

st.subheader("Mission 001 — India Business Opportunity Analysis")

st.info(
    "ATLAS will research each business using Gemini AI "
    "and Google Search grounding. Results include market "
    "demand, competitors, investment, costs, revenue and risks."
)

with st.expander("View all 20 research targets"):
    for i, business in enumerate(BUSINESSES, 1):
        st.write(f"{i}. {business}")

def extract_json(text):
    text = text.strip()
    text = re.sub(r"^```(?:json)?", "", text)
    text = re.sub(r"```$", "", text)
    start = text.find("{")
    end = text.rfind("}") + 1
    if start == -1 or end == 0:
        raise ValueError("No valid JSON found")
    return json.loads(text[start:end])

def research_business(client, business):
    prompt = f"""
You are an experienced Indian market research analyst.

Conduct current internet research on this business:
{business}

Market: India
Currency: INR

Research:
1. Market demand and target customers.
2. Competitors operating in India.
3. Customer acquisition opportunities.
4. Startup investment.
5. Monthly operating expenses.
6. Realistic monthly revenue after initial establishment.
7. Estimated monthly operating profit.
8. Automation feasibility.
9. Major business risks.
10. Practical first 90-day launch plan.

Use current web information and Google Search.
Distinguish verified facts from estimates.
Do not invent market statistics.
Use conservative financial estimates.
Mention assumptions and cite source URLs.

Return ONLY valid JSON in this structure:

{{
 "business": "{business}",
 "market_demand": "Explanation",
 "target_customers": "Explanation",
 "competitors": "Names and comparison",
 "startup_investment_inr": 0,
 "monthly_operating_cost_inr": 0,
 "monthly_revenue_inr": 0,
 "monthly_profit_inr": 0,
 "automation_score": 0,
 "market_score": 0,
 "competition_score": 0,
 "risks": "Explanation",
 "launch_plan": "First 90 days",
 "sources": [
   {{"title": "Source name", "url": "https://example.com"}}
 ],
 "assumptions": "Financial assumptions"
}}

Scores must be integers between 1 and 10.
Financial figures must be numeric INR values.
"""

    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[
                types.Tool(
                    google_search=types.GoogleSearch()
                )
            ],
            temperature=0.2
        )
    )

    data = extract_json(response.text)
    data["research_status"] = "Completed"
    return data

def make_excel(data):
    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(
            writer,
            index=False,
            sheet_name="Business Research"
        )
    return output.getvalue()

def make_csv(data):
    return pd.DataFrame(data).to_csv(
        index=False
    ).encode("utf-8-sig")

st.divider()

st.subheader("Research Execution")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Research completed",
        len(st.session_state.results)
    )

with col2:
    st.metric(
        "Remaining",
        len(BUSINESSES) - len(st.session_state.results)
    )

if st.button(
    "🚀 START RESEARCH — ALL 20 BUSINESSES",
    type="primary",
    use_container_width=True
):
    if not api_key:
        st.error("Please enter your Gemini API key in the sidebar.")
    else:
        try:
            client = genai.Client(api_key=api_key)

            completed_names = {
                item["business"]
                for item in st.session_state.results
            }

            remaining = [
                b for b in BUSINESSES
                if b not in completed_names
            ]

            progress = st.progress(0)
            status = st.empty()

            for index, business in enumerate(remaining):
                status.info(
                    f"Researching {business} "
                    f"({index + 1}/{len(remaining)})"
                )

                try:
                    result = research_business(
                        client,
                        business
                    )

                    st.session_state.results.append(result)

                except Exception as error:
                    st.warning(
                        f"Research failed for {business}: {error}"
                    )

                progress.progress(
                    (index + 1) / len(remaining)
                )

                time.sleep(1)

            st.session_state.completed = True
            status.success("Research execution finished.")
            st.rerun()

        except Exception as error:
            st.error(f"API connection error: {error}")

if st.session_state.results:

    st.divider()
    st.header("📊 Research Results")

    df = pd.DataFrame(st.session_state.results)

    if "monthly_profit_inr" in df.columns:
        df["monthly_profit_inr"] = pd.to_numeric(
            df["monthly_profit_inr"],
            errors="coerce"
        )

    if "market_score" in df.columns:
        df["market_score"] = pd.to_numeric(
            df["market_score"],
            errors="coerce"
        )

    if "automation_score" in df.columns:
        df["automation_score"] = pd.to_numeric(
            df["automation_score"],
            errors="coerce"
        )

    if "monthly_profit_inr" in df.columns:
        df = df.sort_values(
            "monthly_profit_inr",
            ascending=False
        )

    st.subheader("Business Comparison")

    display_columns = [
        "business",
        "startup_investment_inr",
        "monthly_operating_cost_inr",
        "monthly_revenue_inr",
        "monthly_profit_inr",
        "automation_score",
        "market_score"
    ]

    available = [
        c for c in display_columns
        if c in df.columns
    ]

    st.dataframe(
        df[available],
        use_container_width=True,
        hide_index=True
    )

    st.subheader("🏆 Top Three Opportunities")

    for rank, (_, row) in enumerate(
        df.head(3).iterrows(), 1
    ):
        st.markdown(
            f"### {rank}. {row['business']}"
        )

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Startup investment",
            f"₹{row.get('startup_investment_inr', 0):,.0f}"
        )

        c2.metric(
            "Monthly revenue",
            f"₹{row.get('monthly_revenue_inr', 0):,.0f}"
        )

        c3.metric(
            "Monthly profit",
            f"₹{row.get('monthly_profit_inr', 0):,.0f}"
        )

        st.write(
            "Market demand:",
            row.get("market_demand", "Not available")
        )

        st.write(
            "Risks:",
            row.get("risks", "Not available")
        )

        st.divider()

    st.subheader("Detailed Business Research")

    for _, row in df.iterrows():
        with st.expander(str(row["business"])):
            for field in [
                "market_demand",
                "target_customers",
                "competitors",
                "risks",
                "launch_plan",
                "assumptions"
            ]:
                st.markdown(f"**{field.replace('_', ' ').title()}**")
                st.write(row.get(field, "Not available"))

            st.markdown("**Research Sources**")

            sources = row.get("sources", [])

            if isinstance(sources, list):
                for source in sources:
                    if isinstance(source, dict):
                        url = source.get("url", "")
                        title = source.get("title", url)
                        if url.startswith("https://"):
                            st.markdown(f"- [{title}]({url})")

    st.divider()
    st.subheader("📥 Download Research Reports")

    d1, d2 = st.columns(2)

    with d1:
        st.download_button(
            "Download Excel Report",
            data=make_excel(df.to_dict("records")),
            file_name="ATLAS_Mission_001.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    with d2:
        st.download_button(
            "Download CSV Report",
            data=make_csv(df.to_dict("records")),
            file_name="ATLAS_Mission_001.csv",
            mime="text/csv",
            use_container_width=True
        )

    if len(st.session_state.results) < 20:
        st.warning(
            f"{20 - len(st.session_state.results)} "
            "businesses remain to be researched. "
            "Press Start Research again to continue."
        )
    else:
        st.success(
            "All 20 business research records have been generated."
        )

else:
    st.info(
        "No research results yet. Enter your API key "
        "and start the research engine."
    )

st.divider()
st.caption(
    "ATLAS Research Engine | Mission 001 | "
    "AI-generated estimates require independent validation."
)
