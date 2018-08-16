# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestLabBookServiceQueries.test_pagination_noargs 1'] = {
    'data': {
        'labbookList': {
            'localLabbooks': {
                'edges': [
                    {
                        'cursor': 'MA==',
                        'node': {
                            'description': 'Cats labbook 1',
                            'name': 'labbook1'
                        }
                    },
                    {
                        'cursor': 'MQ==',
                        'node': {
                            'description': 'Dogs labbook 2',
                            'name': 'labbook2'
                        }
                    },
                    {
                        'cursor': 'Mg==',
                        'node': {
                            'description': 'Mice labbook 3',
                            'name': 'labbook3'
                        }
                    },
                    {
                        'cursor': 'Mw==',
                        'node': {
                            'description': 'Horses labbook 4',
                            'name': 'labbook4'
                        }
                    },
                    {
                        'cursor': 'NA==',
                        'node': {
                            'description': 'Cheese labbook 5',
                            'name': 'labbook5'
                        }
                    },
                    {
                        'cursor': 'NQ==',
                        'node': {
                            'description': 'Goat labbook 6',
                            'name': 'labbook6'
                        }
                    },
                    {
                        'cursor': 'Ng==',
                        'node': {
                            'description': 'Turtle labbook 7',
                            'name': 'labbook7'
                        }
                    },
                    {
                        'cursor': 'Nw==',
                        'node': {
                            'description': 'Lamb labbook 8',
                            'name': 'labbook8'
                        }
                    },
                    {
                        'cursor': 'OA==',
                        'node': {
                            'description': 'Taco labbook 9',
                            'name': 'labbook9'
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

snapshots['TestLabBookServiceQueries.test_pagination_first_only 1'] = {
    'data': {
        'labbookList': {
            'localLabbooks': {
                'edges': [
                    {
                        'cursor': 'MA==',
                        'node': {
                            'description': 'Cats labbook 1',
                            'name': 'labbook1'
                        }
                    },
                    {
                        'cursor': 'MQ==',
                        'node': {
                            'description': 'Dogs labbook 2',
                            'name': 'labbook2'
                        }
                    },
                    {
                        'cursor': 'Mg==',
                        'node': {
                            'description': 'Mice labbook 3',
                            'name': 'labbook3'
                        }
                    }
                ],
                'pageInfo': {
                    'hasNextPage': True,
                    'hasPreviousPage': False
                }
            }
        }
    }
}

snapshots['TestLabBookServiceQueries.test_pagination_first_and_after 1'] = {
    'data': {
        'labbookList': {
            'localLabbooks': {
                'edges': [
                    {
                        'cursor': 'Mw==',
                        'node': {
                            'description': 'Horses labbook 4',
                            'name': 'labbook4'
                        }
                    },
                    {
                        'cursor': 'NA==',
                        'node': {
                            'description': 'Cheese labbook 5',
                            'name': 'labbook5'
                        }
                    },
                    {
                        'cursor': 'NQ==',
                        'node': {
                            'description': 'Goat labbook 6',
                            'name': 'labbook6'
                        }
                    },
                    {
                        'cursor': 'Ng==',
                        'node': {
                            'description': 'Turtle labbook 7',
                            'name': 'labbook7'
                        }
                    }
                ],
                'pageInfo': {
                    'endCursor': 'Ng==',
                    'hasNextPage': True,
                    'hasPreviousPage': False,
                    'startCursor': 'Mw=='
                }
            }
        }
    }
}

snapshots['TestLabBookServiceQueries.test_pagination_first_and_after 2'] = {
    'data': {
        'labbookList': {
            'localLabbooks': {
                'edges': [
                    {
                        'cursor': 'Nw==',
                        'node': {
                            'description': 'Lamb labbook 8',
                            'name': 'labbook8'
                        }
                    },
                    {
                        'cursor': 'OA==',
                        'node': {
                            'description': 'Taco labbook 9',
                            'name': 'labbook9'
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

snapshots['TestLabBookServiceQueries.test_pagination_first_and_after 3'] = {
    'data': {
        'labbookList': {
            'localLabbooks': {
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

snapshots['TestLabBookServiceQueries.test_pagination_last_only 1'] = {
    'data': {
        'labbookList': {
            'localLabbooks': {
                'edges': [
                    {
                        'cursor': 'Ng==',
                        'node': {
                            'description': 'Turtle labbook 7',
                            'name': 'labbook7'
                        }
                    },
                    {
                        'cursor': 'Nw==',
                        'node': {
                            'description': 'Lamb labbook 8',
                            'name': 'labbook8'
                        }
                    },
                    {
                        'cursor': 'OA==',
                        'node': {
                            'description': 'Taco labbook 9',
                            'name': 'labbook9'
                        }
                    }
                ],
                'pageInfo': {
                    'hasNextPage': False,
                    'hasPreviousPage': True
                }
            }
        }
    }
}

snapshots['TestLabBookServiceQueries.test_pagination_last_and_before 1'] = {
    'data': {
        'labbookList': {
            'localLabbooks': {
                'edges': [
                    {
                        'cursor': 'NA==',
                        'node': {
                            'description': 'Cheese labbook 5',
                            'name': 'labbook5'
                        }
                    },
                    {
                        'cursor': 'NQ==',
                        'node': {
                            'description': 'Goat labbook 6',
                            'name': 'labbook6'
                        }
                    },
                    {
                        'cursor': 'Ng==',
                        'node': {
                            'description': 'Turtle labbook 7',
                            'name': 'labbook7'
                        }
                    }
                ],
                'pageInfo': {
                    'hasNextPage': False,
                    'hasPreviousPage': True
                }
            }
        }
    }
}

snapshots['TestLabBookServiceQueries.test_pagination_last_and_before 2'] = {
    'data': {
        'labbookList': {
            'localLabbooks': {
                'edges': [
                    {
                        'cursor': 'MA==',
                        'node': {
                            'description': 'Cats labbook 1',
                            'name': 'labbook1'
                        }
                    }
                ],
                'pageInfo': {
                    'endCursor': 'MA==',
                    'hasNextPage': False,
                    'hasPreviousPage': False,
                    'startCursor': 'MA=='
                }
            }
        }
    }
}

snapshots['TestLabBookServiceQueries.test_pagination_last_and_before 3'] = {
    'data': {
        'labbookList': {
            'localLabbooks': {
                'edges': [
                ],
                'pageInfo': {
                    'endCursor': None,
                    'hasNextPage': False,
                    'hasPreviousPage': False,
                    'startCursor': None
                }
            }
        }
    }
}

snapshots['TestLabBookServiceQueries.test_pagination 1'] = {
    'data': {
        'labbookList': {
            'localLabbooks': {
                'edges': [
                    {
                        'cursor': 'Mg==',
                        'node': {
                            'description': 'Mice labbook 3',
                            'name': 'labbook3'
                        }
                    },
                    {
                        'cursor': 'Mw==',
                        'node': {
                            'description': 'Horses labbook 4',
                            'name': 'labbook4'
                        }
                    }
                ],
                'pageInfo': {
                    'hasNextPage': True,
                    'hasPreviousPage': False
                }
            }
        }
    }
}

snapshots['TestLabBookServiceQueries.test_pagination 2'] = {
    'data': {
        'labbookList': {
            'localLabbooks': {
                'edges': [
                    {
                        'cursor': 'NA==',
                        'node': {
                            'description': 'Cheese labbook 5',
                            'name': 'labbook5'
                        }
                    },
                    {
                        'cursor': 'NQ==',
                        'node': {
                            'description': 'Goat labbook 6',
                            'name': 'labbook6'
                        }
                    }
                ],
                'pageInfo': {
                    'hasNextPage': False,
                    'hasPreviousPage': True
                }
            }
        }
    }
}

snapshots['TestLabBookServiceQueries.test_list_labbooks_container_status 1'] = {
    'data': {
        'labbookList': {
            'localLabbooks': {
                'edges': [
                    {
                        'cursor': 'MA==',
                        'node': {
                            'description': 'my first labbook1',
                            'environment': {
                                'containerStatus': 'NOT_RUNNING',
                                'imageStatus': 'DOES_NOT_EXIST'
                            },
                            'name': 'labbook1'
                        }
                    },
                    {
                        'cursor': 'MQ==',
                        'node': {
                            'description': 'my first labbook2',
                            'environment': {
                                'containerStatus': 'NOT_RUNNING',
                                'imageStatus': 'DOES_NOT_EXIST'
                            },
                            'name': 'labbook2'
                        }
                    }
                ]
            }
        }
    }
}

snapshots['TestLabBookServiceQueries.test_list_labbooks_container_status_no_labbooks 1'] = {
    'data': {
        'labbookList': {
            'localLabbooks': {
                'edges': [
                ]
            }
        }
    }
}

snapshots['TestLabBookServiceQueries.test_list_files_code 1'] = {
    'data': {
        'labbook': {
            'code': {
                'files': {
                    'edges': [
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJnNyYy8=',
                                'isDir': True,
                                'key': 'src/',
                                'size': '0'
                            }
                        },
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJnRlc3RfZmlsZTEudHh0',
                                'isDir': False,
                                'key': 'test_file1.txt',
                                'size': '6'
                            }
                        },
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJnRlc3RfZmlsZTIudHh0',
                                'isDir': False,
                                'key': 'test_file2.txt',
                                'size': '15'
                            }
                        }
                    ]
                }
            },
            'name': 'labbook1'
        }
    }
}

snapshots['TestLabBookServiceQueries.test_list_files_code 2'] = {
    'data': {
        'labbook': {
            'code': {
                'files': {
                    'edges': [
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJnNyYy9qcy8=',
                                'isDir': True,
                                'key': 'src/js/',
                                'size': '0'
                            }
                        },
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJnNyYy90ZXN0LnB5',
                                'isDir': False,
                                'key': 'src/test.py',
                                'size': '21'
                            }
                        }
                    ]
                }
            },
            'name': 'labbook1'
        }
    }
}

snapshots['TestLabBookServiceQueries.test_list_files_code 3'] = {
    'data': {
        'labbook': {
            'code': {
                'files': {
                    'edges': [
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJnNyYy9qcy8=',
                                'isDir': True,
                                'key': 'src/js/',
                                'size': '0'
                            }
                        },
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJnNyYy90ZXN0LnB5',
                                'isDir': False,
                                'key': 'src/test.py',
                                'size': '21'
                            }
                        }
                    ]
                }
            },
            'name': 'labbook1'
        }
    }
}

snapshots['TestLabBookServiceQueries.test_list_files_many 1'] = {
    'data': {
        'labbook': {
            'code': {
                'files': {
                    'edges': [
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJnRlc3RfZmlsZTEudHh0',
                                'isDir': False,
                                'key': 'test_file1.txt',
                                'size': '6'
                            }
                        },
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJnRlc3RfZmlsZTIudHh0',
                                'isDir': False,
                                'key': 'test_file2.txt',
                                'size': '15'
                            }
                        }
                    ]
                }
            },
            'input': {
                'files': {
                    'edges': [
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZpbnB1dCZzdWJkaXIv',
                                'isDir': True,
                                'key': 'subdir/',
                                'size': '0'
                            }
                        }
                    ]
                }
            },
            'name': 'labbook1',
            'output': {
                'files': {
                    'edges': [
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZvdXRwdXQmZW1wdHkv',
                                'isDir': True,
                                'key': 'empty/',
                                'size': '0'
                            }
                        },
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZvdXRwdXQmcmVzdWx0LmRhdA==',
                                'isDir': False,
                                'key': 'result.dat',
                                'size': '3'
                            }
                        }
                    ]
                }
            }
        }
    }
}

