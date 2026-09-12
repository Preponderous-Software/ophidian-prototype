import json
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from lib.trace_client import TraceClient
from reporting import usage
from reporting.usage import (
    APPLICATION,
    DEFAULT_ENDPOINT,
    DEFAULT_KEY,
    FIRST_RUN_NOTICE,
    createUsageReporter,
    defaultUsageReportingSettings,
    readVersion,
    startupTags,
)


def _stubServer(received):
    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            length = int(self.headers.get("Content-Length", "0"))
            received["path"] = self.path
            received["authorization"] = self.headers.get("Authorization")
            received["body"] = json.loads(self.rfile.read(length))
            self.send_response(201)
            self.send_header("Content-Length", "0")
            self.end_headers()
            received["arrived"].set()

        def log_message(self, *args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def test_default_settings_are_on_and_point_at_the_production_service():
    settings = defaultUsageReportingSettings()
    assert settings == {
        "enabled": True,
        "endpoint": DEFAULT_ENDPOINT,
        "key": DEFAULT_KEY,
    }
    assert DEFAULT_ENDPOINT == "https://trace.danielstephenson.dev"
    assert DEFAULT_KEY.strip() == DEFAULT_KEY and DEFAULT_KEY


def test_default_settings_are_a_fresh_dict_each_time():
    # a shared dict would let one save's edits leak into the next test/save
    assert defaultUsageReportingSettings() is not defaultUsageReportingSettings()


def test_application_is_the_name_the_key_was_issued_for():
    assert APPLICATION == "ophidian"


def test_version_comes_from_version_txt_at_the_repository_root():
    assert os.path.basename(usage.VERSION_FILE) == "version.txt"
    with open(usage.VERSION_FILE) as f:
        expected = f.read().strip()
    assert expected, "version.txt is empty"
    assert readVersion() == expected
    assert startupTags() == {"version": expected}


def test_missing_or_empty_version_file_means_no_version_tag(tmp_path, monkeypatch):
    absent = os.path.join(tmp_path, "absent.txt")
    assert readVersion(absent) is None
    empty = tmp_path / "version.txt"
    empty.write_text("\n")
    assert readVersion(str(empty)) is None

    monkeypatch.setattr(usage, "VERSION_FILE", absent)
    assert readVersion() is None
    assert startupTags() == {}


def test_disabled_settings_yield_a_reporter_that_sends_nothing():
    for settings in (
        None,
        "not a dict",
        {"enabled": False, "endpoint": DEFAULT_ENDPOINT, "key": "k"},
        {"enabled": "true", "endpoint": DEFAULT_ENDPOINT, "key": "k"},
        {"enabled": True, "endpoint": DEFAULT_ENDPOINT, "key": ""},
        {"enabled": True, "endpoint": DEFAULT_ENDPOINT, "key": None},
    ):
        reporter = createUsageReporter(settings)
        assert isinstance(reporter, TraceClient)
        assert reporter.enabled is False, settings
        reporter.report("startup")  # must be a harmless no-op
        reporter.close()


def test_enabled_settings_report_under_the_program_name_to_the_configured_endpoint():
    received = {"arrived": threading.Event()}
    server = _stubServer(received)
    try:
        endpoint = "http://127.0.0.1:%d" % server.server_address[1]
        reporter = createUsageReporter(
            {"enabled": True, "endpoint": endpoint, "key": "test-key"}
        )
        assert reporter.enabled is True
        reporter.report("startup", tags=startupTags(version="9.9.9"))
        assert received["arrived"].wait(5), "the startup event never arrived"
        reporter.close()
    finally:
        server.shutdown()

    assert received["path"] == "/api/metrics"
    assert received["authorization"] == "Bearer test-key"
    assert received["body"] == {
        "application": "ophidian",
        "name": "startup",
        "tags": {"version": "9.9.9"},
    }


def test_first_run_notice_is_one_line_and_names_the_switch():
    assert "\n" not in FIRST_RUN_NOTICE
    assert FIRST_RUN_NOTICE.startswith(
        "Usage reporting is on: ophidian sends a startup event"
    )
    assert "trace.danielstephenson.dev" in FIRST_RUN_NOTICE
    assert '"usageReporting": {"enabled": false} in save.json' in FIRST_RUN_NOTICE
