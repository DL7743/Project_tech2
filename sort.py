from db import connect_db
# 02 Сортировка каталога
# Добавьте сортировку по цене в обе стороны и по остатку от большего к меньшему. 
# При равных значениях сравнивайте ID. 
# Проверьте неверный пункт: он не должен отправлять запрос.

def sorted_catalog():
    choice = input("1 - дешевле | 2 - дороже | 3 - больше в наличии: ")
    orders = {
        "1": "price ASC, id", 
        "2": "price DESC, id",
        "3": "stock DESC, id"
        }
    order = orders.get(choice)
    if order is None:
        print("Неизвестный вариант")
        return

    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, price, stock " 
                        "FROM terminal_products ORDER BY " + order)
            rows = cur.fetchall()

    for row in rows:
        print(row["id"], row["name"], row["price"], row["stock"])        

sorted_catalog()