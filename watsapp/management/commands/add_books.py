import requests
import re
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from watsapp.models import Case


class Command(BaseCommand):
    help = 'Добавить цены на 5000 самых свежих книг на Лабиринте'

    def handle(self, *args, **options):
        url = 'https://www.labirint.ru/books/'

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        products = soup.find_all('div', {'class': 'product'})
        count = 0

        for product in products:
            if count >= 10:
                break

            author_elem = product.find('div', {'class': 'product-author'})
            title_elem = product.find('span', {'class': 'product-title'})
            price_elem = product.find('span', {'class': 'price-val'})

            if author_elem and title_elem and price_elem:
                author = author_elem.text.strip()
                title = title_elem.text.strip()
                price = price_elem.text.replace('₽', '').replace(' ', '')

                # Создаем новый Case для каждой книги
                case = Case.objects.create(
                    name=f'Цена книги: {author} {title}',
                    url=response.url,
                    pattern=int(price),
                )

                case.save()
                count += 1

                # Печатать сообщение для каждой 200й добавленной книге
                if count % 200 == 0:
                    self.stdout.write(self.style.SUCCESS(f'Добавлено {count} книг'))

                # Вывод финального сообщения
            self.stdout.write(self.style.SUCCESS(f'Всего добавлено {count} книг.'))








