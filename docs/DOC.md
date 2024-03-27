# Documentation

- [Verwendete Bibliotheken](#verwendete-Bibliotheken)
- [Openai Schnittstelle](#Openai-Schnittstelle)
- [Scripts](#Scripts)
- [SQLite Datenbank](#SQLite-Datenbank)


## Verwendete Bibliotheken

- [pandas](https://pandas.pydata.org/pandas-docs/stable/index.html) 
- [sqlite3](https://docs.python.org/3/library/sqlite3.html)
- [pydub](https://github.com/jiaaro/pydub)
- [openai](https://github.com/openai/openai-python)

## Openai Schnittstelle

Die Services der OpenAI API werden in verschiedenen Funktionen benutzt.
Ohne einen gültigen OpenAI API KEY läuft das Projekt im Moment nicht.

Der API Key wird verwendet, um eine User-Anfrage zu embedden, um die Segmente zu sortieren und um weiterführende Themen für eine Episode zu erstellen.
Der Production API-Key ist im Moment auf 5$ beschränkt.
Eine Anfrage kostet ca. 0,5 cent.

## Scripts

Hier wird die Funktionsweise des Webservers beschrieben. 
Im scripts Folder sind folgende Unterordner 

- [audio_downloader](#audio_downloader)
- [audio_segmentation](#audio_segmentation)
- [embedding_creation](#embedding_creation)
- [segment_ranking](#segment_ranking)
- [server](#server)
- [utils](#utils)
- [db_connect](#db_connect)


### audio_downloader

In diesem File werden alle Funktionen zum downloaden der MP3 Files von der ARD Audiothek gebündelt.
Außerdem Abfragen für die download-URLs und Metadaten über die GraphQL Schnittstelle.
Die Audiofiles liegen dann in webserver/data/episode_audio_files 

### audio_segmentation

Alle Logik zur Bearbeitung der Audiofiles liegt hier.
In `split_audios.py` werden aus einer Liste an Audiofiles und den Start- und Endzeiten (als pandas Dataframe) die Segment aus diesen Audiofiles geschnitten.
Falls die Audiofiles noch nicht vorhanden sind, wird versucht sie nachzuladen.
Die einzelnen Segmente werden dann als `segment_N.wav` in `webserver/data/audio_segments` abgespeichert.

In `concat_audio.py` werden die einzelnen Segmente zusammengesetzt, indem zwischen jedem Segment eine Audio `inter.wav` aus dem `webserver/data` Ordner geschaltet wird.
Die fertige Audiodatei wird dann in `webserver/scripts/server/static/audio` abgelegt, damit der Server darauf zugreifen kann.
ToDo: in `webserver/data` speichern und den Server dynamisch darauf verlinken

In `get_audio_metadata.py` wird versucht die Titelbilder der Episoden abzugreifen, um sie später in der UI anzeigen zu können.
Die Bilder werden in `webserver/scripts/server/static/images` abgespeichert.
Oft werden hier noch alte Bilder von früheren Abfragen verwendet, da die Abfrage irgendwie häufig fehlschlägt.
ToDo: fixen


### embedding_creation

Hier werden die Embeddings generiert.
In `embeddings_openai.py` wird für jede User-Anfrage ein Embedding mithilfe der OpenAI API erstellt.


### segment_ranking

Hier ist der Code für das Retrieval und Ranking relevanter Dokumente.
In `chromadb_connect.py` werden mithilfe eines Embeddingvektors eine Anfrage an die Chroma Datenbank gestellt, um passende Segmente zu finden.

In `rank_segments.py` werden die Segmente dann enriched, d.h. Es werden für jedes Segmente noch Sätzt vor und nach diesem Segment angefügt.
Außerdem werden sie mithilfe von ChatGPT noch einmal neu nach zusammenhang sortiert.

In `chatgpt_help.py` werden die Anfragen zur Sortierung, für die weiterführenden Themen implementiert.
Die Funktionen, die Segmente von ChatGPT enrichen zu lassen ist außerdem vorhanden, ist aber im Moment nicht eingebaut.
Auch gibt es schon einen Prompt zur enhancing der Useranfrage, um spezifischere Segmente zu finden.
ToDo: implementieren

### server

In diesem Ordner befindet sich der Flask-Webserver.
In `app.py` werden die einzelnen Routen definiert.
Es gibt 
- `/`
    default website mit Form zum ausfüllen
- `/process`
    bearbeitet die Anfrage und gibt Audio aus
- `/api` 
    benötigt Parameter `text` für Anfrage. Optional ist der Parameter `time` für die Anzahl der Segmente 
- `/player`
    eine etwas schönere UI, funktioniert noch nicht ganz
- `/tracks`
    liefert eine Anzahl an verfügbaren schon produzierten generierten Podcast Episoden mit deren Transkripten 
- `/audio/<filename>`
    liefert ein bestimmtes Audiofile, falls vorhanden

in `templates` liegen die HTML templates für den default player und den etwas schöneren Player.

### utils

In `utils.py` sind Funktionen zur Leerung der Audio Ordner, falls diese zu voll sind.

### db_connect

In `db_connect.py` ist der Datenbankzugriff auf die SQLite Datenbank geregelt.
Die Daten werden direkt aus pandas Dataframes abgespeichert und auch wieder geladen.


## SQLite Datenbank

Die Datenbank besteht aus drei Tabellen 
- transcript_sentences 
    besteht aus 
```sh
0|filename|TEXT|0||0
1|sentence|TEXT|0||0
2|start|REAL|0||0
3|end|REAL|0||0
4|sentence_lemmatized|TEXT|0||0
5|sentence_compound_split|TEXT|0||0
6|sentence_id|INTEGER|0||0
7|segment_id|INTEGER|0||0
8|u_id|TEXT|0||0
```

- best_fitting 
    besteht aus 
```sh
0|filename|TEXT|0||0
1|sentence|TEXT|0||0
2|start|REAL|0||0
3|end|REAL|0||0
4|sentence_lemmatized|TEXT|0||0
5|sentence_compound_split|TEXT|0||0
6|sentence_id|INTEGER|0||0
7|segment_id|INTEGER|0||0
8|u_id|TEXT|0||0
```
- episode_metadata
    besteht aus 
```sh
0|title|TEXT|0||0
1|download_url|TEXT|0||0
2|filename|TEXT|0||0
3|description|TEXT|0||0
4|publish_date|TEXT|0||0
5|keywords_json|TEXT|0||0
```

`transcript_sentences` besitzt alle Daten, `best_fitting` enthält nur die enricheden Segmente, die zur Produktion der Episoden notwendig sind.
`episode_metadata` wird im Moment nicht verwendet, kann aber in Zukunft für das Ranking miteinbezogen werden. 
(Ranking nach Keywordmach, nach Aktualität)

