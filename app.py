from __future__ import annotations

import streamlit as st

from search_links import (
    build_manual_decision_maker_search_links,
    build_search_links,
)


st.set_page_config(page_title="Egypt Web Discovery", page_icon="🔎", layout="wide")
st.title("Egypt Web Discovery")
st.caption("Create free Google and Bing links to research Egyptian businesses.")

st.info(
    "Searches open in Google or Bing only when you click a link. This app does not "
    "retrieve search results, scrape social networks, or use a paid search API."
)

with st.form("web_search_generator"):
    business_name = st.text_input(
        "Specific business name (optional)",
        key="web_search_business_name",
        help="Enter a business for decision-maker and Facebook/Instagram page queries, or use industry searches.",
    )
    industry_cols = st.columns(2)
    industry_english = industry_cols[0].text_input(
        "Industry or service (English)", key="web_search_industry_en"
    )
    industry_arabic = industry_cols[1].text_input(
        "Industry or service (Arabic)", key="web_search_industry_ar"
    )
    location_cols = st.columns(2)
    location_english = location_cols[0].text_input(
        "City / governorate (English)", value="Egypt", key="web_search_location_en"
    )
    location_arabic = location_cols[1].text_input(
        "City / governorate (Arabic)", key="web_search_location_ar"
    )
    generate_searches = st.form_submit_button(
        "Generate free search links", key="generate_web_search_links"
    )

if generate_searches:
    try:
        if business_name.strip():
            st.session_state["manual_web_searches"] = (
                build_manual_decision_maker_search_links(
                    business_name=business_name,
                    industry=industry_english or industry_arabic,
                    location=location_english or location_arabic or "Egypt",
                )
            )
        else:
            st.session_state["manual_web_searches"] = build_search_links(
                industry_english=industry_english,
                industry_arabic=industry_arabic,
                location_english=location_english,
                location_arabic=location_arabic,
            )
    except ValueError as error:
        st.error(str(error))

for index, search in enumerate(st.session_state.get("manual_web_searches", [])):
    with st.container(border=True):
        st.write(
            f"**{search.get('topic', search.get('platform', 'Search'))} · "
            f"{search['language']}**"
        )
        st.code(search["query"])
        with st.container(horizontal=True):
            st.link_button(
                "Search Google", search["google_url"], key=f"google_search_{index}"
            )
            st.link_button(
                "Search Bing", search["bing_url"], key=f"bing_search_{index}"
            )

st.caption(
    "Search results can be incomplete, stale, or mismatched. Confirm that each "
    "profile belongs to the business before relying on it."
)
