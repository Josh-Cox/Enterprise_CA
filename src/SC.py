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
    result = Spreadsheet.update(cell_id, formula, method)
    
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
    result = Spreadsheet.read(url_cell_id, method)
    
    if result == None:
        return "", 500 # Internal Server Error
    elif result == "":
        return "", 404 # Not found
    else:
        return result, 200 # Created or Updated

@app.route("/cells/<url_cell_id>", methods=["DELETE"])
def delete(url_cell_id: str):
    """
    Deletes row from cells table

    :param url_cell_id: id of cell to delete
    """
    
    result = Spreadsheet.delete(url_cell_id, method)
    
    # check sql didn't go wrong
    if result != None:
        return result
    else:
        return "", 500 # Internal Server Error

@app.route("/cells", methods=["GET"])
def list_cells():
    """
    Lists id of every row
    """
    result = Spreadsheet.list_cells(method)
    
    if result != None:
        return result, 200
    else:
        return "", 500 # Internal Server Error


if __name__ == "__main__":
    Spreadsheet.setup_db()
    app.run(host="localhost", port=3000)
