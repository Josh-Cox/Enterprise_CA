#!/bin/sh
###############################################################
## Spreadsheet test script                                   ##
###############################################################

HOST=localhost:3000
DB_FILE=sc.db

# rm -f $DB_FILE

SCORE=0
NUM_TESTS=0

###############################################################
## Test [1]: Ensure empty                                    ##
###############################################################
RESOURCE=$HOST/cells
ANSWER="\[\]"

STATUS=$(curl -s -X GET -o body -w "%{http_code}" $RESOURCE)
if [ $STATUS == "200" ]; then
    grep -q $ANSWER body
    if [ $? -eq 0 ]; then
        echo "Test [1]: OK"; SCORE=$(expr $SCORE + 1)
    else
        echo "Test [1]: FAIL"
        echo "Test [3]: Got "$(cat body)", expected" $FORMULA"."
    fi
else
    echo "Test [1]: FAIL (" $STATUS "!= 200 )"
fi
NUM_TESTS=$(expr $NUM_TESTS + 1)

###############################################################
## Test [2]: Scientific notation insert                      ##
###############################################################
ID="B2"; FORMULA="2e1"
RESOURCE=$HOST/cells/$ID

STATUS=$(curl -s -X PUT -d "{\"id\":\"$ID\",\"formula\":\"$FORMULA\"}" \
    -H "Content-Type: application/json" -w "%{http_code}" $RESOURCE)
if [ $STATUS == "201" ]; then
    echo "Test [2]: OK"; SCORE=$(expr $SCORE + 1)
else
    echo "Test [2]: FAIL (" $STATUS "!= 201 )"
fi
NUM_TESTS=$(expr $NUM_TESTS + 1)

###############################################################
## Test [3]: Scientific notation get                         ##
###############################################################
ID="B2"; FORMULA="20.0"
RESOURCE=$HOST/cells/$ID
ANSWER="\"formula\":\"$FORMULA\""

STATUS=$(curl -s -X GET -o body -w "%{http_code}" $RESOURCE)
if [ $STATUS == "200" ]; then
    grep -q $ANSWER body
    if [ $? -eq 0 ]; then
        echo "Test [3]: OK"; SCORE=$(expr $SCORE + 1)
    else
        echo "Test [3]: FAIL"
        echo "Test [3]: Got "$(cat body)", expected" $FORMULA"."
    fi
else
    echo "Test [3]: FAIL (" $STATUS "!= 200 )"
fi
NUM_TESTS=$(expr $NUM_TESTS + 1)

###############################################################
## Test [4]: Complicated formula insert                      ##
###############################################################
ID="B3"; FORMULA="(B2 + -(-B2 + B2 + -B2)) * (--(2 * B2) / B2)"
RESOURCE=$HOST/cells/$ID

STATUS=$(curl -s -X PUT -d "{\"id\":\"$ID\",\"formula\":\"$FORMULA\"}" \
    -H "Content-Type: application/json" -w "%{http_code}" $RESOURCE)
if [ $STATUS == "201" ]; then
    echo "Test [4]: OK"; SCORE=$(expr $SCORE + 1)
else
    echo "Test [4]: FAIL (" $STATUS "!= 201 )"
fi
NUM_TESTS=$(expr $NUM_TESTS + 1)

###############################################################
## Test [5]: Complicated formula get                         ##
###############################################################
ID="B3"; FORMULA="80.0"
RESOURCE=$HOST/cells/$ID
ANSWER="\"formula\":\"$FORMULA\""

STATUS=$(curl -s -X GET -o body -w "%{http_code}" $RESOURCE)
if [ $STATUS == "200" ]; then
    grep -q $ANSWER body
    if [ $? -eq 0 ]; then
        echo "Test [5]: OK"; SCORE=$(expr $SCORE + 1)
    else
        echo "Test [5]: FAIL"
        echo "Test [5]: Got "$(cat body)", expected" $FORMULA"."
    fi
else
    echo "Test [5]: FAIL (" $STATUS "!= 200 )"
