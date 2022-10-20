FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

VOLUME [ "/usr/src/app/config" ]

CMD [ "python", "./bcaus_bot.py" ]