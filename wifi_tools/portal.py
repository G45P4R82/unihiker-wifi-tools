"""Authorized training portal with no password collection."""

import json
import os
import threading
from datetime import datetime

from flask import Flask, jsonify, render_template, request

from .captive import RedirectRules, WildcardDns


class TrainingPortal:
    def __init__(self, host="0.0.0.0", port=8081, data_dir="portal-data"):
        self.host = host
        self.port = port
        self.data_dir = data_dir
        self.app = Flask(__name__, template_folder="templates")
        self._server = None
        self._dns = None
        self._redirects = None
        self.redirect_error = None
        self._configure_routes()

    def _record(self, event, campaign, code):
        os.makedirs(self.data_dir, exist_ok=True)
        path = os.path.join(self.data_dir, "events.jsonl")
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "event": event,
            "campaign": campaign[:80],
            "training_code": code[:80],
        }
        with open(path, "a") as stream:
            stream.write(json.dumps(entry) + "\n")

    def _configure_routes(self):
        @self.app.get("/")
        @self.app.get("/generate_204")
        @self.app.get("/hotspot-detect.html")
        @self.app.get("/connecttest.txt")
        def index():
            campaign = request.args.get("campaign", "WiFi Security Training")
            return render_template("portal.html", campaign=campaign[:80])

        @self.app.post("/training")
        def training():
            campaign = request.form.get("campaign", "WiFi Security Training")
            code = request.form.get("training_code", "")
            self._record("training_submission", campaign, code)
            return render_template("complete.html", campaign=campaign[:80])

        @self.app.get("/api/status")
        def api_status():
            return jsonify({
                "running": True,
                "port": self.port,
                "transparent_redirect": self.redirect_error is None,
            })

    def start(self):
        from werkzeug.serving import make_server
        try:
            self._dns = WildcardDns()
            self._dns.start()
            try:
                self._redirects = RedirectRules(http_port=self.port)
                self._redirects.start()
            except RuntimeError as error:
                self._redirects = None
                self.redirect_error = str(error)
            self._server = make_server(self.host, self.port, self.app)
        except Exception:
            self.stop()
            raise
        thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        thread.start()

    def stop(self):
        if self._server:
            self._server.shutdown()
            self._server = None
        if self._redirects:
            self._redirects.stop()
            self._redirects = None
        if self._dns:
            self._dns.stop()
            self._dns = None
