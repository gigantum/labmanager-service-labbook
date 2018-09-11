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
import graphene
from lmsrvlabbook.api.mutations import (CreateBranch, CheckoutBranch, CreateLabbook, BuildImage, StartContainer,
                                        AddCustomComponent, AddPackageComponents, CreateUserNote, StopContainer,
                                        ImportLabbook, DeleteLabbook,
                                        ImportRemoteLabbook, AddLabbookRemote,
                                        ExportLabbook, AddLabbookFile, MoveLabbookFile, DeleteLabbookFile,
                                        MakeLabbookDirectory, RemoveUserIdentity,
                                        AddLabbookFavorite, RemoveLabbookFavorite, UpdateLabbookFavorite,
                                        AddLabbookCollaborator,
                                        DeleteLabbookCollaborator, SyncLabbook, PublishLabbook, RemoveCustomComponent,
                                        RemovePackageComponents,
                                        StartDevTool, SetLabbookDescription, CreateExperimentalBranch,
                                        DeleteExperimentalBranch,
                                        MergeFromBranch, WorkonBranch, WriteReadme, AddCustomDocker, RemoveCustomDocker,
                                        DeleteRemoteLabbook,
                                        CompleteBatchUploadTransaction, SetVisibility)


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

    # Delete a labbook off the file system
    delete_labbook = DeleteLabbook.Field()

    # Delete a labbook from a remote server
    delete_remote_labbook = DeleteRemoteLabbook.Field()

    # (Re-)set labbook description
    set_labbook_description = SetLabbookDescription.Field()

    # Publish a labbook to a remote (for the first time
    publish_labbook = PublishLabbook.Field()

    # Sync a Labbook with remote (for collaboration)
    sync_labbook = SyncLabbook.Field()

    # Create a new git branch for a given labbook.
    create_branch = CreateBranch.Field()

    # Update a given labbook to be at the tip of a particular git branch.
    checkout_branch = CheckoutBranch.Field()

    # Add a remote to the labbook
    add_labbook_remote = AddLabbookRemote.Field()

    # Build a docker image for a given Labbook.
    build_image = BuildImage.Field()

    # Start a labbook's Docker container.
    start_container = StartContainer.Field()

    # Start a labbook's Docker container.
    stop_container = StopContainer.Field()

    # Start a tool such as Jupyer Lab
    start_dev_tool = StartDevTool.Field()

    # Create a user note in the labbook's current working branch
    create_user_note = CreateUserNote.Field()

    # Add a custom dependency to Labbook environment.
    add_custom_component = AddCustomComponent.Field()

    # Remove a custom dependency to Labbook environment.
    remove_custom_component = RemoveCustomComponent.Field()

    # Add a package to a Labbook environment (e.g., pip package, apt)
    add_package_components = AddPackageComponents.Field()

    # Remove a package from a Labbook environment (e.g., pip package, apt)
    remove_package_components = RemovePackageComponents.Field()

    # Add an arbitrary docker snippet (supplement to custom dependency)
    add_custom_docker = AddCustomDocker.Field()

    # Delete the arbitrary docker snippet.
    remove_custom_docker = RemoveCustomDocker.Field()

    # Add a file to a labbook
    add_labbook_file = AddLabbookFile.Field()

    # Indicate a (potentially) mutlifile batched upload is finished
    # Also contains options to cancel (and rollback aborted changes).
    complete_batch_upload_transaction = CompleteBatchUploadTransaction.Field()

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

    # Write a readme to a LabBook
    write_readme = WriteReadme.Field()

    # Create a Rollback or Feature branch
    create_experimental_branch = CreateExperimentalBranch.Field()

    # Delete a Rollback or Feature branch
    delete_experimental_branch = DeleteExperimentalBranch.Field()

    # Merge from a given branch into the current checked-out branch
    merge_from_branch = MergeFromBranch.Field()

    # Work on a given feature branch (perform a git checkout).
    workon_experimental_branch = WorkonBranch.Field()

    # Set a remote project visibiltiy
    set_visibility = SetVisibility.Field()
