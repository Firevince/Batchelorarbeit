import os
import requests
from urllib.request import urlretrieve

# GraphQL query
query = """
{
  programSet(id: 5945518) {
    title
    items(
      orderBy: PUBLISH_DATE_DESC
      filter: {
        isPublished: {
          equalTo: true
        }
      }
      first: 10
    ) {
      nodes {
        audios {
          downloadUrl
        }
      }
    }
  }
}
"""

graphql_url = "https://api.ardaudiothek.de/graphql"
response = requests.post(graphql_url, json={"query": query})

if response.status_code == 200:
    data = response.json()
    download_dir = "./Podcast_files"
    os.makedirs(download_dir, exist_ok=True)
    for audio_data in data["data"]["programSet"]["items"]["nodes"]:

        audio_url = audio_data["audios"][0]["downloadUrl"]
        filename = os.path.basename(audio_url)
        file_path = os.path.join(download_dir, filename)
        urlretrieve(audio_url, file_path)
        
        print(f"Downloaded: {filename} to {download_dir}")
else:
    print(f"GraphQL request failed with status code {response.status_code}")
