# Introduction

Ce dépôt propose le frontend d'un dashboard simple utilisant l'API proposé dans le dépôt [DS_P7_API](../DS_P7_API) . Il utilise la librairie Streamlit.

Il nécessite les variables d'environnement suivantes:
- API_ENDPOINT_URL : URL complète du endpoint de l'API de prédiction (se termine par /predict/ )
- API_ENDPOINT_TOKEN : code de sécurité partagé avec le backend

# Install dependancies:
```
pip3 install -r requirements.txt
```


# Run frontend
```
# API endpoint for prediction
export API_ENDPOINT_URL=**provided URL**

# security token shared with the backend app
export API_ENDPOINT_TOKEN=**provided token**

streamlit run frontend.py
```
