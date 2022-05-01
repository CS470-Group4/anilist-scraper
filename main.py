from turtle import title
from urllib import response
import requests
import json


query = '''
query ($page: Int) {
  Page (page: $page, perPage: 50) {
    media (sort: POPULARITY_DESC, format: TV, isAdult: false) {
      description
      title {
        english
        romaji
      }
      coverImage {
        medium
      }
      staff (page: 1) {
        nodes {
          name {
            first
            last
          }
          image {
            medium
          }
        }
        edges {
          role
        }
      }
      characters (page: 1) {
        nodes {
          name {
            first
            last
          }
          image {
            medium
          }
        }
        edges {
          role
          voiceActors {
            name {
              first
              last
            }
            image
          }
        }
      }
      relations {
        nodes {
            format
            description
            title {
              english
              romaji
            }
            staff (page: 1) {
              nodes {
                name {
                  first
                  last
                }
              }
              edges {
                role
              }
            }
        }
      }
    }
  }
}
'''



url = 'https://graphql.anilist.co'

anime_obj = []

# Make the HTTP Api request
for i in range(1, 21):
  variables = {
    'page': i
  }

  response = requests.post(url, json={'query': query, 'variables': variables})

  anime_obj.extend(json.loads(response.text)['data']['Page']['media'])

for item in anime_obj:
  if item['title']['english'] == None:
    item['title']['english'] = item['title']['romaji']
  print(item['title']['english'], item['staff']['nodes'][0]['name'], item['staff']['edges'][0]['role'])