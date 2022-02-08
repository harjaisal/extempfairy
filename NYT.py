import requests
from bs4 import BeautifulSoup

def getTitleSource(soup):
    titleSource = soup.title.text

    titleSourceList = titleSource.split(' - ')

    return titleSourceList


def getAuthors(soup):
    authors = []

    for link in soup.find_all('a'):
        if '/by/' in link.get('href'):
            splitURL = link.get('href').split('/by/')

            names = splitURL[1].split('-')

            fullName = names[0].capitalize() + ' ' + names[1].capitalize()

            authors.append(fullName)

    authors = list(dict.fromkeys(authors))

    formattedAuthors = ''

    if len(authors) == 0:
        return 'None'
    elif len(authors) == 1:
        formattedAuthors = authors[0]
    elif len(authors) == 2:
        formattedAuthors = authors[0] + ' and ' + authors[1]
    else:
        for i in range(len(authors) - 1):
            formattedAuthors += authors[i] + ', '

        formattedAuthors += 'and ' + authors[len(authors) - 1]

    return formattedAuthors


def getDate(soup):
    date = soup.find('time')

    if date.has_attr('datetime'):
        fullDate = date['datetime']

        dateTime = fullDate.split('T')

        return dateTime[0]
    else:
        return 'None'


def getContents(soup):
    content = ''

    for section in soup.find_all('section'):
        if 'meteredContent' in section['class']:
            content = section
            break

    for section in content.find_all('section'):
        section.extract()

    for ariaElement in content.find_all():
        for key in ariaElement.attrs.keys():
            if 'aria' in key:
                ariaElement.extract()

    return content.get_text()

def getNYTArticle(url, outputName):
    outputPath = 'articles\\' + outputName + '.txt'

    html = requests.get(url).text

    soup = BeautifulSoup(html, 'html.parser')

    classes = ['script', 'meta', 'noscript', 'link', 'figure']

    for element in soup.find_all(classes):
        element.extract()

    with open(outputPath, 'w', encoding='utf-8') as file:
        text = 'Title: ' + getTitleSource(soup)[0] + '\n' + 'Source: ' + getTitleSource(soup)[
            1] + '\n' + 'Authors: ' + getAuthors(soup) + '\n' + 'Date: ' + getDate(soup) + '\n' + '\n' + getContents(soup)

        file.write(text)