from db import connect_db
# 03 Переименование товара
# Запросите ID и новое имя. Отсекайте пустой ввод до запроса. Покажите, найден ли товар. 
# Проверьте, что цена и остаток не изменились.

# Создаем функцию для вызова ID
def read_int(variable):
    while True:
        text = input(variable)
        try:
            value = int(text)
        except ValueError:
            print("Введите целое число")
            continue
        return value

# Создаем функцию для проверки пустого ввода
def read_non_empty(check):
    while True:
        text = input(check).strip()
        if text:
            return text
        print("Ввод не должен быть пустым!")

# Создаем функцию переименования продукта
def rename_product():
    product_id = read_int("ID товара: ")

# Сначала вызываем продукт с ценой и наличием
    sql_select = """
        SELECT name, price, stock 
        FROM terminal_products 
        WHERE id = %s;
    """
# Теперь устанавливаем новое имя для вызываемого ID 

    sql_update = """
        UPDATE terminal_products
        SET name = %s
        WHERE id =%s;
    """
# Вызываем функцию connect_db и связываем с БД
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute(sql_select, (product_id, ))
# нам необходима только одна строка, поэтому используем fetchone
            row = cur.fetchone()
# с проверкой вытаскиваем текущее название продукта
            if row is None:
                print("Товар не найден!")
                return
            print(f"Текущее наименование товара: {row['name']}")  
#  после уточнения текущего названия продукта, предлагается ввести новое имя продукта
            new_name = read_non_empty("Новое наименование товара: ")   
# здесь происходит выполнение изменения названия продукта
            cur.execute(sql_update, (new_name, product_id))
            row_save = cur.rowcount 
            if row_save == 0:
                print("Ошибка: Изменения не были применены базой данных (строка не обновлена).")
                return
# выполняем commit чтобы передавалось изменение в NEON DB
            conn.commit() 
# выполняем вызов строки уже с новым наименованием 
            cur.execute(sql_select, (product_id, ))
            row_after = cur.fetchone()
            
# проверяем, что цена и наличие остались прежними, а изменилось только наименование
    if row["price"] == row_after["price"] and row["stock"] == row_after["stock"]:
        print("Проверка пройдена: цена и остаток не изменились.")
        print(f"Старое наименование товара: {row['name']} | Новое наименование товара: {new_name}")  
        print(f"Успешное переименование продукта: {row_save}")
        
    else:
        print("Ошибка! Цена или остаток изменились в процессе обновления.")

if __name__ == "__main__":        
    rename_product()
