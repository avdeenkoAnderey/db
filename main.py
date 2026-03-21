import psycopg2

class Postgres:
    def __init__(self, user, password, database, host='localhost', port=5432):
        self.user = user
        self.host = host
        self.port = port
        self.password = password
        self.database = database
    
    def postgres_execute_query(self, query, params=None):
        with psycopg2.connect(
                database=self.database,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            ) as conn:
                with conn.cursor() as cur:
                    cur.execute(query, params)
                    conn.commit()
                    try:
                        return cur.fetchall()
                    except psycopg2.ProgrammingError:
                        return None


class Clients:    
    def __init__(self, postgres):
        self.db = postgres

    def add_client(self, first_name, last_name, email, phone_number=None):
        """
        Добавляет нового клиента в таблицу clients.
        Возвращает ID добавленного клиента или None в случае ошибки.
        В случае если клиент уже существует выводим его ID.
        """
        try:
            # Проверяем, существует ли клиент с таким email
            check_query_email = "SELECT id FROM clients WHERE email =%s;"
            existing_client = self.db.postgres_execute_query(check_query_email, (email,))

            if existing_client:
                print(f"Клиент с email '{email}' уже существует, ID: {existing_client[0][0]}")
                return existing_client[0][0]

            insert_query = """
            INSERT INTO clients (first_name, last_name, email)
            VALUES (%s, %s, %s)
            RETURNING id;
            """
            result = self.db.postgres_execute_query(insert_query, (first_name, last_name, email))
            client_id = result[0][0] if result else None
            print(f"Добавлен новый клиент с ID: {client_id}")
            return client_id
        
        except Exception as e:
            print(f"Ошибка при добавлении клиента: {e}")
            return None
        
    def add_phone_to_client(self, client_id, phone_number):
        """
        Добавляет номер телефона для существующего клиента.
        """
        try:
            # Проверяем существование клиента
            check_client_query = "SELECT id FROM clients WHERE id = %s;"
            client = self.db.postgres_execute_query(check_client_query, (client_id,))
            if not client:
                print(f"Клиент с ID {client_id} не найден")
                return False

            # Проверяем, нет ли уже такого номера у клиента
            check_phone_query = """
            SELECT id FROM public.client_phones WHERE client_id = %s AND phone_number = %s;
            """
            existing_phone = self.db.postgres_execute_query(check_phone_query, (client_id,phone_number))

            if existing_phone:
                print(f"Номер телефона '{phone_number}' уже привязан к клиенту ID: {client_id}")
                return False
            
            # Добавляем номер телефона
            insert_phone = """
            INSERT INTO client_phones (client_id, phone_number)
            VALUES (%s, %s)
            """
            self.db.postgres_execute_query(insert_phone,(client_id,phone_number))
            print(f"Добавлен номер телефона '{phone_number}' для клиента ID: {client_id}")
            return True

        except Exception as e:
            print(f"Ошибка при добавлении телефона: {e}")
            return False           
            

    def update_client(self, client_id, first_name=None, last_name=None, email=None):
        """
        Можно обновить одно или несколько полей.
        """
        try:
            # Проверяем существование клиента
            check_query = "SELECT id FROM clients WHERE id = %s;"
            client = self.db.postgres_execute_query(check_query, (client_id,))
            if not client:
                print(f"Клиент с ID {client_id} не найден")
                return False

            # Формируем запрос динамически
            updates = []
            params = []

            if first_name is not None:
                updates.append("first_name = %s")
                params.append(first_name)
            if last_name is not None:
                updates.append("last_name = %s")
                params.append(last_name)
            if email is not None:
                updates.append("email = %s")
                params.append(email)

            if not updates:
                print("Не указаны поля для обновления")
                return False

            params.append(client_id)  # добавляем ID для WHERE

            update_query = f"UPDATE clients SET {', '.join(updates)} WHERE id = %s;"
            self.db.postgres_execute_query(update_query, params)
            print(f"Данные клиента ID {client_id} обновлены")
            return True

        except Exception as e:
            print(f"Ошибка при обновлении данных клиента: {e}")
            return False


    def delete_phone_from_client(self, client_id, phone_number):
        """
        Удаляет номер телефона для существующего клиента.
        """
        try:
            # Проверяем существование номера телефона у клиента
            check_query = """
            SELECT id FROM client_phones WHERE client_id = %s AND phone_number = %s;
            """
            phone = self.db.postgres_execute_query(check_query, (client_id, phone_number))
            if not phone:
                print(f"Номер '{phone_number}' не найден у клиента ID {client_id}")
                return False

            # Удаляем номер телефона
            delete_query = """
            DELETE FROM client_phones WHERE client_id = %s AND phone_number = %s;
            """
            self.db.postgres_execute_query(delete_query, (client_id, phone_number))
            print(f"Номер '{phone_number}' удалён у клиента ID {client_id}")
            return True

        except Exception as e:
            print(f"Ошибка при удалении телефона: {e}")
            return False

    def delete_client(self, client_id):
        """
        Удаляет существующего клиента и все его телефоны (благодаря ON DELETE CASCADE).
        """
        try:
            # Проверяем существование клиента
            check_query = "SELECT id FROM clients WHERE id = %s;"
            client = self.db.postgres_execute_query(check_query, (client_id,))
            if not client:
                print(f"Клиент с ID {client_id} не найден")
                return False

            # Удаляем клиента (телефоны удалятся автоматически из‑за ON DELETE CASCADE)
            delete_query = "DELETE FROM clients WHERE id = %s;"
            self.db.postgres_execute_query(delete_query, (client_id,))
            print(f"Клиент ID {client_id} удалён вместе со всеми телефонами")
            return True

        except Exception as e:
            print(f"Ошибка при удалении клиента: {e}")
            return False

    def find_client(self, first_name=None, last_name=None, email=None, phone_number=None):
        """
        Находит клиента по указанным данным.
        Может искать по имени, фамилии, email или телефону.
        Возвращает список найденных клиентов или пустой список при отсутствии результатов.
        """
        try:
            conditions = []
            params = []

            if first_name:
                conditions.append("c.first_name ILIKE %s")
                params.append(f"%{first_name}%")
            if last_name:
                conditions.append("c.last_name ILIKE %s")
                params.append(f"%{last_name}%")
            if email:
                conditions.append("c.email ILIKE %s")
                params.append(f"%{email}%")
            if phone_number:
                conditions.append("p.phone_number ILIKE %s")
                params.append(f"%{phone_number}%")

            if not conditions:
                print("Не указаны параметры для поиска")
                return []

            # Формируем запрос с JOIN для поиска по номеру телефона
            where_clause = " AND ".join(conditions)
            query = f"""
            SELECT DISTINCT c.id, c.first_name, c.last_name, c.email
            FROM clients c
            LEFT JOIN client_phones p ON c.id = p.client_id
            WHERE {where_clause}
            ORDER BY c.id;
            """

            result = self.db.postgres_execute_query(query, params)

            if result:
                print(f"Найдено клиентов: {len(result)}")
                for client in result:
                    print(f"ID: {client[0]}, Имя: {client[1]}, Фамилия: {client[2]}, Email: {client[3]}")
            else:
                print("Клиенты не найдены")

            return result

        except Exception as e:
            print(f"Ошибка при поиске клиента: {e}")
            return []        