fi
NUM_TESTS=$(expr $NUM_TESTS + 1)

###############################################################
## Test [6]: Blank formula insert                            ##
###############################################################
ID="B4"; FORMULA=""
RESOURCE=$HOST/cells/$ID

STATUS=$(curl -s -X PUT -d "{\"id\":\"$ID\",\"formula\":\"$FORMULA\"}" \
    -H "Content-Type: application/json" -w "%{http_code}" $RESOURCE)
if [ $STATUS == "201" ]; then
    echo "Test [6]: OK"; SCORE=$(expr $SCORE + 1)
else
    echo "Test [6]: FAIL (" $STATUS "!= 201 )"
fi
NUM_TESTS=$(expr $NUM_TESTS + 1)

###############################################################
## Test [7]: Blank formula get                               ##
###############################################################
ID="B4"; FORMULA="0"
RESOURCE=$HOST/cells/$ID
ANSWER="\"formula\":\"$FORMULA\""

STATUS=$(curl -s -X GET -o body -w "%{http_code}" $RESOURCE)
if [ $STATUS == "200" ]; then
    grep -q $ANSWER body
    if [ $? -eq 0 ]; then
        echo "Test [7]: OK"; SCORE=$(expr $SCORE + 1)
    else
        echo "Test [7]: FAIL"
        echo "Test [7]: Got "$(cat body)", expected" $FORMULA"."
    fi
else
    echo "Test [7]: FAIL (" $STATUS "!= 200 )"
fi
NUM_TESTS=$(expr $NUM_TESTS + 1)

###############################################################
## Test [8]: Just an integer insert                          ##
###############################################################
ID="B5"; FORMULA="5"
RESOURCE=$HOST/cells/$ID

STATUS=$(curl -s -X PUT -d "{\"id\":\"$ID\",\"formula\":\"$FORMULA\"}" \
    -H "Content-Type: application/json" -w "%{http_code}" $RESOURCE)
if [ $STATUS == "201" ]; then
    echo "Test [8]: OK"; SCORE=$(expr $SCORE + 1)
else
    echo "Test [8]: FAIL (" $STATUS "!= 201 )"
fi
NUM_TESTS=$(expr $NUM_TESTS + 1)

###############################################################
## Test [9]: Just an integer get                             ##
###############################################################
ID="B5"; FORMULA="5"
RESOURCE=$HOST/cells/$ID
ANSWER="\"formula\":\"$FORMULA\""

STATUS=$(curl -s -X GET -o body -w "%{http_code}" $RESOURCE)
if [ $STATUS == "200" ]; then
    grep -q $ANSWER body
    if [ $? -eq 0 ]; then
        echo "Test [9]: OK"; SCORE=$(expr $SCORE + 1)
    else
        echo "Test [9]: FAIL"
        echo "Test [9]: Got "$(cat body)", expected" $FORMULA"."
    fi
else
    echo "Test [9]: FAIL (" $STATUS "!= 200 )"
fi
NUM_TESTS=$(expr $NUM_TESTS + 1)

###############################################################
## Test [10]: Just a float insert                             ##
###############################################################
ID="B6"; FORMULA="5.0"
RESOURCE=$HOST/cells/$ID

STATUS=$(curl -s -X PUT -d "{\"id\":\"$ID\",\"formula\":\"$FORMULA\"}" \
    -H "Content-Type: application/json" -w "%{http_code}" $RESOURCE)
if [ $STATUS == "201" ]; then
    echo "Test [10]: OK"; SCORE=$(expr $SCORE + 1)
else
    echo "Test [10]: FAIL (" $STATUS "!= 201 )"
fi
NUM_TESTS=$(expr $NUM_TESTS + 1)

###############################################################
## Test [11]: Just a float get                                ##
###############################################################
ID="B6"; FORMULA="5.0"
RESOURCE=$HOST/cells/$ID
ANSWER="\"formula\":\"$FORMULA\""

