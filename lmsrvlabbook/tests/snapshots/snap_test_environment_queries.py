# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestEnvironmentServiceQueries.test_get_environment_status 1'] = {
    'data': {
        'labbook': {
            'environment': {
                'containerStatus': 'NOT_RUNNING',
                'imageStatus': 'DOES_NOT_EXIST'
            }
        }
    }
}

snapshots['TestEnvironmentServiceQueries.test_get_base_image 1'] = {
    'data': {
        'labbook': {
            'environment': {
                'baseImage': None
            }
        }
    }
}

snapshots['TestEnvironmentServiceQueries.test_get_base_image 2'] = {
    'data': {
        'labbook': {
            'environment': {
                'baseImage': {
                    'author': {
                        'organization': 'Aperture Science'
                    },
                    'availablePackageManagers': [
                        'pip3',
                        'apt-get'
                    ],
                    'component': {
                        'componentClass': 'base_image',
                        'name': 'ubuntu1604-python3',
                        'namespace': 'gigantum',
                        'repository': 'gig-dev_environment-components',
                        'version': '0.4'
                    },
                    'id': 'QmFzZUltYWdlOmJhc2VfaW1hZ2UmZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJnVidW50dTE2MDQtcHl0aG9uMyYwLjQ=',
                    'info': {
                        'humanName': 'Ubuntu 16.04 Python 3 Developer',
                        'name': 'ubuntu1604-python3',
                        'versionMajor': 0,
                        'versionMinor': 4
                    },
                    'server': 'hub.docker.com',
                    'tag': '7a7c9d41-2017-08-03'
                }
            }
        }
    }
}

snapshots['TestEnvironmentServiceQueries.test_get_dev_env 1'] = {
    'data': {
        'labbook': {
            'environment': {
                'devEnvs': {
                    'edges': [
                    ],
                    'pageInfo': {
                        'hasNextPage': False,
                        'hasPreviousPage': False
                    }
                }
            }
        }
    }
}

snapshots['TestEnvironmentServiceQueries.test_get_dev_env 2'] = {
    'data': {
        'labbook': {
            'environment': {
                'devEnvs': {
                    'edges': [
                        {
                            'cursor': 'MA==',
                            'node': {
                                'author': {
                                    'organization': 'Strange Science Laboratories'
                                },
                                'component': {
                                    'componentClass': 'dev_env',
                                    'name': 'jupyter-ubuntu',
                                    'namespace': 'gigantum',
                                    'repository': 'gig-dev_environment-components',
                                    'version': '0.1'
                                },
                                'developmentEnvironmentClass': 'web',
                                'execCommands': [
                                    "jupyter notebook --ip=0.0.0.0 --NotebookApp.token='' --no-browser"
                                ],
                                'exposedTcpPorts': [
                                    '8000',
                                    '8888'
                                ],
                                'id': 'RGV2RW52OmRldl9lbnYmZ2lnLWRldl9lbnZpcm9ubWVudC1jb21wb25lbnRzJmdpZ2FudHVtJmp1cHl0ZXItdWJ1bnR1JjAuMQ==',
                                'info': {
                                    'humanName': 'Python 3 Jupyter Notebook for Ubuntu',
                                    'name': 'jupyter-ubuntu',
                                    'versionMajor': 0,
                                    'versionMinor': 1
                                },
                                'installCommands': [
                                    'pip3 install jupyter'
                                ],
                                'osBaseClass': 'ubuntu'
                            }
                        }
                    ],
                    'pageInfo': {
                        'hasNextPage': False,
                        'hasPreviousPage': False
                    }
                }
            }
        }
    }
}