if __name__ == '__main__':
    # Инициализация подключения
    postgres = Postgres(
        user='postgres',
        password='postgres',
        database='postgres'
    )

    # Создание таблиц
    create_clients_table = """
    DROP TABLE IF EXISTS client_phones CASCADE;
    DROP TABLE IF EXISTS clients CASCADE;
    CREATE TABLE clients (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(100) NOT NULL,
        last_name VARCHAR(100) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL
    );
    """

    create_phones_table = """
    CREATE TABLE client_phones (
        id SERIAL PRIMARY KEY,
        client_id INTEGER NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
        phone_number VARCHAR(50) NOT NULL
    );
    """

    try:
        postgres.postgres_execute_query(create_clients_table)
        postgres.postgres_execute_query(create_phones_table)
        print("Таблицы созданы успешно!")
    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")

    # Создание экземпляра Clients
    client_manager = Clients(postgres)

    # 1. Добавляем нового клиента
    print("\n1. Добавление нового клиента:")
    client_id1 = client_manager.add_client("Николай", "Петров", "ni@example.com")

    # 2. Добавляем телефон для существующего клиента
    print("\n2. Добавление телефона:")
    client_manager.add_phone_to_client(client_id1, "+7 (999) 123-45-67")

    # 3. Ищем клиента по email
    print("\n3. Поиск по email:")
    client_manager.find_client(email="ni@example.com")

    # 4. Обновляем данные клиента
    print("\n4. Обновление данных клиента:")
    client_manager.update_client(client_id1, last_name="Петров")

    # 5. Ищем клиента после обновления
    print("\n5. Поиск после обновления:")
    client_manager.find_client(last_name="Николай")

    # 6. Добавляем ещё одного клиента с телефоном
    print("\n6. Добавление второго клиента:")
    client_id2 = client_manager.add_client("Мария", "Иванова", "maria@example.com")
    client_manager.add_phone_to_client(client_id2, "+7 (888) 765-43-21")

    # 7. Ищем всех клиентов с телефоном 888
    print("\n7. Поиск по номеру телефона:")
    client_manager.find_client(phone_number="888")

    # 8. Удаляем телефон у первого клиента
    print("\n8. Удаление телефона:")
    client_manager.delete_phone_from_client(client_id1, "+7 (999) 123-45-67")

    # 9. Удаляем второго клиента
    print("\n9. Удаление клиента:")
    client_manager.delete_client(client_id2)

    # 10. Финальный поиск всех клиентов
    print("\n10. Финальный поиск всех клиентов:")
    client_manager.find_client(last_name="Петров")