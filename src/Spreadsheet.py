import sqlite3
import re

db = "sc.db"

class Spreadsheet:
        
    def update(cell_id, formula):
        """
        Update or create a new cell in the database
        
        :param cell_id: the id of the cell to create or update
        :param formula: the formula to insert into the cell
        """
        
        # format formula
        formula = formula.replace(" ", "")
        
        # check for double operators E.g. -+ ** ++ (--, +- *- are allowed as - unary)
        if re.findall("[+-/*][+/*]", formula) != []:
            return "", 400 # Bad request
        
        print(re.findall("^[A-Za-z]+\d+.*", cell_id))
        # check id is valid
        if re.match("[[A-Za-z]+\d+]", cell_id) != []:
            pass
        
        # open connection with database
        with sqlite3.connect(db) as connection:
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
            
    def read(cell_id):
        """
        Return the contents of a cell
        
        :param cell_id: the id of the cell to return
        """
        
        # open connection with database
        with sqlite3.connect(db) as connection:
            cursor = connection.cursor()
            
            # get the cell
            cursor.execute("SELECT id, formula FROM cells WHERE id = ?", (cell_id,))
            record = cursor.fetchone()
            
            if record == None:
                return {"id":cell_id,"formula":0}
            
            # get id and formula
            cell_id = record[0]
            formula = record[1]
            
            # check if formula contains any other cells
            if re.search('[a-zA-Z]', formula) == None:
                return {"id":cell_id,"formula":eval(formula)}
            else:
                
                # split elements by operators and brackets
                formula = re.split(r"([-*+/()])", formula)
  
                # new formula string
                result = ""
                
                # loop through element, recurisvely calling if element is cell_id (contains a letter)
                for element in formula:
                    if re.search('[a-zA-Z]', element) != None:
                        element = Spreadsheet.read(element)["formula"]
                        
                    result += str(element) + " "
                    
                return {"id":cell_id,"formula":eval(result)}
            
                        
                
            
            
            

        