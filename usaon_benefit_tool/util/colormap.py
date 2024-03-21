from functools import cache
from io import BytesIO

from leafmap.colormaps import create_colormap
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.colors import Normalize, rgb2hex

from usaon_benefit_tool.constants.colormap import (
    COLORMAP,
    COLORMAP_DATA_VALUE_RANGE,
    COLORMAP_PALETTE,
)

# TODO: Should we be using BoundaryNorm instead?
norm = Normalize(
    vmin=COLORMAP_DATA_VALUE_RANGE[0],
    vmax=COLORMAP_DATA_VALUE_RANGE[1],
)


def color_for_performance_rating(performance_rating: int):
    """Return the hex color value for the given performance rating."""
    lookup_val = norm(performance_rating)

    color = COLORMAP(lookup_val)
    return rgb2hex(color)


@cache
def colormap_png_bytes() -> bytes:
    """Render the colormap as a binary image (png).

    TODO: Rewrite in pure matplotlib. I struggled to do this quickly. Leafmap got the
    ticks right but still struggling with text getting cut off (hence call to
    `subplots_adjust()`).
    """
    fig = create_colormap(
        colors=COLORMAP_PALETTE,
        discrete=True,
        vmin=COLORMAP_DATA_VALUE_RANGE[0],
        vmax=COLORMAP_DATA_VALUE_RANGE[1],
    )
    fig.subplots_adjust(bottom=0.6, hspace=1)

    output = BytesIO()
    FigureCanvas(fig).print_png(output)
    return output.getvalue()
