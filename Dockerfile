FROM python

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY game ./game/
COPY game/data ./data/
COPY game/templates ./templates/
COPY game/app.py .
COPY game/utils.py .

CMD flask run -h 0.0.0.0 -p 80