STATUS=$(curl -s -X GET -o body -w "%{http_code}" $RESOURCE)
if [ $STATUS == "200" ]; then
    grep -q $ANSWER body
    if [ $? -eq 0 ]; then
        echo "Test [11]: OK"; SCORE=$(expr $SCORE + 1)
    else
        echo "Test [11]: FAIL"
        echo "Test [11]: Got "$(cat body)", expected" $FORMULA"."
    fi
else
    echo "Test [11]: FAIL (" $STATUS "!= 200 )"
fi
NUM_TESTS=$(expr $NUM_TESTS + 1)

###############################################################
## Test [12]: Just a cell value insert                       ##
###############################################################
ID="B7"; FORMULA="B6"
RESOURCE=$HOST/cells/$ID

STATUS=$(curl -s -X PUT -d "{\"id\":\"$ID\",\"formula\":\"$FORMULA\"}" \
    -H "Content-Type: application/json" -w "%{http_code}" $RESOURCE)
if [ $STATUS == "201" ]; then
    echo "Test [12]: OK"; SCORE=$(expr $SCORE + 1)
else
    echo "Test [12]: FAIL (" $STATUS "!= 201 )"
fi
NUM_TESTS=$(expr $NUM_TESTS + 1)

###############################################################
## Test [13]: Just a cell value get                          ##
###############################################################
ID="B7"; FORMULA="5.0"
RESOURCE=$HOST/cells/$ID
ANSWER="\"formula\":\"$FORMULA\""

STATUS=$(curl -s -X GET -o body -w "%{http_code}" $RESOURCE)
if [ $STATUS == "200" ]; then
    grep -q $ANSWER body
    if [ $? -eq 0 ]; then
        echo "Test [13]: OK"; SCORE=$(expr $SCORE + 1)
    else
        echo "Test [13]: FAIL"
        echo "Test [13]: Got "$(cat body)", expected" $FORMULA"."
    fi
else
    echo "Test [13]: FAIL (" $STATUS "!= 200 )"
fi
NUM_TESTS=$(expr $NUM_TESTS + 1)

###############################################################
## Test [14]: Long cell identifiers insert                   ##
###############################################################
ID="LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGID123456789123456789123456789123456789123456789"; FORMULA="1"
RESOURCE=$HOST/cells/$ID

STATUS=$(curl -s -X PUT -d "{\"id\":\"$ID\",\"formula\":\"$FORMULA\"}" \
    -H "Content-Type: application/json" -w "%{http_code}" $RESOURCE)
if [ $STATUS == "201" ]; then
    echo "Test [14]: OK"; SCORE=$(expr $SCORE + 1)
else
    echo "Test [14]: FAIL (" $STATUS "!= 201 )"
fi
NUM_TESTS=$(expr $NUM_TESTS + 1)

###############################################################
## Test [15]: Long cell identifiers get                      ##
###############################################################
ID="LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGID123456789123456789123456789123456789123456789"; FORMULA="1"
RESOURCE=$HOST/cells/$ID
ANSWER="\"formula\":\"$FORMULA\""

STATUS=$(curl -s -X GET -o body -w "%{http_code}" $RESOURCE)
if [ $STATUS == "200" ]; then
    grep -q $ANSWER body
    if [ $? -eq 0 ]; then
        echo "Test [15]: OK"; SCORE=$(expr $SCORE + 1)
    else
        echo "Test [15]: FAIL"
        echo "Test [15]: Got "$(cat body)", expected" $FORMULA"."
    fi
else
    echo "Test [15]: FAIL (" $STATUS "!= 200 )"
fi
NUM_TESTS=$(expr $NUM_TESTS + 1)

###############################################################
## Test [16]: Order of operations insert                     ##
###############################################################
ID="B8"; FORMULA="5 + 5 - 5 * 10 / 5 * (25 / 5 * 10 - -(10 * 20 + 5))"
RESOURCE=$HOST/cells/$ID

STATUS=$(curl -s -X PUT -d "{\"id\":\"$ID\",\"formula\":\"$FORMULA\"}" \
    -H "Content-Type: application/json" -w "%{http_code}" $RESOURCE)
