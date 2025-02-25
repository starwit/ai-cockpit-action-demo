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
    export SERVICE_URI=http://ip:8000 # if you want to access from outside, default is localhost
    python ai_cockpit_action_demo/main.py
```

You can reach API via: http://localhost:8000/docs (or http://ip:8000/docs)

Following Docker command runs executor on a Raspberry Pi (4 or newer, or you retire while waiting)
```bash
    docker run -it --device /dev/gpiochip0  -e SERVICE_URI=http://ip:8000 -p 8000:8000  --rm starwitorg/ai-cockpit-action-demo:0.0.8
```

Without hardware connection, app will run with the following command.
```bash
    docker run -it -e SERVICE_URI=http://ip:8000 -p 8000:8000  --rm starwitorg/ai-cockpit-action-demo:0.0.8
```


## How to install to Kubernetes

App can also be deployed to a Kubernetes cluster. Helm chart is located [here](https://hub.docker.com/r/starwitorg/ai-cockpit-action-demo-chart). See there for instructions how to deploy app.


## Contact & Contribution
This project was partly funded by the government of the federal republic of Germany. It is part of a research project aiming to keep _humans in command_ and is organized by the Federal Ministry of Labour and Social Affairs.

![BMAS](doc/BMAS_Logo.svg)

# License

Software in this repository is licensed under the AGPL-3.0 license. See [license agreement](LICENSE) for more details.