import requests, json, csv
from bs4 import BeautifulSoup as BS

def get_html(url):
    r = requests.get(url)

    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(r.text)

def get_href():
    with open('index.html', encoding='utf-8') as file:
        html = file.read()

    soup = BS(html, 'lxml')

    all_taxi = soup.find_all(class_='views-field views-field-field-adresse-bild')

    for taxi in all_taxi:
        href = taxi.find(class_='field-content').find('a').get('href')

        with open('index.txt', 'a', encoding='utf-8') as file:
            file.write(f'https://www.taxi-heute.de{href}\n')

def get_data():
    data = []
    count = 1

    with open('index.txt', encoding='utf-8') as file:
        hrefs = [href.strip() for href in file.readlines()]

    for i in range(0, len(hrefs)):
        r = requests.get(hrefs[i])

        soup = BS(r.content, 'lxml')

        title = soup.find(class_='field field--name-node-title field--type-ds field--label-hidden field__item').text.strip()

        try:
            street = soup.find(
                class_='field field--name-field-adresse-strasse-nr field--type-string field--label-inline clearfix').find(
                class_='field__item').text.strip().replace('.', ',')
        except Exception:
            street = None
        try:
            zip_city = soup.find(class_='field field--name-field-adresse-plz-ort field--type-string field--label-inline clearfix')\
                           .find(class_='field__item').text.strip().split(' ')
            zip_number = zip_city[0]
            city = zip_city[1]
        except Exception:
            zip_number = None
            city = None
        try:
            state = soup.find(class_='field field--name-field-adressen-bundesland field--type-entity-reference field--label-inline clearfix')\
                        .find(class_='field__item').text.strip()
        except Exception:
            state = None
        try:
            email = soup.find(class_='field field--name-field-adresse-mail field--type-email field--label-above')\
                        .find(class_='field__item').text.strip()
        except Exception:
            email = None

        data.append({
            'name': title,
            'address': {
                'street': street,
                'city': city,
                'zip': zip_number,
                'federal_state': state
            },
            'e-mail address': email
        })

        print(f'Taxi #{count} was scraped!')
        count += 1

    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def main():
    url = 'https://www.taxi-heute.de/de/adressen/kategorien/955#top'

    # get_html(url)
    # get_href()
    get_data()

if __name__ == '__main__':
    main()
