# Documentation

Hier wird die Funktionsweise des Webservers beschrieben. 
Im scripts Folder sind folgende Unterordner 

- [audio_downloader](#audio_downloader)
- [audio_segmentation](#audio_segmentation)
- [embedding_creation](#embedding_creation)
- [segment_ranking](#segment_ranking)
- [server](#server)
- [utils](#utils)
- [db_connect](#db_connect)

## verwendete Bibliotheken

- [pandas](https://pandas.pydata.org/pandas-docs/stable/index.html) 
- [sqlite3](https://docs.python.org/3/library/sqlite3.html)
- [pydub](https://github.com/jiaaro/pydub)
- [openai](https://github.com/openai/openai-python)

## Openai Schnittstelle

Die Services der OpenAI API werden in verschiedenen Funktionen benutzt.
Ohne einen gültigen OpenAI API KEY läuft das Projekt im Moment nicht.
