import streamlit as st
import os
import requests

API_URL = "http://127.0.0.1:8000/api/v1/search"

os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

st.set_page_config(
    page_title="AI Vinyl & CD Search",
    page_icon="🎵",
    layout="wide"
)

# ----------------------------
# Helper functions
# ----------------------------

def get_cover_url(asin):
    return (
        "https://ws-na.amazon-adsystem.com/widgets/"
        f"q?_encoding=UTF8&Format=_SL500_&ASIN={asin}"
        "&MarketPlace=US&ID=AsinImage&WS=1"
        "&ServiceVersion=20070822"
    )


# ----------------------------
# Header
# ----------------------------

st.title("🎵 AI Vinyl & CD Search")

st.write(
    "Search Amazon's music catalog using **semantic AI search**. "
    "Describe what you're looking for naturally."
)

st.divider()

# ----------------------------
# Search
# ----------------------------

col1, col2 = st.columns([5, 1])

with col1:
    query = st.text_input(
        "Search",
        placeholder="Ex: relaxing jazz for a rainy day",
        label_visibility="collapsed"
    )

with col2:
    search_clicked = st.button(
        "🔍 Search",
        type="primary",
        use_container_width=True
    )


# ----------------------------
# Results
# ----------------------------

if search_clicked:

    if not query.strip():
        st.warning("Please enter a search query before clicking Search.")

    else:
        with st.spinner("Searching for the best matches..."):

            try:

                payload = {
                    "query": query,
                    "limit": 5
                }

                response = requests.post(
                    API_URL,
                    json=payload,
                    timeout=30
                )

                if response.status_code == 200:

                    data = response.json()
                    results = data.get("results", [])

                    if results:

                        st.success(
                            f"Found {len(results)} matching albums!"
                        )

                        for i, record in enumerate(results):

                            asin = record.get("ASIN")
                            title = record.get(
                                "Title",
                                "Unknown Title"
                            )
                            distance = record.get(
                                "Distance",
                                None
                            )

                            with st.container(border=True):

                                # Album cover + information
                                cover_col, info_col = st.columns(
                                    [1, 4],
                                    vertical_alignment="center"
                                )

                                with cover_col:

                                    try:
                                        st.image(
                                            get_cover_url(asin),
                                            width=180
                                        )

                                    except Exception:
                                        st.markdown(
                                            """
                                            <div style="
                                                width: 180px;
                                                height: 180px;
                                                display: flex;
                                                align-items: center;
                                                justify-content: center;
                                                background: #222;
                                                border-radius: 10px;
                                                font-size: 60px;
                                            ">
                                                🎵
                                            </div>
                                            """,
                                            unsafe_allow_html=True
                                        )

                                with info_col:

                                    st.subheader(title)

                                    st.caption(
                                        f"Amazon ASIN: `{asin}`"
                                    )

                                    col_button, col_metric = st.columns(
                                        [2, 1]
                                    )

                                    with col_button:
                                        st.link_button(
                                            "🛒 View on Amazon",
                                            f"https://www.amazon.com/dp/{asin}",
                                            use_container_width=True
                                        )

                                    with col_metric:

                                        if distance is not None:
                                            st.metric(
                                                "AI Distance",
                                                f"{float(distance):.3f}"
                                            )

                                    with st.expander(
                                        "🤖 AI Search Details"
                                    ):

                                        st.write(
                                            "This result was retrieved "
                                            "using semantic vector search."
                                        )

                                        if distance is not None:
                                            st.write(
                                                f"Vector distance: "
                                                f"`{float(distance):.6f}`"
                                            )

                    else:

                        st.info(
                            "No results found. "
                            "Try describing the music differently."
                        )

                else:

                    st.error(
                        f"API Error: {response.text}"
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Failed to connect to the backend API. "
                    "Make sure the FastAPI server or Docker container "
                    "is running."
                )

            except requests.exceptions.Timeout:

                st.error(
                    "The request took too long. "
                    "Please try again."
                )