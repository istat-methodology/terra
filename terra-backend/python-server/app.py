from __future__ import annotations

import os

from flask import Flask
from flask_cors import CORS
from waitress import serve
from dotenv import load_dotenv

from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.ext.flask.flask_middleware import FlaskMiddleware
from opencensus.trace.samplers import ProbabilitySampler

from modules import utils, orm
from resources import py_server_params
from routes import ALL_BLUEPRINTS

from modules.db import make_session_factory
from modules.graph_engine import GraphEngine
from modules.request_handler import RequestHandler
from modules.misc import Misc
from modules.timeseries import TimeSeries


def _str_to_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _maybe_enable_azure_tracing(app: Flask, logger) -> None:
    enabled = _str_to_bool(os.getenv("ENABLE_AZURE_TRACING"), default=False)
    if not enabled:
        logger.info("[TERRA] Azure tracing disabled.")
        return

    try:
        azure_exporter = AzureExporter()
        azure_exporter.add_telemetry_processor(utils.ai_callback_function)

        FlaskMiddleware(
            app,
            exporter=azure_exporter,
            sampler=ProbabilitySampler(rate=1.0),
        )
        logger.info("[TERRA] Azure tracing enabled.")
    except BaseException as e:
        logger.warning(f"[TERRA] Azure tracing setup failed: {e}")


def create_app() -> Flask:
    # Do not override real environment variables (Azure/App Service)
    load_dotenv(override=False)

    logger = utils.get_logger()
    utils.execute_preliminaries(logger)

    if not py_server_params.DB_SETTINGS.get("CONNECTION_STRING"):
        logger.warning("[TERRA] DB connection string is empty. Check your .env / App Service settings.")

    engine = orm.orm_setup(py_server_params.DB_SETTINGS)
    SessionFactory = make_session_factory(engine)

    app = Flask(__name__)

    app.config["SERVICES"] = {
        "logger": logger,
        "engine": engine,
        "session_factory": SessionFactory,
        "params": py_server_params,
        "orm": orm,
        "misc": Misc(engine, logger, SessionFactory),
        "graphs": GraphEngine(engine, logger, SessionFactory, country_eu_table=orm.countryEU),
        "timeseries": TimeSeries(engine, logger, SessionFactory, country_eu_table=orm.countryEU),
        "request_handler": RequestHandler(
            logger,
            criterion=str(py_server_params.ENDPOINT_SETTINGS["CRITERION"]),
        ),
    }

    # CORS (keep permissive by default; you can restrict with env later)
    CORS(app, resources={r"/*": {"origins": "*"}})

    _maybe_enable_azure_tracing(app, logger)

    for bp in ALL_BLUEPRINTS:
        app.register_blueprint(bp)

    return app


def main() -> None:
    app = create_app()
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "5500"))
    serve(app, host=host, port=port)


if __name__ == "__main__":
    main()