snapshots['TestLabBookServiceQueries.test_list_files_many 2'] = {
    'data': {
        'labbook': {
            'code': {
                'files': {
                    'edges': [
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJnRlc3RfZmlsZTEudHh0',
                                'isDir': False,
                                'key': 'test_file1.txt',
                                'size': '6'
                            }
                        },
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJnRlc3RfZmlsZTIudHh0',
                                'isDir': False,
                                'key': 'test_file2.txt',
                                'size': '15'
                            }
                        }
                    ]
                }
            },
            'input': {
                'files': {
                    'edges': [
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZpbnB1dCZzdWJkaXIvZGF0YS5kYXQ=',
                                'isDir': False,
                                'key': 'subdir/data.dat',
                                'size': '12'
                            }
                        },
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZpbnB1dCZzdWJkaXIvZGF0YS8=',
                                'isDir': True,
                                'key': 'subdir/data/',
                                'size': '0'
                            }
                        }
                    ]
                }
            },
            'name': 'labbook1',
            'output': {
                'files': {
                    'edges': [
                    ]
                }
            }
        }
    }
}

snapshots['TestLabBookServiceQueries.test_list_all_files_many 1'] = {
    'data': {
        'labbook': {
            'code': {
                'allFiles': {
                    'edges': [
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJnRlc3RfZmlsZTEudHh0',
                                'isDir': False,
                                'key': 'test_file1.txt',
                                'size': '6'
                            }
                        },
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJnRlc3RfZmlsZTIudHh0',
                                'isDir': False,
                                'key': 'test_file2.txt',
                                'size': '15'
                            }
                        }
                    ]
                }
            },
            'input': {
                'allFiles': {
                    'edges': [
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZpbnB1dCZzdWJkaXIv',
                                'isDir': True,
                                'key': 'subdir/',
                                'size': '0'
                            }
                        },
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZpbnB1dCZzdWJkaXIvZGF0YS8=',
                                'isDir': True,
                                'key': 'subdir/data/',
                                'size': '0'
                            }
                        },
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZpbnB1dCZzdWJkaXIvZGF0YS5kYXQ=',
                                'isDir': False,
                                'key': 'subdir/data.dat',
                                'size': '12'
                            }
                        }
                    ]
                }
            },
            'name': 'labbook1',
            'output': {
                'allFiles': {
                    'edges': [
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZvdXRwdXQmZW1wdHkv',
                                'isDir': True,
                                'key': 'empty/',
                                'size': '0'
                            }
                        },
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZvdXRwdXQmcmVzdWx0LmRhdA==',
                                'isDir': False,
                                'key': 'result.dat',
                                'size': '3'
                            }
                        }
                    ]
                }
            }
        }
    }
}

