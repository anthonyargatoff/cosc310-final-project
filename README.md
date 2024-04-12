# QuakeQuake
QuakeQuest is an application that delivers realtime and historical earthquake data. It uses an interactive map to display data based on a query from a user. A user may sign up and create an account and set custom notifications.

## Instructions on running the app

1. A user must have [python](https://www.python.org/downloads/) installed on their local machine (version 3.10).
1. Clone the repository onto your local machine.
1. It is recommended to create a virtual environment. Full details can be found at this [link](https://docs.python.org/3/library/venv.html).
    - On windows, use `python -m venv venv`
    - On macOS and Linux, use `python3 -m venv venv`
1. Activate your virtual environment with:
    - On Windows: `venv\Scripts\activate`
    - On macOS and Linux: `source venv/bin/activate`

1. Ensure you have _pip_ installed on your device with `pip -V`. If not installed, follow [this](https://pip.pypa.io/en/stable/installation/) guide.
1. Install the requirements file with `pip install -r requirements.txt`.
1. Upon successful installation of the requirements, the development server can be started with `python main.py` on Windows, or `python3 main.py` on macOS and Linux. Alternatively, the app can be started with  `flask --app flaskr run`, or debug mode can be run with `flask --app flaskr run --debug`. 
1. Navigate to _localhost:5000/_ to view the app.
