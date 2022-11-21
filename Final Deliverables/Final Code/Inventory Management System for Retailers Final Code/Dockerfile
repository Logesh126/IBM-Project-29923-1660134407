FROM python:3.10.6
RUN apt-get update
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]



#FROM python:3.10.6
#WORKDIR /app
##ADD . /app
#COPY requirements.txt /app
##RUN pip install -r requirements.txt
#pip install --no-cache-dir -r requirements.txt
#
##RUN python3 -m pip install ibm_db
#EXPOSE 5000
##CMD ["python","app.py"]
#
#CMD ["gunicorn", "--blind", "0.0.0.0:5000", "app:app"]