snapshots['TestLabBookServiceQueries.test_get_activity_records_reverse_error 1'] = {
    'data': {
        'labbook': {
            'activityRecords': None,
            'description': 'my first labbook1',
            'name': 'labbook12'
        }
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 13,
                    'line': 6
                }
            ],
            'message': 'Only `after` and `first` arguments are supported when paging activity records',
            'path': [
                'labbook',
                'activityRecords'
            ]
        }
    ]
}

snapshots['TestLabBookServiceQueries.test_get_activity_records_reverse_error 2'] = {
    'data': {
        'labbook': {
            'activityRecords': None,
            'description': 'my first labbook1',
            'name': 'labbook12'
        }
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 13,
                    'line': 6
                }
            ],
            'message': 'Only `after` and `first` arguments are supported when paging activity records',
            'path': [
                'labbook',
                'activityRecords'
            ]
        }
    ]
}

snapshots['TestLabBookServiceQueries.test_get_activity_records_reverse_error 3'] = {
    'data': {
        'labbook': {
            'activityRecords': None,
            'description': 'my first labbook1',
            'name': 'labbook12'
        }
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 13,
                    'line': 6
                }
            ],
            'message': 'Only `after` and `first` arguments are supported when paging activity records',
            'path': [
                'labbook',
                'activityRecords'
            ]
        }
    ]
}

