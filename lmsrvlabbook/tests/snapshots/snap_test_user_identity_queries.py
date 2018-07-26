# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestUserIdentityQueries.test_logged_in_user 1'] = {
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

snapshots['TestUserIdentityQueries.test_no_logged_in_user 1'] = {
    'data': {
        'userIdentity': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 35,
                    'line': 4
                }
            ],
            'message': "({'code': 'missing_token', 'description': 'JWT must be provided if no locally stored identity is available'}, 401)",
            'path': [
                'userIdentity',
                'id'
            ]
        },
        {
            'locations': [
                {
                    'column': 35,
                    'line': 5
                }
            ],
            'message': "({'code': 'missing_token', 'description': 'JWT must be provided if no locally stored identity is available'}, 401)",
            'path': [
                'userIdentity',
                'username'
            ]
        },
        {
            'locations': [
                {
                    'column': 35,
                    'line': 6
                }
            ],
            'message': "({'code': 'missing_token', 'description': 'JWT must be provided if no locally stored identity is available'}, 401)",
            'path': [
                'userIdentity',
                'email'
            ]
        },
        {
            'locations': [
                {
                    'column': 35,
                    'line': 7
                }
            ],
            'message': "({'code': 'missing_token', 'description': 'JWT must be provided if no locally stored identity is available'}, 401)",
            'path': [
                'userIdentity',
                'givenName'
            ]
        },
        {
            'locations': [
                {
                    'column': 35,
                    'line': 8
                }
            ],
            'message': "({'code': 'missing_token', 'description': 'JWT must be provided if no locally stored identity is available'}, 401)",
            'path': [
                'userIdentity',
                'familyName'
            ]
        }
    ]
}

snapshots['TestUserIdentityQueries.test_logged_in_user_invalid_token 1'] = {
    'data': {
        'userIdentity': {
            'isSessionValid': False
        }
    }
}

snapshots['TestUserIdentityQueries.test_invalid_token 1'] = {
    'data': {
        'userIdentity': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 35,
                    'line': 4
                }
            ],
            'message': "({'code': 'invalid_header', 'description': 'Unable to parse authentication token.'}, 400)",
            'path': [
                'userIdentity',
                'id'
            ]
        },
        {
            'locations': [
                {
                    'column': 35,
                    'line': 5
                }
            ],
            'message': "({'code': 'invalid_header', 'description': 'Unable to parse authentication token.'}, 400)",
            'path': [
                'userIdentity',
                'username'
            ]
        },
        {
            'locations': [
                {
                    'column': 35,
                    'line': 6
                }
            ],
            'message': "({'code': 'invalid_header', 'description': 'Unable to parse authentication token.'}, 400)",
            'path': [
                'userIdentity',
                'email'
            ]
        },
        {
            'locations': [
                {
                    'column': 35,
                    'line': 7
                }
            ],
            'message': "({'code': 'invalid_header', 'description': 'Unable to parse authentication token.'}, 400)",
            'path': [
                'userIdentity',
                'givenName'
            ]
        },
        {
            'locations': [
                {
                    'column': 35,
                    'line': 8
                }
            ],
            'message': "({'code': 'invalid_header', 'description': 'Unable to parse authentication token.'}, 400)",
            'path': [
                'userIdentity',
                'familyName'
            ]
        }
    ]
}
