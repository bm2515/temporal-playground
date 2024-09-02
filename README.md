# Temporal Example Python Project

## Original Repository

This repository is originally forked from [Temporal Money Transfer Example](https://github.com/temporalio/money-transfer-project-template-python).


To use this code, make sure you have a [Temporal Cluster running](https://learn.temporal.io/getting_started/python/dev_environment/) first.

Clone this repo and run this application.

```bash
git clone https://github.com/bm2515/temporal-playground.git
cd temporal-playground
```

Create a virtual environment and activate it. On macOS and Linux, run these commands:

```
python3 -m venv env
source env/bin/activate
```

On Windows, run these commands:

```
python -m venv env
env\Scripts\activate
```

With the virtual environment configured, install the Temporal SDK:

```
python -m pip install temporalio
```

Set up a local Temporal Service for development with Temporal CLI:

```
brew install temporal
```

Once you've installed Temporal CLU and added it to your PATH, open a new terminal window and run:

```
temporal server start-dev
```

The Temporal Service will be available on localhost:7233.
The Temporal Web UI will be available at http://localhost:8233.

Run the workflow:

```bash
python run_workflow.py
```

In another window, activate the virtual environment:

On macOS or Linux, run this command:

```
source env/bin/activate
```

On Windows, run this command:

```
env\Scripts\activate
```


Then run the worker:


```bash
python run_worker.py
```

Please [read the tutorial](https://learn.temporal.io/getting_started/python/first_program_in_python/) for more details.
