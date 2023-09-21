import streamlit as st
import os

st.set_page_config(
    page_title="Fine Tuning",
    page_icon="🏦",
    layout="wide"
    )
version = "21.09.23."

from myfunc.mojafunkcija import st_style, positive_login, show_logo
import Priprema_podataka_za_FT as priprema
import Fine_Tuning_Turbo as ft

st_style()
def main():
    if "izr" not in st.session_state:
        st.session_state["izr"] = False 

    if "prip" not in st.session_state:
        st.session_state["prip"] = False 

    show_logo()
    st.markdown(f"<p style='font-size: 10px; color: grey;'>{version}</p>", unsafe_allow_html=True)
    st.subheader('Izaberite operaciju za Fine-Tuning')

    with st.expander("Pročitajte uputstvo:"):
        st.caption("""
                   Prethodni korak bio je kreiranje pitanja. To smo radili pomoću besplatnog ChatGPT modela. Iz svake oblasti (ili iz dokumenta) zamolimo ChatGPT da kreira relevantna pitanja. Na pitanja možemo da odgovorimo sami ili se odgovori mogu izvući iz dokumenta.\n
                   Ukoliko želite da vam model kreira odgovore, odaberite ulazni fajl sa pitanjma iz prethodnog koraka. Opciono, ako je za odgovore potreban izvor, odaberite i fajl sa izvorom. Unesite sistemsku poruku (opis ponašanja modela) i naziv FT modela. Kliknite na Submit i sačekajte da se obrada završi. Fajl sa odgovorima ćete kasnije korisiti za kreiranje FT modela.\n
                   Pre prelaska na sledeću fazu OBAVEZNO pregledajte izlazni dokument sa odgovorima i korigujte ga po potrebi.
                   """)

    colona1, colona2 = st.columns(2)

    with colona1:
        with st.form(key='priprema', clear_on_submit=False):
            priprema_button = st.form_submit_button(
                label='Pripremi ulazne dokumente', use_container_width=True, help = "Pripremi ulazne dokumente")
            if priprema_button:    
                st.session_state.prip=True
                st.session_state.izr=False
    with colona2:
        with st.form(key='izrada', clear_on_submit=False):
            izrada_button = st.form_submit_button(
                label='Izradi FT Model', use_container_width=True, help = "Izrada FT Modela")
            if izrada_button:
                st.session_state.izr=True
                st.session_state.prip=False
    col1, col2 = st.columns(2)

    ph1 = st.empty()
    if st.session_state.prip:
        with ph1.container():
            priprema.pripremaft()


    if st.session_state.izr:
        with ph1.container():
            ft.main()

# Koristi se samo za deploy na streamlit.io
deployment_environment = os.environ.get("DEPLOYMENT_ENVIRONMENT")

if deployment_environment == "Streamlit":
    name, authentication_status, username = positive_login(main, f"{version}")
else:
    if __name__ == "__main__":
        main()


