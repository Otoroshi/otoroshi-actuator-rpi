Raspberry Pi Actuator
=====================

Setting up a dev environment
----------------------------

After cloning the repository make sure to install a virtual env as follow :

```
virtualenv .venv
```

To start using the environment use ``source .venv/bin/activate`` (and ``deactivate`` to quit it). To install the required dependencies you need to run pip install :

```
pip install -r requirements.txt
```

A config file need to be created, an example is provided (**config.dist.ini**).

To run the server, use the provided script as follow :
```
# Run the server
env OTOROSHI_RPI_CONFIG=./config.ini.dist ./actuator-rpi
```
