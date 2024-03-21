from leafmap.colormaps import get_palette
from matplotlib import colormaps, colors

COLORMAP_CLASSES = 8
COLORMAP_DATA_VALUE_RANGE = (0, 100)

cmap_name = 'viridis'
cmap = colormaps[cmap_name]
# FIXME: This duplication is only for expedience. We can do this in pure matplotlib
#        without leafmap.
COLORMAP_PALETTE = get_palette(cmap_name, n_class=COLORMAP_CLASSES)

COLORMAP = colors.LinearSegmentedColormap.from_list(
    f'{cmap_name}_{COLORMAP_CLASSES}',
    cmap.colors,
    N=COLORMAP_CLASSES,
)
