# /usr/bin/python3
from configparser import ConfigParser
from os import name

import psycopg2


def config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Setion {0} not found in the {1} file'.format(section, filename))

    return db


def connect():
    connection = None

    try:
        params = config()
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        cursor.execute("SELECT version()")
        print(cursor.fetchone())

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)

    return connection


def push_data(collection: dict):
    connection = connect()
    if connection != None:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO password_collection(name, url, username, password) VALUES('{name}', '{url}', '{username}', '{password}')".
                       format(name=collection["name"], url=collection["url"], username=collection["username"], password=collection["password"]))

        connection.commit()
        connection.close()


def get_password(choice: str):
    if choice == "Y":
        return input("Enter the password:")


def save_new_record():
    collection = {}
    collection["name"] = input("Enter the Name: ")
    collection["url"] = input("URL: ")
    collection["username"] = input("Username: ")
    password = ''
    while True:
        print("Do you have your own password, else we will generate a strong password")
        print("Y/N")
        choice = input(":").upper()
        if choice == "Y" or choice == "N":
            collection["password"] = get_password(choice)
            break
        else:
            print("Wrong Option, try again")
    push_data(collection)


def menu():
    while True:
        print("------------------Cero Password Manager------------------")
        print("Select a option by entering it's numeric")
        print("1. Save a New Password")
        print("0. Exit")
        choice = input(":")
        if choice == "1":
            save_new_record()
        elif choice == "0":
            return
        else:
            print("Wrong Option, Try again")


menu()
