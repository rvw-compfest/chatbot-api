FROM continuumio/miniconda3

WORKDIR /app

COPY requirements.txt .

RUN conda create --name myenv python=3.10.12 && \
    conda activate myenv && \
    pip install -r requirements.txt

COPY . .

ENV FLASK_APP=api/app.py
ENV FLASK_ENV=production

CMD ["conda", "run", "--no-capture-output", "-n", "myenv", "flask", "run", "--host=0.0.0.0"]