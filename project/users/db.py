import sqlite3
import logging

# making it private in the module level, but still imported with `import db`
def _connect_to_db():
    conn = sqlite3.connect('TestDatabase.db')
    cursor = conn.cursor()
    # check if the table `user` already exist, if not, create it. 
    # get the count of tables with the name
    cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='users' ''')

    #if the count is 1, then table exists
    if cursor.fetchone()[0] == 0:
        _create_db_table(conn) 

    return conn

# private in module level
def _create_db_table(conn):
    try:
        conn.execute('''
            CREATE TABLE users (
                id TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                login_date TEXT NOT NULL, 
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
        ''')

        conn.commit() # confirms transaction
        logging.info("User table created successfully")
    except Exception as e:
        logging.error(e)
        logging.info("User table creation failed")


def get_all_users():
    users = []
    try:
        conn = _connect_to_db()
        conn.row_factory = sqlite3.Row  
        # ^^ index-based and case-insensitive name based access
        # from raw tuples to objects accessible by name 
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for row in rows:
            user = {}
            user["id"] = row["id"]
            user["password"] = row["password"]
            user["email"] = row["email"]
            user["login_date"] = row["login_date"]
            user["created_at"] = row["created_at"]
            user["updated_at"] = row["updated_at"]

            users.append(user)

    except Exception as e:
        logging.error(e)
        users = None

    return users


def get_user_by_id(id):
    """placeholder for function description...

    Args:
        id (String): user ID

    Returns:
        User dictionary on success. \n
        None if user doesn't exist. 
    """
    user = {}
    try:
        conn = _connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE id = ?", 
                       (id,))
        row = cur.fetchone()

        # convert row object to dictionary
        user["id"] = row["id"]
        user["password"] = row["password"]
        user["email"] = row["email"]
        user["login_date"] = row["login_date"]
        user["created_at"] = row["created_at"]
        user["updated_at"] = row["updated_at"]
    except Exception as e:
        logging.error(e)
        user = None

    return user


def update_user(user):
    updated_user = {}
    try:
        conn = _connect_to_db()

        cur = conn.cursor()
        cur.execute("UPDATE users SET id = ?, email = ?, password = ?, login_date = ?, created_at = ?, updated_at = ? WHERE id = ? ",  
                     (user["id"], 
                     user["email"], 
                     user["password"], 
                     user["login_date"], 
                     user["created_at"], 
                     user["updated_at"],
                     user['id']))
        conn.commit()
        # confirm by returning the user 
        updated_user = get_user_by_id(user["id"])

    except Exception as e:
        logging.error(e)
        conn.rollback()
        updated_user = None
    finally:
        conn.close()

    return updated_user


# takes a dictionary, all textfields
def insert_user(user):
    inserted_user = {}
    try:
        conn = _connect_to_db()
        cur = conn.cursor()

        # check if user already exist
        cur.execute("SELECT * FROM users WHERE id = ?", (user['id'],))
        if cur.fetchone():
            return {}

        cur.execute("INSERT INTO users (id, email, password, login_date, created_at, updated_at) \
                    VALUES (?, ?, ?, ?, ?, ?)",
                    (user['id'], 
                    user['email'], 
                    user['password'],   
                    user['login_date'],
                    user['created_at'],
                    user['updated_at']))
        
        # data = [
        #     (   user['id'], 
        #         user['email'], 
        #         user['password'],   
        #         user['login_date'],
        #         user['created_at'],
        #         user['updated_at']
        #     ),
        # ]
        # cur.executemany("INSERT INTO users (id, email, password, login_date, created_at, updated_at) VALUES(?)", data)

        conn.commit()
        #print('the cur.lastrowid = {}'.format(cur.lastrowid))
        inserted_user = get_user_by_id(user['id']) # confirm we have inserted correctly. 
    except Exception as e:
        inserted_user = None
        logging.error(e)
        conn().rollback() # reverse the last commit

    finally:
        conn.close()

    return inserted_user


def delete_user(id):
    message = {}
    try:
        conn = _connect_to_db()
        conn.execute("DELETE from users WHERE id = ?",     
                      (id,))
        conn.commit()
        message["status"] = "User deleted successfully"
    except Exception as e:
        logging.error(e)
        conn.rollback()
        message["status"] = "Cannot delete user"
    finally:
        conn.close()

    return message


def reset_table():
    conn = _connect_to_db()
    conn.execute("DELETE FROM users")
    conn.commit()
    conn.execute("VACUUM")
    conn.commit()
    conn.close()
