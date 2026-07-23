import streamlit as st
import requests
import pandas as pd
import time

# =====================================================================
# ⚙️ INTERFACE INITIALIZATION
# =====================================================================

st.set_page_config(
    page_title="GuardianAI Live Telemetry Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================================
# 🔗 BACKEND ROUTES
# =====================================================================
# Replace this URL with your own deployed FastAPI backend
BASE_URL = "https://aca3-49-37-249-57.ngrok-free.app"

LATEST_ENDPOINT = f"{BASE_URL}/history/latest"
HISTORY_ENDPOINT = f"{BASE_URL}/history/Instagram/test_user_1"

# =====================================================================
# 📡 SIDEBAR CONTROLS
# =====================================================================

st.sidebar.header("📡 Live Telemetry Control")

live_feed_active = st.sidebar.toggle(
    "Auto Refresh",
    value=True
)

refresh_interval = st.sidebar.slider(
    "Refresh Interval (seconds)",
    1,
    10,
    2
)

st.sidebar.markdown("---")

st.sidebar.info(
    "Connected to GuardianAI Cloud Core"
)

# =====================================================================
# 📥 FETCH LATEST RECORD
# =====================================================================

def pull_latest_analysis():

    try:

        response = requests.get(
            LATEST_ENDPOINT,
            timeout=5
        )

        if response.status_code == 200:

            payload = response.json()

            if (
                isinstance(payload, dict)
                and "message" in payload
            ):
                return None

            return payload

        return None

    except Exception:
        return None


# =====================================================================
# 📥 FETCH HISTORY
# =====================================================================

def pull_history():

    try:

        response = requests.get(
            HISTORY_ENDPOINT,
            timeout=5
        )

        if response.status_code == 200:
            return response.json()

        return []

    except Exception:
        return []


# =====================================================================
# 🎨 MAIN DASHBOARD
# =====================================================================

def render_dashboard(payload):

    st.title("🛡️ GuardianAI Telemetry Dashboard")

    st.caption(
        f"Application: {payload.get('app','Unknown')} | "
        f"Hash: {payload.get('contact_hash','')[:16]}..."
    )

    st.divider()

    # ==========================================================
    # RISK OVERVIEW
    # ==========================================================

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Risk Score",
            payload.get("risk_score", 0)
        )

    with col2:
        st.metric(
            "Tripwire Score",
            payload.get("tripwire_score", 0)
        )

    with col3:
        st.metric(
            "Threat Level",
            payload.get("risk_level", "UNKNOWN")
        )

    with col4:
        st.metric(
            "Stage",
            payload.get(
                "grooming_stage",
                "Unknown"
            )
        )

    with col5:
        st.metric(
            "Confidence",
            f"{payload.get('confidence',0)}%"
        )

    # ==========================================================
    # ALERTS
    # ==========================================================

    st.subheader("⚠️ Threat Assessment")

    if payload.get("status") == "HIGH":

        st.error(
            payload.get(
                "alert",
                "Threat detected."
            )
        )

        st.warning(
            payload.get(
                "advice",
                ""
            )
        )

    else:

        st.success(
            payload.get(
                "alert",
                "Conversation safe."
            )
        )

    # ==========================================================
    # EXPLANATION
    # ==========================================================

    with st.expander(
        "🔍 Explainable AI Analysis",
        expanded=True
    ):

        st.write(
            payload.get(
                "explanation",
                "No explanation available."
            )
        )

        blocks = payload.get(
            "explanation_blocks",
            []
        )

        if blocks:

            df = pd.DataFrame(blocks)

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

    # ==========================================================
    # BEHAVIORAL SCORES
    # ==========================================================

    st.subheader("📊 Behavioral Indicators")

    behavior_scores = payload.get(
        "behavior_scores",
        {}
    )

    if behavior_scores:

        chart_df = pd.DataFrame(
            {
                "Behavior": list(
                    behavior_scores.keys()
                ),
                "Score": list(
                    behavior_scores.values()
                )
            }
        )

        chart_df = chart_df.sort_values(
            by="Score",
            ascending=False
        )

        st.bar_chart(
            chart_df.set_index("Behavior")
        )

    # ==========================================================
    # RELATIONSHIP CONTEXT
    # ==========================================================

    st.subheader("👥 Relationship Context")

    ctx = payload.get(
        "relationship_context",
        {}
    )

    rc1, rc2, rc3 = st.columns(3)

    with rc1:
        st.metric(
            "Known Friend",
            str(
                ctx.get(
                    "known_friend",
                    False
                )
            )
        )

    with rc2:
        st.metric(
            "Long-Term Contact",
            str(
                ctx.get(
                    "long_term_contact",
                    False
                )
            )
        )

    with rc3:
        st.metric(
            "Online Only",
            str(
                ctx.get(
                    "online_only_contact",
                    False
                )
            )
        )

    # ==========================================================
    # HISTORY
    # ==========================================================

    history = pull_history()

    if history:

        st.subheader("📈 Risk Evolution")

        trend = []

        for idx, item in enumerate(
            reversed(history)
        ):

            trend.append(
                {
                    "Event": idx + 1,
                    "Risk Score":
                    item.get(
                        "risk_score",
                        0
                    )
                }
            )

        trend_df = pd.DataFrame(trend)

        st.line_chart(
            trend_df.set_index("Event")
        )

        # ======================================================
        # ESCALATION TABLE
        # ======================================================

        st.subheader(
            "🚨 Historical Escalation Log"
        )

        escalation = []

        for item in reversed(history):

            escalation.append(
                {
                    "Risk":
                    item.get(
                        "risk_score",
                        0
                    ),

                    "Level":
                    item.get(
                        "risk_level",
                        "UNKNOWN"
                    ),

                    "Stage":
                    item.get(
                        "grooming_stage",
                        "-"
                    ),

                    "Confidence":
                    item.get(
                        "confidence",
                        0
                    )
                }
            )

        st.dataframe(
            pd.DataFrame(escalation),
            use_container_width=True,
            hide_index=True
        )

    # ==========================================================
    # DEBUG
    # ==========================================================

    with st.expander(
        "🛠️ Telemetry & Risk Breakdown"
    ):

        c1, c2 = st.columns(2)

        with c1:

            st.subheader("Debug")

            st.json(
                payload.get(
                    "debug",
                    {}
                )
            )

        with c2:

            st.subheader(
                "Risk Breakdown"
            )

            st.json(
                payload.get(
                    "risk_breakdown",
                    {}
                )
            )


