# model-deployment

## About

model-deployment is a consumable REST API service for the [image-service](https://github.com/Bangkit-C23-PS414/image-service) and collaboratively developed by Bangkit Academy 2023 Cohort.

Contributor to this repostory:

- [Dimas Ichsanul Arifin](https://github.com/Dimasichsanul)
- [Ramdhan Firdaus Amelia](https://github.com/ramdhanfirdaus)
- [Saddam Sinatrya Jalu Mukti](https://github.com/myxzlpltk)

## Build With

- [Python](https://www.python.org/)
- [Docker](https://www.docker.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Google App Engine](https://cloud.google.com/appengine)

## API endpoints

Deployment URL : https://c23-ps414-ml-service.et.r.appspot.com/docs/

## Development

### Install dependencies

```
pip install -r requirements.txt
```

### Running the Service without Container

```bash
$ uvicorn app.main:app --reload
```

Or

```bash
$ uvicorn app.main:app --reload
```

### Building the Container

```bash
$ docker build -t model-deployment .
```

### Running the Container

```bash
$ docker run -d -p 8000:8000 model-deployment
```

## Load the ML model

Put your model file to model folder
