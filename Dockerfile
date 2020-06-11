FROM pytorch/pytorch:latest

RUN apt-get update && apt-get upgrade -y && \
    apt-get install build-essential -y

# torch dependencies
RUN pip install transformers regex tqdm sentencepiece

# fastapi dependencies
COPY Pipfile* /
RUN pip install pipenv && \
    pipenv install --system --deploy


COPY api/ /api
# COPY config_default.yaml config_default.yaml
COPY Makefile /
WORKDIR /

ENTRYPOINT ["make", "serve"]
# ENTRYPOINT ["/bin/bash"]
