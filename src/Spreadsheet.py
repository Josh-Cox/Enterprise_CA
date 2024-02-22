import sqlite3
import re
import requests
import json
import os


class Spreadsheet:
    
    def setup_db(method: str):
        """
        Create sql database with "cells" table
        Wipe firebase realtime database
        """
        
        # When using sqlite, won't error if FBASE is not defined
        if method == 'f':
            global FBASE
            FBASE = os.environ['FBASE']
            global FBASE_URL
            FBASE_URL = f"https://{FBASE}-default-rtdb.europe-west1.firebasedatabase.app/"
            
            # delete all values in firebase realtime database
            endpoint = FBASE_URL + ".json"
            response = requests.delete(endpoint)
            
            if response.status_code != 200:
                return "", 500 # Internal Server Error

        else:
            global database
            database = "sc.db"
            
            # delete the database
            try:
                os.remove(database)#
            except Exception as e:
                pass
        
            # recreate the database
            with sqlite3.connect(database) as connection:
                cursor = connection.cursor()
                cursor.execute("CREATE TABLE IF NOT EXISTS cells" + "(id TEXT PRIMARY KEY, formula TEXT)")
                connection.commit()
            
  
        
    def update(cell_id: str, formula: str, method: str):
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
        
        # check for double operators, number then letter (E.g. 2B2), start with +*/, isn't just an operartor, check id is valid
        if re.findall("[+-/*][+/*]|[0-9][A-DF-Za-df-z]|^[+/*]|^[-]$|[+-/*]$", formula) or re.findall("^(?![A-Za-z]+\d+$).*", cell_id) != []:
            return "", 400 # Bad request

        
        # check sql or firebase
        if method == "s":
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
        else:
            # create endpoint
            endpoint = FBASE_URL + "cells" + f"/{cell_id}.json"
            
            # check if data exists
            record = Spreadsheet.read(cell_id, method)
            
            # if exists update formula else create new
            if record == "":
                record = {"id": cell_id,"formula": formula}
                response_code = 201 # Created
            else:
                record["formula"] = formula
                response_code = 204 # Updated
            
            # include the id so can retrieve in read()
            # record["id"] = cell_id
            
            # return response
            response = requests.put(endpoint, data=json.dumps(record))
            
            if response.status_code == 200:
                return "", response_code

            return "", 500 # Internal Server Error
            
    def read(cell_id: str, method: str, recursive=False):
        """
        Return the contents of a cell
        
        :param cell_id: the id of the cell to return
        :param method: sql or firebase
        :param recursive: whether the method is called directly or recursively (in a formula)
        """
        
        if method == "s":
            # open connection with database
            with sqlite3.connect(database) as connection:
                connection.row_factory = sqlite3.Row
                cursor = connection.cursor()
                
                # get the cell
                cursor.execute("SELECT id, formula FROM cells WHERE id = ?", (cell_id,))
                record = cursor.fetchone()

        else:
            endpoint = FBASE_URL + "cells" + f"/{cell_id}.json"
            response = requests.get(endpoint)
            record = response.json()
            
            
        # if doesn't exist then return 0 or error 404
        if record == None:
            # check if call was recursive or direct
            if recursive == True:
                return {"id":cell_id,"formula":0}
            else:
                return ""
        
        # get id and formula
        cell_id = record['id']
        formula = record['formula']
        
        # check if formula contains any other cells (any letter exlcuding Ee if it has a number before it)
        if re.findall('(?<![0-9])[Ee]|[A-Da-dF-Zf-z]', formula) == []:
            return {"id":cell_id,"formula":str(eval(formula))}
            
        # split elements by operators and brackets
        formula = re.split(r"([-*+/()])", formula)

        # new formula string
        result = ""
        
        # loop through element, recurisvely calling if element is cell_id (contains a letter)
        for element in formula:
            if re.search('(?<![0-9])[Ee]|[A-Da-dF-Zf-z]', element) != None:
                element = Spreadsheet.read(element, method, True)["formula"]
                
            result += str(element)
            
        return {"id":cell_id,"formula":str(eval(result))}
            
    def delete(cell_id: str, method: str):
        """
        Deletes a record from the table
        
        :param cell_id: id of record to delete
        ::param method: sql or firebase
        """

        # check sql or firebase
        if method == "s":
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
                
                # if nothing went wrong then return 204
                return "", 204 # Deleted
        else:
            # check if exists
            check = Spreadsheet.read(cell_id, method)
            
            # if exists then delete it, else return 404
            if check != "" and check != None:
                endpoint = FBASE_URL + "cells" + f"/{cell_id}.json"
                response = requests.delete(endpoint)
            else:
                return "", 404 # Not found
            
            if response == None:
                return "", 500 # Internal Server Error
        
            # if nothing went wrong return 204
            return "", 204 # Deleted
    
    def list_cells(method: str):
        
        # check sql or firebase
        if method == "s":
            with sqlite3.connect(database) as connection:
                cursor = connection.cursor()
                
                # get list of ids
                cursor.execute("SELECT id FROM cells")
                
                # convert from list of tuples to list and return as json
                return json.dumps([cell[0] for cell in cursor.fetchall()]) 
        else:
            endpoint = FBASE_URL + "cells.json"
            response = requests.get(endpoint)
            
            if response.status_code == 200:
                if response.json() != None:
                    return json.dumps(list(response.json().keys()))
                else:
                    return json.dumps([])
            else:
                return None