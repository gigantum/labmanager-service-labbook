# Copyright (c) 2018 FlashX, LLC
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
import os
import uuid
import time

import graphene
import confhttpproxy

from lmcommon.labbook import LabBook
from lmcommon.container.container import ContainerOperations
from lmcommon.logging import LMLogger
from lmcommon.activity.services import start_labbook_monitor

from lmsrvcore.auth.user import get_logged_in_username, get_logged_in_author

logger = LMLogger.get_logger()


class StartDevTool(graphene.relay.ClientIDMutation):
    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        dev_tool = graphene.String(required=True)
        container_override_id = graphene.String(required=False)

    # Return the Environment instance
    path = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, owner, labbook_name, dev_tool,
                               container_override_id=None, client_mutation_id=None):
        username = get_logged_in_username()
        lb = LabBook(author=get_logged_in_author())
        lb.from_name(username, owner, labbook_name)

        lb_ip = ContainerOperations.get_labbook_ip(lb, username)
        lb_port = 8888
        lb_endpoint = f'http://{lb_ip}:{lb_port}'

        pr = confhttpproxy.ProxyRouter.get_proxy(lb.labmanager_config.config['proxy'])
        routes = pr.routes
        est_target = [k for k in routes.keys()
                      if lb_endpoint in routes[k]['target']
                      and 'jupyter' in k]

        if len(est_target) == 1:
            suffix = est_target[0]
        elif len(est_target) == 0:
            rt_prefix = str(uuid.uuid4()).replace('-', '')[:8]
            rt_prefix, _ = pr.add(lb_endpoint, f'jupyter/{rt_prefix}')

            # Start jupyterlab
            _, suffix = ContainerOperations.start_dev_tool(
                lb, dev_tool_name=dev_tool, username=username,
                tag=container_override_id, proxy_prefix=rt_prefix)

            # Ensure we start monitor IFF jupyter isn't already running.
            start_labbook_monitor(lb, username, dev_tool,
                                  url=f'{lb_endpoint}/{rt_prefix}',
                                  author=get_logged_in_author())
        else:
            raise ValueError(f"Multiple Jupyter instances for {str(lb)}")

        # Don't include the port in the path if running on 80
        apparent_proxy_port = lb.labmanager_config.config['proxy']["apparent_proxy_port"]
        if apparent_proxy_port == 80:
            path = suffix
        else:
            path = f':{apparent_proxy_port}{suffix}'

        return StartDevTool(path=path)
