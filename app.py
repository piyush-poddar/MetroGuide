import streamlit as st
import json
from main import get_route
import math

metro = "dmrc"
with open(rf"{metro}\name_to_id.json") as name_id_file:
    name_id = json.load(name_id_file)

station_list = list(name_id.keys())

st.title("Metro Route Finder")

src = st.selectbox(
    "Source:",
    station_list,
    index = None,
    placeholder = "Source Station"
)

dest = st.selectbox(
    "Destination:", 
    station_list,
    index = None,
    placeholder = "Destination Station"
)

st.markdown("""
<style>
    .route-container {
        background-color: #f9f9f9;
        border-radius: 10px;
        padding: 20px;
        width: 90%;
        margin: 0 auto;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .station-header {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .direction {
        color: #999;
        font-size: 14px;
        margin-top: 0px;
    }
    .station-info {
        font-size: 24px;
        font-weight: bold;
    }
    .station-item {
        display: flex;
        align-items: center;
        margin: 0px 0;
    }
    .station-bullet {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 10px;
        flex-shrink: 0;
    }
    .station-name {
        font-size: 16px;
        
        font-weight: bold;
    }
    .divider-line {
        border-left: 5px solid #3b76c0;
        height: 25px;
        margin: 0 4px;
    }
    .interchange {
        font-size: 20px;
        font-weight: bold;
        margin: 15px 15px 15px 0px;
    }
    .end-of-route {
        font-size: 14px;
        text-align: center;
        color: white;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

if src and dest:
    src_id = name_id[src]
    dest_id = name_id[dest]
    complete_route = get_route(src_id, dest_id)
    print()
    print(complete_route)
    # st.markdown('<div class="route-container">', unsafe_allow_html=True)

    st.markdown(f"""
        <div class="station-header">From: {src}</div>
        <div class="station-header">To: {dest}</div>
        <div class="station-info">🕒 {math.ceil(complete_route["total_time"]/60)} mins</div>
        <hr style="border: none; border-top: 1px solid #ccc; margin: 15px 0;" />
        """, unsafe_allow_html=True)
    
    old_line = None
    for path in complete_route["route"]:
        cur_line = path["line"]
        if old_line!=None:
            st.markdown(f"""
            <div class="interchange">🔀 Change here and move towards {cur_line}</div>
            """, unsafe_allow_html=True)
        for station in path["path"]:
            st.markdown(f"""
            <div class="station-item">
                <div class="station-bullet" style="background-color: {path["line_color"]};"></div>
                <div>
                    <div class="station-name">{station}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if station!=path["path"][-1]:
                # Add divider between stations
                st.markdown(f"""
                <div class="divider-line" style="border-left: 5px solid {path["line_color"]};"></div>
                """, unsafe_allow_html=True)
        old_line = cur_line
    st.markdown(f"""
        <div class="end-of-route">End of Route</div>
        """, unsafe_allow_html=True)