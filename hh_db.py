import sqlite3

conn = sqlite3.connect('hh_database')
cursor = conn.cursor()


def create_database():
    cursor.execute('DROP TABLE IF EXISTS company')
    cursor.execute('DROP TABLE IF EXISTS vacancy')
    cursor.execute('''
            CREATE TABLE company(
              id INTEGER PRIMARY KEY,
              title VARCHAR(200),
              is_trusted BOOL,
              is_hr_badge BOOL
          );

            ''')

    cursor.execute('''
          CREATE TABLE vacancy(
              id INTEGER PRIMARY KEY,
              title VARCHAR(200),
              salary VARCHAR(200),
              experience VARCHAR(200),
              employ_mode VARCHAR(200),
              parttime_opt VARCHAR(200),
              temp_opt VARCHAR(200),
              is_remote BOOLEAN,
              is_resume BOOLEAN,
              address VARCHAR(200),
              company_id INTEGER,
              FOREIGN KEY (company_id) REFERENCES company(id)
          );
            ''')

    conn.commit()


def insert_companies(companies):
    sql = 'insert into company values'
    counter = 0
    for company in companies:
        sql += '(' + str(counter) + ', \'' + company + '\',' + \
            str(companies[company]['is_trusted']) + ',' + \
            str(companies[company]['is_hr_brand']) + ')'
        sql += ',' if company != list(companies)[-1] else ';'
        counter += 1
    cursor.execute(sql)
    conn.commit()


def insert_jobs(jobs, companies):
    sql = 'insert into vacancy values'
    counter = 0
    for job in jobs:
        sql += '(' + str(counter) + ', \'' + str(job['title']) + '\','

        sql += '\'' + job['salary'] + '\'' if job['salary'] != None else 'NULL'
        sql += ','

        sql += ('\'' + job['experience'] +
                '\'') if job['experience'] != None else 'NULL'
        sql += ','

        sql += ('\'' + job['employ_mode'] +
                '\'') if job['employ_mode'] != None else 'NULL'
        sql += ','

        sql += ('\'' + job['parttime_options'] +
                '\'') if job['parttime_options'] != None else 'NULL'
        sql += ','

        sql += ('\'' + job['temp_options'] +
                '\'') if job['temp_options'] != None else 'NULL'
        sql += ','

        sql += str(job['is_remote'])
        sql += ','

        sql += str(job['is_resume'])
        sql += ','

        sql += ('\'' + job['full_address'] +
                '\'') if job['full_address'] != None else '\'Алматы\''
        sql += ','

        sql += str(list(companies.keys()).index(job['company_title']))

        sql += '),' if job != jobs[-1] else ');'
        counter += 1
    cursor.execute(sql)
    conn.commit()


def select_companies():
    cursor.execute('SELECT * FROM company')
    print(cursor.fetchall())
    conn.commit()


def select_jobs():
    cursor.execute('SELECT * FROM vacancy')
    print(cursor.fetchall())
    conn.commit()


def close_connection():
    conn.close()
