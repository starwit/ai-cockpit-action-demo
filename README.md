# AI Cockpit Action Executor

This component is part of project AI Cockpit, [see here](https://github.com/starwit/ai-cockpit-deployment) for a an overview of all components.

Actions selected and defined by AI componets are approved in AI Cockpit. Thus in order to execute them, decisions made in AI Cockpit needs to be communicated into the system landscape, that executes whatever AI has proposed. 

Here is a sample implementation of all necessary functions, to forward AI Cockpit's decisions.

## What does it do
Service offers REST endpoints, to trigger actions and to feedback execution status.

## How to run locally
Service is written in Python and packaged in a Docker container. It is using Poetry package manager and to run application locally, use the following commands

```bash
    poetry install
    poetry shell
    uvicorn ai_cockpit_action_demo.main:app --reload
```

You can reach API via: http://localhost:8000/info

TODO Docker


## How to install

TODO
* Docker
* Helm/Helmfile
* Raspberry PI hardware config


## Contact & Contribution
This project was partly funded by the government of the federal republic of Germany. It is part of a research project aiming to keep _humans in command_ and is organized by the Federal Ministry of Labour and Social Affairs.

![BMAS](doc/BMAS_Logo.svg)

# License

Software in this repository is licensed under the AGPL-3.0 license. See [license agreement](LICENSE) for more details.