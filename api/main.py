#!/usr/bin/env python3
import argparse
import logging
import os
from datetime import datetime
import math
import uvicorn
import pytz
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from model_bert_base_ml_conll2002_ner import Model
from schemas import (
    outputSchema,
    inputSchema,
)


VERSION = 1
START_TIME = datetime.now(pytz.utc)

logger = logging.getLogger(__name__)
logger.setLevel(logging.getLevelName('INFO'))
logger.addHandler(logging.StreamHandler())

config = {
    'proxy_prefix': os.getenv('PROXY_PREFIX', '/'),
    'server': {
        'host': os.getenv('HOST', '127.0.0.1'),
        'port': int(os.getenv('PORT', '5000')),
        'log_level': os.getenv('LOG_LEVEL', 'info'),
        'timeout_keep_alive': 0,
    },
    'log_level': 'info',
}

app = FastAPI(openapi_prefix=config['proxy_prefix'])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL = Model()


# ############################################################### SERVER ROUTES
# #############################################################################
@app.get('/')
def root():
    """
    Query service status
    """
    now = datetime.now(pytz.utc)
    delta = now - START_TIME
    delta_s = math.floor(delta.total_seconds())
    return {
        'all_systems': 'nominal',
        'timestamp': now,
        'start_time': START_TIME,
        'uptime': f'{delta_s} seconds | {divmod(delta_s, 60)[0]} minutes | {divmod(delta_s, 86400)[0]} days',
        'api_version': VERSION,
    }


@app.post('/run', response_model=outputSchema)
def run(data: inputSchema):
    """
    Run Named Entity Recognition trained-model on provided document

    At this time only a single model is supported and provided
    """
    logger.debug("received query, length: %s", len(data.text))
    entities = [{'group': w, 'family': f} for w, f in MODEL.run(data.text, data.params) if w and f]
    entities = list({v['group']: v for v in entities}.values())
    logger.debug("Entities discovered: %s", entities)

    return {
        '_v': VERSION,
        '_timestamp': datetime.now(pytz.utc),
        'entities': entities,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Matching server process')
    parser.add_argument('--config', dest='config', help='config file', default=None)
    parser.add_argument('--debug', dest='debug', action='store_true', default=False, help='Debug mode')
    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.getLevelName('DEBUG'))
        logger.debug('Debug activated')
        config['log_level'] = 'debug'
        config['server']['log_level'] = 'debug'
        logger.debug('Arguments: %s', args)

    uvicorn.run(
        app,
        **config['server']
    )
