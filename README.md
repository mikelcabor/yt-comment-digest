Python version 3.11

Installation:

python -m venv venv

.\venv\Scripts\activate

pip install fastapi    

pip install "uvicorn[standard]"

pip install python-multipart sqlalchemy jinja2

pip install -r requirements.txt  

Start:

uvicorn app:app --reload
