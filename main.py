import shlex
import sqlite3
import os
import subprocess

import readline

from jobs import insert_command, view_command, select_command, filter_command
from update import update_app_db

#Setting Up connecion and database
connection_status = True
conn = sqlite3.connect("database/inventory.db")
with open('database/database-set-up.sql', 'r') as commands_file:
    sql_set_up_script = commands_file.read()

cursor = conn.cursor()

#Set up headers list
headers_name = []
filters_text = ""

try:
    #Making Sure table exists
    cursor.executescript(sql_set_up_script)
    conn.commit()

    #Getting Table Headers
    cursor.execute("SELECT * FROM items LIMIT 0")
    headers_name = update_app_db(
        [description[0] for description in cursor.description],
        conn,
        cursor
    )

except sqlite3.Error as e:
    print(f"Database connection error: {e}")
    connection_status = False

while connection_status:
    filters = []
    command_line_filter_text = ""
    if len(filters_text) > 0:
        command_line_filter_text = f"?{filters_text}"
        filters = filters_text.split("&")

    else:
        filters_text = ""

    user_command_text = input(f"(inventory_manager{command_line_filter_text})=> ")
    user_commands = user_command_text.split(";")
    exit_command_called = False

    for user_command in user_commands:
        user_command_split = shlex.split(f"phase {user_command}")

        #Check to see if job was given
        if len(user_command_split) < 2:
            print("No Job requested")

        #Getting job data
        job = user_command_split[1]

        try:
            if job == "insert":
                insert_command(user_command_split, cursor, conn, headers_name)

            elif job == "view":
                view_command(user_command_split, cursor, headers_name, filters)

            elif job == "select":
                select_command(user_command_split, cursor, conn, headers_name)

            elif job == "filter":
                temp_filters_text = filter_command(user_command_split, headers_name, filters)
                if isinstance(temp_filters_text, str):
                    filters_text = temp_filters_text

            elif job == "clear":
                clear_command = 'cls' if os.name == 'nt' else 'clear'
                subprocess.run(clear_command, shell=True)

            elif job == "help":
                with open("help.txt", "r", encoding="utf-8") as help_file:
                    for line in help_file:
                        print(line.strip())

            elif job == "exit" or job == "quit":
                exit_command_called = True
                conn.close()

            else:
                raise IndexError("Invaild job provided. Vaild jobs are insert, view, select, exit, quit")

        except sqlite3.Error as e:
            print(f"An error has occur with you query: {e}")

        except IndexError as e:
            print(f"Command Line error: {e}")

    if exit_command_called:
        break