snapshots['TestLabBookServiceQueries.test_get_detail_record 1'] = {
    'data': {
        'labbook': {
            'description': 'my test description',
            'detailRecord': {
                'data': [
                    [
                        'text/plain',
                        'Added new Code file code/test_file.txt'
                    ]
                ],
                'importance': 0,
                'show': False,
                'tags': [
                ],
                'type': 'CODE'
            },
            'name': 'labbook11'
        }
    }
}

snapshots['TestLabBookServiceQueries.test_get_activity_records_next_page 1'] = {
    'data': {
        'createLabbook': {
            'labbook': {
                'description': 'my test 1',
                'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2stcGFnZS10ZXN0',
                'name': 'labbook-page-test'
            }
        }
    }
}

snapshots['TestLabBookServiceQueries.test_get_activity_records 1'] = {
    'data': {
        'labbook': {
            'activityRecords': {
                'edges': [
                    {
                        'node': {
                            'importance': 255,
                            'message': 'Added new Output Data file output/test_file.txt',
                            'show': True,
                            'tags': [
                                '.txt'
                            ],
                            'type': 'OUTPUT_DATA'
                        }
                    }
                ],
                'pageInfo': {
                    'hasNextPage': True,
                    'hasPreviousPage': False
                }
            },
            'description': 'my test description',
            'name': 'labbook11'
        }
    }
}

snapshots['TestLabBookServiceQueries.test_get_activity_records 2'] = {
    'data': {
        'labbook': {
            'activityRecords': {
                'edges': [
                    {
                        'node': {
                            'email': 'tester@test.com',
                            'importance': 255,
                            'message': 'Added new Input Data file input/test_file.txt',
                            'show': True,
                            'tags': [
                                '.txt'
                            ],
                            'type': 'INPUT_DATA',
                            'username': 'tester'
                        }
                    },
                    {
                        'node': {
                            'email': 'tester@test.com',
                            'importance': 255,
                            'message': 'Added new Code file code/test_file.txt',
                            'show': True,
                            'tags': [
                                '.txt'
                            ],
                            'type': 'CODE',
                            'username': 'tester'
                        }
                    }
                ],
                'pageInfo': {
                    'hasNextPage': True,
                    'hasPreviousPage': False
                }
            },
            'description': 'my test description',
            'name': 'labbook11'
        }
    }
}

snapshots['TestLabBookServiceQueries.test_get_activity_records 3'] = {
    'data': {
        'labbook': {
            'activityRecords': {
                'edges': [
                    {
                        'node': {
                            'importance': 255,
                            'message': 'Added new Code file code/test_file.txt',
                            'show': True,
                            'tags': [
                                '.txt'
                            ],
                            'type': 'CODE'
                        }
                    }
                ],
                'pageInfo': {
                    'hasNextPage': True,
                    'hasPreviousPage': False
                }
            },
            'description': 'my test description',
            'name': 'labbook11'
        }
    }
}

snapshots['TestLabBookServiceQueries.test_get_activity_records 4'] = {
    'data': {
        'labbook': {
            'activityRecords': {
                'edges': [
                ],
                'pageInfo': {
                    'hasNextPage': False,
                    'hasPreviousPage': False
                }
            },
            'description': 'my test description',
            'name': 'labbook11'
        }
    }
}

