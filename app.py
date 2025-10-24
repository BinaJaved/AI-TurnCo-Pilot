import streamlit as st
import os
from datetime import datetime
from openai import OpenAI
import streamlit.components.v1 as components

# the newest OpenAI model is "gpt-5" which was released August 7, 2025.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

st.set_page_config(
    page_title="AI Turn Co-Pilot",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 AI Turn Co-Pilot")
st.markdown("### Adaptive AI Driving Assistant")
st.markdown("---")

if 'scenario_history' not in st.session_state:
    st.session_state.scenario_history = {}

if 'alert_log' not in st.session_state:
    st.session_state.alert_log = []

if 'current_alert' not in st.session_state:
    st.session_state.current_alert = None

if 'current_scenario_name' not in st.session_state:
    st.session_state.current_scenario_name = None

if 'current_occurrence' not in st.session_state:
    st.session_state.current_occurrence = 0

if 'current_urgency' not in st.session_state:
    st.session_state.current_urgency = "calm"

scenarios = {
    "🚗 Left Turn": {
        "name": "Left Turn",
        "description": "Driver preparing to make a left turn at an intersection",
        "icon": "🚗"
    },
    "🚦 Distracted Driver": {
        "name": "Distracted Driver",
        "description": "Driver showing signs of distraction (phone, dashboard, etc.)",
        "icon": "🚦"
    },
    "🌧️ Rainy Weather": {
        "name": "Rainy Weather",
        "description": "Driving in poor weather conditions with reduced visibility",
        "icon": "🌧️"
    },
    "🚶 Pedestrian Crossing": {
        "name": "Pedestrian Crossing",
        "description": "Pedestrian detected near or in crosswalk",
        "icon": "🚶"
    },
    "😴 Drowsy Driver": {
        "name": "Drowsy Driver",
        "description": "Driver showing signs of fatigue or drowsiness",
        "icon": "😴"
    }
}

def get_urgency_level(scenario_name):
    count = st.session_state.scenario_history.get(scenario_name, 0)
    if count == 1:
        return "calm"
    elif count == 2:
        return "moderate"
    elif count == 3:
        return "firm"
    elif count >= 4:
        return "critical"
    else:
        return "calm"

def generate_adaptive_alert(scenario_name, scenario_description):
    count = st.session_state.scenario_history.get(scenario_name, 0)
    urgency = get_urgency_level(scenario_name)
    
    recent_alerts = [alert['message'] for alert in st.session_state.alert_log[-3:]]
    
    prompt = f"""You are an AI driving co-pilot assistant. Generate a natural, human-like safety alert for the following scenario:

Scenario: {scenario_name}
Description: {scenario_description}
Occurrence count: {count} time(s)
Urgency level: {urgency}

Recent alerts (to avoid repetition): {recent_alerts if recent_alerts else "None"}

Guidelines:
- For the 1st occurrence (calm): Use a gentle, friendly tone. Make it conversational and non-alarming.
- For the 2nd occurrence (moderate): Be slightly more direct and emphasize the importance of attention.
- For the 3rd occurrence (firm): Use a more serious tone, emphasizing the pattern of behavior.
- For 4+ occurrences (critical): Be urgent and strongly recommend taking action (like pulling over or taking a break).

Requirements:
- Keep the alert natural and conversational (like a helpful co-pilot, not a robot)
- Vary the phrasing to avoid sounding repetitive
- Be concise (1-2 sentences max)
- Make it feel personalized based on the repetition pattern
- Do not use generic phrases from previous alerts

Generate only the alert message, nothing else."""

    try:
        response = openai_client.chat.completions.create(
            model="gpt-5",
            messages=[{"role": "user", "content": prompt}],
            max_completion_tokens=150
        )
        
        alert_text = response.choices[0].message.content
        if alert_text:
            alert_text = alert_text.strip()
        
        if not alert_text:
            alert_text = f"Alert: {scenario_name} detected. Please stay focused on the road."
        
        return alert_text
    except Exception as e:
        return f"Alert: {scenario_name} detected. Please stay focused on the road."

def speak_alert(text):
    """Use browser's Web Speech API to play audio"""
    # Escape single quotes in text to prevent JavaScript errors
    safe_text = text.replace("'", "\\'").replace('"', '\\"')
    
    speech_html = f"""
    <script>
        // Use the browser's built-in text-to-speech
        var msg = new SpeechSynthesisUtterance('{safe_text}');
        msg.rate = 1.0;
        msg.pitch = 1.0;
        msg.volume = 1.0;
        window.speechSynthesis.speak(msg);
    </script>
    """
    components.html(speech_html, height=0)

def trigger_scenario(scenario_key):
    scenario = scenarios[scenario_key]
    scenario_name = scenario['name']
    
    if scenario_name not in st.session_state.scenario_history:
        st.session_state.scenario_history[scenario_name] = 0
    
    st.session_state.scenario_history[scenario_name] += 1
    
    alert_message = generate_adaptive_alert(scenario_name, scenario['description'])
    
    alert_entry = {
        'scenario': scenario_name,
        'icon': scenario['icon'],
        'message': alert_message,
        'timestamp': datetime.now().strftime("%H:%M:%S"),
        'occurrence': st.session_state.scenario_history[scenario_name]
    }
    
    st.session_state.alert_log.append(alert_entry)
    
    if len(st.session_state.alert_log) > 5:
        st.session_state.alert_log = st.session_state.alert_log[-5:]
    
    st.session_state.current_alert = alert_message
    st.session_state.current_scenario_name = scenario_name
    st.session_state.current_occurrence = st.session_state.scenario_history[scenario_name]
    st.session_state.current_urgency = get_urgency_level(scenario_name)

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🎯 Test Driving Scenarios")
    st.markdown("Click a scenario button to generate an adaptive AI alert:")
    
    cols = st.columns(3)
    scenario_keys = list(scenarios.keys())
    
    for idx, scenario_key in enumerate(scenario_keys):
        with cols[idx % 3]:
            if st.button(scenario_key, key=scenario_key, use_container_width=True):
                with st.spinner(f"Generating alert for {scenarios[scenario_key]['name']}..."):
                    trigger_scenario(scenario_key)
                st.rerun()
    
    if st.session_state.current_alert:
        st.markdown("---")
        
        urgency_info = {
            "calm": {"color": "🟢", "label": "Calm", "message_type": "info", "bg_color": "#d4edda"},
            "moderate": {"color": "🟡", "label": "Moderate", "message_type": "warning", "bg_color": "#fff3cd"},
            "firm": {"color": "🟠", "label": "Firm", "message_type": "warning", "bg_color": "#ffe5cc"},
            "critical": {"color": "🔴", "label": "Critical", "message_type": "error", "bg_color": "#f8d7da"}
        }
        
        current_info = urgency_info.get(st.session_state.current_urgency, urgency_info["calm"])
        
        st.markdown(f"### {current_info['color']} Current Alert - {current_info['label']} Level")
        st.markdown(f"**{st.session_state.current_scenario_name}** • Occurrence #{st.session_state.current_occurrence}")
        
        if st.session_state.current_urgency == "calm":
            st.success(st.session_state.current_alert)
        elif st.session_state.current_urgency == "moderate":
            st.warning(st.session_state.current_alert)
        elif st.session_state.current_urgency == "firm":
            firm_container = st.container(border=True)
            with firm_container:
                st.markdown(f"""
                <div style="padding: 0.5rem; border-radius: 0.25rem; background-color: #ff9800; color: white;">
                    <strong>⚠️ {st.session_state.current_alert}</strong>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error(f"🚨 {st.session_state.current_alert}")
        
        st.markdown(f"_This is your **{st.session_state.current_occurrence}{'st' if st.session_state.current_occurrence == 1 else ('nd' if st.session_state.current_occurrence == 2 else ('rd' if st.session_state.current_occurrence == 3 else 'th'))}** {st.session_state.current_scenario_name} alert. The AI adapts its tone based on repetition._")
        
        if st.button("🔊 Replay Alert (Audio)", use_container_width=True):
            speak_alert(st.session_state.current_alert)

with col2:
    st.subheader("📊 Scenario Statistics")
    
    if st.session_state.scenario_history:
        for scenario_name, count in sorted(st.session_state.scenario_history.items(), key=lambda x: x[1], reverse=True):
            urgency = get_urgency_level(scenario_name)
            urgency_colors = {
                "calm": "🟢",
                "moderate": "🟡",
                "firm": "🟠",
                "critical": "🔴"
            }
            st.markdown(f"{urgency_colors.get(urgency, '⚪')} **{scenario_name}**: {count} times")
    else:
        st.info("No scenarios triggered yet")

st.markdown("---")
st.subheader("📝 Scenario Log (Last 5 Alerts)")

if st.session_state.alert_log:
    for alert in reversed(st.session_state.alert_log):
        with st.container():
            col_a, col_b = st.columns([1, 10])
            with col_a:
                st.markdown(f"### {alert['icon']}")
            with col_b:
                st.markdown(f"**{alert['scenario']}** • Occurrence #{alert['occurrence']} • {alert['timestamp']}")
                st.markdown(f"_{alert['message']}_")
            st.markdown("")
else:
    st.info("No alerts yet. Click a scenario button to start testing the AI co-pilot.")

st.markdown("---")
st.caption("🚗 AI Turn Co-Pilot - Adaptive AI driving alerts powered by OpenAI")
