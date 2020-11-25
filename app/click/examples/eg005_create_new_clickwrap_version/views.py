"""Example 005: Creating a new clickwrap version"""

from os import path
import json

from docusign_click.client.api_exception import ApiException
from flask import render_template, current_app, Blueprint, session

from .controller import Eg005Controller
from app.docusign import authenticate
from app.ds_config import DS_CONFIG
from app.error_handlers import process_error

eg = "eg005"  # reference (and url) for this example
eg005 = Blueprint("eg005", __name__)


@eg005.route("/eg005", methods=["POST"])
@authenticate(eg=eg)
def create_new_clickwrap_version():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """
    # 1. Get required arguments
    args = Eg005Controller.get_args()

    try:
        # 2. Call the worker method to create a new clickwrap version
        results = Eg005Controller.worker(args)
        current_app.logger.info(
            f"""The 2nd version of clickwrap "{args['clickwrap_name']}" has been created!"""
        )
    except ApiException as err:
        return process_error(err)

    # 3. Render the response
    return render_template(
        "example_done.html",
        title="Creating a new clickwrap version",
        h1="Creating a new clickwrap version",
        message=f"""The 2nd version of clickwrap "{args['clickwrap_name']}" has been created!""",
        json=json.dumps(json.dumps(results.to_dict(), default=str))
    )


@eg005.route("/eg005", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """responds with the form for the example"""
    return render_template(
        "eg005_create_new_clickwrap_version.html",
        title="Creating a new clickwrap version",
        clickwrap_ok="clickwrap_id" in session,
        source_file=path.basename(path.dirname(__file__)) + "/controller.py",
        source_url=DS_CONFIG["github_example_url"] + path.basename(
            path.dirname(__file__)) + "/controller.py",
    )