snapshots['TestLabBookServiceQueries.test_get_activity_records_with_details 1'] = {
    'data': {
        'labbook': {
            'activityRecords': {
                'edges': [
                    {
                        'node': {
                            'detailObjects': [
                                {
                                    'action': 'CREATE',
                                    'data': [
                                        [
                                            'text/plain',
                                            'Added new Output Data file output/test_file.txt'
                                        ]
                                    ],
                                    'importance': 0,
                                    'show': False,
                                    'tags': [
                                    ],
                                    'type': 'OUTPUT_DATA'
                                }
                            ],
                            'importance': 255,
                            'message': 'Added new Output Data file output/test_file.txt',
                            'show': True,
                            'tags': [
                                '.txt'
                            ],
                            'type': 'OUTPUT_DATA'
                        }
                    },
                    {
                        'node': {
                            'detailObjects': [
                                {
                                    'action': 'CREATE',
                                    'data': [
                                        [
                                            'text/plain',
                                            'Added new Input Data file input/test_file.txt'
                                        ]
                                    ],
                                    'importance': 0,
                                    'show': False,
                                    'tags': [
                                    ],
                                    'type': 'INPUT_DATA'
                                }
                            ],
                            'importance': 255,
                            'message': 'Added new Input Data file input/test_file.txt',
                            'show': True,
                            'tags': [
                                '.txt'
                            ],
                            'type': 'INPUT_DATA'
                        }
                    },
                    {
                        'node': {
                            'detailObjects': [
                                {
                                    'action': 'CREATE',
                                    'data': [
                                        [
                                            'text/plain',
                                            'Added new Code file code/test_file.txt'
                                        ]
                                    ],
                                    'importance': 0,
                                    'show': False,
                                    'tags': [
                                    ],
                                    'type': 'CODE'
                                }
                            ],
                            'importance': 255,
                            'message': 'Added new Code file code/test_file.txt',
                            'show': True,
                            'tags': [
                                '.txt'
                            ],
                            'type': 'CODE'
                        }
                    }
                ]
            },
            'description': 'my test description',
            'name': 'labbook11'
        }
    }
}

snapshots['TestLabBookServiceQueries.test_get_detail_records 1'] = {
    'data': {
        'labbook': {
            'description': 'my test description',
            'detailRecords': [
                {
                    'data': [
                        [
                            'text/plain',
                            'Added new Code file code/test_file.txt'
                        ]
                    ],
                    'importance': 0,
                    'show': False,
                    'tags': [
                    ],
                    'type': 'CODE'
                },
                {
                    'data': [
                        [
                            'text/plain',
                            'Added new Input Data file input/test_file.txt'
                        ]
                    ],
                    'importance': 0,
                    'show': False,
                    'tags': [
                    ],
                    'type': 'INPUT_DATA'
                }
            ],
            'name': 'labbook11'
        }
    }
}

snapshots['TestLabBookServiceQueries.test_list_favorites 1'] = {
    'data': {
        'labbook': {
            'code': {
                'favorites': {
                    'edges': [
                        {
                            'node': {
                                'associatedLabbookFileId': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJnRlc3QxLnR4dA==',
                                'description': 'My file with stuff 1',
                                'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmY29kZSZ0ZXN0MS50eHQ=',
                                'index': 0,
                                'isDir': False,
                                'key': 'test1.txt'
                            }
                        },
                        {
                            'node': {
                                'associatedLabbookFileId': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJnRlc3QyLnR4dA==',
                                'description': 'My file with stuff 2',
                                'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmY29kZSZ0ZXN0Mi50eHQ=',
                                'index': 1,
                                'isDir': False,
                                'key': 'test2.txt'
                            }
                        },
                        {
                            'node': {
                                'associatedLabbookFileId': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJmJsYWgv',
                                'description': 'testing',
                                'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmY29kZSZibGFoLw==',
                                'index': 2,
                                'isDir': True,
                                'key': 'blah/'
                            }
                        }
                    ]
                }
            },
            'name': 'labbook1'
        }
    }
}

snapshots['TestLabBookServiceQueries.test_list_favorites 2'] = {
    'data': {
        'labbook': {
            'input': {
                'favorites': {
                    'edges': [
                        {
                            'node': {
                                'associatedLabbookFileId': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZpbnB1dCZkYXRhMS8=',
                                'description': 'Data dir 1',
                                'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmaW5wdXQmZGF0YTEv',
                                'index': 0,
                                'isDir': True,
                                'key': 'data1/'
                            }
                        }
                    ]
                }
            },
            'name': 'labbook1'
        }
    }
}

snapshots['TestLabBookServiceQueries.test_list_favorites 3'] = {
    'data': {
        'labbook': {
            'name': 'labbook1',
            'output': {
                'favorites': {
                    'edges': [
                        {
                            'node': {
                                'associatedLabbookFileId': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZvdXRwdXQmZGF0YTIv',
                                'description': 'Data dir 2',
                                'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmb3V0cHV0JmRhdGEyLw==',
                                'index': 0,
                                'isDir': True,
                                'key': 'data2/'
                            }
                        }
                    ]
                }
            }
        }
    }
}

