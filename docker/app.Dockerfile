FROM python:3.11

# new
ADD ./docker/app/ /home/
ADD ./docker/shared/ /home/
# backup data
ADD ./appendix/symbols/ /home/backup
# archive
ADD ./archive/Informatikprojekt_WS22_23_Kinetz/data/stocks_data.csv /home/archive/Informatikprojekt_WS22_23_Kinetz/data/stocks_data.csv
ADD ./archive/WI_Projekt_SS23_Juelich_Kalacevic/src /home/archive/WI_Projekt_SS23_Juelich_Kalacevic/src
ADD ./archive/WI_Projekt_SS23_Juelich_Kalacevic/assets /home/archive/WI_Projekt_SS23_Juelich_Kalacevic/assets
ADD ./archive/WI_Projekt_SS23_Juelich_Kalacevic/__init__.py /home/archive/WI_Projekt_SS23_Juelich_Kalacevic/__init__.py
# remove this one later
ADD ./archive/WI_Projekt_SS23_Juelich_Kalacevic/showcase.py /home/archive/WI_Projekt_SS23_Juelich_Kalacevic/showcase.py
# new
RUN pip install requests
RUN pip install stocksymbol
# archive
RUN pip install requests_html
RUN pip install pandas
RUN pip install matplotlib

CMD ["python", "home/interface.py"]
