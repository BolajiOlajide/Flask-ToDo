FROM python:3.6.2

RUN mkdir -p /proton

WORKDIR /proton

COPY . .

RUN pip install -r requirements.txt

VOLUME ["/proton"]

ENTRYPOINT ["./run_web.sh"]