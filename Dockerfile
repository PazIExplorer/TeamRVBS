FROM tiangolo/uwsgi-nginx-flask:
RUN apk --update add bash nano
ENV STATIC_URL /static
ENV STATIC_PATH /TeamRVBS/app/static
COPY ./requirements.txt /TeamRVBS/requirements.txt
RUN pip install -r /var/www/requirements.txt
