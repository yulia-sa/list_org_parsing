import sys
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate


def load_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
    }

    if not url.startswith('http'):
        return None

    response = requests.get(url, headers=headers)

    if not response.ok:
        return None

    return response.text


def get_company_data(text):
    soup = BeautifulSoup(text, 'html.parser')
    company_data = soup.find_all('div', {'class': 'c2m'})

    return company_data


def parse_data(text):
    company_info_dict = dict.fromkeys(['company_name',
                                       'chief_name',
                                       'registration_date',
                                       'status',
                                       'inn',
                                       'kpp',
                                       'ogrn'])

    general_text = text[0]
    additional_text = text[2]

    company_name = general_text.find('a', {'class': 'upper'}).text
    company_info_dict['company_name'] = company_name

    general_items = general_text.find_all('tr')
    additional_items = additional_text.find_all('p')

    for item in general_items:
        splited_item = item.text.split(':', 1)

        key = splited_item[0]
        value = splited_item[1]

        if key == 'Полное юридическое наименование':
            company_info_dict['company_name'] = value

        elif key == 'Руководитель':
            company_info_dict['chief_name'] = value
           
        elif key == 'Дата регистрации':
            company_info_dict['registration_date'] = value

        elif key == 'Статус':
            company_info_dict['status'] = value

    for item in additional_items:
        splited_item = item.text.split(':', 1)

        key = splited_item[0]
        value = splited_item[1]

        if key == 'ИНН':
            company_info_dict['inn'] = value.strip()

        elif key == 'КПП':
            company_info_dict['kpp'] = value.strip()
           
        elif key == 'ОГРН':
            company_info_dict['ogrn'] = value.strip()

    return company_info_dict


def main():
    if len(sys.argv) < 2:
        print('Не задана ссылка на страницу компании!')
    else:
        url = sys.argv[1]
        text = load_page(url)

        if text is None:
            exit('Не удалось загрузить страницу {}'.format(url))

        company_data = get_company_data(text)
        company_info_dict = parse_data(company_data)

        table = [
                    ['Полное юридическое наименование', company_info_dict['company_name']],
                    ['Руководитель', company_info_dict['chief_name']],
                    ['Дата регистрации', company_info_dict['registration_date']],
                    ['Статус', company_info_dict['status']],
                    ['ИНН', company_info_dict['inn']],
                    ['КПП', company_info_dict['kpp']],
                    ['ОГРН', company_info_dict['ogrn']]
                ]

        print(tabulate(table, tablefmt='grid'))


if __name__ == '__main__':
    main()
