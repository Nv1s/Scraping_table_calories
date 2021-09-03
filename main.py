from bs4 import BeautifulSoup
import requests
import json
import csv


# url = 'https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie'
# req = requests.get(url)
# src = req.text
#
# with open('try.html', 'w', encoding='utf-8') as file:
#     file.write(src)

# with open('try.html', encoding='utf-8') as file:
#     src = file.read()
#
# soup = BeautifulSoup(src, 'lxml')
# find_a = soup.find_all(class_='mzr-tc-group-item-href')
#
#
# all_cat = {}
# for item in find_a:
#     text = item.text
#     href = 'https://health-diet.ru' + item.get('href')
#     all_cat[text] = href
#
# with open("all_cat.json", 'w') as file:
#     json.dump(all_cat, file, indent=4, ensure_ascii=False)

with open("all_cat.json") as file:
    all_cat = json.load(file)

iter_count = int(len(all_cat)) - 1
count = 0
print(f'Всего иттераций: {iter_count}')
for category_name, category_href in all_cat.items():

    rep = [',', ' ', ', ', '-', "'"]
    for i in rep:
        if i in category_name:
            category_name = category_name.replace(i, '_')
    req = requests.get(url=category_href)
    src = req.text

    with open(f'data/{count}_{category_name}.html', 'w', encoding='utf-8') as file:
        file.write(src)

    with open(f'data/{count}_{category_name}.html', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    # проверка наличии таблицы

    alert = soup.find(class_='uk-alert-danger')
    if alert is not None:
        continue

    # заголовки таблиицы
    table = soup.find(class_='mzr-tc-group-table').find('tr').find_all('th')
    product = table[0].text
    calories = table[1].text
    proteins = table[2].text
    fats = table[3].text
    carbohydrates = table[4].text

    with open(f'data/{count}_{category_name}.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                product,
                calories,
                proteins,
                fats,
                carbohydrates
            )
        )


    # данные продуктов
    products_data = soup.find(class_='mzr-tc-group-table').find('tbody').find_all('tr')
    product_info = []
    for i in products_data:
        products_td = i.find_all('td')
        title = products_td[0].find('a').text
        calories = products_td[1].text
        proteins = products_td[2].text
        fats = products_td[3].text
        carbohydrates = products_td[4].text

        product_info.append(
            {
                'Title': title,
                'Calories': calories,
                'Proteins': proteins,
                'Fats': fats,
                'Carbohydrates': carbohydrates
            }
        )

        with open(f'data/{count}_{category_name}.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    title,
                    calories,
                    proteins,
                    fats,
                    carbohydrates
                )
            )

        with open(f'data/{count}_{category_name}.json', 'a', encoding='utf-8') as file:
            json.dump(product_info, file, indent=4, ensure_ascii=False)


    count += 1
    print(f'# Итерация {count}. {category_name} записан... ')

    if iter_count == 0:
        print('Работа закончена')
        break

    iter_count -= 1
    print(f'Осталось итераций: {iter_count}')