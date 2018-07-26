# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestUserIdentityMutations.test_remove_user_identity 1'] = {
    'data': {
        'userIdentity': {
            'email': 'jane@doe.com',
            'familyName': 'Doe',
            'givenName': 'Jane',
            'id': 'VXNlcklkZW50aXR5OmRlZmF1bHQ=',
            'username': 'default'
        }
    }
}

snapshots['TestUserIdentityMutations.test_remove_user_identity 2'] = {
    'data': {
        'removeUserIdentity': {
            'userIdentityEdge': {
                'username': None
            }
        }
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 23,
                    'line': 5
                }
            ],
            'message': "({'code': 'missing_token', 'description': 'JWT must be provided if no locally stored identity is available'}, 401)",
            'path': [
                'removeUserIdentity',
                'userIdentityEdge',
                'username'
            ]
        }
    ]
}
