FROM python
WORKDIR /bg_api
COPY requirements.txt ./requirements.txt
COPY ./ ./
RUN pip install --no-cache-dir -r ./requirements.txt
ENV FLASK_APP app.py
ENV FLASK_DEBUG 0
ENTRYPOINT ["flask"]
CMD ["run", "--host", "0.0.0.0"]