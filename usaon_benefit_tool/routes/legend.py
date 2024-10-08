from flask import Blueprint, Response, send_file

from usaon_benefit_tool.constants.paths import PACKAGE_DIR
from usaon_benefit_tool.util.colormap import colormap_png_bytes

legend_bp = Blueprint('legend', __name__)


@legend_bp.route('/colorbar.png', methods=['GET'])
def get_colorbar_legend():
    return Response(
        colormap_png_bytes(),
        mimetype="image/png",
    )


@legend_bp.route('/line_thickness_legend.png', methods=['GET'])
def get_line_thickness_legend():
    filepath = PACKAGE_DIR / "static" / "line_thickness_legend.png"
    return send_file(filepath)
