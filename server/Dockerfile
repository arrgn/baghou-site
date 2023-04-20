FROM python
WORKDIR /app
COPY requirements.txt ./requirements.txt
COPY ./ ./
RUN pip install --no-cache-dir -r ./requirements.txt
ENV FLASK_APP app.py
ENV FLASK_DEBUG 0
CMD ["python", "-m", "flask", "run"]