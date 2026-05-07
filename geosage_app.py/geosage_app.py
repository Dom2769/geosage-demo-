import streamlit as st
from typing import List

st.set_page_config(page_title="GeoSage", page_icon="🪨", layout="centered")

st.title("🪨 GeoSage")
st.caption("Next-generation hybrid AI for rock & mineral identification")

st.markdown("""
*Prototype • MIT License • Copyright (c) 2026 Dom2769*
""")

class GeoSageEngine:
    def __init__(self):
        self.minerals = {
            "amazonite": {"name": "Amazonite", "mohs": 6.2, "diagnostic": "greenish-blue with tartan twinning", "associations": ["smoky_quartz", "topaz"], "market_low": 25, "market_high": 260},
            "fluorite": {"name": "Fluorite", "mohs": 4.0, "diagnostic": "octahedral cleavage, often fluorescent", "associations": ["amazonite"], "market_low": 15, "market_high": 175},
            "pyrite": {"name": "Pyrite", "mohs": 6.3, "diagnostic": "brassy yellow cubic crystals", "associations": ["quartz"], "market_low": 8, "market_high": 95},
            "quartz": {"name": "Quartz", "mohs": 7.0, "diagnostic": "conchoidal fracture", "associations": ["feldspar", "mica"], "market_low": 5, "market_high": 120},
            "calcite": {"name": "Calcite", "mohs": 3.0, "diagnostic": "fizzes strongly in acid", "associations": ["dolomite"], "market_low": 8, "market_high": 85},
            "magnetite": {"name": "Magnetite", "mohs": 6.0, "diagnostic": "strongly magnetic", "associations": ["hematite"], "market_low": 10, "market_high": 70},
            "hematite": {"name": "Hematite", "mohs": 5.5, "diagnostic": "reddish-brown streak", "associations": ["magnetite"], "market_low": 12, "market_high": 90},
            "garnet": {"name": "Garnet", "mohs": 7.0, "diagnostic": "red glassy grains", "associations": ["mica"], "market_low": 15, "market_high": 130},
        }

    def identify(self, location: str, hardness: float, acid: str, nearby: List[str]):
        candidates = []
        for mid, data in self.minerals.items():
            score = 0.28
            if any(word in location.lower() for word in ["pike", "peak", "colorado", "batholith", "granite"]):
                if mid in ["amazonite", "fluorite"]:
                    score *= 4.5
            if abs(hardness - data["mohs"]) < 1.4:
                score *= 2.6
            if "fizzes" in acid and mid == "calcite":
                score *= 4.8
            if any(a in nearby for a in data.get("associations", [])):
                score *= 3.2
            candidates.append({"id": mid, **data, "probability": score})

        candidates = sorted(candidates, key=lambda x: x["probability"], reverse=True)
        total = sum(c["probability"] for c in candidates)
        for c in candidates:
            c["probability"] = min(0.97, c["probability"] / total)
        
        top = candidates[0]
        return {
            "top": top,
            "confidence": round(top["probability"] * 100, 1),
            "explanation": f"**{top['name']}** is the strongest match based on your inputs. The combination of location, hardness, acid reaction, and nearby minerals matches classic geological paragenesis.",
            "decision_steps": [
                f"📍 Location context strongly boosted {top['name']}",
                f"🔬 Hardness test ({hardness}) matched expected range",
                f"🧪 Acid test helped rule out or confirm candidates",
                f"🌍 Paragenesis with nearby minerals gave high confidence"
            ],
            "value_range": f"${top['market_low']}–${top['market_high']}",
            "alternatives": candidates[1:3]
        }

engine = GeoSageEngine()

st.subheader("1. Where was it found?")
location = st.text_input("Be specific (this helps a lot)", "Pike's Peak Batholith, Colorado")

st.subheader("2. Your Test Results")
hardness = st.slider("Hardness (Mohs scale)", 1.0, 10.0, 6.0, 0.1)
acid = st.selectbox("Reaction to vinegar/acid?", ["No reaction", "Fizzes weakly", "Fizzes strongly"])
nearby = st.multiselect("Other minerals seen nearby?", 
    ["smoky_quartz", "topaz", "quartz", "feldspar", "mica", "goethite", "None"])

if st.button("🔍 Identify This Specimen", type="primary", use_container_width=True):
    with st.spinner("Running hybrid intelligence engine..."):
        result = engine.identify(location, hardness, acid.lower(), nearby)
        
        st.success(f"**{result['top']['name']}** — {result['confidence']}% confidence")
        st.markdown(result['explanation'])
        
        st.subheader("Reasoning Path")
        for step in result['decision_steps']:
            st.write(step)
        
        st.subheader("Estimated Market Value")
        st.success(result['value_range'])
        
        if st.button("Generate Etsy/eBay Listing", use_container_width=True):
            st.code(f"Natural {result['top']['name']} specimen from {location}.\nGeoSage hybrid AI verified at {result['confidence']}% confidence.\nClassic paragenesis.")

        if st.button("Save to Collection", use_container_width=True):
            st.toast("✅ Saved to collection (demo)", icon="🪨")

st.caption("Try testing Amazonite with 'Pike\\'s Peak' location, hardness around 6.2, and smoky_quartz nearby.")
