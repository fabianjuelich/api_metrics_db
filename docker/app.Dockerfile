FROM debian:bookworm

RUN apt update && apt install python3 python3-pip -y

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
RUN pip3 install requests --break-system-packages
RUN pip3 install stocksymbol --break-system-packages
# archive
RUN pip3 install requests_html --break-system-packages
RUN pip3 install pandas --break-system-packages
RUN pip3 install matplotlib --break-system-packages

# ENV PYTHONPATH "${PYTHONPATH}:/home/archive/WI_Projekt_SS23_Juelich_Kalacevic"

CMD ["python3", "home/interface.py"]
