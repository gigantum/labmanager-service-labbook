# Copyright (c) 2017 FlashX, LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import pytest
import multiprocessing
import threading
import pprint
import time
import json

from snapshottest import snapshot
from lmsrvlabbook.tests.fixtures import fixture_working_dir

from graphene.test import Client
import graphene
from mock import patch
import rq

from lmcommon.dispatcher import Dispatcher, jobs
from lmcommon.configuration import Configuration


@pytest.fixture()
def temporary_worker():
    """A pytest fixture that creates a temporary directory and a config file to match. Deletes directory after test"""
    def run_worker():
        with rq.Connection():
            qs = 'labmanager_unittests'
            w = rq.Worker(qs)
            w.work()

    # This task is used to kill the worker. Sometimes if tests fail the worker runs forever and
    # holds up the entire process. This gives each test 25 seconds to run before killing the worker
    # and forcing the test to fail.
    def watch_proc(p):
        count = 0
        while count < 4:
            count = count + 1
            time.sleep(1)

        try:
            p.terminate()
        except:
            pass

    worker_proc = multiprocessing.Process(target=run_worker)
    worker_proc.start()

    watchdog_thread = threading.Thread(target=watch_proc, args=(worker_proc,))
    watchdog_thread.start()

    dispatcher = Dispatcher('labmanager_unittests')
    yield worker_proc, dispatcher


class TestLabBookServiceQueries(object):

    def test_query_finished_task(self, fixture_working_dir, temporary_worker):
        """Test listing labbooks"""
        w, d = temporary_worker

        job_id = d.dispatch_task(jobs.test_exit_success)

        time.sleep(1)

        query = """
        {
            jobStatus(jobId: "%s") {
                result
                status
                jobMetadata
                failureMessage
                startedAt
                finishedAt
            }
        }
        """ % job_id.key_str

        try:
            r = fixture_working_dir[2].execute(query)
            assert 'errors' not in r
            assert int(r['data']['jobStatus']['result']) == 0
            assert r['data']['jobStatus']['status'] == 'finished'
            assert r['data']['jobStatus']['startedAt'] is not None
            assert r['data']['jobStatus']['failureMessage'] is None
            assert r['data']['jobStatus']['finishedAt']
            assert r['data']['jobStatus']['jobMetadata'] == '{}'

        except:
            w.terminate()
            raise

        w.terminate()

    def test_query_failed_task(self, fixture_working_dir, snapshot, temporary_worker):
        """Test listing labbooks"""

        w, d = temporary_worker

        job_id = d.dispatch_task(jobs.test_exit_fail)

        time.sleep(1)

        query = """
        {
            jobStatus(jobId: "%s") {
                result
                status
                jobMetadata
                failureMessage
                startedAt
                finishedAt
            }
        }
        """ % job_id

        try:
            r = fixture_working_dir[2].execute(query)
            assert 'errors' not in r
            assert r['data']['jobStatus']['result'] is None
            assert r['data']['jobStatus']['status'] == 'failed'
            assert r['data']['jobStatus']['failureMessage'] == \
                   'Exception: Intentional Exception from job `test_exit_fail`'
            assert r['data']['jobStatus']['startedAt'] is not None
            assert r['data']['jobStatus']['finishedAt'] is not None
            # Assert the following dict is empty
            assert not json.loads(r['data']['jobStatus']['jobMetadata'])

        except:
            w.terminate()
            raise

        w.terminate()

    def test_query_started_task(self, fixture_working_dir, snapshot, temporary_worker):
        """Test listing labbooks"""

        w, d = temporary_worker

        job_id = d.dispatch_task(jobs.test_sleep, args=(2,))

        time.sleep(1)

        query = """
        {
            jobStatus(jobId: "%s") {
                result
                status
                jobMetadata
                failureMessage
                startedAt
                finishedAt
            }
        }
        """ % job_id

        try:
            r = fixture_working_dir[2].execute(query)
            pprint.pprint(r)
            assert 'errors' not in r
            assert r['data']['jobStatus']['result'] is None
            assert r['data']['jobStatus']['status'] == 'started'
            assert r['data']['jobStatus']['failureMessage'] is None
            assert r['data']['jobStatus']['startedAt'] is not None
            assert json.loads(r['data']['jobStatus']['jobMetadata'])['sample'] == 'test_sleep metadata'
        except:
            time.sleep(3)
            w.terminate()
            raise

        time.sleep(3)
        w.terminate()

    def test_query_queued_task(self, fixture_working_dir, snapshot, temporary_worker):
        """Test listing labbooks"""

        w, d = temporary_worker

        job_id1 = d.dispatch_task(jobs.test_sleep, args=(2,))
        job_id2 = d.dispatch_task(jobs.test_sleep, args=(2,))

        time.sleep(0.5)

        query = """
        {
            jobStatus(jobId: "%s") {
                result
                status
                jobMetadata
                failureMessage
                startedAt
                finishedAt
            }
        }
        """ % job_id2

        try:
            r = fixture_working_dir[2].execute(query)
            pprint.pprint(r)
            assert 'errors' not in r
            assert r['data']['jobStatus']['result'] is None
            assert r['data']['jobStatus']['status'] == 'queued'
            assert r['data']['jobStatus']['failureMessage'] is None
            assert r['data']['jobStatus']['startedAt'] is None
        except:
            time.sleep(5)
            w.terminate()
            raise

        time.sleep(5)
        w.terminate()
