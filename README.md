# HYDRANT

Hydrant is a consumer for Software Factory's Firehose. It aims at storing events
for later retrieval, allowing auditing.

## Running and testing

Hydrant is tested against and runs on python 2.7 and python 3.5.

Install the requirements like this:

```bash
pip install -r requirements.txt
```

And to start hydrant, run

```bash
hydrant -c /path/to/config/file.yaml
```

## The configuration file

Hydrant uses a yaml configuration file to define the mosquitto service to subscribe
to, and the backend to publish to. See etc/hydrant.yaml for an example.

## Contributing

Hydrant is developped in **Software Factory** and contributions follow a review workflow.

To contribute:

1. Log in once to Software Factory at https://softwarefactory-project.io
2. Set up your ssh key in Gerrit's settings page
3. Clone the project:
```bash
git clone ssh://<your_username>@softwarefactory-project.io:29418/software-factory/hydrant.git
```
4. Set up git review
```bash
cd hydrant && git review -s
```
5. Work on your feature, make a commit, then send the review
```bash
git commit -m'my feature' && git review
```
