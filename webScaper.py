# import the needed libraries
import requests
from bs4 import BeautifulSoup as bs
import re
import csv


def main():
    # set up the driver
    url = 'https://en.wikipedia.org/wiki/List_of_computer_scientists'
    response = requests.get(url)

    # initialize parameters
    scientists = []
    scientists_links = {}
    scientists_education = {}
    scientists_awards = {}
    names = False
    prefix = 'https://en.wikipedia.org'
    soup = bs(response.text, 'html.parser')

    # scrape the names, links and education
    scientists_list_items = soup.find_all('li')
    for item in scientists_list_items:
        scientist_name_tag = item.find('a', title=True)
        if scientist_name_tag and scientist_name_tag.text == 'Atta ur Rehman Khan':
            names = True
        if names and scientist_name_tag:
            scientist_name = str(scientist_name_tag.text)
            scientists.append(scientist_name)
            scientists_links[scientist_name] = str(scientist_name_tag['href'])
            text = str(item.get_text())
            index1 = text.find("– ")
            index2 = text.find("— ")
            if index1 != -1:
                output_string = text[index1 + 2:]
                output = output_string.replace(', ', ' ')
            elif index2 != -1:
                output_string = text[index2 + 2:]
                output = output_string.replace(', ', ' ')
            else:
                output = []
            scientists_education[scientist_name] = output
            if (scientist_name == 'Konrad Zuse'):
                break



    # known bug: in the education dictionary items beggining vwith "and "
    # should have their index started on 4 in order for the "and " not to show up
    # exaple : 'Shlomo Zilberstein': ['artificial intelligence', 'anytime algorithms',
    # 'automated planning', 'and decentralized POMDPs'],

    # use the links in order to check whether there is an information box with awards
    # and then if there is count them '

    for scientist in scientists:
        url = prefix + scientists_links[scientist]
        response = requests.get(url)
        soup = bs(response.text, 'html.parser')
        award_label = soup.find('th', class_='infobox-label', string='Awards')
        if (award_label):
            award_box = award_label.parent
            li_tags = len(award_box.find_all('li'))
            br_tags = len(award_box.find_all('br')) + 1
            scientists_awards[scientist] = max(li_tags, br_tags)
        else:
            scientists_awards[scientist] = 0


    sc_ed = list(scientists_education.values())
    sc_aw = list(scientists_awards.values())
    data = list(zip(scientists, sc_aw, sc_ed))

    fields = ['Name', 'Number', 'Education']
    with open('scientists.csv', "w", newline='', encoding="utf-8") as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(data)