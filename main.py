import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Book, Publisher, Shop, Stock, Sale
from sqlalchemy import or_

DSN = 'postgresql://postgres:OkMa79088325@localhost:5432/ORMSQL'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)
Session = sessionmaker(bind=engine)
session = Session()

publisher1 = Publisher(name="Доусон")
publisher2 = Publisher(name="Бхаргава")
publisher3 = Publisher(name="Лутц")
session.add_all([publisher1, publisher2, publisher3])
session.commit()
# print(publisher1.id)
# print(publisher1)

book1 = Book(title="Программируем на Python", publisher=publisher1)
book2 = Book(title="Грокаем алгоритмы", publisher=publisher2)
book3 = Book(title="Изучаем Python", publisher=publisher3)
session.add_all([book1, book2, book3])
session.commit()

shop1 = Shop(name="Labirint")
shop2 = Shop(name="Bookbridge")
shop3 = Shop(name="MDK")
session.add_all([shop1, shop2, shop3])
session.commit()

stock1 = Stock(book=book1, shop=shop1, count=3)
stock2 = Stock(book=book2, shop=shop2, count=5)
stock3 = Stock(book=book3, shop=shop3, count=8)
stock4 = Stock(book=book2, shop=shop1, count=4)
stock5 = Stock(book=book1, shop=shop3, count=9)
session.add_all([stock1, stock2, stock3])
session.commit()

sale1 = Sale(price=500, date_sale='20-09-2022', stock=stock3, count=2)
sale2 = Sale(price=700, date_sale='21-10-2022', stock=stock2, count=4)
sale3 = Sale(price=900, date_sale='23-11-2022', stock=stock1, count=1)
sale4 = Sale(price=850, date_sale='25-09-2022', stock=stock4, count=3)
sale5 = Sale(price=997, date_sale='01-10-2022', stock=stock5, count=8)

session.add_all([stock1, stock2, stock3])
session.commit()

"""Задание 2. Чтобы определить в каких магазинах продаются книги данного издателя, 
    необходимо ввести, если известен, его идентификатор, а на запрос ввода имени, пропустить, нажав ENTER,
    если неизвестен идентификатор, то поиск осуществляем по фамилии автора, 
    а на просьбу ввести идентификатор издателя проставляем 0"""


for name in session.query(Shop).join(Stock, Shop.id == Stock.id_shop). \
        join(Book, Stock.id_book == Book.id). \
        join(Publisher, Book.id_publisher == Publisher.id). \
        where(or_(Publisher.name == input("Введите имя издателя "),
                  Publisher.id == input("Введите идентификатор издателя "))).all():
    print(f"Книги этого издателя имеются в продаже в магазине {name}")



session.close()
