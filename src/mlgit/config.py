"""
© Copyright 2020 HP Development Company, L.P.
SPDX-License-Identifier: GPL-2.0-only
"""

from mlgit.utils import getOrElse, yaml_load, yaml_save
import os

mlgit_config = {
    "mlgit_path": os.path.join(getOrElse(os.getenv, "MLGITROOT", "."), ".ml-git/"),
    "mlgit_conf": "config.yaml",

    "model": {
        "git": "ssh://git@github.com/standel/ml-git",
        "metadata": "ml-git/models/",
        "data": "ml-git/data/models",
    },
    "dataset": {
        "git": "ssh://git@github.com/standel/ml-datasets",
        "metadata": "ml-git/datasets/",
        "data": "ml-git/data/datasets/",
    },

    "store": {
        "ipfs": {
            "default": {
                "node": "127.0.0.1",
                "port": 5001,
            }
        },

        "s3": {
	        "ml-git-models": {
		        "region" : "us-east-1",
			    "aws-credentials" : { "profile" : "personal" }
	        },
            "mlgit": {
	            "aws-credentials": { "profile" : "personal" }

            }
        }
    },

    "auto_create_category": True,

    "verbose": "vvv",
}


def config_verbose():
    global mlgit_config
    try:
        return mlgit_config["verbose"]
    except:
        return None


def __get_subpath(relative_subpath):
    global mlgit_config
    return os.path.join(mlgit_config["mlgit_path"], relative_subpath)


def get_key(key, config=None):
    global mlgit_config

    conf = mlgit_config
    if config is not None: conf = config
    try:
        return getOrElse(conf, key, lambda: "")()
    except:
        return getOrElse(conf, key, "")


def __config_from_environment():
    global mlgit_config

    for key in mlgit_config.keys():
        val = os.getenv(key.upper())
        if val is not None: mlgit_config[key] = val


def __get_conf_filepath():
	#TODO: find root directory to find config file from subdirs.
	models_path = os.getenv("MLMODELS_PATH")
	if models_path is None: models_path = get_key("mlgit_path")
	return os.sep.join([models_path, get_key("mlgit_conf")])


def config_load():
    global mlgit_config

    config_file_path = __get_conf_filepath()
    actx = yaml_load(config_file_path)

    for key, value in actx.items():
        mlgit_config[key] = value

    __config_from_environment()

    return mlgit_config


# loads ml-git config.yaml file
def mlgit_config_load():
	mlgit_file = __get_conf_filepath()
	if os.path.exists(mlgit_file) == False:
		return {}

	return yaml_load(mlgit_file)

# saves initial config file in .ml-git/config.yaml
def mlgit_config_save():
    global mlgit_config

    mlgit_file = __get_conf_filepath()
    if os.path.exists(mlgit_file) == True:
        return

    config = {
        "dataset": mlgit_config["dataset"],
        "models": mlgit_config["model"],
        "store": mlgit_config["store"]
    }

    return yaml_save(config, mlgit_file)

def list_repos():
    global mlgit_config
    return mlgit_config["repos"].keys()


def repo_config(repo):
    global mlgit_config
    return mlgit_config["repos"][repo]
