from flask import Blueprint, Response

from usaon_benefit_tool.util.colormap import colormap_png_bytes

legend_bp = Blueprint('legend', __name__)


@legend_bp.route('/colorbar.png', methods=['GET'])
def get_colorbar_legend():
    return Response(
        colormap_png_bytes(),
        mimetype="image/png",
    )
