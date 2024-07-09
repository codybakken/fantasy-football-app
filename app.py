import streamlit as st
import get_results
from ui import float_to_ordinal as fto

st.markdown('# Sounds by the Sea')
st.markdown('### Tenative Draft Day: August 24, 2024')
st.markdown('### Buy-In Details')
st.markdown("""
            * 100 total buy-in
            * $90 for the pot
            * $10 for the weekly point winner""")

#side bar element for navigation
with st.sidebar:
    select_owner = st.selectbox("Owner",get_results.owner_name_list)

owner = get_results.filter_df(get_results.owner_df,'manager_name',select_owner).values.tolist()
grade = owner[0][7]
st.markdown(f"## {select_owner}'s Keeper List")
keeper_df = get_results.owner_keepers(get_results.keeper_eval,select_owner)
st.markdown('### Eligible Keepers')
for k in keeper_df.values.tolist():
    round_value = fto(k[6])
    if k[5] == "eligible": 
        st.markdown(f"**{k[2]}** ({k[4]} - {k[3]}): {round_value}")

st.markdown('### Other Players')
for k in keeper_df.values.tolist():
    round_value = fto(k[6])
    if k[5] == "ineligible": 
        if k[0] == 1 or k[0] == 2:
            reason = "drafted in the first two rounds"
        elif k[7]:
            reason = "you dropped this player"
        elif k[8] == 1:
            reason = "you kept them last year"
        else:
            reason = "no reason"
        st.markdown(f"**{k[2]}** ({k[4]} - {k[3]}) - {reason}")


