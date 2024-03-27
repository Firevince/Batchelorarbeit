<div align="center">

  <img src="assets/docs/docs_images/logo.png" width="20%" height="20%">
  
  # Ba(t)chelorarbeit


[![python][python-shield]][python-url]
[![pytorch][pytorch-shield]][pytorch-url]
[![HuggingFace][HuggingFace-shield]][HuggingFace-url]
[![whisper][whisper-shield]][whisper-url]

</div>

---

<details>
<summary>Table of Contents</summary>

- [Ziel](#ziel)
- [LaTeX](#bachelorarbeit-latex)
- [Projekt Struktur](#structure)
- [Setup](#setup)
- [Deployment](#deployment)
- [Docker-compose](#docker-compose)
- [Weiterentwicklung](#weiterentwicklung)

</details>

## Ziel

Das Ziel dieser Bachelorarbeit besteht darin zu untersuchen, wie sich aus umfangreichem Audiomaterial aus Radioprogrammen oder Podcasts on-the-fly ein eigener Podcast zusammenstellen lässt, der relevante Ausschnitte aus einer Vielzahl von Audiomaterial enthält.

Ein möglicher Anwendungsfall wäre ein/e Benutzer*in, die/der sich über das Thema "Überfischung der Meere" informieren möchte und dafür genau 20 Minuten während einer Autofahrt einplant. 
Das System erstellt nun einen Zusammenschnitt aus verschiedenen Podcast Episoden zu diesem Thema, der 20 Minuten lang ist und stellt ihn dem/der Benutzer*in zur Verfügung. 
Der Vorteil für den/die Nutzer*in liegt darin, dass er/sie selbst das Thema auswählen und die exakte Länge festlegen kann, um beispielsweise während einer 20-minütigen Autofahrt einen Podcast anzuhören. 
Außerdem werden das Thema von verschiedenen Personen aus unterschiedlichen Blickpunkten erklärt. 

Für die Interaktion mit dem Benutzer soll außerdem eine Grafische Benutzeroberfläche bereitgestellt werden, die dem Nutzer die Auswahl eines Themas und die Länge der Podcast Episode ermöglicht.


## Bachelorarbeit LaTeX

Das ist das Repository für das Deployment meiner Bachelorarbeit auf der pub. Infrastruktur.
Das originale Repository mit allen Jupyter-Notebooks zum Testen von verschiedenen Methoden zur Verbesserung ist [hier](https://github.com/Firevince/Batchelorarbeit) zu finden.
Die gesamte Bachelorarbeit ist dort im Branch LaTeX zu finden.
Im Branch exposee ist ein kleines Exposee für die Bachelorarbeit, welches im Vorfeld entstand.


## Structure

Das Projekt besteht aus 3 Haupt-Branches, master, deploy und self-deploy.
Die Branches master und deploy sind nahezu identisch. 
Allerdings wird nur der Branch master vom Shadowbroker auch wirklich deployed.
Im Branch self-deploy ist eine docker-compose.yaml auf Root Ebene mit der das Projekt gestartet werden kann.
Außerdem sind die Dockerfiles dort so konfiguriert, dass Sie automatisch laufen, ohne über Kubernetes exteren Volumes anzuschließen.


Die Ordnerstruktur sieht wie folgt aus: 

chroma:
- die Chroma Vektor-Datenbank, diese ist nicht im Repository, da sie ca. 7 GB umfasst. 

docs
- weitere Dokumentation des Projektes

k8s
- Kubernetes Files 

telegram-bot
- Der Telegram-Bot in Typescript, der die API vom webserver benutzt, um Telegram Nachrichten zu verarbeiten

webserver
- Der Flask Webserver und die gesamte Logik des Systems. Benutzt sowohl eine eigene SQLite Datenbank als auch die Chroma Datenbank. 



## Setup 

### Clone das Repository:

```sh
mkdir podcast_generator
cd podcast_generator
git clone https://github.com/digitalegarage/podcast-generator.git
```

### Env Vraiblen

- Erstelle ein $\textcolor{brown}{\text{.env file}}$ und ein $\textcolor{brown}{\text{.docker\_env file}}$ im [root folder](/) und setze die Environment Variablen.

```sh
# .env example
AUDIO_SEGMENT_PATH=<path/to/temporary/audiosegments>
AUDIO_SOURCE_PATH=<path/to/mp3s>
CHROMADB_HOST=localhost
CHROMADB_PATH=<path/to/chroma/db>
CHROMADB_PORT=8000
DATA_PATH=<path/to/data/directory>
OPENAI_KEY=<your_api_token> 
SERVER_PATH=<path/to/flask/server>
```

### Weitere Files

Zur Funktion des Projektes sind die folgenden Directories/Files noch notwendig:

- chroma/chromadb directory - enthält die Chroma Datenbank (eine sqlite db und eine direcctory mit binary data)

- webserver/data - benötigt noch ein inter.wav als Audio, die zwischen den einzelnen Segmenten gespielt wird, sowie eine transcritpts.sqlite 

Bei Bedarf entweder bei SRE nachfrage, ob sie die Production-Datenbanken sharen können, die Momentan in einem gcp-bucket angeschlossen ist, oder mich anschreiben (zum Beispiel über Telegram @f1revince).

### Development 

Um aktiv zu entwickeln, bietet es sich an, ein python virtual environment im root folder zu erstellen.
```sh
pip install python-dotenv 
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Der Webserver kann dann gestartet werden mit 
```sh
python webserver/scripts/server/app.py
```
oder 
```sh
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 600 webserver.scripts.server.app:app
```
Die chromadb kann dann gestartet werden über 
```sh
chroma run --path data/chromadb 
```
Der Telegram-Bot kann gestartet werden über 
```sh
npm start --prefix scripts/telegram_bot
```




## Deployment

Der Master-Branch des Projektes wird automatisch über den Shadowbroker deployed. 
Durch das Jenkinsfile-pub wird das Projekt in die Jenkins CI-Pipeline der pub aufgenommen.
Die einzelnen Dockercontainer werden gebaut und der Webserver ist dann über 
https://web.master.podcast-generator.pub-master.tech erreichbar.
Der Telegram-Bot ist über https://t.me/PodcastGenerator verfügbar.


## Docker-compose


Wenn alle Daten vorhanden sind, kann das Projekt als docker-compose gestartet werden mit.

```sh
docker-compose up
```

## Weiterentwicklung

Zur Weiterentwicklung des Projektes ist das [Haupt-Repo](https://github.com/Firevince/Batchelorarbeit) vermutlich besser geeignet.
Darin sind Skripte zur Transkription neuer Podcast-Episoden, dem Einfügen neuer Daten in die Datenbank und Visualisierungen der Daten vorhanden.
Außerdem gibt es Skripte zum Vergleich von verschiedenen Embeddingmodellen.


## Author

[@Vincent](https://github.com/firevince)


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
<!-- https://shields.io/badges (Bagde generator) -->
<!-- https://github.com/Ileriayo/markdown-badges -->
[python-shield]: https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python&logoColor=white
[python-url]: https://www.python.org

[pytorch-shield]: https://img.shields.io/badge/PyTorch-latest-EE4C2C.svg?style=flat&logo=pytorch
[pytorch-url]:https://pytorch.org

[HuggingFace-shield]: https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-latest-orange
[HuggingFace-url]: https://huggingface.co/

[whisper-shield]: https://img.shields.io/badge/Whisper-74aa9c?logo=openai&logoColor=white
[whisper-url]: https://github.com/openai/whisper
