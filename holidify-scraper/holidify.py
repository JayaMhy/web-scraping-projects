import requests
import re
from bs4 import BeautifulSoup as BS
import csv


def scrape_countries(directions, continents, limit=float('inf')):
    countries = []
    f = open("countries.txt", "w")
    for direction in directions:
        for continent in continents:
            res = requests.get(
                "https://www.holidify.com/region/%s-%s/countries-to-visit.html" % (direction, continent))
            soup = BS(res.text, 'html.parser')
            for link in soup.findAll('a', attrs={'href': re.compile("^/country/.*/$")}):
                countries.append(link.get('href'))
                f.write(link.get('href')+"\n")
                print(link.get('href'))
                if len(countries) >= limit:
                    return countries
    f.close()
    return countries


def scrape_states(countries, limit=float('inf')):
    states = []
    f = open("states.txt", "w")
    for country in countries:
        for j in range(1000):
            res = requests.get(
                "https://www.holidify.com%splaces-to-visit.html?pageNum=%s" % (country, j))
            soup = BS(res.text, 'html.parser').find(
                "div", {"class": "row no-gutters mb-50 negative-margin-mobile"})
            if not soup:
                break
            if not soup.findAll('a', attrs={'href': re.compile("^/places/.*/$")}):
                break
            for link in soup.findAll('a', attrs={'href': re.compile("^/places/.*/$")}):
                states.append(link.get('href'))
                f.write(link.get('href')+"\n")
                print(link.get('href'))
                if len(states) >= limit:
                    return states
    f.close()
    return states


def scrape_places(states, limit=float('inf')):
    f = open("places.txt", "w")
    places = []
    for state in states:
        for i in range(1000):
            url = "https://www.holidify.com%ssightseeing-and-things-to-do.html?pageNum=%s" % (
                state, i)
            res = requests.get(url)
            soup = BS(res.text, 'html.parser').find(id="attractionList")
            if not soup:
                break
            if not soup.findAll('a', attrs={'href': re.compile("^https://www.holidify.com%s.*.html$" % state)}):
                break
            for link in soup.findAll('a', attrs={'href': re.compile("^https://www.holidify.com%s.*.html$" % state)}):
                places.append(link.get('href'))
                f.write(link.get('href')+"\n")
                print(link.get('href'))
                if len(places) >= limit:
                    break
        if len(places) >= limit:
            break
    f.close()
    row = ["Place Name", "City", "State", "Country", "Weather",
           "Required Hrs", "Entry Fee", "Timings", "URL"]
    with open('places.csv', 'w', newline="") as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)
    return places


def scrape_destinations(places):
    for place in places:
        try:
            url = place
            res = requests.get(place)
            soup = BS(res.text, 'html.parser')

            title = soup.find("h1", {"class": "heading1"}).string
            print(title)
            attraction_atf = soup.find("div", {"class": "attraction-atf"})
            links = attraction_atf.findAll('a')
            address = []
            for a in links:
                if(a.string):
                    address.append(a.string)
            try:
                country = address[-1]
            except:
                country = ""
            try:
                state = address[-2]
            except:
                state = ""
            try:
                city = address[-3]
            except:
                city = ""
            objective_information = soup.find(
                "div", {"class": "objective-information"}).text
            try:
                time_required = re.search(
                    r"Time Required : (.*) ", objective_information).groups()[0]
            except:
                time_required = ""
            try:
                entry_fee = re.search(r"Entry Fee : (.*) ",
                                      objective_information).groups()[0]
            except:
                entry_fee = ""
            try:
                timings = re.search(r"Timings : (.*) ",
                                    objective_information).groups()[0]
            except:
                timings = ""
            try:
                weather = re.search(r"fetchWeather((.*));",
                                    soup.text).groups()[0]
            except:
                weather = ""
            row = [title, city, state, country, weather,
                   time_required, entry_fee, timings, url]
            with open('places.csv', 'a', newline="") as csvFile:
                try:
                    writer = csv.writer(csvFile)
                    writer.writerow(row)
                except:
                    pass
        except Exception as e:
            print(e)
            pass


if __name__ == "__main__":
    # directions = ["eastern", "western", "southern", "northern", "east", "west", "north", "south"]
    # continents = ["asia", "europe", "africa", "america"]

    # For test, because the data is too big I will take only 10 each and only one continent and direction
    directions = ["eastern"]
    continents = ["america"]
    countries = scrape_countries(directions, continents, 10)
    states = scrape_states(countries, 10)
    places = scrape_places(states, 50)
    destinations = scrape_destinations(places)