snapshots['TestLabBookServiceQueries.test_list_favorites 4'] = {
    'data': {
        'labbook': {
            'code': {
                'favorites': {
                    'edges': [
                        {
                            'node': {
                                'associatedLabbookFileId': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJnRlc3QxLnR4dA==',
                                'description': 'My file with stuff 1',
                                'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmY29kZSZ0ZXN0MS50eHQ=',
                                'index': 0,
                                'isDir': False,
                                'key': 'test1.txt'
                            }
                        },
                        {
                            'node': {
                                'associatedLabbookFileId': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJnRlc3QyLnR4dA==',
                                'description': 'My file with stuff 2',
                                'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmY29kZSZ0ZXN0Mi50eHQ=',
                                'index': 1,
                                'isDir': False,
                                'key': 'test2.txt'
                            }
                        },
                        {
                            'node': {
                                'associatedLabbookFileId': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJmJsYWgv',
                                'description': 'testing',
                                'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmY29kZSZibGFoLw==',
                                'index': 2,
                                'isDir': True,
                                'key': 'blah/'
                            }
                        }
                    ]
                }
            },
            'input': {
                'favorites': {
                    'edges': [
                        {
                            'node': {
                                'associatedLabbookFileId': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZpbnB1dCZkYXRhMS8=',
                                'description': 'Data dir 1',
                                'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmaW5wdXQmZGF0YTEv',
                                'index': 0,
                                'isDir': True,
                                'key': 'data1/'
                            }
                        }
                    ]
                }
            },
            'name': 'labbook1',
            'output': {
                'favorites': {
                    'edges': [
                        {
                            'node': {
                                'associatedLabbookFileId': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZvdXRwdXQmZGF0YTIv',
                                'description': 'Data dir 2',
                                'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmb3V0cHV0JmRhdGEyLw==',
                                'index': 0,
                                'isDir': True,
                                'key': 'data2/'
                            }
                        }
                    ]
                }
            }
        }
    }
}

snapshots['TestLabBookServiceQueries.test_list_favorite_and_files 1'] = {
    'data': {
        'labbook': {
            'code': {
                'favorites': {
                    'edges': [
                        {
                            'node': {
                                'description': 'My file with stuff 2',
                                'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmY29kZSZ0ZXN0Mi50eHQ=',
                                'index': 0,
                                'isDir': False,
                                'key': 'test2.txt'
                            }
                        },
                        {
                            'node': {
                                'description': 'testing',
                                'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmY29kZSZibGFoLw==',
                                'index': 1,
                                'isDir': True,
                                'key': 'blah/'
                            }
                        }
                    ]
                },
                'files': {
                    'edges': [
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJmJsYWgv',
                                'isDir': True,
                                'key': 'blah/',
                                'size': '0'
                            }
                        },
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJnRlc3QxLnR4dA==',
                                'isDir': False,
                                'key': 'test1.txt',
                                'size': '5'
                            }
                        },
                        {
                            'node': {
                                'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJnRlc3QyLnR4dA==',
                                'isDir': False,
                                'key': 'test2.txt',
                                'size': '5'
                            }
                        }
                    ]
                }
            },
            'name': 'labbook1'
        }
    }
}

snapshots['TestLabBookServiceQueries.test_page_favorites 1'] = {
    'data': {
        'labbook': {
            'code': {
                'favorites': {
                    'edges': [
                        {
                            'cursor': 'MA==',
                            'node': {
                                'associatedLabbookFileId': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJnRlc3QxLnR4dA==',
                                'description': 'My file with stuff 1',
                                'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmY29kZSZ0ZXN0MS50eHQ=',
                                'index': 0,
                                'isDir': False,
                                'key': 'test1.txt'
                            }
                        },
                        {
                            'cursor': 'MQ==',
                            'node': {
                                'associatedLabbookFileId': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJnRlc3QyLnR4dA==',
                                'description': 'My file with stuff 2',
                                'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmY29kZSZ0ZXN0Mi50eHQ=',
                                'index': 1,
                                'isDir': False,
                                'key': 'test2.txt'
                            }
                        }
                    ],
                    'pageInfo': {
                        'endCursor': 'MQ==',
                        'hasNextPage': True,
                        'hasPreviousPage': False,
                        'startCursor': 'MA=='
                    }
                }
            },
            'name': 'labbook1'
        }
    }
}

snapshots['TestLabBookServiceQueries.test_page_favorites 2'] = {
    'data': {
        'labbook': {
            'code': {
                'favorites': {
                    'edges': [
                        {
                            'cursor': 'Mg==',
                            'node': {
                                'associatedLabbookFileId': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJmJsYWgv',
                                'description': 'testing',
                                'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmY29kZSZibGFoLw==',
                                'index': 2,
                                'isDir': True,
                                'key': 'blah/'
                            }
                        }
                    ],
                    'pageInfo': {
                        'endCursor': 'Mg==',
                        'hasNextPage': False,
                        'hasPreviousPage': False,
                        'startCursor': 'Mg=='
                    }
                }
            },
            'name': 'labbook1'
        }
    }
}

