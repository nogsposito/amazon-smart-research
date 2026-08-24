import streamlit as st
import os

os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

from src.pipeline.search import search_disks


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
    "Search Amazon's music catalog using semantic AI search. "
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

        st.warning(
            "Please enter a search query before clicking Search."
        )

    else:

        with st.spinner("Searching for the best matches..."):

            try:

                # Search directly using your project's
                # search pipeline
                results = search_disks(
                    query=query,
                    limit=5
                )

                if results:

                    st.success(
                        f"Found {len(results)} matching albums!"
                    )

                    for record in results:

                        # Depending on how search_disks
                        # returns data, adjust these keys if necessary
                        asin = record.get("ASIN")
                        title = record.get(
                            "Title",
                            "Unknown Title"
                        )

                        distance = record.get("Distance")

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

                                    st.markdown("# 🎵")

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
                                    "🤖 Technical AI Details"
                                ):

                                    st.write(
                                        "Results retrieved using "
                                        "semantic vector search."
                                    )

                                    if distance is not None:

                                        st.write(
                                            f"Vector distance: "
                                            f"`{float(distance):.6f}`"
                                        )

                else:

                    st.warning(
                        "No results found. "
                        "Please try a different query."
                    )

            except Exception as e:

                st.error(
                    f"An error occurred while searching: {e}"
                )