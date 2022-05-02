from turtle import title
from urllib import response
import requests
import json

def get_anime():
  query = '''
    query ($page: Int) {
      Page (page: $page, perPage: 50) {
        media (sort: POPULARITY_DESC, format: TV, isAdult: false) {
          description
          studios(isMain: true) {
            nodes {
              name
            }
          }
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
                full
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
                full
              }
              image {
                medium
              }
            }
            edges {
              role
              voiceActors {
                name {
                  full
                }
                image {
                  medium
                }
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
                coverImage {
                  medium
                }
                staff (page: 1) {
                  nodes {
                    name {
                      full
                    }
                    image {
                      medium
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
    cleaned_response = json.loads(response.text)['data']['Page']['media']
    anime_obj.extend(json.loads(response.text)['data']['Page']['media'])

  #If no English title is available, replace with romaji
  for item in anime_obj[:]:
    if item['title']['english'] == None:
      item['title']['english'] = item['title']['romaji']
    #Drop anything that doesn't have a primary studio
    try:
      studio = item['studios']['nodes'][0]
    except IndexError:
      anime_obj.remove(item)

  #Remove Entries that aren't manga from the "related media" query
  for item in anime_obj[:]:
    related_media = item['relations']['nodes']
    for related in related_media[:]:
      if related['format'] != 'MANGA':
        related_media.remove(related)
    item['relations']['nodes'] = related_media

  #If no English title is available in Manga, replace with romaji
  for item in anime_obj[:]:
    related_media = item['relations']['nodes']
    for related in related_media[:]:
      if related['title']['english'] == None:
        related['title']['english'] = related['title']['romaji']
    item['relations']['nodes'] = related_media


  for item in anime_obj[:]:
    if item['description'] == None:
      item['description'] = "No description available"
      print(item)

  return anime_obj