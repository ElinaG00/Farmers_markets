import psycopg
#from psycopg import sql

conn = psycopg.connect(dbname="farmers_markets",
                      host="localhost",
                      user="postgres",
                      password="Astana3102",
                      port="5432")

cur = conn.cursor()

with open('C:/Users/User/test/markets.csv', 'r') as f:
    with cur.copy("COPY markets (FMID, market_name, website, facebook, twitter, youtube, other_media) FROM STDIN WITH (FORMAT csv)") as copy:
        while data := f.read(1000000):  # Читаем файл частями
            copy.write(data)
    
with open('C:/Users/User/test/states.csv', 'r') as f:
    with cur.copy("COPY states (state_id, state_full) FROM STDIN WITH (FORMAT csv)") as copy:
        while data := f.read(1000000):  # Читаем файл частями
            copy.write(data)

with open('C:/Users/User/test/county.csv', 'r') as f:
    with cur.copy("COPY county (county_id, county_full) FROM STDIN WITH (FORMAT csv)") as copy:
        while data := f.read(1000000):  # Читаем файл частями
            copy.write(data)

with open('C:/Users/User/test/address_market.csv', 'r') as f:
    with cur.copy("COPY address_market (FMID, street, county_id, states_id, zip) FROM STDIN WITH (FORMAT csv)") as copy:
        while data := f.read(1000000):  # Читаем файл частями
            copy.write(data)

with open('C:/Users/User/test/pay.csv', 'r') as f:
    with cur.copy("COPY pay (pay_id, name_of_pay) FROM STDIN WITH (FORMAT csv)") as copy:
        while data := f.read(1000000):  # Читаем файл частями
            copy.write(data)


with open('C:/Users/User/test/markets_pay.csv', 'r') as f:
    with cur.copy("COPY markets_pay (markets_pay_id, FMID, pay_id) FROM STDIN WITH (FORMAT csv)") as copy:
        while data := f.read(10000):  # Читаем файл частями
            copy.write(data)

with open('C:/Users/User/test/categorias.csv', 'r') as f:
    with cur.copy("COPY categorias (categorias_id, categorias_name) FROM STDIN WITH (FORMAT csv)") as copy:
        while data := f.read(10000):  # Читаем файл частями
            copy.write(data)

with open('C:/Users/User/test/market_categories.csv', 'r') as f:
    with cur.copy("COPY market_categories (market_categories_id, FMID, categorias_id) FROM STDIN WITH (FORMAT csv)") as copy:
        while data := f.read(10000):  # Читаем файл частями
            copy.write(data)




def display_menu():
    print("\nДобро пожаловать в приложение! Выберите пункт меню:")
    print("1 - Просмотр всех фермерских магазинов по названию")
    print("2 - Просмотр всех веб-станиц магазинов")
    print("3 - Поиск магазина по адресу (улица и штат)")
    print("4 - Поиск магазина по индексу и графству")
    print("5 - Просмотр категорий товаров по названию магазина")
    print("6 - Поиск магазина по категории товаров")
    print("0 - Выход")

def display_all_markets(cur):
    try:
        cur.execute("""
            SELECT market_name FROM markets ORDER BY market_name
        """)
        markets = cur.fetchall()
        print("\nСписок всех фермерских рынков:")
        for idx, market in enumerate(markets, 1):
            print(f"{idx}. {market[0]}")
    except Exception as e:
        print(f"Ошибка при получении списка рынков: {e}")

def display_all_websites(cur):
    try:
        cur.execute("""
            SELECT market_name, website FROM markets 
            WHERE website IS NOT NULL ORDER BY market_name
        """)
        websites = cur.fetchall()
        print("\nСписок веб-сайтов рынков:")
        for idx, (name, url) in enumerate(websites, 1):
            print(f"{idx}. {name}: {url}")
    except Exception as e:
        print(f"Ошибка при получении списка сайтов: {e}")

def search_by_address(cur):
    street = input("Введите улицу: ").strip()
    state = input("Введите штат: ").strip()
    
    try:
        query = """
            SELECT 
                m.market_name, a.street, s.state_full, c.county_full
            FROM 
                markets m
            JOIN address_market a ON m.FMID = a.FMID
            JOIN states s ON a.states_id = s.state_id
            JOIN county c ON a.county_id = c.county_id
            WHERE 
                a.street ILIKE %s AND s.state_full ILIKE %s
            ORDER BY m.market_name
        """
        cur.execute(query, [f'%{street}%', f'%{state}%'])
        
        results = cur.fetchall()
        if not results:
            print("\nРынков по указанному адресу не найдено.")
            return
            
        print("\nРезультаты поиска по адресу:")
        for idx, (name, street, state, county) in enumerate(results, 1):
            print(f"{idx}. {name}")
            print(f"   Адрес: {street}, {county}, {state}")
    except Exception as e:
        print(f"Ошибка при поиске по адресу: {e}")

