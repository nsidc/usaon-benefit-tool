from flask import Blueprint, Response

from usaon_benefit_tool.util.colormap import colormap_png_bytes

colorbar_bp = Blueprint('colorbar', __name__)


@colorbar_bp.route('/colorbar.png', methods=['GET'])
def get():
    return Response(
        colormap_png_bytes(),
        mimetype="image/png",
    )
