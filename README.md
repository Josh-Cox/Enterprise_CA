# Spreadsheet Microservices Project

This is a spreadsheet that runs using a microservice. You can enter an ID and a FORMULA for each cell, with the FORMULA being able to contain other cell IDs. This project is for the module ECM3408 Enterprise Computing.

## Getting Started

This project runs using python 3.6.8, flask and requests. This section will guide you on how to install the dependecies and run the project.

### Prerequisites

To use this project you will need to install `flask` and `requests`.
Using a [virtual environment](https://docs.python.org/3/library/venv.html) is recommended.

#### Create and activate a virtual environment

```sh
python3 -m venv venv
```

<br>

- Linux

```sh
source venv/bin/activate
```

- Windows (CMD)

```sh
venv\Scripts\activate.bat
```

<br>

#### Install dependencies

```sh
python3 -m pip install flask requests
```

<br>

## Usage

If you are using firebase you need to set the environment variable to your realtime database:

#### linux

```sh
export FBASE=<your_database_name>
```

#### Windows

```sh
set FBASE <your_database_name>
```

To run the microservice, open a terminal and run the `SC.py` command with the desired parameter:

- `-r firebase|sqlite`\
  Determines which database is used

```sh
python3 SC.py -r sqlite
pyhton3 SC.py -r firebase
```

The microservice will now be running, to use it open another terminal and use `curl`.

#### Using `curl` from terminal

- Create or Update cell

```sh
curl -X PUT -H "Content-Type: application/json" -d "{\"id\":\"<YOUR_ID>\",\"formula\":\"<YOUR_FORMULA>\"}" localhost:3000/cells/<YOUR_ID>
```

- `<YOUR_ID>`\
   Any amount of letters followed by any amount of numbers.

- `<YOUR_FORMULA>`\
   Checks does not contain `[+-/*][+/*]|[0-9][A-DF-Za-df-z]|^[+/*]|^[-]$|[+-/*]$`

<br>

- Get cell FORMULA

```sh
curl -X GET localhost:3000/cells/<YOUR_ID>
```

<br>

- Get list of cell IDs

```sh
curl -X GET localhost:3000/cells
```

<br>

- Delete cell

```sh
curl -X DELETE localhost:3000/cells/<YOUR_ID>
```

<br>

#### Using a `.sh` file

```sh
chmod +x <your_script_name>.sh
./<your_script_name>.sh
```

<br>

**IMPORTANT: Everytime `SC.py` is run, it will wipe the respective database**

<br>

|                    |                                            |
| :----------------: | :----------------------------------------: |
|      `Author`      |                  Josh Cox                  |
| `test10.sh Author` |               David Wakeling               |
|     `License`      |                    MIT                     |
|   `Source Code`    | https://github.com/Josh-Cox/Enterprise_CA/ |
|                    |                                            |
