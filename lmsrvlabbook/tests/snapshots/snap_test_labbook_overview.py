# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestLabBookOverviewQueries.test_empty_package_counts 1'] = {
    'data': {
        'labbook': {
            'overview': {
                'numAptPackages': 0,
                'numConda2Packages': 0,
                'numConda3Packages': 0,
                'numPipPackages': 0
            }
        }
    }
}

snapshots['TestLabBookOverviewQueries.test_package_counts 1'] = {
    'data': {
        'labbook': {
            'overview': {
                'numAptPackages': 1,
                'numConda2Packages': 4,
                'numConda3Packages': 3,
                'numPipPackages': 2
            }
        }
    }
}

snapshots['TestLabBookOverviewQueries.test_get_recent_activity 1'] = {
    'data': {
        'labbook': {
            'overview': {
                'recentActivity': [
                    {
                        'importance': 255,
                        'message': 'Added new Output Data file /test_file.txt',
                        'show': True,
                        'tags': [
                            '.txt'
                        ],
                        'type': 'OUTPUT_DATA'
                    },
                    {
                        'importance': 255,
                        'message': 'Added new Input Data file /test2/test_file.txt',
                        'show': True,
                        'tags': [
                            '.txt'
                        ],
                        'type': 'INPUT_DATA'
                    },
                    {
                        'importance': 255,
                        'message': 'Added new Input Data file /test/test_file.txt',
                        'show': True,
                        'tags': [
                            '.txt'
                        ],
                        'type': 'INPUT_DATA'
                    },
                    {
                        'importance': 255,
                        'message': 'Added new Input Data file /test_file.txt',
                        'show': True,
                        'tags': [
                            '.txt'
                        ],
                        'type': 'INPUT_DATA'
                    }
                ]
            }
        }
    }
}

snapshots['TestLabBookOverviewQueries.test_no_remote_url 1'] = {
    'data': {
        'labbook': {
            'overview': {
                'remoteUrl': None
            }
        }
    }
}
