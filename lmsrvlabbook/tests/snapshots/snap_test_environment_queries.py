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

snapshots['TestEnvironmentServiceQueries.test_get_base 1'] = {
    'data': {
        'createLabbook': {
            'labbook': {
                'description': 'my test 1',
                'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2stYmFzZS10ZXN0',
                'name': 'labbook-base-test'
            }
        }
    }
}

snapshots['TestEnvironmentServiceQueries.test_get_base 2'] = {
    'data': {
        'labbook': {
            'description': 'my test 1',
            'environment': {
                'base': {
                    'componentId': 'quickstart-jupyterlab',
                    'description': 'Data Science Quickstart using Jupyterlab, numpy, and Matplotlib. A great base for any analysis.',
                    'developmentTools': [
                        'jupyterlab'
                    ],
                    'dockerImageNamespace': 'gigantum',
                    'dockerImageRepository': 'python3-minimal',
                    'dockerImageServer': 'hub.docker.com',
                    'dockerImageTag': '1effaaea-2018-05-23',
                    'icon': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=',
                    'id': 'QmFzZUNvbXBvbmVudDpnaWctZGV2X2NvbXBvbmVudHMyJnF1aWNrc3RhcnQtanVweXRlcmxhYiYy',
                    'languages': [
                        'python3'
                    ],
                    'license': 'MIT',
                    'name': 'Data Science Quickstart with JupyterLab',
                    'osClass': 'ubuntu',
                    'osRelease': '18.04',
                    'packageManagers': [
                        'apt',
                        'pip3'
                    ],
                    'readme': 'Empty for now',
                    'tags': [
                        'ubuntu',
                        'python3',
                        'jupyterlab'
                    ],
                    'url': None
                }
            },
            'name': 'labbook-base-test'
        }
    }
}

