from flask import Flask, request
import sqlite3
from Spreadsheet import Spreadsheet

db = "sc.db"

app = Flask(__name__)

def create_db():
    """
    Create database with "cells" table
    """
    
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS cells" + "(id TEXT PRIMARY KEY, formula TEXT)")
        connection.commit()


@app.route("/cells/<url_cell_id>", methods=["PUT"])
def update(url_cell_id):
    """
    Updates row in cells table
    
    :param id: id of cell to update
    :param formula: formula to insert into row
    
    """
    
    # get values from json
    js = request.get_json()
    cell_id = js.get("id")
    formula = js.get("formula")
    
    # check they are not null and url value and passed value are equal
    if cell_id == None or formula == None or url_cell_id != cell_id:
        return "", 400 # Bad request
    
    else:
        # update the database
        result = Spreadsheet.update(cell_id, formula)
        
        if result != None:
            return result # Created | Updated | Bad Request
        else:
            return "", 500 # Internal Server Error
        
@app.route("/cells/<url_cell_id>", methods=["GET"])
def read(url_cell_id):
    """
    Reads row in cells table
    
    :param id: id of cell to read
    """
    
    # update the database
    result = Spreadsheet.read(url_cell_id)
    
    if result != None:
        return result, 200 # Created or Updated
    else:
        return "", 500 # Internal Server Error

def test_read(cell_id):
    print(Spreadsheet.read(cell_id))

def test_update(cell_id, formula):
    Spreadsheet.update(cell_id, formula)

def print_db():
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM cells")
        result = cursor.fetchall()
        
        for x in result:
            print(x)


if __name__ == "__main__":
    create_db()
    # app.run(host="localhost", port=3000)
    # print(test_update("B2", "B3 + 4"))
    # test_update("B3", "7")
    test_update("D4D", "B4 * B3")
    # test_update("BB6Z8", " (-B3 + B4 ) *B2")
    # test_read("B2")
    # print_db()