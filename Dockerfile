FROM pytorch/pytorch:latest

# torch dependencies
RUN pip install transformers regex tqdm sentencepiece

# fastapi dependencies
RUN pip install fastapi


COPY api/ /api
# COPY config_default.yaml config_default.yaml
COPY Makefile /

WORKDIR /

ENTRYPOINT ["make", "serve"]
# ENTRYPOINT ["/bin/bash"]
