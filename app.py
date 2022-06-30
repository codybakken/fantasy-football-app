import streamlit as st
import get_results


st.title("Keeper List")

#side bar element for navigation
with st.sidebar:
    select_owner = st.selectbox("Owner",get_results.owner_name_list)

owner = get_results.filter_df(get_results.owner_df,'manager_name',select_owner).values.tolist()
grade = owner[0][7]
st.markdown(f"### {select_owner}'s Draft Grade last year was {grade}")


keeper_df = get_results.owner_keepers(get_results.keeper_eval,select_owner)

st.dataframe(keeper_df,750,600)
st.text("if the Player Name is 'nan', it means they probably didn't get any points at all.\nI only pulled in the top 700 players")