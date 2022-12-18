# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/10_lo.ipynb.

# %% auto 0
__all__ = ['Lo', 'lo']

# %% ../nbs/10_lo.ipynb 3
from typing import Union

import numpy as np
from fastcore.all import store_attr

from IPython.core.pylabtools import print_figure


from .utils import history_warning
from .repr_str import lovely
from .repr_plt import plot
from .repr_rgb import rgb
from .repr_chans import chans




# %% ../nbs/10_lo.ipynb 4
class RGBProxy():
    """Flexible `PIL.Image.Image` wrapper"""
    
    def __init__(self, x:np.ndarray):
        # super().__init__()
        assert x.ndim >= 3, f"Expecting at least 3 dimensions, got shape{x.shape}={x.ndim}"
        self.x = x

    def __call__(   self,
                    denorm=None,
                    cl=True,
                    gutter_px=3, frame_px=1,
                    scale=1,
                    view_width=966):

        return rgb(self.x, denorm=denorm, cl=cl, gutter_px=gutter_px,
                frame_px=frame_px, view_width=view_width, scale=scale)
    
    def _repr_png_(self):
        return self.__call__()._repr_png_()

# %% ../nbs/10_lo.ipynb 5
class ChanProxy():
    def __init__(self, x: np.ndarray):
        self.t = x
    
    def __call__(self,
                 cmap = "twilight",
                 cm_below="blue",
                 cm_above="red",
                 cm_ninf="cyan",
                 cm_pinf="fuchsia",
                 cm_nan="yellow",
                 view_width=966,
                 gutter_px=3,
                 frame_px=1,
                 scale=1):
        
        return chans(self.t,
                     cmap=cmap,
                     cm_below=cm_below,
                     cm_above=cm_above,
                     cm_ninf=cm_ninf,
                     cm_pinf=cm_pinf,
                     cm_nan=cm_nan,
                     view_width=view_width,
                     gutter_px=gutter_px,
                     frame_px=frame_px,
                     scale=scale)
    
    def _repr_png_(self):
        return self.__call__()._repr_png_()

# %% ../nbs/10_lo.ipynb 6
class PlotProxy(): 
    """Flexible `PIL.Image.Image` wrapper"""
    
    def __init__(self, x:np.ndarray, center="zero", max_s=10000, plt0=True, fmt="png"):
        self.x = x
        self.center = center
        self.fmt = fmt
        self.max_s = max_s
        self.plt0 = plt0
        assert fmt in ["png", "svg"]
        assert center in ["zero", "mean", "range"]

    def __call__(self, center=None, max_s=None, plt0=None, fmt=None, ax=None):
        center = center or self.center
        fmt = fmt or self.fmt
        if max_s is None: max_s = self.max_s
        if plt0 is None: plt0 = self.plt0
        if ax:
            plot(self.x, center=center, max_s=max_s, plt0=plt0, ax=ax)
            return ax

        return PlotProxy(self.x, center=center, max_s=max_s, plt0=plt0, fmt=fmt)

    # Do an explicit print_figure instead of relying on IPythons repr formatter
    # for pyplot.Figure. Mainly for speed.
    #
    # IPython will attempt to render the figure in a bunch of formats, and then
    # pick one to show. This takes a noticeable amount of time. Render just
    # one format instead.
    def _repr_svg_(self):
        if self.fmt == "svg":
            return print_figure(plot(self.x, center=self.center, max_s=self.max_s, plt0=self.plt0), fmt="svg")

    def _repr_png_(self):
        if self.fmt == "png":
            return print_figure(plot(self.x, center=self.center, max_s=self.max_s, plt0=self.plt0), fmt="png")


# %% ../nbs/10_lo.ipynb 7
class Lo():
    """Lo and behold! What a lovely `numpy.ndarray`!"""
    def __init__(   self,
                    x: Union[np.ndarray, np.generic], # Your data
                    plain       =False, # Show as plain text - values only
                    verbose     =False, # Verbose - show values too
                    depth       =0,     # Expand up to `depth`
                    color :bool =None): # Use ANSI colors
        store_attr()
        history_warning()

    def __repr__(self):
        return lovely(self.x, plain=self.plain, verbose=self.verbose,
                      depth=self.depth, color=self.color)

    @property
    def v(self):
        "Verbose"
        return Lo(self.x, verbose=True, color=self.color)

    @property
    def p(self):
        "Good old plain representation"
        return Lo(self.x, plain=True, color=self.color)

    @property
    def deeper(self):
        "Going deeper"
        return Lo(self.x, verbose=False, plain=False, depth=1, color=self.color)

    @property
    def rgb(self):
        "Show an image"
        return RGBProxy(self.x)

    @property
    def chans(self):
        "Show color channels"
        return ChanProxy(self.x)

    @property
    def plt(self):
        return PlotProxy(self.x)

    # This is used for .deeper attribute and .deeper(depth=...).
    # The second one results in a __call__.
    def __call__(self, depth=1):
        return Lo(self.x, depth=depth, color=self.color)

# %% ../nbs/10_lo.ipynb 8
def lo(x: Union[np.ndarray, np.generic],    # Your data
        plain       =False, # Show as plain text - values only
        verbose     =False, # Verbose - show values too
        depth       =0,     # Expand up to `depth`
        color :bool =None): # Use ANSI colors
    return Lo(x, plain=plain, verbose=verbose, depth=depth, color=color)
