import streamlit as st
import os
import requests

API_URL = "http://127.0.0.1:8000/api/v1/search"

os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"


# ----------------------------
# Streamlit configuration
# ----------------------------

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
# Search bar
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

        st.warning(
            "Please enter a search query before clicking Search."
        )

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

                        for record in results:

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

                                cover_col, info_col = st.columns(
                                    [1, 4],
                                    vertical_alignment="center"
                                )

                                # Album cover
                                with cover_col:

                                    if asin:
                                        st.image(
                                            get_cover_url(asin),
                                            width=180
                                        )

                                    else:
                                        st.markdown("### 🎵")

                                # Album information
                                with info_col:

                                    st.subheader(title)

                                    if asin:
                                        st.caption(
                                            f"Amazon ASIN: `{asin}`"
                                        )

                                    button_col, metric_col = st.columns(
                                        [2, 1]
                                    )

                                    with button_col:

                                        if asin:
                                            st.link_button(
                                                "🛒 View on Amazon",
                                                f"https://www.amazon.com/dp/{asin}",
                                                use_container_width=True
                                            )

                                    with metric_col:

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
                        f"Backend API returned an error: "
                        f"{response.status_code}"
                    )

                    with st.expander("Show error details"):
                        st.code(response.text)

            except requests.exceptions.ConnectionError:

                st.error(
                    "Unable to connect to the FastAPI backend."
                )

                st.info(
                    "Make sure the backend server is running on "
                    "`http://127.0.0.1:8000`."
                )

                st.code(
                    "uvicorn src.main:app --reload",
                    language="bash"
                )

            except requests.exceptions.Timeout:

                st.error(
                    "The request to the backend took too long."
                )

            except requests.exceptions.RequestException as e:

                st.error(
                    f"An error occurred while contacting the API: {e}"
                )