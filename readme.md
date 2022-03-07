# Turkish Movie Search Engine

<br>

<p style="text-align:center">
<img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" width="200" > 
<img src="https://plugins.jetbrains.com/files/16111/151977/icon/pluginIcon.png" width="100">
<img src="https://www.bujarra.com/wp-content/uploads/2018/11/kibana0.jpg" width="100" >
<img src="https://devnot.com/wp-content/uploads/2017/09/docker-compose.jpg" width="200" >

</p>
<br>
<br> 
<center>

![](https://im2.ezgif.com/tmp/ezgif-2-d2bcaa85eb.gif)
</center>

Code contains a template for using FastAPI backend with Elasticsearch & Kibana.

Data source: [Turkish Movie Sentiment Analysis Dataset](https://www.kaggle.com/mustfkeskin/turkish-movie-sentiment-analysis-dataset)
* I just selected unique movie names.

## Installation

There are only two prerequisites:

* [Docker](https://docs.docker.com/get-docker/)
* [Docker-compose](https://docs.docker.com/compose/install/)

<br>

``` bash
git clone https://github.com/silverstone1903/autocomplete-search-fastapi-es-kibana
```

## Usage
### Start 

``` bash
docker-compose up -d
```

If you make any changes you can add `--build`. 

``` bash
docker-compose up --build -d
``` 

### Stopping containers

``` bash
docker-compose down
```
### Container Logs
When running containers with detached mode (`-d`) they work in the background thus you can't see the flowing logs. If you want to check compose logs with cli you can use `logs`.

``` bash
docker-compose logs --tail 50
```

* FastAPI (UI): http://localhost:8000
* Elasticsearch: http://localhost:9200
* Kibana: http://localhost:5601

# Tests

If you want to run the tests inside the container;

```bash
docker-compose exec web pytest tests -sv
```


# Sources
* [DataAPI](https://github.com/naciyuksel/DataAPI)
* [Fast Autocomplete Search for Your Website](https://github.com/simonw/24ways-datasette)
* [Elastic.co](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-lang-analyzer.html#turkish-analyzer)
