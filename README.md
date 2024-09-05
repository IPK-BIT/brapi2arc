# BrAPI2ARC

[![Documentation Status](https://readthedocs.org/projects/brapi2arc/badge/?version=latest)](https://brapi2arc.readthedocs.io/?badge=latest)
![License](https://img.shields.io/github/license/IPK-BIT/brapi2arc)

## Description

This API allows researchers to submit phenotyping observations to a dataset stored as an Annotated Research Context (ARC). The ARC provides a standardized structure for capturing and sharing research data, enabling reproducibility and transparency in scientific investigations.

## Installation

The brapi2arc tool is offered as a docker container. To install it start a new container with the environment variables `ARC_URI`, `DATAHUB_URL` and `DATAHUB_TOKEN` set.

```sh
docker run -e ARC_URI=<ARC_URI_VALUE> -e DATAHUB_URL=<DATAHUB_URL_VALUE> -e DATAHUB_TOKEN=<DATAHUB_TOKEN_VALUE> -p 8000:8000 ghcr.io/ipk-bit/brapi2arc
```

Or using docker compose.

```yml
services:
  brapi2arc:
    image: ghcr.io/ipk-bit/brapi2arc
    ports:
      - 8000:8000
    environment:
      - ARC_URI='<YOUR ARC URI>'
      - DATAHUB_URL='<YOUR DATAHUB URL>'
      - DATAHUB_TOKEN='<YOUR PERSONAL ACCESS TOKEN>'
```

## Usage

There is a tutorial on how to use brapi2arc in the [documentation](https://brapi2arc.readthedocs.io/en/latest/simple_example/). The basic idea is that this tool acts as a converter that takes phenotypic observations through the BrAPI interface and writes them to an ARC. This allows the automation of the data import into ARCs from every observation scoring application that is BrAPI enabled.
