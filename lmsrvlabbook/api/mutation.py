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
import graphene
from lmsrvlabbook.api.mutations import CreateBranch, CheckoutBranch, CreateLabbook, BuildImage, StartContainer, \
    AddEnvironmentComponent, AddEnvironmentPackage, CreateUserNote, StopContainer, ImportLabbook,\
    ImportRemoteLabbook, AddLabbookRemote, PullActiveBranchFromRemote, PushActiveBranchToRemote, \
    ExportLabbook, AddLabbookFile, MoveLabbookFile, DeleteLabbookFile, MakeLabbookDirectory, RemoveUserIdentity, \
    AddLabbookFavorite, RemoveLabbookFavorite, RenameLabbook, UpdateLabbookFavorite, AddLabbookCollaborator, \
    DeleteLabbookCollaborator, SyncLabbook, PublishLabbook


class LabbookMutations(graphene.ObjectType):
    """Entry point for all graphql mutations"""

    # Import a labbook from an uploaded file (Archive as zip).
    import_labbook = ImportLabbook.Field()

    # Import a labbook from a remote Git repository.
    import_remote_labbook = ImportRemoteLabbook.Field()

    # Export a labbook and return URL to its zipped archive.
    export_labbook = ExportLabbook.Field()

    # Create a new labbook on the file system.
    create_labbook = CreateLabbook.Field()

    # Rename new labbook
    rename_labbook = RenameLabbook.Field()

    # Publish a labbook to a remote (for the first time
    publish_labbook = PublishLabbook.Field()

    # Sync a Labbook with remote (for collaboration)
    sync_labbook = SyncLabbook.Field()

    # Create a new git branch for a given labbook.
    create_branch = CreateBranch.Field()

    # Update a given labbook to be at the tip of a particular git branch.
    checkout_branch = CheckoutBranch.Field()

    #
    pull_active_branch_from_remote = PullActiveBranchFromRemote.Field()

    #
    push_active_branch_to_remote = PushActiveBranchToRemote.Field()

    # Add a remote to the labbook
    add_labbook_remote = AddLabbookRemote.Field()

    # Build a docker image for a given Labbook.
    build_image = BuildImage.Field()

    # Start a labbook's Docker container.
    start_container = StartContainer.Field()

    # Start a labbook's Docker container.
    stop_container = StopContainer.Field()

    # Create a user note in the labbook's current working branch
    create_user_note = CreateUserNote.Field()

    # Add a development environment or complex dependency to Labbook environment.
    add_environment_component = AddEnvironmentComponent.Field()

    # Add a package to a Labbook environment (e.g., pip package, apt)
    add_environment_package = AddEnvironmentPackage.Field()

    # Add a file to a labbook
    add_labbook_file = AddLabbookFile.Field()

    # Move files or directory within a labbook
    move_labbook_file = MoveLabbookFile.Field()

    # Delete a file or directory inside of a Labbook.
    delete_labbook_file = DeleteLabbookFile.Field()

    # Make a directory (with auto-included .gitkeep) inside of a Labbook
    make_labbook_directory = MakeLabbookDirectory.Field()

    # Remove a locally stored user identity (no-op for non-local installations)
    remove_user_identity = RemoveUserIdentity.Field()

    # Add a favorite file or dir in a labbook subdirectory (code, input, output)
    add_favorite = AddLabbookFavorite.Field()

    # Update a favorite file or dir in a labbook subdirectory (code, input, output)
    update_favorite = UpdateLabbookFavorite.Field()

    # Remove a favorite file or dir in a labbook subdirectory (code, input, output)
    remove_favorite = RemoveLabbookFavorite.Field()

    # Add a collaborator to a LabBook
    add_collaborator = AddLabbookCollaborator.Field()

    # Delete a collaborator from a LabBook
    delete_collaborator = DeleteLabbookCollaborator.Field()
