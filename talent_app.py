import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, timedelta
import random
import math

# ──────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Talent Intelligence Hub",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# CUSTOM CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0f1117; }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1d2e 0%, #161829 100%);
        border-right: 1px solid #2d3561;
    }
    
    /* Metric cards */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #1e2140 0%, #252a4a 100%);
        border: 1px solid #3d4580;
        border-radius: 12px;
        padding: 16px;
    }
    
    /* Headers */
    h1, h2, h3 { color: #e8eaff !important; }
    
    /* Cards */
    .talent-card {
        background: linear-gradient(135deg, #1e2140 0%, #252a4a 100%);
        border: 1px solid #3d4580;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
    }
    
    /* Skill pill */
    .skill-pill {
        display: inline-block;
        background: linear-gradient(90deg, #4f6ef7, #7c4dff);
        color: white;
        border-radius: 20px;
        padding: 4px 12px;
        margin: 3px;
        font-size: 12px;
        font-weight: 500;
    }
    
    /* Score badge */
    .score-high { color: #4ade80; font-weight: 700; }
    .score-mid  { color: #facc15; font-weight: 700; }
    .score-low  { color: #f87171; font-weight: 700; }
    
    /* Section divider */
    .section-header {
        border-left: 4px solid #4f6ef7;
        padding-left: 12px;
        margin: 20px 0 12px 0;
        color: #c7d2fe;
        font-size: 18px;
        font-weight: 600;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        background: #1a1d2e;
        border-radius: 10px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #9ca3af;
        border-radius: 8px;
    }
    .stTabs [aria-selected="true"] {
        background: #4f6ef7 !important;
        color: white !important;
    }
    
    /* Dataframe */
    [data-testid="stDataFrame"] { border-radius: 10px; }
    
    /* Button */
    .stButton>button {
        background: linear-gradient(90deg, #4f6ef7, #7c4dff);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
    }
    
    /* Progress bar */
    .stProgress > div > div { background: linear-gradient(90deg, #4f6ef7, #7c4dff) !important; }
    
    /* Select box */
    .stSelectbox label, .stMultiSelect label { color: #9ca3af !important; }
    
    p, li, label { color: #9ca3af; }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# SEED DATA GENERATOR
# ──────────────────────────────────────────────
@st.cache_data
def generate_data():
    random.seed(42)

    depts = ["Engineering", "Data Science", "HR", "Finance", "Product", "Marketing", "Operations", "Legal"]
    locations = ["Hyderabad", "Bangalore", "Mumbai", "Chennai", "Pune", "Delhi", "Remote"]
    statuses = ["Active", "Active", "Active", "On Leave", "Active", "Probation"]
    genders = ["Male", "Female", "Non-Binary"]

    skill_pool = {
        "Technical": ["Python", "SQL", "Java", "Scala", "Spark", "Snowflake", "AWS", "Azure", "GCP",
                      "Kubernetes", "Docker", "Terraform", "React", "Node.js", "TensorFlow", "PyTorch"],
        "Behavioral": ["Leadership", "Communication", "Problem Solving", "Collaboration", "Adaptability",
                       "Critical Thinking", "Time Management", "Creativity"],
        "Domain": ["SAP", "Workday", "Talent Management", "HR Analytics", "Agile", "Scrum",
                   "Data Governance", "Machine Learning", "NLP", "Computer Vision"]
    }
    all_skills = [s for v in skill_pool.values() for s in v]

    # Employees
    employees = []
    for i in range(1, 101):
        emp_skills = random.sample(all_skills, random.randint(4, 12))
        hire_date = date(2015, 1, 1) + timedelta(days=random.randint(0, 3000))
        employees.append({
            "employee_id": f"EMP{i:04d}",
            "name": f"Employee {i:03d}",
            "department": random.choice(depts),
            "location": random.choice(locations),
            "role": random.choice(["Analyst", "Senior Analyst", "Manager", "Director", "Lead", "Associate"]),
            "gender": random.choice(genders),
            "hire_date": hire_date,
            "status": random.choice(statuses),
            "skills": emp_skills,
            "skill_count": len(emp_skills),
            "performance_score": round(random.uniform(2.5, 5.0), 2),
            "potential_score": round(random.uniform(2.0, 5.0), 2),
            "years_exp": round(random.uniform(1, 20), 1),
        })
    emp_df = pd.DataFrame(employees)

    # Skills detail
    skill_rows = []
    for _, row in emp_df.iterrows():
        for s in row["skills"]:
            cat = next((k for k, v in skill_pool.items() if s in v), "Technical")
            skill_rows.append({
                "employee_id": row["employee_id"],
                "skill": s,
                "category": cat,
                "proficiency": random.randint(1, 5),
                "years_exp": round(random.uniform(0.5, 10), 1),
                "confidence": round(random.uniform(0.6, 1.0), 2),
            })
    skills_df = pd.DataFrame(skill_rows)

    # Learning history
    courses = ["Python Bootcamp", "Snowflake Fundamentals", "Leadership Excellence", "SAP S/4HANA",
               "Machine Learning Basics", "Cloud Architecture", "Data Governance", "Agile Practitioner",
               "Communication Skills", "HR Analytics Certification"]
    providers = ["Coursera", "Udemy", "LinkedIn Learning", "Internal LMS", "Pluralsight", "edX"]
    learning = []
    for _, row in emp_df.iterrows():
        for _ in range(random.randint(1, 5)):
            cdate = date(2021, 1, 1) + timedelta(days=random.randint(0, 1200))
            learning.append({
                "employee_id": row["employee_id"],
                "course": random.choice(courses),
                "provider": random.choice(providers),
                "completion_date": cdate,
                "status": random.choice(["Completed", "Completed", "In Progress", "Not Started"]),
                "score": round(random.uniform(60, 100), 1),
            })
    learning_df = pd.DataFrame(learning)

    # Opportunities
    opportunities = []
    for i in range(1, 21):
        req = random.sample(all_skills, random.randint(3, 6))
        opportunities.append({
            "opportunity_id": f"OPP{i:03d}",
            "title": random.choice(["Senior Data Engineer", "ML Engineer", "HR Business Partner",
                                    "Product Manager", "Cloud Architect", "Analytics Lead",
                                    "Scrum Master", "Finance Analyst", "Talent Manager"]),
            "department": random.choice(depts),
            "location": random.choice(locations),
            "required_skills": req,
            "skill_count_req": len(req),
            "open_since": date(2024, 1, 1) + timedelta(days=random.randint(0, 400)),
        })
    opp_df = pd.DataFrame(opportunities)

    # Performance reviews
    reviews = []
    for _, row in emp_df.iterrows():
        for yr in [2022, 2023, 2024]:
            reviews.append({
                "employee_id": row["employee_id"],
                "year": yr,
                "performance": round(random.uniform(2.5, 5.0), 2),
                "potential": round(random.uniform(2.0, 5.0), 2),
                "department": row["department"],
            })
    reviews_df = pd.DataFrame(reviews)

    # Skill demand (market intelligence)
    demand_data = []
    for s in all_skills:
        demand_data.append({
            "skill": s,
            "demand_score": round(random.uniform(40, 100), 1),
            "category": next((k for k, v in skill_pool.items() if s in v), "Technical"),
            "yoy_change": round(random.uniform(-10, 30), 1),
        })
    demand_df = pd.DataFrame(demand_data).sort_values("demand_score", ascending=False)

    return emp_df, skills_df, learning_df, opp_df, reviews_df, demand_df, skill_pool


emp_df, skills_df, learning_df, opp_df, reviews_df, demand_df, skill_pool = generate_data()


# ──────────────────────────────────────────────
# SIDEBAR NAV
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧠 Talent Intelligence Hub")
    st.markdown("---")
    page = st.radio(
        "Navigate",
        ["📊 Dashboard", "👤 Talent Profiles", "🧩 Skills Intelligence",
         "🎓 Learning & Certifications", "🎯 Opportunity Matching",
         "📈 Performance & Potential", "🌍 Market Intelligence"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown("**Filters**")
    dept_filter = st.multiselect("Department", options=sorted(emp_df["department"].unique()), default=[])
    loc_filter = st.multiselect("Location", options=sorted(emp_df["location"].unique()), default=[])

    # Apply filters
    filtered_emp = emp_df.copy()
    if dept_filter:
        filtered_emp = filtered_emp[filtered_emp["department"].isin(dept_filter)]
    if loc_filter:
        filtered_emp = filtered_emp[filtered_emp["location"].isin(loc_filter)]

    st.markdown("---")
    st.markdown(f"<small style='color:#6b7280'>📁 {len(filtered_emp)} employees</small>", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# PAGE: DASHBOARD
# ──────────────────────────────────────────────
if page == "📊 Dashboard":
    st.markdown("# 📊 Talent Intelligence Dashboard")
    st.markdown("<p>Enterprise view · Powered by SAP Talent Intelligence Hub schema</p>", unsafe_allow_html=True)

    # KPIs
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("👥 Total Employees", len(filtered_emp))
    c2.metric("🧩 Avg Skills / Employee", f"{filtered_emp['skill_count'].mean():.1f}")
    c3.metric("⭐ Avg Performance", f"{filtered_emp['performance_score'].mean():.2f}")
    c4.metric("🎯 Open Opportunities", len(opp_df))
    c5.metric("🎓 Courses Completed",
              len(learning_df[learning_df["status"] == "Completed"]))

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">Headcount by Department</div>', unsafe_allow_html=True)
        dept_counts = filtered_emp["department"].value_counts().reset_index()
        dept_counts.columns = ["Department", "Count"]
        fig = px.bar(dept_counts, x="Department", y="Count",
                     color="Count", color_continuous_scale=["#4f6ef7", "#7c4dff"],
                     template="plotly_dark")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          showlegend=False, coloraxis_showscale=False, height=300)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">9-Box Grid: Performance vs Potential</div>', unsafe_allow_html=True)
        sample = filtered_emp.sample(min(60, len(filtered_emp)), random_state=42)
        fig2 = px.scatter(sample, x="potential_score", y="performance_score",
                          color="department", size=[10] * len(sample),
                          template="plotly_dark", height=300,
                          labels={"potential_score": "Potential", "performance_score": "Performance"})
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(20,22,40,0.8)")
        fig2.add_hline(y=3.5, line_dash="dash", line_color="#9ca3af", opacity=0.4)
        fig2.add_vline(x=3.5, line_dash="dash", line_color="#9ca3af", opacity=0.4)
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="section-header">Location Distribution</div>', unsafe_allow_html=True)
        loc_counts = filtered_emp["location"].value_counts().reset_index()
        loc_counts.columns = ["Location", "Count"]
        fig3 = px.pie(loc_counts, names="Location", values="Count",
                      color_discrete_sequence=px.colors.sequential.Plasma,
                      template="plotly_dark", hole=0.45)
        fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", height=300)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown('<div class="section-header">Hiring Trend (by Year)</div>', unsafe_allow_html=True)
        hire_df = filtered_emp.copy()
        hire_df["hire_year"] = pd.to_datetime(hire_df["hire_date"]).dt.year
        trend = hire_df.groupby("hire_year").size().reset_index(name="hires")
        fig4 = px.area(trend, x="hire_year", y="hires",
                       template="plotly_dark", color_discrete_sequence=["#4f6ef7"])
        fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(20,22,40,0.8)", height=300)
        st.plotly_chart(fig4, use_container_width=True)

    # Top skills org-wide
    st.markdown('<div class="section-header">Top 15 Skills Across Organisation</div>', unsafe_allow_html=True)
    skill_counts = skills_df[skills_df["employee_id"].isin(filtered_emp["employee_id"])]["skill"].value_counts().head(15)
    fig5 = px.bar(x=skill_counts.values, y=skill_counts.index, orientation="h",
                  color=skill_counts.values, color_continuous_scale=["#4f6ef7", "#7c4dff"],
                  template="plotly_dark")
    fig5.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                       yaxis=dict(autorange="reversed"), coloraxis_showscale=False, height=380)
    st.plotly_chart(fig5, use_container_width=True)


# ──────────────────────────────────────────────
# PAGE: TALENT PROFILES
# ──────────────────────────────────────────────
elif page == "👤 Talent Profiles":
    st.markdown("# 👤 Talent Profiles")

    search = st.text_input("🔍 Search by name or ID", "")
    view_all = filtered_emp.copy()
    if search:
        view_all = view_all[
            view_all["name"].str.contains(search, case=False) |
            view_all["employee_id"].str.contains(search, case=False)
        ]

    # Summary table
    display = view_all[["employee_id", "name", "role", "department", "location",
                         "status", "performance_score", "skill_count", "years_exp"]].copy()
    display.columns = ["ID", "Name", "Role", "Dept", "Location", "Status", "Perf ⭐", "Skills 🧩", "Exp (yrs)"]

    st.dataframe(display, use_container_width=True, height=300)

    st.markdown("---")
    st.markdown("### 🔎 Employee Deep-Dive")
    emp_sel = st.selectbox("Select Employee", options=view_all["employee_id"].tolist())

    if emp_sel:
        emp_row = view_all[view_all["employee_id"] == emp_sel].iloc[0]
        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown(f"""
            <div class="talent-card">
                <h3 style="color:#c7d2fe">{emp_row['name']}</h3>
                <p>🏷️ <b>{emp_row['role']}</b></p>
                <p>🏢 {emp_row['department']} · 📍 {emp_row['location']}</p>
                <p>📅 Hired: {emp_row['hire_date']}</p>
                <p>⏱️ {emp_row['years_exp']} yrs experience</p>
                <p>🔵 {emp_row['status']}</p>
                <br/>
                <p>⭐ Performance: <span class="score-high">{emp_row['performance_score']}</span></p>
                <p>🚀 Potential: <span class="score-high">{emp_row['potential_score']}</span></p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            emp_skills = skills_df[skills_df["employee_id"] == emp_sel]
            pills = "".join([f'<span class="skill-pill">{s["skill"]} ({s["proficiency"]}/5)</span>'
                             for _, s in emp_skills.iterrows()])
            st.markdown(f"**Skills ({len(emp_skills)})**")
            st.markdown(pills, unsafe_allow_html=True)

            st.markdown("**Proficiency Breakdown**")
            if not emp_skills.empty:
                fig = px.bar(emp_skills.sort_values("proficiency", ascending=False).head(10),
                             x="skill", y="proficiency",
                             color="category",
                             color_discrete_map={"Technical": "#4f6ef7", "Behavioral": "#7c4dff", "Domain": "#06b6d4"},
                             template="plotly_dark")
                fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=220,
                                  showlegend=True, xaxis_tickangle=-30)
                st.plotly_chart(fig, use_container_width=True)

        # Learning history
        emp_learn = learning_df[learning_df["employee_id"] == emp_sel]
        st.markdown("**Learning History**")
        st.dataframe(emp_learn[["course", "provider", "completion_date", "status", "score"]],
                     use_container_width=True, height=200)


# ──────────────────────────────────────────────
# PAGE: SKILLS INTELLIGENCE
# ──────────────────────────────────────────────
elif page == "🧩 Skills Intelligence":
    st.markdown("# 🧩 Skills Intelligence")

    tabs = st.tabs(["📊 Org Overview", "🔍 Skill Deep-Dive", "⚠️ Skill Gaps"])

    with tabs[0]:
        col1, col2 = st.columns(2)
        with col1:
            cat_counts = skills_df[skills_df["employee_id"].isin(filtered_emp["employee_id"])]["category"].value_counts()
            fig = px.pie(names=cat_counts.index, values=cat_counts.values,
                         title="Skills by Category", template="plotly_dark", hole=0.4,
                         color_discrete_sequence=["#4f6ef7", "#7c4dff", "#06b6d4"])
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", height=320)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            prof_dist = skills_df[skills_df["employee_id"].isin(filtered_emp["employee_id"])]["proficiency"].value_counts().sort_index()
            fig2 = px.bar(x=[f"Level {i}" for i in prof_dist.index], y=prof_dist.values,
                          title="Proficiency Distribution", template="plotly_dark",
                          color=prof_dist.values, color_continuous_scale=["#f87171", "#facc15", "#4ade80"])
            fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                               coloraxis_showscale=False, height=320)
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("**Top Skills by Average Proficiency**")
        top_prof = (skills_df[skills_df["employee_id"].isin(filtered_emp["employee_id"])]
                    .groupby("skill")["proficiency"].mean()
                    .sort_values(ascending=False).head(20).reset_index())
        top_prof.columns = ["Skill", "Avg Proficiency"]
        top_prof["Avg Proficiency"] = top_prof["Avg Proficiency"].round(2)
        st.dataframe(top_prof, use_container_width=True, height=300)

    with tabs[1]:
        skill_sel = st.selectbox("Choose a Skill", options=sorted(skills_df["skill"].unique()))
        skill_data = skills_df[(skills_df["skill"] == skill_sel) &
                               (skills_df["employee_id"].isin(filtered_emp["employee_id"]))]
        merged = skill_data.merge(emp_df[["employee_id", "department", "location"]], on="employee_id")

        c1, c2, c3 = st.columns(3)
        c1.metric("Employees with skill", len(skill_data))
        c2.metric("Avg Proficiency", f"{skill_data['proficiency'].mean():.2f}")
        c3.metric("Avg Confidence", f"{skill_data['confidence'].mean():.0%}")

        fig = px.histogram(merged, x="proficiency", color="department", nbins=5,
                           title=f"Proficiency Distribution – {skill_sel}",
                           template="plotly_dark", barmode="overlay")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(20,22,40,0.8)")
        st.plotly_chart(fig, use_container_width=True)

    with tabs[2]:
        st.markdown("**Skill Gap Analysis** — skills with fewer than 10 proficient employees")
        gap = (skills_df[skills_df["employee_id"].isin(filtered_emp["employee_id"])]
               .groupby("skill").apply(lambda x: (x["proficiency"] >= 4).sum())
               .reset_index())
        gap.columns = ["Skill", "Expert Count"]
        gap = gap.sort_values("Expert Count").head(20)
        fig = px.bar(gap, x="Expert Count", y="Skill", orientation="h",
                     color="Expert Count", color_continuous_scale=["#f87171", "#facc15", "#4ade80"],
                     template="plotly_dark")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          coloraxis_showscale=False, height=500)
        st.plotly_chart(fig, use_container_width=True)


# ──────────────────────────────────────────────
# PAGE: LEARNING & CERTIFICATIONS
# ──────────────────────────────────────────────
elif page == "🎓 Learning & Certifications":
    st.markdown("# 🎓 Learning & Certifications")

    emp_ids = filtered_emp["employee_id"]
    ldf = learning_df[learning_df["employee_id"].isin(emp_ids)]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Enrollments", len(ldf))
    c2.metric("Completed", len(ldf[ldf["status"] == "Completed"]))
    c3.metric("In Progress", len(ldf[ldf["status"] == "In Progress"]))
    c4.metric("Avg Score", f"{ldf[ldf['status']=='Completed']['score'].mean():.1f}")

    col1, col2 = st.columns(2)

    with col1:
        status_counts = ldf["status"].value_counts()
        fig = px.pie(names=status_counts.index, values=status_counts.values,
                     title="Learning Status Distribution", template="plotly_dark", hole=0.4,
                     color_discrete_sequence=["#4ade80", "#4f6ef7", "#facc15", "#f87171"])
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", height=300)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        provider_counts = ldf[ldf["status"] == "Completed"]["provider"].value_counts()
        fig2 = px.bar(x=provider_counts.values, y=provider_counts.index, orientation="h",
                      title="Completions by Provider", template="plotly_dark",
                      color=provider_counts.values, color_continuous_scale=["#4f6ef7", "#7c4dff"])
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                           coloraxis_showscale=False, height=300, yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("**Most Popular Courses**")
    popular = ldf["course"].value_counts().reset_index()
    popular.columns = ["Course", "Enrollments"]
    st.dataframe(popular, use_container_width=True, height=300)

    st.markdown("**Learning Timeline**")
    ldf2 = ldf.copy()
    ldf2["completion_date"] = pd.to_datetime(ldf2["completion_date"])
    ldf2["month"] = ldf2["completion_date"].dt.to_period("M").astype(str)
    timeline = ldf2[ldf2["status"] == "Completed"].groupby("month").size().reset_index(name="completions")
    fig3 = px.line(timeline, x="month", y="completions", template="plotly_dark",
                   color_discrete_sequence=["#4f6ef7"], markers=True)
    fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(20,22,40,0.8)")
    st.plotly_chart(fig3, use_container_width=True)


# ──────────────────────────────────────────────
# PAGE: OPPORTUNITY MATCHING
# ──────────────────────────────────────────────
elif page == "🎯 Opportunity Matching":
    st.markdown("# 🎯 Opportunity Matching (AI Core)")

    opp_sel = st.selectbox("Select an Opportunity", options=opp_df["opportunity_id"].tolist(),
                           format_func=lambda x: f"{x} – {opp_df[opp_df['opportunity_id']==x]['title'].values[0]}")

    opp_row = opp_df[opp_df["opportunity_id"] == opp_sel].iloc[0]

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"""
        <div class="talent-card">
            <h3 style="color:#c7d2fe">{opp_row['title']}</h3>
            <p>🏢 {opp_row['department']}</p>
            <p>📍 {opp_row['location']}</p>
            <p>📅 Open since: {opp_row['open_since']}</p>
            <br/>
            <b>Required Skills:</b><br/>
        """ + "".join([f'<span class="skill-pill">{s}</span>' for s in opp_row["required_skills"]]) +
        "</div>", unsafe_allow_html=True)

    with col2:
        # Compute match scores
        req_skills = set(opp_row["required_skills"])
        match_rows = []
        for _, emp in filtered_emp.iterrows():
            emp_skills_set = set(emp["skills"])
            overlap = emp_skills_set & req_skills
            score = len(overlap) / len(req_skills) * 100
            match_rows.append({
                "Employee": emp["name"],
                "ID": emp["employee_id"],
                "Department": emp["department"],
                "Match Score": round(score, 1),
                "Matched Skills": len(overlap),
                "Total Required": len(req_skills),
                "Perf": emp["performance_score"],
            })
        match_df = pd.DataFrame(match_rows).sort_values("Match Score", ascending=False).head(15)

        fig = px.bar(match_df.head(10), x="Employee", y="Match Score",
                     color="Match Score", color_continuous_scale=["#f87171", "#facc15", "#4ade80"],
                     template="plotly_dark", title="Top 10 Employee Match Scores")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(20,22,40,0.8)",
                          xaxis_tickangle=-30, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Top Matched Candidates**")
    st.dataframe(match_df[["Employee", "ID", "Department", "Match Score", "Matched Skills", "Perf"]],
                 use_container_width=True, height=350)


# ──────────────────────────────────────────────
# PAGE: PERFORMANCE & POTENTIAL
# ──────────────────────────────────────────────
elif page == "📈 Performance & Potential":
    st.markdown("# 📈 Performance & Potential")

    rev_dept = reviews_df[reviews_df["employee_id"].isin(filtered_emp["employee_id"])]

    tabs = st.tabs(["🏆 Leaderboard", "📊 Trends", "🎯 9-Box Grid"])

    with tabs[0]:
        top_perf = (filtered_emp.sort_values("performance_score", ascending=False)
                    [["employee_id", "name", "department", "performance_score", "potential_score", "skill_count"]]
                    .head(20))
        top_perf.columns = ["ID", "Name", "Dept", "Perf ⭐", "Potential 🚀", "Skills 🧩"]
        st.dataframe(top_perf, use_container_width=True, height=500)

    with tabs[1]:
        dept_trend = rev_dept.groupby(["year", "department"])[["performance", "potential"]].mean().reset_index()
        fig = px.line(dept_trend, x="year", y="performance", color="department",
                      title="Performance Trend by Department", template="plotly_dark", markers=True)
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(20,22,40,0.8)")
        st.plotly_chart(fig, use_container_width=True)

        fig2 = px.box(rev_dept[rev_dept["year"] == 2024], x="department", y="performance",
                      title="2024 Performance Distribution by Dept", template="plotly_dark",
                      color="department")
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(20,22,40,0.8)",
                           showlegend=False, xaxis_tickangle=-30)
        st.plotly_chart(fig2, use_container_width=True)

    with tabs[2]:
        def nine_box_label(p, q):
            row = "Low" if p < 3.0 else ("Medium" if p < 4.0 else "High")
            col = "Low" if q < 3.0 else ("Medium" if q < 4.0 else "High")
            labels = {
                ("High", "High"): "⭐ Star", ("High", "Medium"): "🔑 Key Talent",
                ("High", "Low"): "✅ Reliable", ("Medium", "High"): "🌱 Future Star",
                ("Medium", "Medium"): "🔄 Core", ("Medium", "Low"): "⚠️ Needs Dev",
                ("Low", "High"): "💡 Enigma", ("Low", "Medium"): "📉 Underperformer",
                ("Low", "Low"): "❌ Risk",
            }
            return labels.get((row, col), "Core")

        plot_df = filtered_emp.copy()
        plot_df["9-Box"] = plot_df.apply(lambda r: nine_box_label(r["performance_score"], r["potential_score"]), axis=1)
        fig3 = px.scatter(plot_df, x="potential_score", y="performance_score",
                          color="9-Box", hover_data=["name", "department"],
                          template="plotly_dark", title="9-Box Grid – All Employees",
                          labels={"potential_score": "← Low Potential  |  High Potential →",
                                  "performance_score": "← Low Performance  |  High Performance →"})
        fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(20,22,40,0.8)", height=500)
        fig3.add_hline(y=3.5, line_dash="dash", line_color="#9ca3af", opacity=0.5)
        fig3.add_vline(x=3.5, line_dash="dash", line_color="#9ca3af", opacity=0.5)
        fig3.add_hline(y=4.0, line_dash="dot", line_color="#6b7280", opacity=0.3)
        fig3.add_vline(x=4.0, line_dash="dot", line_color="#6b7280", opacity=0.3)
        st.plotly_chart(fig3, use_container_width=True)


# ──────────────────────────────────────────────
# PAGE: MARKET INTELLIGENCE
# ──────────────────────────────────────────────
elif page == "🌍 Market Intelligence":
    st.markdown("# 🌍 External Labor Market Intelligence")

    c1, c2, c3 = st.columns(3)
    c1.metric("Skills Tracked", len(demand_df))
    c2.metric("Avg Market Demand", f"{demand_df['demand_score'].mean():.1f}")
    c3.metric("High-Demand Skills (>80)", len(demand_df[demand_df["demand_score"] > 80]))

    col1, col2 = st.columns(2)

    with col1:
        top_demand = demand_df.head(15)
        fig = px.bar(top_demand, x="demand_score", y="skill", orientation="h",
                     color="demand_score", color_continuous_scale=["#4f6ef7", "#7c4dff", "#06b6d4"],
                     title="Top 15 In-Demand Skills", template="plotly_dark")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          coloraxis_showscale=False, height=450, yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.scatter(demand_df, x="demand_score", y="yoy_change",
                          color="category", size=[10] * len(demand_df),
                          hover_name="skill", title="Demand vs YoY Growth",
                          template="plotly_dark",
                          labels={"demand_score": "Market Demand Score", "yoy_change": "YoY Change %"})
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(20,22,40,0.8)", height=450)
        fig2.add_hline(y=0, line_color="#9ca3af", opacity=0.4)
        st.plotly_chart(fig2, use_container_width=True)

    # Org coverage vs market demand
    st.markdown("### 🔗 Org Coverage vs Market Demand")
    org_skill_counts = (skills_df[skills_df["employee_id"].isin(filtered_emp["employee_id"])]
                        .groupby("skill").size().reset_index(name="org_count"))
    combined = demand_df.merge(org_skill_counts, on="skill", how="left").fillna(0)
    combined["coverage_pct"] = (combined["org_count"] / len(filtered_emp) * 100).round(1)

    fig3 = px.scatter(combined, x="demand_score", y="coverage_pct",
                      color="category", size="org_count",
                      hover_name="skill", template="plotly_dark",
                      title="High Demand + Low Coverage = Strategic Gap",
                      labels={"demand_score": "Market Demand", "coverage_pct": "Org Coverage %"})
    fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(20,22,40,0.8)", height=420)
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("**Full Skill Demand Table**")
    disp = demand_df.copy()
    disp["trend"] = disp["yoy_change"].apply(lambda x: "📈" if x > 5 else ("📉" if x < 0 else "➡️"))
    st.dataframe(disp[["skill", "category", "demand_score", "yoy_change", "trend"]],
                 use_container_width=True, height=350)
