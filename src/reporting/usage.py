import os

from lib.trace_client import TraceClient

# @author Daniel McCoy Stephenson
# @since September 11th, 2026

# The name this program's key was issued for. It is the `application` field
# of every event, and the trace server rejects a key used under any other.
APPLICATION = "ophidian"

DEFAULT_ENDPOINT = "https://trace.danielstephenson.dev"

# Bundled with the game the way a plugin bundles its key in config.yml: it
# only lets the game post usage events under its own name, nothing else.
DEFAULT_KEY = "P2kWGUhAW4-5LIvQ8L0P8qs3unOPXTulkyikLGpsulI"

# version.txt at the repository root is what run.sh prints as the current
# version, so it is the version the startup event carries too.
VERSION_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "version.txt",
)

# Shown once, the first time the game starts with a save that predates the
# usageReporting block (or with no save at all); SaveManager then writes the
# block so it is never shown again. Printed rather than queued on the banner:
# the banner is a single 30px line and this would not fit.
FIRST_RUN_NOTICE = (
    "Usage reporting is on: ophidian sends a startup event (program name and "
    "version only) and a run-ended event (how the run ended only) to "
    "trace.danielstephenson.dev. Turn it off with "
    '"usageReporting": {"enabled": false} in save.json.'
)


def defaultUsageReportingSettings():
    """The usageReporting block a fresh save.json gets. Reporting is on by
    default; the block is where a player turns it off."""
    return {
        "enabled": True,
        "endpoint": DEFAULT_ENDPOINT,
        "key": DEFAULT_KEY,
    }


def readVersion(path=None):
    """The game's version as version.txt states it, or None if the file is
    missing or empty - in which case the startup event carries no version
    rather than a made-up one."""
    try:
        with open(path or VERSION_FILE, "r") as f:
            version = f.read().strip()
    except OSError:
        return None
    return version or None


def createUsageReporter(settings):
    """Builds the client the game reports through, from the usageReporting
    block of the save data.

    Every path through here yields a client whose report() returns at once
    and never raises, so nothing about reporting can stop a run: a block
    that is missing, malformed, disabled, or without a key gives the
    no-op client.
    """
    if not isinstance(settings, dict):
        return TraceClient.disabled()
    enabled = settings.get("enabled", True)
    endpoint = settings.get("endpoint") or DEFAULT_ENDPOINT
    key = settings.get("key")
    if enabled is not True or not isinstance(endpoint, str) or not isinstance(key, str):
        return TraceClient.disabled()
    try:
        return TraceClient(endpoint, APPLICATION, key=key, enabled=True)
    except ValueError:
        return TraceClient.disabled()


def startupTags(version=None):
    """Tags for the startup event: the version, when there is one."""
    if version is None:
        version = readVersion()
    if version is None:
        return {}
    return {"version": version}
