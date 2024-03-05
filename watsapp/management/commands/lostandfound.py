from django.core.management.base import BaseCommand, CommandError
from watsapp.models import Case, Found, News
import re
from urllib.request import urlopen
import ssl

ssl._create_default_https_context = ssl._create_stdlib_context

class Command(BaseCommand):
    help = "Найти информацию"


    def handle(self, *args, **options):
        count = 0

        for case in Case.objects.filter(active=True): # Фильтр по галочке активности
            print(case)
            data = urlopen(case.url).read().decode('utf8')

            if case.pattern.isdigit():
                # Если паттерн = числу, используем его сразу
                text = str(case.pattern)
            else:
                # Если это регулярное выражение, используем re
                text_matches = re.findall(case.pattern, data)
                text = text_matches[0] if text_matches else ''


            old_found = Found.objects.filter(case=case).order_by('-created').first()
            if old_found:
                if old_found.text != text:
                    n = News(case=case, oldtext=old_found.text, newtext=text)
                    n.save()

            found = Found(case=case, text=text)
            found.save()

            count += 1

        self.stdout.write(
            self.style.SUCCESS('Successfully found: %s.' % count)
        )


