from flask import Flask, jsonify, request
from Spreadsheet import Spreadsheet, database
import sqlite3
import requests
import os
import sys
import argparse

app = Flask(__name__)

# create action for command line arguments
parser = argparse.ArgumentParser(description="Database Method")
parser.add_argument("-r", required=True)
args = parser.parse_args()

# default databse to sql
method = "s"

# if firebase used then use firebase realtime database
if args.r.lower() == "firebase":
    method = "f"

print(method)

def create_db():
    """
    Create database with "cells" table
    """
    
    with sqlite3.connect(database) as connection:
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS cells" + "(id TEXT PRIMARY KEY, formula TEXT)")
        connection.commit()

@app.route("/cells/<url_cell_id>", methods=["PUT"])
def update(url_cell_id: str):
    """
    Updates row in cells table
    
    :param id: id of cell to update
    :param formula: formula to insert into row
    
    """
    
    # get values from json
    js = request.get_json()
    cell_id = js.get("id")
    formula = js.get("formula")
    
    # check they are not null and that the url value and the passed value are equal
    if cell_id == None or formula == None or url_cell_id != cell_id:
        return "", 400 # Bad request
    
    # update the correct database
    if method != "s":
        result = Spreadsheet.firebase_update(cell_id, formula)
    else:
        result = Spreadsheet.update(cell_id, formula)
    
    if result != None:
        return result # Created | Updated | Bad Request
    else:
        return "", 500 # Internal Server Error
        
@app.route("/cells/<url_cell_id>", methods=["GET"])
def read(url_cell_id: str):
    """
    Reads row in cells table
    
    :param id: id of cell to read
    """
    
    # update the database
    if method != "s":
        result = Spreadsheet.firebase_read(url_cell_id)
    else:
        result = Spreadsheet.read(url_cell_id)
    
    if result != None:
        return result, 200 # Created or Updated
    else:
        return "", 500 # Internal Server Error

@app.route("/cells/<url_cell_id>", methods=["DELETE"])
def delete(url_cell_id: str):
    """
    Deletes row from cells table

    :param url_cell_id: id of cell to delete
    """
    
    result = Spreadsheet.delete(url_cell_id)
    
    if result != None:
        return result
    else:
        return "", 500 # Internal Server Error

@app.route("/cells", methods=["GET"])
def list_formulas():
    """
    Lists id of every row
    """
    result = Spreadsheet.list_formulas()
    
    if result != None:
        return jsonify(result), 200
    else:
        return "", 500 # Internal Server Error


if __name__ == "__main__":
    # create_db()
    app.run(host="localhost", port=3000)
