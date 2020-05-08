FROM python:3.8-slim-buster
# Copy project files and work in that directory
COPY . /app
WORKDIR /app
# Install dependencies
RUN pip3 install -r requirements.txt && \
    pip3 install waitress
# Set entrypoint as running the server. Waitress binds to 8080
EXPOSE 8080
ENTRYPOINT [ "python3" ]
CMD [ "src/prod_serve.py" ]