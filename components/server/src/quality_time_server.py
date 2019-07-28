"""Quality-time server."""

from gevent import monkey  # pylint: disable=import-error
monkey.patch_all()

# pylint: disable=wrong-import-order,wrong-import-position

import bottle
import logging
import urllib
import os

from initialization import init_bottle, init_database


def serve() -> None:  # pragma: nocover
    """Connect to the database and start the application server."""
    logging.getLogger().setLevel(logging.INFO)
    database = init_database()
    init_bottle(database)
    server = urllib.parse.urlparse(os.environ.get("SERVER_URL", "http://localhost:5001"))
    bottle.run(server="gevent", host="0.0.0.0", port=server.port, reloader=True, log=logging.getLogger())  # nosec


if __name__ == "__main__":
    serve()