# =====================================================================
# 🚀 APP ENTRY
# =====================================================================

payload = pull_latest_analysis()

payload = pull_latest_analysis()

if not payload:

    payload = {
        "app": "Instagram",
        "contact_hash": "demo_guardianai",
        "status": "HIGH",
        "tripwire_score": 86,
        "risk_score": 100,
        "risk_level": "HIGH",
        "grooming_stage": "Offline Meeting Attempt",
        "confidence": 75,
        "alert": "This interaction looks unsafe.",
        "advice": "Stop interaction and avoid further engagement.",
        "explanation": "Demo mode sample analysis.",
        "behavior_scores": {
            "trust_building": 45,
            "meeting_request": 88,
            "secrecy": 15,
            "sexual_request": 20
        },
        "relationship_context": {
            "known_friend": False,
            "long_term_contact": False,
            "online_only_contact": True
        },
        "debug": {},
        "risk_breakdown": {}
    }

render_dashboard(payload)
if payload:

    st.sidebar.success(
        "🟢 Backend Connected"
    )

    st.sidebar.caption(
        f"Updated: {time.strftime('%H:%M:%S')}"
    )

    render_dashboard(payload)

else:

    st.warning(
        "📡 Waiting for live telemetry..."
    )

# =====================================================================
# 🔄 AUTO REFRESH
# =====================================================================

if live_feed_active:

    time.sleep(
        refresh_interval
    )

    st.rerun()