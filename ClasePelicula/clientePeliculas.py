import requests
from time import sleep


class ClienteHttp():

    def __init__(self, url, retry=0, retry_codes=[]):
        self.url = url
        self.retry = retry
        self.retry_codes = retry_codes

    def get(self, payload={}, headers={}) -> dict:
        titulo = input("Ingrese la palabra clave de la pelicula que quiere buscar: ")
        page = 1
        params = {
            'Title': titulo,
            'Page': page
        }
        moviesFind = []
        dates = []
        yearMovies = {}
        response = requests.request("GET", self.url, headers=headers,
                                    data=payload, params=params)
        total = response.json().get("total_pages")
        for i in range(total):
            newParams = {
                "Title": titulo,
                "page": i + 1
            }
            req = requests.request("GET", self.url, headers=headers,
                                   data=payload, params=newParams)
            movies = req.json().get("data")
            for movie in movies:
                date = movie.get("Year")
                dates.append(date)
                moviesFind.append(movie)
        dates2 = list(set(dates))
        for date3 in dates2:
            list2 = []
            for bd in moviesFind:
                dateCompare = bd.get("Year")
                if date3 == dateCompare:
                    list2.append(bd)
                    yearMovies[date3] = list2
        print(yearMovies)

        print(f'{i},{response.status_code}')
        if response.status_code == 200 \
                or response.status_code not in self.retry_codes:
            return response.json()


if __name__ == '__main__':
    cliente = ClienteHttp('https://jsonmock.hackerrank.com/api/movies/search/', 50, [500, 503, 301])
    cliente.get()
