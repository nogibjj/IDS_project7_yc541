import sqlite3

def connect_db():
    return sqlite3.connect('mydatabase.db')

def create_table():
    with connect_db() as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)''')
        conn.commit()

def add_user(name):
    with connect_db() as conn:
        c = conn.cursor()
        c.execute("INSERT INTO users (name) VALUES (?)", (name,))
        conn.commit()

def list_users():
    with connect_db() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users")
        return c.fetchall()

def update_user_name(user_id, new_name):
    with connect_db() as conn:
        c = conn.cursor()
        c.execute("UPDATE users SET name=? WHERE id=?", (new_name, user_id))
        conn.commit()

def delete_user(user_id):
    with connect_db() as conn:
        c = conn.cursor()
        c.execute("DELETE FROM users WHERE id=?", (user_id,))
        conn.commit()

def find_user_by_name(name):
    with connect_db() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE name LIKE ?", ('%' + name + '%',))
        return c.fetchall()

def main():
    import argparse

    parser = argparse.ArgumentParser(description="A tool to manage users in a database.")
    parser.add_argument('--add', help="Add a new user", action="store")
    parser.add_argument('--list', help="List all users", action="store_true")
    parser.add_argument('--update', nargs=2, metavar=('ID', 'NEW_NAME'), help="Update a user's name based on ID")
    parser.add_argument('--delete', metavar='ID', help="Delete a user based on ID", action="store")
    parser.add_argument('--find', metavar='NAME', help="Find a user by name", action="store")

    args = parser.parse_args()

    if args.add:
        add_user(args.add)
        print(f"Added user {args.add}")

    elif args.list:
        users = list_users()
        for user in users:
            print(user)

    elif args.update:
        update_user_name(args.update[0], args.update[1])
        print(f"Updated user ID {args.update[0]} to name {args.update[1]}")

    elif args.delete:
        delete_user(args.delete)
        print(f"Deleted user with ID {args.delete}")

    elif args.find:
        users = find_user_by_name(args.find)
        for user in users:
            print(user)

if __name__ == '__main__':
    main()
