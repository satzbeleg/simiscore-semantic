[![DOI](https://zenodo.org/badge/355460576.svg)](https://zenodo.org/badge/latestdoi/355460576)


# simiscore-semantic
An ML API to compute semantic similarity scores between sentence examples. 
The API is programmed with the [`fastapi` Python package](https://fastapi.tiangolo.com/), 
and the semantic similarities are computed based on [SBert (`sentence-transformers` package)](https://github.com/UKPLab/sentence-transformers). 
The deployment is configured for Docker Compose.



## Docker Deployment
Call Docker Compose

```sh
export API_PORT=8083
docker-compose -f docker-compose.yml up --build

# or as oneliner:
API_PORT=8083 docker-compose -f docker-compose.yml up --build
```

(Start docker daemon before, e.g. `open /Applications/Docker.app` on MacOS).

Check

```sh
curl http://localhost:8083
```

Notes: Only `main.py` is used in `Dockerfile`.



## Local Development

### Install a virtual environment

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
pip install -r requirements-dev.txt --no-cache-dir
```

(If your git repo is stored in a folder with whitespaces, then don't use the subfolder `.venv`. Use an absolute path without whitespaces.)

### Specify where to store the SBert model
SBert allows to set the `cache_folder` via the environment variable `SENTENCE_TRANSFORMERS_HOME` (See [here](https://github.com/UKPLab/sentence-transformers/blob/bd19871d99068f4824ff6ef213d91596885889f7/sentence_transformers/SentenceTransformer.py#L48)).

```sh
mkdir ./sbert-models
export SENTENCE_TRANSFORMERS_HOME="$(pwd)/sbert-models"
```


### Start Server

```sh
source .venv/bin/activate
# uvicorn app.main:app --reload
gunicorn app.main:app --reload --bind=0.0.0.0:8083 \
    --worker-class=uvicorn.workers.UvicornH11Worker \
    --workers=1 --timeout=600
```


### Usage Examples

a) Send a list of strings.

```sh
curl -X 'POST' \
  'http://localhost:8083/similarities/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '[
    "Der Film ist super.",
    "Der Spielfilm ist gut.",
    "Der Film ist Müll.",
    "Der Spielfilm ist schlecht."
  ]'
```

b) Send an JSON object with UUID4 as keys and text as values.

```sh
curl -X 'POST' \
  'http://localhost:8083/similarities/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "80ba0456-1d26-4d22-8e80-113b919502ee": "Der Film ist super.",
    "a47fe293-26e7-40f0-b0b5-202e0955458f": "Der Spielfilm ist gut.",
    "86e356a3-5b42-4e03-91fc-cf69098b6dd2": "Der Film ist Müll.",
    "779d0245-8f54-49ec-9f0f-8e29dc987b41": "Der Spielfilm ist schlecht."
   }'
```

### Other commands and help
* Check syntax: `flake8 --ignore=F401 --exclude=$(grep -v '^#' .gitignore | xargs | sed -e 's/ /,/g')`
* Run Unit Tests: `PYTHONPATH=. pytest`
- Show the docs: [http://localhost:8083/docs](http://localhost:8083/docs)
- Show Redoc: [http://localhost:8083/redoc](http://localhost:8083/redoc)


### Clean up 
```sh
find . -type f -name "*.pyc" | xargs rm
find . -type d -name "__pycache__" | xargs rm -r
rm -r .pytest_cache
rm -r .venv
```


## Appendix

### Citation

```
@software{ulf_hamster_2022_7096002,
  author       = {Ulf Hamster and
                  Luise Köhler},
  title        = {simiscore-semantic: ML API for semantic similarities},
  month        = sep,
  year         = 2022,
  publisher    = {Zenodo},
  version      = {0.1.0},
  doi          = {10.5281/zenodo.7096002},
  url          = {https://doi.org/10.5281/zenodo.7096002}
}
```

### References
- Sebastián Ramírez, 2018, FastAPI, [https://github.com/tiangolo/fastapi](https://github.com/tiangolo/fastapi)
- Nils Reimers and Iryna Gurevych. 2019. Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks. In Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP), pages 3982–3992, Hong Kong, China. Association for Computational Linguistics. [http://dx.doi.org/10.18653/v1/D19-1410](http://dx.doi.org/10.18653/v1/D19-1410)

### Support
Please [open an issue](https://github.com/satzbeleg/simiscore-semantic/issues) for support. 


### Contributing
Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/satzbeleg/simiscore-semantic/compare/).


### Acknowledgements
The "Evidence" project was funded by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) - [433249742](https://gepris.dfg.de/gepris/projekt/433249742) (GU 798/27-1; GE 1119/11-1).

### Maintenance
- till 31.Aug.2023 (v0.1.0) the code repository was maintained within the DFG project [433249742](https://gepris.dfg.de/gepris/projekt/433249742)
- since 01.Sep.2023 (v0.2.0) the code repository is maintained by Ulf Hamster.
