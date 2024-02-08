import sqlite3
import re
import requests
import json

database = "sc.db"
FBASE = "enterprise-ca-d05cd"
FBASE_URL = f"https://{FBASE}-default-rtdb.europe-west1.firebasedatabase.app/"

class Spreadsheet:
        
    def update(cell_id: str, formula: str):
        """
        Update or create a new cell in the database
        
        :param cell_id: the id of the cell to create or update
        :param formula: the formula to insert into the cell
        """
        
        
        # format formula
        formula = formula.replace(" ", "")
        
        # if formula is empty then set to 0
        if formula == "":
            formula = "0"
        
        # check for double operators E.g. -+ ** ++ (--, +- *- are allowed as - unary)
        if re.findall("[+-/*][+/*]", formula) != []:
            return "", 400 # Bad request
        
        # check id is valid (one or more letters then 1 or more numbers)
        if re.findall("^(?![A-Za-z]+\d+$).*", cell_id) != []:
            return "", 400 # Bad Request
        
        # open connection with database
        with sqlite3.connect(database) as connection:
            cursor = connection.cursor()
            
            # check if cell exists
            cursor.execute("SELECT 1 FROM cells WHERE id = ? LIMIT 1", (cell_id,))
            
            # if cell doesn't exist then create
            if cursor.fetchone() == None:
                cursor.execute("INSERT INTO cells VALUES(?, ?)", (cell_id, formula))
                connection.commit()
                
                return "", 201 # Created
            
            # else update
            else:
                cursor.execute("UPDATE cells SET id = ?, formula = ? WHERE id = ?", (cell_id, formula, cell_id))
                connection.commit()
                
                return "", 204 # Updated
            
    def read(cell_id: str, recursive=False):
        """
        Return the contents of a cell
        
        :param cell_id: the id of the cell to return
        """
        
        # open connection with database
        with sqlite3.connect(database) as connection:
            cursor = connection.cursor()
            
            # get the cell
            cursor.execute("SELECT id, formula FROM cells WHERE id = ?", (cell_id,))
            record = cursor.fetchone()
        
        # if doesn't exist then return 0
        if record == None:
            # check if call was recursive or direct
            if recursive == True:
                return {"id":cell_id,"formula":0}
            else:
                return "", 404
        
        # get id and formula
        cell_id = record[0]
        formula = record[1]
        
        # check if formula contains any other cells
        if re.search('[a-zA-Z]', formula) == None:
            return {"id":cell_id,"formula":eval(formula)}
            
        # split elements by operators and brackets
        formula = re.split(r"([-*+/()])", formula)

        # new formula string
        result = ""
        
        # loop through element, recurisvely calling if element is cell_id (contains a letter)
        for element in formula:
            if re.search('[a-zA-Z]', element) != None:
                element = Spreadsheet.read(element, True)["formula"]
                
            result += str(element) + " "
            
        return {"id":cell_id,"formula":eval(result)}, 200
            
    def delete(cell_id: str):
        # open connection with database
        with sqlite3.connect(database) as connection:
            cursor = connection.cursor()
            
            # check if cell exists
            cursor.execute("SELECT 1 FROM cells WHERE id = ? LIMIT 1", (cell_id,))
            
            if cursor.fetchone() == None:                
                return "", 404 # Not found

            # delete the cell
            cursor.execute("DELETE FROM cells WHERE id = ?", (cell_id,))
            connection.commit()

        return "", 204
    
    def list_formulas():
         with sqlite3.connect(database) as connection:
            cursor = connection.cursor()
            
            # get list of ids
            cursor.execute("SELECT id FROM cells")
            
            # convert from list of tuples to list
            formulas = cursor.fetchall()
            formula_list = [i[0] for i in formulas]
            
            return formula_list

    def firebase_update(cell_id: str, formula: str):
    
        # create endpoint
        endpoint = FBASE_URL + "cells" + f"/{cell_id}.json"
        
        # check if data exists
        record = Spreadsheet.firebase_read(cell_id)
        
        # if exists update formula else create new
        if record != None:
            record["formula"] = formula
            response_code = 204 # Updated
        else:
            record = {"id": cell_id,"formula": formula}
            response_code = 201 # Created
        
        # include the id so can retrieve in firebase_read()
        record["id"] = cell_id
        
        # return response
        response = requests.put(endpoint, data=json.dumps(record))
        
        if response.status_code == 200:
            return "", response_code

        return "", 500 # Internal Server Error
        

    def firebase_read(cell_id: str):
        endpoint = FBASE_URL + "cells" + f"/{cell_id}.json"
        response = requests.get(endpoint)
        
        if response.status_code == 200:
            return response.json()
        else:
            return "", 404