if [ $STATUS == "201" ]; then
    echo "Test [16]: OK"; SCORE=$(expr $SCORE + 1)
else
    echo "Test [16]: FAIL (" $STATUS "!= 201 )"
fi
NUM_TESTS=$(expr $NUM_TESTS + 1)

###############################################################
## Test [17]: Order of operations get                        ##
###############################################################
ID="B8"; FORMULA="-2540.0"
RESOURCE=$HOST/cells/$ID
ANSWER="\"formula\":\"$FORMULA\""

STATUS=$(curl -s -X GET -o body -w "%{http_code}" $RESOURCE)
if [ $STATUS == "200" ]; then
    grep -q $ANSWER body
    if [ $? -eq 0 ]; then
        echo "Test [17]: OK"; SCORE=$(expr $SCORE + 1)
    else
        echo "Test [17]: FAIL"
        echo "Test [17]: Got "$(cat body)", expected" $FORMULA"."
    fi
else
    echo "Test [17]: FAIL (" $STATUS "!= 200 )"
fi
NUM_TESTS=$(expr $NUM_TESTS + 1)

###############################################################
## Test [18]: Invalid formula: Just operator                 ##
###############################################################
ID="B9"; FORMULA="+"
RESOURCE=$HOST/cells/$ID

STATUS=$(curl -s -X PUT -d "{\"id\":\"$ID\",\"formula\":\"$FORMULA\"}" \
    -H "Content-Type: application/json" -w "%{http_code}" $RESOURCE)
if [ $STATUS == "400" ]; then
    echo "Test [18]: OK"; SCORE=$(expr $SCORE + 1)
else
    echo "Test [18]: FAIL (" $STATUS "!= 400 )"
fi
NUM_TESTS=$(expr $NUM_TESTS + 1)

###############################################################
## Test [19]: Invalid formula: Unary plus                    ##
###############################################################
ID="B9"; FORMULA="+B8"
RESOURCE=$HOST/cells/$ID

STATUS=$(curl -s -X PUT -d "{\"id\":\"$ID\",\"formula\":\"$FORMULA\"}" \
    -H "Content-Type: application/json" -w "%{http_code}" $RESOURCE)
if [ $STATUS == "400" ]; then
    echo "Test [19]: OK"; SCORE=$(expr $SCORE + 1)
else
    echo "Test [19]: FAIL (" $STATUS "!= 400 )"
fi
NUM_TESTS=$(expr $NUM_TESTS + 1)

###############################################################
## Test [20]: Invalid formula: No unary identifier           ##
###############################################################
ID="B9"; FORMULA="B6 + -"
RESOURCE=$HOST/cells/$ID

STATUS=$(curl -s -X PUT -d "{\"id\":\"$ID\",\"formula\":\"$FORMULA\"}" \
    -H "Content-Type: application/json" -w "%{http_code}" $RESOURCE)
if [ $STATUS == "400" ]; then
    echo "Test [20]: OK"; SCORE=$(expr $SCORE + 1)
else
    echo "Test [20]: FAIL (" $STATUS "!= 400 )"
fi
NUM_TESTS=$(expr $NUM_TESTS + 1)

###############################################################
## Test [21]: Invalid formula: Invalid identifier            ##
###############################################################
ID="B9"; FORMULA="B6A"
RESOURCE=$HOST/cells/$ID

STATUS=$(curl -s -X PUT -d "{\"id\":\"$ID\",\"formula\":\"$FORMULA\"}" \
    -H "Content-Type: application/json" -w "%{http_code}" $RESOURCE)
if [ $STATUS == "400" ]; then
    echo "Test [21]: OK"; SCORE=$(expr $SCORE + 1)
else
    echo "Test [21]: FAIL (" $STATUS "!= 400 )"
fi
NUM_TESTS=$(expr $NUM_TESTS + 1)



echo "** Overall score:" $SCORE "/" $NUM_TESTS "**"
