# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestNodeQueries.test_node_labbook_from_object 1'] = {
    'data': {
        'node': {
            'activeBranch': {
                'refName': 'gm.workspace-default'
            },
            'description': 'Test cat labbook from obj',
            'id': 'TGFiYm9vazpkZWZhdWx0JmNhdC1sYWItYm9vazE=',
            'name': 'cat-lab-book1'
        }
    }
}

snapshots['TestNodeQueries.test_node_environment 1'] = {
    'data': {
        'node': {
            'description': 'Example labbook by mutation.',
            'environment': {
                'containerStatus': 'NOT_RUNNING',
                'id': 'RW52aXJvbm1lbnQ6ZGVmYXVsdCZub2RlLWVudi10ZXN0LWxi',
                'imageStatus': 'DOES_NOT_EXIST'
            },
            'id': 'TGFiYm9vazpkZWZhdWx0Jm5vZGUtZW52LXRlc3QtbGI=',
            'name': 'node-env-test-lb'
        }
    }
}

snapshots['TestNodeQueries.test_node_environment 2'] = {
    'data': {
        'node': {
            'containerStatus': 'NOT_RUNNING',
            'id': 'RW52aXJvbm1lbnQ6ZGVmYXVsdCZub2RlLWVudi10ZXN0LWxi',
            'imageStatus': 'DOES_NOT_EXIST'
        }
    }
}

snapshots['TestNodeQueries.test_file_node 1'] = {
    'data': {
        'node': {
            'id': 'TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJnRlc3QxLnR4dA==',
            'isDir': False,
            'key': 'test1.txt',
            'size': '5'
        }
    }
}

snapshots['TestNodeQueries.test_favorites_node 1'] = {
    'data': {
        'node': {
            'description': None,
            'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmY29kZSZ0ZXN0MzMzLnR4dA==',
            'index': None,
            'isDir': None,
            'key': 'test333.txt'
        }
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 33,
                    'line': 7
                }
            ],
            'message': "'test333.txt'",
            'path': [
                'node',
                'description'
            ]
        },
        {
            'locations': [
                {
                    'column': 33,
                    'line': 8
                }
            ],
            'message': "'test333.txt'",
            'path': [
                'node',
                'isDir'
            ]
        },
        {
            'locations': [
                {
                    'column': 33,
                    'line': 9
                }
            ],
            'message': "'test333.txt'",
            'path': [
                'node',
                'index'
            ]
        }
    ]
}

snapshots['TestNodeQueries.test_favorites_node 2'] = {
    'data': {
        'node': {
            'description': 'My file with stuff 1',
            'id': 'TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmY29kZSZ0ZXN0MS50eHQ=',
            'index': 0,
            'isDir': False,
            'key': 'test1.txt'
        }
    }
}
