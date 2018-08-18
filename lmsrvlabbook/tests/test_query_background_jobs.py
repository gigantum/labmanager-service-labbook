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
import multiprocessing
import threading
import pytest
import time

from snapshottest import snapshot
from lmsrvlabbook.tests.fixtures import fixture_working_dir_env_repo_scoped
from graphene.test import Client
from mock import patch
import redis
import rq

from lmcommon.dispatcher import Dispatcher, jobs


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
        while count < 12:
            count = count + 1
            time.sleep(1)

        try:
            p.terminate()
        except:
            pass

    r = redis.Redis()
    r.flushall()

    worker_proc = multiprocessing.Process(target=run_worker)
    worker_proc.daemon = True
    worker_proc.start()

    watchdog_thread = threading.Thread(target=watch_proc, args=(worker_proc,))
    watchdog_thread.daemon = True
    watchdog_thread.start()

    dispatcher = Dispatcher('labmanager_unittests')

    assert worker_proc.is_alive()
    yield worker_proc, dispatcher


class TestBackgroundJobs(object):
    def test_get_background_jobs_basics(self, temporary_worker, fixture_working_dir_env_repo_scoped, snapshot):

        w, d = temporary_worker
        assert w.is_alive()

        time.sleep(0.25)

        t1 = d.dispatch_task(jobs.test_exit_fail).key_str
        t2 = d.dispatch_task(jobs.test_exit_success).key_str
        t3 = d.dispatch_task(jobs.test_sleep, args=(1,)).key_str

        query = """
                {
                  backgroundJobs {
                    edges {
                      node {
                        id
                        jobKey
                        failureMessage
                        status
                        result
                      }
                    }
                  }
                }
        """
        time.sleep(1)
        try:
            assert w.is_alive()
            time1 = time.time()
            result = fixture_working_dir_env_repo_scoped[2].execute(query)
            #import pprint; print('----'); pprint.pprint(result); print('-<<<')
            time2 = time.time()
            tdiff = time2 - time1
            assert tdiff < 0.5, "Query should not take more than a few millis (took {}s)".format(tdiff)

            assert any([t1 == x['node']['jobKey']
                        and 'failed' == x['node']['status']
                        and 'Exception: ' in x['node']['failureMessage']
                        for x in result['data']['backgroundJobs']['edges']])
            assert any([t2 == x['node']['jobKey'] and "finished" == x['node']['status']
                        and x['node']['failureMessage'] is None
                        for x in result['data']['backgroundJobs']['edges']])
            assert any([t3 == x['node']['jobKey'] and "started" == x['node']['status']
                        and x['node']['failureMessage'] is None
                        for x in result['data']['backgroundJobs']['edges']])
            time.sleep(2)
        except:
            time.sleep(2)
            w.terminate()
            raise

        w.terminate()