snapshots['TestLabBookServiceQueries.test_get_labbook_readme 1'] = {
    'data': {
        'labbook': {
            'description': 'my first labbook1',
            'name': 'labbook1',
            'readme': None
        }
    }
}

snapshots['TestLabBookServiceQueries.test_get_labbook_readme 2'] = {
    'data': {
        'labbook': {
            'description': 'my first labbook1',
            'name': 'labbook1',
            'readme': '''##Summary
This is my readme!!'''
        }
    }
}

snapshots['TestLabBookServiceQueries.test_pagination_sort_az 1'] = {
    'data': {
        'labbookList': {
            'localLabbooks': {
                'edges': [
                    {
                        'cursor': 'MA==',
                        'node': {
                            'description': 'Cats labbook 1',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2sx',
                            'name': 'labbook1'
                        }
                    },
                    {
                        'cursor': 'MQ==',
                        'node': {
                            'description': 'Dogs labbook 2',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2sy',
                            'name': 'labbook2'
                        }
                    },
                    {
                        'cursor': 'Mg==',
                        'node': {
                            'description': 'Mice labbook 3',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2sz',
                            'name': 'labbook3'
                        }
                    },
                    {
                        'cursor': 'Mw==',
                        'node': {
                            'description': 'Horses labbook 4',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2s0',
                            'name': 'labbook4'
                        }
                    },
                    {
                        'cursor': 'NA==',
                        'node': {
                            'description': 'Cheese labbook 5',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2s1',
                            'name': 'labbook5'
                        }
                    },
                    {
                        'cursor': 'NQ==',
                        'node': {
                            'description': 'Goat labbook 6',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2s2',
                            'name': 'labbook6'
                        }
                    },
                    {
                        'cursor': 'Ng==',
                        'node': {
                            'description': 'Turtle labbook 7',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2s3',
                            'name': 'labbook7'
                        }
                    },
                    {
                        'cursor': 'Nw==',
                        'node': {
                            'description': 'Lamb labbook 8',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2s4',
                            'name': 'labbook8'
                        }
                    },
                    {
                        'cursor': 'OA==',
                        'node': {
                            'description': 'Taco labbook 9',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2s5',
                            'name': 'labbook9'
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

snapshots['TestLabBookServiceQueries.test_pagination_sort_az_reverse 1'] = {
    'data': {
        'labbookList': {
            'localLabbooks': {
                'edges': [
                    {
                        'cursor': 'MA==',
                        'node': {
                            'description': 'Taco labbook 9',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2s5',
                            'name': 'labbook9'
                        }
                    },
                    {
                        'cursor': 'MQ==',
                        'node': {
                            'description': 'Lamb labbook 8',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2s4',
                            'name': 'labbook8'
                        }
                    },
                    {
                        'cursor': 'Mg==',
                        'node': {
                            'description': 'Turtle labbook 7',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2s3',
                            'name': 'labbook7'
                        }
                    },
                    {
                        'cursor': 'Mw==',
                        'node': {
                            'description': 'Goat labbook 6',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2s2',
                            'name': 'labbook6'
                        }
                    },
                    {
                        'cursor': 'NA==',
                        'node': {
                            'description': 'Cheese labbook 5',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2s1',
                            'name': 'labbook5'
                        }
                    },
                    {
                        'cursor': 'NQ==',
                        'node': {
                            'description': 'Horses labbook 4',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2s0',
                            'name': 'labbook4'
                        }
                    },
                    {
                        'cursor': 'Ng==',
                        'node': {
                            'description': 'Mice labbook 3',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2sz',
                            'name': 'labbook3'
                        }
                    },
                    {
                        'cursor': 'Nw==',
                        'node': {
                            'description': 'Dogs labbook 2',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2sy',
                            'name': 'labbook2'
                        }
                    },
                    {
                        'cursor': 'OA==',
                        'node': {
                            'description': 'Cats labbook 1',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2sx',
                            'name': 'labbook1'
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

snapshots['TestLabBookServiceQueries.test_list_local_by_id 1'] = {
    'data': {
        'labbookList': {
            'localById': [
                {
                    'description': 'my first labbook1',
                    'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2sx',
                    'name': 'labbook1',
                    'owner': 'default'
                },
                {
                    'description': 'my first labbook3',
                    'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2sz',
                    'name': 'labbook3',
                    'owner': 'default'
                },
                None
            ]
        }
    }
}

snapshots['TestLabBookServiceQueries.test_pagination_sort_create 1'] = {
    'data': {
        'labbookList': {
            'localLabbooks': {
                'edges': [
                    {
                        'cursor': 'MA==',
                        'node': {
                            'description': 'Cats labbook 1',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2sx',
                            'name': 'labbook1'
                        }
                    },
                    {
                        'cursor': 'MQ==',
                        'node': {
                            'description': 'Dogs labbook 2',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2sy',
                            'name': 'labbook2'
                        }
                    },
                    {
                        'cursor': 'Mg==',
                        'node': {
                            'description': 'Mice labbook 3',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2sz',
                            'name': 'labbook3'
                        }
                    },
                    {
                        'cursor': 'Mw==',
                        'node': {
                            'description': 'Horses labbook 4',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2s0',
                            'name': 'labbook4'
                        }
                    },
                    {
                        'cursor': 'NA==',
                        'node': {
                            'description': 'Cheese labbook 5',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2s1',
                            'name': 'labbook5'
                        }
                    },
                    {
                        'cursor': 'NQ==',
                        'node': {
                            'description': 'Goat labbook 6',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2s2',
                            'name': 'labbook6'
                        }
                    },
                    {
                        'cursor': 'Ng==',
                        'node': {
                            'description': 'Turtle labbook 7',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2s3',
                            'name': 'labbook7'
                        }
                    },
                    {
                        'cursor': 'Nw==',
                        'node': {
                            'description': 'Lamb labbook 8',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2s4',
                            'name': 'labbook8'
                        }
                    },
                    {
                        'cursor': 'OA==',
                        'node': {
                            'description': 'Taco labbook 9',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2s5',
                            'name': 'labbook9'
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

snapshots['TestLabBookServiceQueries.test_pagination_sort_modified 1'] = {
    'data': {
        'labbookList': {
            'localLabbooks': {
                'edges': [
                    {
                        'cursor': 'MA==',
                        'node': {
                            'description': 'Cats labbook 1',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2sx',
                            'name': 'labbook1'
                        }
                    },
                    {
                        'cursor': 'MQ==',
                        'node': {
                            'description': 'Dogs labbook 2',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2sy',
                            'name': 'labbook2'
                        }
                    },
                    {
                        'cursor': 'Mg==',
                        'node': {
                            'description': 'Mice labbook 3',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2sz',
                            'name': 'labbook3'
                        }
                    },
                    {
                        'cursor': 'Mw==',
                        'node': {
                            'description': 'Horses labbook 4',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2s0',
                            'name': 'labbook4'
                        }
                    },
                    {
                        'cursor': 'NA==',
                        'node': {
                            'description': 'Cheese labbook 5',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2s1',
                            'name': 'labbook5'
                        }
                    },
                    {
                        'cursor': 'NQ==',
                        'node': {
                            'description': 'Goat labbook 6',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2s2',
                            'name': 'labbook6'
                        }
                    },
                    {
                        'cursor': 'Ng==',
                        'node': {
                            'description': 'Turtle labbook 7',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2s3',
                            'name': 'labbook7'
                        }
                    },
                    {
                        'cursor': 'Nw==',
                        'node': {
                            'description': 'Lamb labbook 8',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2s4',
                            'name': 'labbook8'
                        }
                    },
                    {
                        'cursor': 'OA==',
                        'node': {
                            'description': 'Taco labbook 9',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2s5',
                            'name': 'labbook9'
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

snapshots['TestLabBookServiceQueries.test_pagination_sort_modified 2'] = {
    'data': {
        'labbookList': {
            'localLabbooks': {
                'edges': [
                    {
                        'cursor': 'MA==',
                        'node': {
                            'description': 'Cats labbook 1',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2sx',
                            'name': 'labbook1'
                        }
                    },
                    {
                        'cursor': 'MQ==',
                        'node': {
                            'description': 'Dogs labbook 2',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2sy',
                            'name': 'labbook2'
                        }
                    },
                    {
                        'cursor': 'Mg==',
                        'node': {
                            'description': 'Mice labbook 3',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2sz',
                            'name': 'labbook3'
                        }
                    },
                    {
                        'cursor': 'Mw==',
                        'node': {
                            'description': 'Cheese labbook 5',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2s1',
                            'name': 'labbook5'
                        }
                    },
                    {
                        'cursor': 'NA==',
                        'node': {
                            'description': 'Goat labbook 6',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2s2',
                            'name': 'labbook6'
                        }
                    },
                    {
                        'cursor': 'NQ==',
                        'node': {
                            'description': 'Turtle labbook 7',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2s3',
                            'name': 'labbook7'
                        }
                    },
                    {
                        'cursor': 'Ng==',
                        'node': {
                            'description': 'Lamb labbook 8',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2s4',
                            'name': 'labbook8'
                        }
                    },
                    {
                        'cursor': 'Nw==',
                        'node': {
                            'description': 'Taco labbook 9',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2s5',
                            'name': 'labbook9'
                        }
                    },
                    {
                        'cursor': 'OA==',
                        'node': {
                            'description': 'Horses labbook 4',
                            'id': 'TGFiYm9vazpkZWZhdWx0JmxhYmJvb2s0',
                            'name': 'labbook4'
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
