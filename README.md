Личный блог для 1 человека. Желательно создать всего 4 категории(т.к под них он и сделан). В админ панели установлен редактор теста Ckeditor. 
Стэк: Python, JS, Html&Css, Django, SQLite
Шаги для запуска CMD:
1. mkdir SelfBlog
2. cd SelfBlog
3. git clone git@github.com:Bogd4nB1/SelfBlog.git
4. python -m venv venv
5. venv\Scripts\activate
6. cd SelfBlog
7. pip install -r requirements.txt
8. python manage.py makemigrations
9. python manage.py migrate
10. python manage.py createsuperuser
11. python manage.py runserver
