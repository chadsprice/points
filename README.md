## Setup

### Install Python 3

If you do not have Python 3 installed, the official distribution is [here](https://www.python.org/downloads/)

### Install Flask

Run `pip install flask`. If you encounter issues, [consult the installation guide](https://flask.palletsprojects.com/en/1.1.x/installation/)

## Running

Run `python points.py`. If you encounter issues, check that your environment configuration is running Python 3 with the Flask module installed.

## REST API

All requests are `GET` for simplicity. All requests require the `Content-Type: application/json` header.

### route: `/add`

body:
```
{
  "user": <string>,
  "date": <string>,
  "payer": <string>,
  "points": <number>
}
```

responses:
success: `HTTP 200`
failure (incorrect input type, insufficient points): `HTTP 400`

### route: `/deduct`

body:
```
{
  "user": <string>,
  "points": <number>
}
```

responses:
success: `HTTP 200`
example body:
```
[
  {
    "date": "2021-01-01"
    "payer": "payer a"
    "points": -200
  },
  {
    "date": "2021-01-02"
    "payer": "payer b"
    "points": -100
  }
]
```
failure (incorrect input type, insufficient points): `HTTP 400`

### route: `/balance`

body:
```
{
  "user": <string>
}
```

responses:
success: `HTTP 200`
example body:
```
{
  "payer a": 200,
  "payer b": 100
}
```
failure (incorrect input type): `HTTP 400`

## Non-Goals

To keep the code short and simple, the following decisions were made:

* The code does not parse dates or handle things like timezones. All dates are assumed to be strings in the 'YYYY-MM-DD' format, so that they can be sorted easily by just comparing the strings.
* The code does not "expire" points by checking the current date or deleting date/payer records where the number of points is zero. Naturally, you would want to do this to keep the data from growing indefinitely, but that is not necessary for this short example.
* The code does not handle user validation, any user string with no points records is treated as a valid user with a balance of zero.
* The code has no built in examples or automated tests. Naturally, you would want to have a separate test module, but that is not necessary for this short example.
