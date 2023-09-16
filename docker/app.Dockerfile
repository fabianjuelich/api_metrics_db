FROM python:3.11

ADD ./app/ /home/
ADD ./shared/ /home/
RUN pip install requests
RUN pip install stocksymbol

CMD ["python", "home/interface.py"]
