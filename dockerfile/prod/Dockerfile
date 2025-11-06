FROM leno_image:1.0.0

ENV PYTHONUNBUFFERED=1

WORKDIR /home/app

COPY . .

RUN chmod +x ./scripts/*

EXPOSE 8000

ENTRYPOINT ["./scripts/start.sh"]