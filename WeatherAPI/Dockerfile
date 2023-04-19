FROM python:latest
COPY . .
#WORKDIR /WeatherAPI
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN useradd cont_user
RUN su cont_user
RUN chown cont_user .
RUN chmod u+rwx .
# RUN pwd
# RUN ls
# ENV BG_COLOR=silver
USER cont_user
EXPOSE 9090
CMD gunicorn --bind 0.0.0.0:9090 application:application

