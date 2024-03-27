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

- [Ziel](##ziel)
- [LaTeX](##bachelorarbeit-latex)
- [Projekt Struktur](##structure)
- [Setup](##setup)
- [Deployment](##docker)

</details>

## <u>Ziel</u>

Das Ziel dieser Bachelorarbeit besteht darin zu untersuchen, wie sich aus umfangreichem Audiomaterial aus Radioprogrammen oder Podcasts on-the-fly ein eigener Podcast zusammenstellen lässt, der relevante Ausschnitte aus einer Vielzahl von Audiomaterial enthält.

Ein möglicher Anwendungsfall wäre ein/e Benutzer*in, die/der sich über das Thema "Überfischung der Meere" informieren möchte und dafür genau 20 Minuten während einer Autofahrt einplant. 
Das System erstellt nun einen Zusammenschnitt aus verschiedenen Podcast Episoden zu diesem Thema, der 20 Minuten lang ist und stellt ihn dem/der Benutzer*in zur Verfügung. 
Der Vorteil für den/die Nutzer*in liegt darin, dass er/sie selbst das Thema auswählen und die exakte Länge festlegen kann, um beispielsweise während einer 20-minütigen Autofahrt einen Podcast anzuhören. 
Außerdem werden das Thema von verschiedenen Personen aus unterschiedlichen Blickpunkten erklärt. 

Für die Interaktion mit dem Benutzer soll außerdem eine Grafische Benutzeroberfläche bereitgestellt werden, die dem Nutzer die Auswahl eines Themas und die Länge der Podcast Episode ermöglicht.


## <u>Bachelorarbeit LaTeX</u>

Das ist das Repository für das Deployment meiner Bachelorarbeit.
Das originale Repository mit allen Jupyter-Notebooks zum Testen von verschiedenen Methoden zur Verbesserung ist [hier](https://github.com/Firevince/Batchelorarbeit) zu finden.
Die gesamte Bachelorarbeit ist dort im Branch LaTeX zu finden.
Im Branch exposee ist ein kleines Exposee für die Bachelorarbeit, welches im Vorfeld entstand.

## <u> Structure </u>

Das Projekt besteht aus 


## <u> Setup </u>

- Clone das Repository:

```sh
mkdir podcast_generator
cd podcast_generator
git clone https://github.com/digitalegarage/podcast-generator.git
```


- Erstelle ein $`\textcolor{red}{\text{.env file}}`$ und ein $`\textcolor{red}{\text{.docker\_env file}}`$ im [root folder](/) und setze die Environment Variablen.

```sh
# .env example
AUDIO_SEGMENT_PATH=<path/to/temporary/audiosegments>
AUDIO_SOURCE_PATH=<path/to/mp3s> # kann sehr viel Daten beanspruchen
CHROMADB_HOST=localhost
CHROMADB_PATH=/Users/br/Projects/Bachelorarbeit/webserver/data/chromadb
CHROMADB_PORT=8000
DATA_PATH=<path/to/data/directory>
OPENAI_KEY=<your_api_token> 
SERVER_PATH=<path/to/flask/server>
```

Zur Funktion des Projektes sind die folgenden Files noch notwendig:



## <u> Docker </u>

### Docker container

Das Projekt kann auch in einem Docker container gestartet werden mit 

```sh
docker-compose up
```


## <u> Author </u>

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
