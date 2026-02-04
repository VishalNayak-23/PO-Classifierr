import json
import streamlit as st
from classifier import classify_po

st.set_page_config(page_title="PO Category Classifier", layout="centered")

with st.sidebar:
    st.subheader("Theme")
    theme_choice = st.radio(
        "Select UI theme",
        ["Black", "Dark Green"],
        horizontal=True,
        label_visibility="collapsed",
    )

if theme_choice == "Dark Green":
    theme_vars = """
        --bg: #07100c;
        --panel: #0f1814;
        --panel-2: #121d18;
        --ink: #e8f2ee;
        --muted: #9eb3aa;
        --accent: #7bf0c0;
        --accent-2: #63d9a6;
        --border: #22302a;
        --chip: #16231d;
    """
    app_bg = "radial-gradient(900px 500px at 12% -12%, #0f1a15 0%, var(--bg) 55%, #050906 100%)"
    hero_bg = "linear-gradient(135deg, #0f1b16 0%, #0c1512 55%, #0a120f 100%)"
else:
    theme_vars = """
        --bg: #0b0c0f;
        --panel: #12141a;
        --panel-2: #161922;
        --ink: #f5f7fb;
        --muted: #a7b0c0;
        --accent: #7bdcff;
        --accent-2: #9b8cff;
        --border: #242a36;
        --chip: #1b2230;
    """
    app_bg = "radial-gradient(900px 500px at 12% -12%, #141724 0%, var(--bg) 50%, #0a0b10 100%)"
    hero_bg = "linear-gradient(135deg, #121621 0%, #10131b 55%, #0e1017 100%)"

st.markdown(
    f"""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600&family=Space+Mono:wght@400;700&display=swap');

      :root {{
        {theme_vars}
      }}

      .stApp {{
        background: {app_bg};
        color: var(--ink);
      }}

      .app-hero {{
        padding: 20px 22px;
        border-radius: 16px;
        background: {hero_bg};
        border: 1px solid var(--border);
        box-shadow: 0 8px 22px rgba(0, 0, 0, 0.45);
        animation: riseIn 700ms ease both;
      }}
      .app-hero h1 {{
        margin: 0 0 6px 0;
        font-size: 32px;
        letter-spacing: 0.4px;
        font-family: 'Space Grotesk', sans-serif;
        color: var(--ink);
      }}
      .app-hero p {{
        margin: 0;
        color: var(--muted);
        font-family: 'Space Grotesk', sans-serif;
        font-size: 14px;
      }}
      .section-title {{
        font-weight: 600;
        margin: 10px 0 6px 0;
        font-family: 'Space Grotesk', sans-serif;
        color: var(--ink);
      }}
      .chip {{
        display: inline-block;
        padding: 4px 10px;
        border-radius: 999px;
        background: var(--chip);
        border: 1px solid var(--border);
        font-size: 12px;
        color: var(--muted);
        margin-right: 6px;
        font-family: 'Space Mono', monospace;
        animation: chipIn 500ms ease both;
      }}
      .chip:nth-child(1) {{ animation-delay: 40ms; }}
      .chip:nth-child(2) {{ animation-delay: 120ms; }}
      .chip:nth-child(3) {{ animation-delay: 200ms; }}

      .result-card {{
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 14px 16px;
        background: var(--panel);
        box-shadow: 0 3px 12px rgba(0, 0, 0, 0.4);
        animation: fadeIn 500ms ease both;
      }}
      .stTextArea textarea, .stTextInput input {{
        font-family: 'Space Grotesk', sans-serif;
        background: var(--panel-2) !important;
        color: var(--ink) !important;
        border: 1px solid var(--border) !important;
      }}
      .stButton > button {{
        border-radius: 10px;
        background: linear-gradient(135deg, var(--accent) 0%, var(--accent-2) 100%);
        color: #0b0c0f;
        border: none;
        font-family: 'Space Grotesk', sans-serif;
      }}
      .stButton > button:hover {{
        filter: brightness(1.05);
      }}

      @keyframes riseIn {{
        from {{ opacity: 0; transform: translateY(8px); }}
        to {{ opacity: 1; transform: translateY(0); }}
      }}
      @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(6px); }}
        to {{ opacity: 1; transform: translateY(0); }}
      }}
      @keyframes chipIn {{
        from {{ opacity: 0; transform: translateY(4px) scale(0.98); }}
        to {{ opacity: 1; transform: translateY(0) scale(1); }}
      }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="app-hero">
      <h1>PO L1-L2-L3 Classifier</h1>
      <p>Paste a PO description and (optionally) a supplier name to classify into L1 / L2 / L3.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.subheader("Quick Tips")
    st.write("- Be specific with item or service details.")
    st.write("- Include quantities and product type.")
    st.write("- Supplier helps disambiguate.")
    st.markdown("---")
    st.caption("Examples")
    st.write("- Purchase 15 laptops for new hires")
    st.write("- Monthly AWS cloud hosting charges")
    st.write("- Office cleaning service - Q1")

if "last_result" not in st.session_state:
    st.session_state.last_result = None

st.markdown("<div class='section-title'>Inputs</div>", unsafe_allow_html=True)
po_description = st.text_area(
    "PO Description",
    height=140,
    placeholder="e.g., Purchase 15 laptops for new hires",
)
supplier = st.text_input(
    "Supplier (optional)",
    placeholder="e.g., Dell, AWS, Staples",
)

col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    classify_clicked = st.button("Classify", type="primary", use_container_width=True)
with col2:
    clear_clicked = st.button("Clear", use_container_width=True)
with col3:
    st.markdown(
        "<span class='chip'>Fast</span><span class='chip'>JSON Output</span><span class='chip'>L1/L2/L3</span>",
        unsafe_allow_html=True,
    )

if clear_clicked:
    st.session_state.last_result = None
    st.experimental_rerun()

if classify_clicked:
    if not po_description.strip():
        st.warning("Please enter a PO description.")
    else:
        with st.spinner("Classifying..."):
            result = classify_po(po_description.strip(), supplier.strip())

        try:
            parsed = json.loads(result)
            st.session_state.last_result = parsed
        except Exception:
            st.session_state.last_result = {"error": "Invalid model response", "raw": result}

if st.session_state.last_result:
    st.markdown("<div class='section-title'>Result</div>", unsafe_allow_html=True)
    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
    if "error" in st.session_state.last_result:
        st.error(st.session_state.last_result["error"])
        st.text(st.session_state.last_result.get("raw", ""))
    else:
        st.success("Classification complete.")
        st.json(st.session_state.last_result)
    st.markdown("</div>", unsafe_allow_html=True)

st.caption("Tip: If results look off, try adding supplier name or a more specific item description.")
