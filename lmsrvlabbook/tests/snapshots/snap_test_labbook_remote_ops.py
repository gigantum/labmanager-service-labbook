# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestLabBookRemoteOperations.test_list_remote_labbooks_az 1'] = {
    'data': {
        'labbookList': {
            'remoteLabbooks': {
                'edges': [
                    {
                        'cursor': 'MA==',
                        'node': {
                            'creationDateUtc': '2018-04-19T19:36:11.009Z',
                            'description': '',
                            'id': 'UmVtb3RlTGFiYm9vazp0ZXN0dXNlciZ0ZXN0Mg==',
                            'isLocal': False,
                            'modifiedDateUtc': '2018-04-19T20:58:05.974Z',
                            'name': 'test2',
                            'owner': 'testuser'
                        }
                    },
                    {
                        'cursor': 'MA==',
                        'node': {
                            'creationDateUtc': '2018-04-19T19:06:11.009Z',
                            'description': '',
                            'id': 'UmVtb3RlTGFiYm9vazp0ZXN0dXNlciZ0ZXN0MTE=',
                            'isLocal': False,
                            'modifiedDateUtc': '2018-04-19T22:08:05.974Z',
                            'name': 'test11',
                            'owner': 'testuser'
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

snapshots['TestLabBookRemoteOperations.test_list_remote_labbooks_az 2'] = {
    'data': {
        'labbookList': {
            'remoteLabbooks': {
                'edges': [
                    {
                        'cursor': 'MA==',
                        'node': {
                            'creationDateUtc': '2018-04-19T19:06:11.009Z',
                            'description': '',
                            'id': 'UmVtb3RlTGFiYm9vazp0ZXN0dXNlciZ0ZXN0MTE=',
                            'modifiedDateUtc': '2018-04-19T22:08:05.974Z',
                            'name': 'test11',
                            'owner': 'testuser'
                        }
                    },
                    {
                        'cursor': 'MA==',
                        'node': {
                            'creationDateUtc': '2018-04-19T19:36:11.009Z',
                            'description': '',
                            'id': 'UmVtb3RlTGFiYm9vazp0ZXN0dXNlciZ0ZXN0Mg==',
                            'modifiedDateUtc': '2018-04-19T20:58:05.974Z',
                            'name': 'test2',
                            'owner': 'testuser'
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

snapshots['TestLabBookRemoteOperations.test_list_remote_labbooks_invalid_args 1'] = {
    'data': {
        'labbookList': {
            'remoteLabbooks': None
        }
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 23,
                    'line': 4
                }
            ],
            'message': 'Unsupported order_by: asdf. Use `name`, `created_on`, `modified_on`',
            'path': [
                'labbookList',
                'remoteLabbooks'
            ]
        }
    ]
}

snapshots['TestLabBookRemoteOperations.test_list_remote_labbooks_invalid_args 2'] = {
    'data': {
        'labbookList': {
            'remoteLabbooks': None
        }
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 23,
                    'line': 4
                }
            ],
            'message': 'Unsupported sort_str: asdf. Use `desc`, `asc`',
            'path': [
                'labbookList',
                'remoteLabbooks'
            ]
        }
    ]
}

snapshots['TestLabBookRemoteOperations.test_list_remote_labbooks_modified 1'] = {
    'data': {
        'labbookList': {
            'remoteLabbooks': {
                'edges': [
                    {
                        'cursor': 'MA==',
                        'node': {
                            'creationDateUtc': '2018-04-19T19:06:11.009Z',
                            'description': '',
                            'id': 'UmVtb3RlTGFiYm9vazp0ZXN0dXNlciZ0ZXN0MTE=',
                            'isLocal': False,
                            'modifiedDateUtc': '2018-04-19T22:08:05.974Z',
                            'name': 'test11',
                            'owner': 'testuser'
                        }
                    },
                    {
                        'cursor': 'MA==',
                        'node': {
                            'creationDateUtc': '2018-04-19T19:36:11.009Z',
                            'description': '',
                            'id': 'UmVtb3RlTGFiYm9vazp0ZXN0dXNlciZ0ZXN0Mg==',
                            'isLocal': False,
                            'modifiedDateUtc': '2018-04-19T20:58:05.974Z',
                            'name': 'test2',
                            'owner': 'testuser'
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

snapshots['TestLabBookRemoteOperations.test_list_remote_labbooks_modified 2'] = {
    'data': {
        'labbookList': {
            'remoteLabbooks': {
                'edges': [
                    {
                        'cursor': 'MA==',
                        'node': {
                            'creationDateUtc': '2018-04-19T19:36:11.009Z',
                            'description': '',
                            'id': 'UmVtb3RlTGFiYm9vazp0ZXN0dXNlciZ0ZXN0Mg==',
                            'modifiedDateUtc': '2018-04-19T20:58:05.974Z',
                            'name': 'test2',
                            'owner': 'testuser'
                        }
                    },
                    {
                        'cursor': 'MA==',
                        'node': {
                            'creationDateUtc': '2018-04-19T19:06:11.009Z',
                            'description': '',
                            'id': 'UmVtb3RlTGFiYm9vazp0ZXN0dXNlciZ0ZXN0MTE=',
                            'modifiedDateUtc': '2018-04-19T22:08:05.974Z',
                            'name': 'test11',
                            'owner': 'testuser'
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

snapshots['TestLabBookRemoteOperations.test_list_remote_labbooks_created 1'] = {
    'data': {
        'labbookList': {
            'remoteLabbooks': {
                'edges': [
                    {
                        'cursor': 'MA==',
                        'node': {
                            'creationDateUtc': '2018-04-19T19:36:11.009Z',
                            'description': '',
                            'id': 'UmVtb3RlTGFiYm9vazp0ZXN0dXNlciZ0ZXN0Mg==',
                            'isLocal': False,
                            'modifiedDateUtc': '2018-04-19T20:58:05.974Z',
                            'name': 'test2',
                            'owner': 'testuser'
                        }
                    },
                    {
                        'cursor': 'MA==',
                        'node': {
                            'creationDateUtc': '2018-04-19T19:06:11.009Z',
                            'description': '',
                            'id': 'UmVtb3RlTGFiYm9vazp0ZXN0dXNlciZ0ZXN0MTE=',
                            'isLocal': False,
                            'modifiedDateUtc': '2018-04-19T22:08:05.974Z',
                            'name': 'test11',
                            'owner': 'testuser'
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

snapshots['TestLabBookRemoteOperations.test_list_remote_labbooks_created 2'] = {
    'data': {
        'labbookList': {
            'remoteLabbooks': {
                'edges': [
                    {
                        'cursor': 'MA==',
                        'node': {
                            'creationDateUtc': '2018-04-19T19:06:11.009Z',
                            'description': '',
                            'id': 'UmVtb3RlTGFiYm9vazp0ZXN0dXNlciZ0ZXN0MTE=',
                            'modifiedDateUtc': '2018-04-19T22:08:05.974Z',
                            'name': 'test11',
                            'owner': 'testuser'
                        }
                    },
                    {
                        'cursor': 'MA==',
                        'node': {
                            'creationDateUtc': '2018-04-19T19:36:11.009Z',
                            'description': '',
                            'id': 'UmVtb3RlTGFiYm9vazp0ZXN0dXNlciZ0ZXN0Mg==',
                            'modifiedDateUtc': '2018-04-19T20:58:05.974Z',
                            'name': 'test2',
                            'owner': 'testuser'
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

snapshots['TestLabBookRemoteOperations.test_list_remote_labbooks_page 1'] = {
    'data': {
        'labbookList': {
            'remoteLabbooks': {
                'edges': [
                    {
                        'cursor': 'MA==',
                        'node': {
                            'creationDateUtc': '2018-04-19T19:36:11.009Z',
                            'description': '',
                            'id': 'UmVtb3RlTGFiYm9vazp0ZXN0dXNlciZ0ZXN0Mg==',
                            'isLocal': False,
                            'modifiedDateUtc': '2018-04-19T20:58:05.974Z',
                            'name': 'test2',
                            'owner': 'testuser'
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

snapshots['TestLabBookRemoteOperations.test_list_remote_labbooks_page 2'] = {
    'data': {
        'labbookList': {
            'remoteLabbooks': {
                'edges': [
                    {
                        'cursor': 'MQ==',
                        'node': {
                            'creationDateUtc': '2018-04-19T19:06:11.009Z',
                            'description': '',
                            'id': 'UmVtb3RlTGFiYm9vazp0ZXN0dXNlciZ0ZXN0MTE=',
                            'modifiedDateUtc': '2018-04-19T22:08:05.974Z',
                            'name': 'test11',
                            'owner': 'testuser'
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