def search_by_address_2(cur):
    index = input("Введите индекс: ").strip()
    county = input("Введите название графства: ").strip()
    
    try:
        query = """
            SELECT 
                m.market_name, a.zip, s.state_full, c.county_full
            FROM 
                markets m
            JOIN address_market a ON m.FMID = a.FMID
            JOIN states s ON a.states_id = s.state_id
            JOIN county c ON a.county_id = c.county_id
            WHERE 
                a.zip ILIKE %s AND c.county_full ILIKE %s
            ORDER BY m.market_name
        """
        cur.execute(query, [f'%{index}%', f'%{county}%'])
        
        results = cur.fetchall()
        if not results:
            print("\nРынков по указанному индексу и графству не найдено.")
            return
            
        print("\nРезультаты поиска по адресу:")
        for idx, (name, index, state, county) in enumerate(results, 1):
            print(f"{idx}. {name}")
            print(f"   Адрес: {index}, {county}, {state}")
    except Exception as e:
        print(f"Ошибка при поиске по адресу: {e}")

def get_categories_by_market(cur):
    market_name = input("Введите название рынка: ").strip()
    
    try:
        query = """
            SELECT 
                m.market_name, cat.categorias_name
            FROM 
                markets m
            JOIN market_categories mc ON m.FMID = mc.FMID
            JOIN categorias cat ON mc.categorias_id = cat.categorias_id
            WHERE 
                m.market_name ILIKE %s
            ORDER BY m.market_name, cat.categorias_name
        """
        cur.execute(query, [f'%{market_name}%'])
        
        results = cur.fetchall()
        if not results:
            print("\nРынков с указанным названием не найдено.")
            return
            
        current_market = None
        print("\nКатегории товаров:")
        for market, category in results:
            if market != current_market:
                print(f"\n{market}:")
                current_market = market
            print(f" - {category}")
    except Exception as e:
        print(f"Ошибка при получении категорий: {e}")

def get_market_by_categories(cur):
    categories_input = input("Введите точные названия категорий через запятую: ").strip()
    categories = [cat.strip() for cat in categories_input.split(',')]
    
    if not categories:
        print("Не указаны категории для поиска.")
        return
    
    try:
        query = """
            SELECT 
                m.market_name, a.street, c.county_full, s.state_full
            FROM 
                markets m
            JOIN address_market a ON m.FMID = a.FMID
            JOIN county c ON a.county_id = c.county_id
            JOIN states s ON a.states_id = s.state_id
            WHERE m.FMID IN (
                SELECT mc.FMID
                FROM market_categories mc
                JOIN categorias cat ON mc.categorias_id = cat.categorias_id
                WHERE cat.categorias_name = ANY(%s)
                GROUP BY mc.FMID
                HAVING COUNT(DISTINCT cat.categorias_id) = %s
            )
            ORDER BY m.market_name
        """
        
        cur.execute(query, (categories, len(categories)))
        results = cur.fetchall()
        
        if not results:
            print(f"\nРынков со всеми категориями ({', '.join(categories)}) не найдено.")
            return
            
        print(f"\nРынки со всеми категориями ({', '.join(categories)}):")
        for idx, (name, street, county, state) in enumerate(results, 1):
            print(f"{idx}. {name}")
            print(f"   Адрес: {street}, {county}, {state}")
            
    except Exception as e:
        print(f"Ошибка при поиске по категориям: {e}")

while True:
    display_menu()
    choice = input("Ваш выбор: ").strip()
        
    if choice == "0":
        print("Выход из программы.")
        break
    elif choice == "1":
        display_all_markets(cur)
    elif choice == "2":
        display_all_websites(cur)
    elif choice == "3":
        search_by_address(cur)
    elif choice == "4":
        search_by_address_2(cur)
    elif choice == "5":
        get_categories_by_market(cur)
    elif choice == "6":
        get_market_by_categories(cur)
    else:
        print("Неверный ввод. Пожалуйста, выберите пункт меню от 0 до 6.")
        
    input("\nНажмите Enter для продолжения...")
    
conn.close()