snapshots['TestEnvironmentServiceQueries.test_get_custom 1'] = {
    'data': {
        'labbook': {
            'environment': {
                'customDependencies': {
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

snapshots['TestEnvironmentServiceQueries.test_get_custom 2'] = {
    'data': {
        'labbook': {
            'environment': {
                'customDependencies': {
                    'edges': [
                        {
                            'cursor': 'MA==',
                            'node': {
                                'componentId': 'pillow',
                                'description': 'Pillow v4.2.1 for Ubuntu and Python3',
                                'dockerSnippet': '''RUN apt-get -y install libjpeg-dev libtiff5-dev zlib1g-dev libfreetype6-dev liblcms2-dev libopenjpeg-dev
RUN pip3 install Pillow==4.2.1
''',
                                'id': 'Q3VzdG9tQ29tcG9uZW50OmdpZy1kZXZfY29tcG9uZW50czImcGlsbG93JjA=',
                                'license': 'PIL Software License',
                                'name': 'Pillow',
                                'repository': 'gig-dev_components2',
                                'requiredPackageManagers': [
                                    'apt',
                                    'pip'
                                ],
                                'revision': 0,
                                'schema': 1,
                                'tags': [
                                    'ubuntu',
                                    'python',
                                    'python3',
                                    'image',
                                    'jpeg',
                                    'png'
                                ],
                                'url': 'http://pillow.readthedocs.io/en/4.2.1/'
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

snapshots['TestEnvironmentServiceQueries.test_get_package_manager 1'] = {
    'data': {
        'labbook': {
            'environment': {
                'packageDependencies': {
                    'edges': [
                    ],
                    'pageInfo': {
                        'hasNextPage': False
                    }
                }
            }
        }
    }
}

snapshots['TestEnvironmentServiceQueries.test_get_package_manager 3'] = {
    'data': {
        'labbook': {
            'environment': {
                'packageDependencies': {
                    'edges': [
                        {
                            'cursor': 'MQ==',
                            'node': {
                                'fromBase': False,
                                'id': 'UGFja2FnZUNvbXBvbmVudDphcHQmbHhtbCYzLjQ=',
                                'manager': 'apt',
                                'package': 'lxml',
                                'version': '3.4'
                            }
                        },
                        {
                            'cursor': 'Mg==',
                            'node': {
                                'fromBase': False,
                                'id': 'UGFja2FnZUNvbXBvbmVudDpwaXAmbnVtcHkmMS4xMg==',
                                'manager': 'pip',
                                'package': 'numpy',
                                'version': '1.12'
                            }
                        }
                    ],
                    'pageInfo': {
                        'hasNextPage': True
                    }
                }
            }
        }
    }
}

snapshots['TestEnvironmentServiceQueries.test_package_query_with_errors 1'] = {
    'data': {
        'labbook': {
            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2s1',
            'packages': [
                {
                    'id': 'UGFja2FnZUNvbXBvbmVudDpwaXAmbnVtcHkmMS4xNC4y',
                    'isValid': True,
                    'manager': 'pip',
                    'package': 'numpy',
                    'version': '1.14.2'
                },
                {
                    'id': 'UGFja2FnZUNvbXBvbmVudDpwaXAmcGxvdGx5JjEwMC4wMA==',
                    'isValid': False,
                    'manager': 'pip',
                    'package': 'plotly',
                    'version': '100.00'
                },
                {
                    'id': 'UGFja2FnZUNvbXBvbmVudDpwaXAmc2NpcHkmMS4xLjA=',
                    'isValid': True,
                    'manager': 'pip',
                    'package': 'scipy',
                    'version': '1.1.0'
                },
                {
                    'id': 'UGFja2FnZUNvbXBvbmVudDpwaXAmYXNkZmFzZGZhc2RmJg==',
                    'isValid': False,
                    'manager': 'pip',
                    'package': 'asdfasdfasdf',
                    'version': ''
                }
            ]
        }
    }
}

snapshots['TestEnvironmentServiceQueries.test_package_query 1'] = {
    'data': {
        'labbook': {
            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2s2',
            'packages': [
                {
                    'id': 'UGFja2FnZUNvbXBvbmVudDpwaXAmbnVtcHkmMS4xNC4y',
                    'isValid': True,
                    'manager': 'pip',
                    'package': 'numpy',
                    'version': '1.14.2'
                },
                {
                    'id': 'UGFja2FnZUNvbXBvbmVudDpwaXAmc2NpcHkmMS4xLjA=',
                    'isValid': True,
                    'manager': 'pip',
                    'package': 'scipy',
                    'version': '1.1.0'
                }
            ]
        }
    }
}

snapshots['TestEnvironmentServiceQueries.test_get_package_manager 2'] = {
    'data': {
        'labbook': {
            'environment': {
                'packageDependencies': {
                    'edges': [
                        {
                            'cursor': 'MA==',
                            'node': {
                                'fromBase': False,
                                'id': 'UGFja2FnZUNvbXBvbmVudDphcHQmZG9ja2VyJmxhdGVzdA==',
                                'manager': 'apt',
                                'package': 'docker',
                                'schema': 1,
                                'version': 'latest'
                            }
                        },
                        {
                            'cursor': 'MQ==',
                            'node': {
                                'fromBase': False,
                                'id': 'UGFja2FnZUNvbXBvbmVudDphcHQmbHhtbCYzLjQ=',
                                'manager': 'apt',
                                'package': 'lxml',
                                'schema': 1,
                                'version': '3.4'
                            }
                        },
                        {
                            'cursor': 'Mg==',
                            'node': {
                                'fromBase': False,
                                'id': 'UGFja2FnZUNvbXBvbmVudDpwaXAmbnVtcHkmMS4xMg==',
                                'manager': 'pip',
                                'package': 'numpy',
                                'schema': 1,
                                'version': '1.12'
                            }
                        },
                        {
                            'cursor': 'Mw==',
                            'node': {
                                'fromBase': False,
                                'id': 'UGFja2FnZUNvbXBvbmVudDpwaXAmcmVxdWVzdHMmMS4z',
                                'manager': 'pip',
                                'package': 'requests',
                                'schema': 1,
                                'version': '1.3'
                            }
                        }
                    ],
                    'pageInfo': {
                        'hasNextPage': False
                    }
                }
            }
        }
    }
}
