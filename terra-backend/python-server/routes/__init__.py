from .health import bp as health_bp
from .graph import bp as graph_bp
from .timeseries import bp as timeseries_bp
from .data import bp as data_bp

ALL_BLUEPRINTS = [health_bp, graph_bp, timeseries_bp, data_bp]
