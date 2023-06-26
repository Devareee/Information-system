import psycopg


class Postgres:
    def get_socialstatuses(self):
        with self.connection.cursor() as cur:
            cur.execute('''
                SELECT * FROM social_statuses
            ''')
            return cur.fetchall()

    def get_cities(self):
        with self.connection.cursor() as cur:
            cur.execute('''
                SELECT * FROM cities
            ''')
            return cur.fetchall()

    def get_insurancetypes(self):
        with self.connection.cursor() as cur:
            cur.execute('''
                SELECT * FROM insurance_types
            ''')
            return cur.fetchall()

    def get_companytypes(self):
        with self.connection.cursor() as cur:
            cur.execute('''
                SELECT * FROM company_types
            ''')
            return cur.fetchall()

    def get_companies(self):
        with self.connection.cursor() as cur:
            cur.execute('''
                SELECT co.id, co.name, ct.type, co.year, c.city, co.phone
                FROM companies co
                LEFT JOIN cities c ON c.id=co.city_id
                LEFT JOIN company_types ct ON co.company_type_id=ct.id
            ''')
            return cur.fetchall()

    def get_branches(self):
        with self.connection.cursor() as cur:
            cur.execute('''
                SELECT b.id, co.name, b.name, c.city, b.address, b.phone, b.workers_count
                FROM branches b
                LEFT JOIN cities c ON c.id=b.city_id
                LEFT JOIN companies co ON b.company_id=co.id
            ''')
            return cur.fetchall()

    def get_all_clients(self):
        with self.connection.cursor() as cur:
            cur.execute('''
                SELECT c.id, c.name, c.date, s.status, c.phone
                FROM clients c
                LEFT JOIN social_statuses s ON s.id=c.social_status_id
            ''')
            return cur.fetchall()

    def get_all_contracts(self):
        with self.connection.cursor() as cur:
            cur.execute('''
                SELECT co.id, b.name, c.name, i.type, co.sum, co.date
                FROM contracts co
                LEFT JOIN branches b ON co.branch_id=b.id
                LEFT JOIN clients c ON co.client_id=c.id
                LEFT JOIN insurance_types i ON co.insurance_type_id=i.id
            ''')
            return cur.fetchall()

    def get_users(self):
        with self.connection.cursor() as cur:
            cur.execute('''
                SELECT * FROM users
            ''')
            return cur.fetchall()      

    def get_branch(self):
        with self.connection.cursor() as cur:
            cur.execute('''
                SELECT co.name, b.name, c.city, b.address, b.phone, b.workers_count
                FROM branches b
                LEFT JOIN cities c ON c.id=b.city_id
                LEFT JOIN companies co ON b.company_id=co.id
            ''')
            return cur.fetchone()

    def get_contracts(self):
        with self.connection.cursor() as cur:
            cur.execute('''
                SELECT co.id, c.name, i.type, co.sum, co.date
                FROM contracts co
                LEFT JOIN clients c ON co.client_id=c.id
                LEFT JOIN insurance_types i ON co.insurance_type_id=i.id
            ''')
            return cur.fetchall()

    def get_client_by_id(self, client_id):
        with self.connection.cursor() as cur:
            cur.execute(f'''
                SELECT c.name, c.date, s.status, c.phone
                FROM clients c
                LEFT JOIN social_statuses s ON s.id=c.social_status_id
                WHERE c.id={client_id}
            ''')
            return cur.fetchone()
        
    def get_contracts_by_client_id2(self, client_id):
        with self.connection.cursor() as cur:
            cur.execute(f'''
                SELECT co.id, b.name, i.type, co.sum, co.date
                FROM contracts co
                LEFT JOIN branches b ON co.branch_id=b.id
                LEFT JOIN insurance_types i ON co.insurance_type_id=i.id
                WHERE co.client_id={client_id}
            ''')
            return cur.fetchall()

    def get_contracts_by_client_id(self, client_id):
        with self.connection.cursor() as cur:
            cur.execute(f'''
                SELECT co.id, i.type, co.sum, co.date
                FROM contracts co
                LEFT JOIN insurance_types i ON co.insurance_type_id=i.id
                WHERE co.client_id={client_id}
            ''')
            return cur.fetchall()

    def connect(self, login, password):
        self.connection = psycopg.connect(f'host=127.0.0.1 dbname=postgres user={login} password={password}')
    
    def check_role(self):
        with self.connection.cursor() as cur:
            try:
                role = 'branch_employees'
                cur.execute(f'SET ROLE {role}')
                return role
            except:
                self.connection.rollback()
            
            try:
                role = 'clients_role'
                cur.execute(f'SET ROLE {role}')
                return role
            except:
                self.connection.rollback()

            try:
                role = 'queries_role'
                cur.execute(f'SET ROLE {role}')
                return role
            except:
                self.connection.rollback()

            role = 'admins'
            cur.execute(f'SET ROLE {role}')
            return role
    
    def reset_role(self):
        with self.connection.cursor() as cur:
            cur.execute('RESET ROLE')

    def drop_user(self, user):
        with self.connection.cursor() as cur:
            cur.execute(f"DELETE FROM users WHERE login='{user}'")
            self.connection.commit()

    def get_user_role(self, login):
        with self.connection.cursor() as cur:
            cur.execute(f"SELECT role FROM users WHERE login='{login}'")
            return cur.fetchone()[0]

    def create_user(self, login, password, role, branch_id):
        with self.connection.cursor() as cur:
            cur.execute(f"CREATE USER {login} PASSWORD '{password}'")
            cur.execute(f'''
                INSERT INTO users
                VALUES ('{login}', {branch_id}, '{role}')
            ''')
            self.connection.commit()

    def get_field_by_id(self, id, field, table):
        with self.connection.cursor() as cur:
            cur.execute(f'SELECT {field} FROM {table} WHERE id={id}')
            return cur.fetchone()[0]

    def update_values(self, values, id, table):
        with self.connection.cursor() as cur:
            cur.execute(f'UPDATE {table} SET {values} WHERE id={id}')
            self.connection.commit()

    def select_contracts_where(self, branch=None, client=None, insurance_type=None, sum=None, date=None):
        values = []
        if branch: values.append(f"b.name LIKE '%{branch}%'")
        if client: values.append(f"c.name LIKE '%{client}%'")
        if insurance_type: values.append(f"i.type='{insurance_type}'")
        if sum: values.append(f'co.sum={sum}')
        if date: values.append(f'co.date={date}')
        where = ' AND '.join(values)
        with self.connection.cursor() as cur:
            cur.execute(f'''
                SELECT co.id, b.name, c.name, i.type, co.sum, co.date
                FROM contracts co
                LEFT JOIN branches b ON b.id=co.branch_id
                LEFT JOIN clients c ON c.id=co.client_id
                LEFT JOIN insurance_types i ON i.id=co.insurance_type_id
                WHERE {where}
            ''')
            return cur.fetchall()    

    def select_contracts_where2(self, branch=None, insurance_type=None, sum=None, date=None):
        values = []
        if branch: values.append(f"b.name LIKE '%{branch}%'")
        if insurance_type: values.append(f"i.type='{insurance_type}'")
        if sum: values.append(f'co.sum={sum}')
        if date: values.append(f'co.date={date}')
        where = ' AND '.join(values)
        print(where)
        with self.connection.cursor() as cur:
            cur.execute(f'''
                SELECT b.name, i.type, co.sum, co.date
                FROM contracts co
                LEFT JOIN branches b ON b.id=co.branch_id
                LEFT JOIN insurance_types i ON i.id=co.insurance_type_id
                WHERE {where}
            ''')
            return cur.fetchall()    

    def select_contracts_where3(self, client=None, insurance_type=None, sum=None, date=None):
            values = []
            if client: values.append(f"c.name LIKE '%{client}%'")
            if insurance_type: values.append(f"i.type='{insurance_type}'")
            if sum: values.append(f'co.sum={sum}')
            if date: values.append(f'co.date={date}')
            where = ' AND '.join(values)
            with self.connection.cursor() as cur:
                cur.execute(f'''
                    SELECT co.id, c.name, i.type, co.sum, co.date
                    FROM contracts co
                    LEFT JOIN clients c ON c.id=co.client_id
                    LEFT JOIN insurance_types i ON i.id=co.insurance_type_id
                    WHERE {where}
                ''')
                return cur.fetchall() 

    def select_clients_where(self, name=None, date=None, social_status=None, phone=None):
        values = []
        if name: values.append(f"c.name LIKE '%{name}%'")
        if date: values.append(f'c.date={date}')
        if social_status: values.append(f"s.status LIKE '%{social_status}%'")
        if phone: values.append(f"c.phone='{phone}'")
        where = ' AND '.join(values)
        with self.connection.cursor() as cur:
            cur.execute(f'''
                SELECT c.id, c.name, c.date, s.status, c.phone
                FROM clients c
                LEFT JOIN social_statuses s ON s.id=c.social_status_id
                WHERE {where}
            ''')
            return cur.fetchall()        

    def select_companies_where(self, name=None, company_type=None, year=None, city=None, phone=None):
        values = []
        if name: values.append(f"co.name LIKE '%{name}%'")
        if company_type: values.append(f"ct.type LIKE '%{company_type}%'")
        if year: values.append(f"co.year='{year}'")
        if city: values.append(f'c.city={city}')
        if phone: values.append(f'co.phone={phone}')
        where = ' AND '.join(values)
        with self.connection.cursor() as cur:
            cur.execute(f'''
                SELECT co.id, co.name, ct.type, co.year, c.city, co.phone
                FROM companies co
                LEFT JOIN company_types ct ON ct.id=co.company_type_id
                LEFT JOIN cities c ON c.id=co.city_id
                WHERE {where}
            ''')
            return cur.fetchall()        

    def select_branches_where(self, company=None, name=None, city=None, address=None, phone=None, workers_count=None):
        values = []
        if company: values.append(f"co.name LIKE '%{company}%'")
        if name: values.append(f"b.name LIKE '%{name}%'")
        if city: values.append(f"c.city='{city}'")
        if address: values.append(f'b.address={address}')
        if phone: values.append(f'b.phone={phone}')
        if workers_count: values.append(f'b.workers_count={workers_count}')
        where = ' AND '.join(values)
        with self.connection.cursor() as cur:
            cur.execute(f'''
                SELECT b.id, co.name, b.name, c.city, b.address, b.phone, b.workers_count
                FROM branches b
                LEFT JOIN companies co ON co.id=b.company_id
                LEFT JOIN cities c ON c.id=b.city_id
                WHERE {where}
            ''')
            return cur.fetchall()        

    def get_id_field(self, field, table):
        with self.connection.cursor() as cur:
            cur.execute(f'SELECT id, {field} FROM {table}')
            return cur.fetchall()

    def insert_values(self, values, table):
        if table == 'exhibits':
            values += f', {self.get_company_id()}'
        with self.connection.cursor() as cur:
            cur.execute(f'INSERT INTO {table} VALUES (DEFAULT, {values})')
            self.connection.commit()

    def delete_by_id(self, id, table):
        with self.connection.cursor() as cur:
            cur.execute(f'DELETE FROM {table} WHERE id={id}')
            self.connection.commit()     
                
    def rollback(self):
        self.connection.rollback()

    def get_all(self, from_):
        with self.connection.cursor() as cur:
            cur.execute(f'''
                SELECT * FROM {from_}
            ''')
            return cur.fetchall()

    def get_column_names(self, from_):
        with self.connection.cursor() as cur:
            cur.execute(f'SELECT * FROM {from_} WHERE FALSE')
            return [desc[0] for desc in cur.description]

    def get_id(self, field, value, table):
            with self.connection.cursor() as cur:
                cur.execute(f"SELECT id FROM {table} WHERE {field} LIKE '%{value}%'")
                return cur.fetchone()