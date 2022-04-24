from urllib import response
import requests


query = '''
query ($id: Int) {
  Media (id: $id, type: ANIME) {
    id
    title {
      romaji
      english
      native
    }
  }
}
'''

# Define our query variables and values that will be used in the query request
variables = {
    'id': 15125
}

url = 'https://graphql.anilist.co'

# Make the HTTP Api request
response = requests.post(url, json={'query': query, 'variables': variables})

print(response.text)