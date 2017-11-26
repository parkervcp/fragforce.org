import boto
import os.path
from uuid import uuid4
from werkzeug.utils import secure_filename
from flask import app
import re

EXT_MATCH = re.compile(r'^[a-zA-Z0-9]+$')


def upload(src_fil, dst_dir, acl='public-read'):
    """ Upload a file to S3 """
    source_filename = secure_filename(src_fil.data.filename)
    source_extension = os.path.splitext(source_filename)[1]
    if not EXT_MATCH.match(source_extension):
        raise ValueError("Bad Extension")
    destination_filename = uuid4().hex + source_extension

    conn = boto.connect_s3(app.config["BUCKETEER_AWS_ACCESS_KEY_ID"], app.config["BUCKETEER_AWS_SECRET_ACCESS_KEY"])
    b = conn.get_bucket(app.config["BUCKETEER_BUCKET_NAME"])

    sml = b.new_key("/".join([dst_dir, destination_filename]))
    sml.set_contents_from_string(src_fil.data.read())
    sml.set_acl(acl)

    return destination_filename
