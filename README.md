## Machine-learning assisted data pseudonymiser

Pseudonymisation par des modèles IA préentrainés de type [BERT](https://ai.googleblog.com/2018/11/open-sourcing-bert-state-of-art-pre.html), à travers une API python.

Le service utilise [pytorch](https://pytorch.org/) et les transformateurs de [huggingface](https://huggingface.co/) afin de fournir une fonctionnalité NER (Named Entity Recognition), en d'autres termes l'identification et la classification d'entités, sur base d'un texte fourni.

L'API est documenté par OpenAPI.

## Usage
Exemple de déploiement local avec docker:
```bash
docker build -t "anon_bert" ./  && docker run --rm -it -p5000:5000 -e HOST=0.0.0.0 anon_bert
```

Une fois deployé, les URL suivantes sont accessibles:

* [http://localhost:5000](http://localhost:5000) : racine de l'API
* [http://localhost:5000/docs](http://localhost:5000/docs) : documentation OpenAPI

