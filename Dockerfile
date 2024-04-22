FROM python:3.10

WORKDIR /usr/src/app

EXPOSE 5000

COPY . .

RUN pip install --no-cache-dir -r req.txt

# CMD ["python", "manage.py", "run"]
CMD ["gunicorn", "-w 2", "-b", "0.0.0.0:5000", "src:app"]