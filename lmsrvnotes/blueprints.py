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
from flask import Blueprint
from flask_graphql import GraphQLView
import graphene

from .api import NotesQueries, NoteQueries, NoteMutations

from lmcommon.configuration import Configuration

# Load config data for the LabManager instance
config = Configuration()

# Create Blueprint
notes_service = Blueprint('notes_service', __name__)

# Add routes -- each must have their own view
notes_service.add_url_rule('/note/',
                           view_func=GraphQLView.as_view('graphql-note',
                                                         schema=graphene.Schema(query=NoteQueries,
                                                                                mutation=NoteMutations),
                                                         graphiql=config.config["flask"]["DEBUG"]))

notes_service.add_url_rule('/notes/',
                           view_func=GraphQLView.as_view('graphql-notes',
                                                         schema=graphene.Schema(query=NotesQueries),
                                                         graphiql=config.config["flask"]["DEBUG"]))