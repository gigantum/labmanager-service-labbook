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
    }
}
