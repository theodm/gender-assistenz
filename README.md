# Voraussetzungen
 - Python 3.9+ (https://www.python.org/)
 - Poetry (https://python-poetry.org/)
 - NodeJS (https://nodejs.org/en/)

# Schritte zum Installieren & Starten

Ausgehend von dem Projektverzeichnis als Working Directory

- poetry install
- cd client
- npm install
- npm run build
- cd ..
- poetry shell
- python3.9 -m spacy download de_dep_news_trf
- python3.9 -m spacy download de_core_news_lg
- python3.9 -m pip install coreferee
- python3.9 -m coreferee install de
- python3.9 -m pip install bottle
- python3.9 -m pip install loguru
- python3.9 -m pip install dataset
- python3.9 web_server.py

# Neu starten
- poetry shell
- python web_server.py

Aufruf über http://localhost:8088/index.html
