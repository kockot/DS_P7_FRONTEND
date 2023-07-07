import streamlit as st
from streamlit.components.v1 import html
import requests
import base64
import time
import os

API_ENDPOINT_URL = os.environ.get("API_ENDPOINT_URL")
assert API_ENDPOINT_URL is not None
if not API_ENDPOINT_URL.endswith("/"):
    API_ENDPOINT_URL = API_ENDPOINT_URL + "/"

API_ENDPOINT_TOKEN = os.environ.get("API_ENDPOINT_TOKEN")
assert API_ENDPOINT_TOKEN is not None

def clear_cb():
    for c in [explanation_container, result_container_col1, result_container_col2, result_container_col3]:
        with c:
            st.empty()
    status_container.empty()
    time.sleep(0.2)

def alert(msg):
    with status_container.container():
        st.empty()
        #time.sleep(2.2)

    st.warning(f'''# {msg}''', icon="⚠️")
    #time.sleep(5)


def call_api():
    global loading_str
    
    clear_cb()
    if loading_str is None:
        with open("assets/loading.gif", "rb") as img_file:
            loading_str = base64.encodebytes(img_file.read()).decode('utf-8')
            
    
    html_string = f"""<p align="center"><img 
        src="data:@file/gif;base64,{loading_str}"
    ></p>"""
    with status_container.container():
        st.markdown(html_string, unsafe_allow_html=True)

    try:
        r = requests.get(
            f"{API_ENDPOINT_URL}{sk_id_curr}?max_display={max_display}",
            headers={
                'Content-Type':'application/json',
                'Authorization': 'Bearer {}'.format(API_ENDPOINT_TOKEN)
            }
        )
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        alert(f"Http error: {errh}")
        return
    except requests.exceptions.ConnectionError as errc:
        alert(f"Error Connecting: {errc}")
        return
    except requests.exceptions.Timeout as errt:
        alert(f"Timeout Error: {errt}")
        return
    except requests.exceptions.RequestException as err:
        alert(f"Error: {err}")
        return

    #status_container.empty()
    r = r.json()
    if not r["success"]:
        alert(r["message"])
    else:
        with result_container_col1:
            if r["conclusion"]==0:
                st.success("Résultat: crédit accordé")
            else:
                st.error("Résultat: crédit refusé")
        with result_container_col2:
            st.write(f"""Probabilité accord: {r["conclusion_proba"][0]}""")
        with result_container_col3:
            st.write(f"""Probabilité refus: {r["conclusion_proba"][1]}""")
        with explanation_container:
            st.image("data:image/png;base64, "+r["image"])

loading_str = None

st.set_page_config(
    layout="wide", 
    page_title="Prêt à dépenser", 
    page_icon="🤝"
)

status_container = st.empty()

st.info("""Entrez l'identifiant de la demande de prêt, éventuellement changez le nombre d'éléments explicatifs à afficher puis cliquez sur le bouton "Chercher".""")
top_container = st.container()
with top_container:
    top_col0,top_col1,top_col_dummy, top_col2,top_col3 = st.columns([2,6,0.05,1,1])
    with top_col0:
        st.write("Entrez l'identifiant de la demande: ")
    with top_col1:
        sk_id_curr = st.number_input("ID de a demande",
            min_value=0, step=1, label_visibility="collapsed"
        )
    with top_col2:
        sk_id_curr_btn = st.button(
            label="Chercher",
            key="sk_id_curr_btn",
            type="primary",
            on_click=call_api
        )
    with top_col3:
        sk_id_clear_btn = st.button(
                label="Effacer",
                key="sk_id_clear_btn",
                type="secondary",
                on_click=clear_cb
        )
    with top_col_dummy:
        st.write(" ")
        
st.info("Réglez éventuellement le nombre d'éléments à expliquer pour la price de décision")

top_container2 = st.container()
with top_container2:
    top_col2_0,top_col2_1,top_col2_2 = st.columns([2,6,2.05])
    with top_col2_0:
        st.write("Nb de features à détailler: ")
    with top_col2_1:
        max_display = st.slider('', 10, 512, 25, 1, label_visibility="collapsed")
    with top_col2_2:
        st.write(" ")


result_container_col1 = st.container()
with result_container_col1:
    st.write("")
    
result_container2 = st.container()
with result_container2:
    result_container_col2, result_container_col3 = st.columns(2)
    with result_container_col2:
        st.write(" ")
    with result_container_col3:
        st.write(" ")

explanation_container = st.container()
with explanation_container:
    st.write(" ")
