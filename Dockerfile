FROM python:3.12
EXPOSE 8080
WORKDIR /app
COPY . ./
RUN pip install -r requirements.txt
ENTRYPOINT ["streamlit", "run", "routes.py", "--server.port=8080", "--server.address=0.0.0.0"]