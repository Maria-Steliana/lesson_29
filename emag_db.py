import json
import psycopg2 as ps


def read_config(path: str = "config.json"):
    with open(path, "r") as f:
        config = json.loads(f.read())
    return config


def read_admins(config: dict, table: str = "emag.emag_admin"):

    with ps.connect(**config) as conn: # doua withstatemnts necesare pt citirea bazei de date
        with conn.cursor() as cursor:
            sql_query = f"select * from {table}"
            cursor.execute(sql_query)
            users = cursor.fetchone()
            return users


def read_products(config: dict, table: str = "emag.products"):
    with ps.connect(**config) as conn:
        with conn.cursor() as cursor:
            sql_query = f"select name, store, price from {table}"
            cursor.execute(sql_query)
            products = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            products_list = []
            for item in products:
                products_list.append(dict(zip(columns, item)))
            print(products_list)
            return products_list


def add_product(config: dict, product: dict, table: str = "emag.products"):
    with ps.connect(**config) as conn:
        with conn.cursor() as cursor:
            sql_query = f"INSERT INTO {table} (name, store, price) VALUES (%s, %s, %s)"
            cursor.execute(sql_query, (product['name'], product['store'], product['price']))
            conn.commit() # confirma modificarile in baza de date


if __name__ == '__main__':
    config = read_config()
    admins = read_admins(config)

    products = read_products(config)
    new_prod = input("Enter all data about product: name/store/price -> ")
    new_prod = new_prod.split("/")
    new_prod = {"name": new_prod[0], "store": new_prod[1], "price": (new_prod[2])}
    if new_prod['name'] not in [prod['name'] for prod in products]:
        add_product(config, new_prod)


