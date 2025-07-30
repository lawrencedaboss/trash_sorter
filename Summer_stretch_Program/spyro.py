from spyrograph import Hypotrochoid # type: ignore
import numpy as np # type: ignore

Hypotrochoid.animate(
    R=307,
    r=np.arange(57, 75, .05),
    d=33,
    thetas=np.arange(0,100, .1),
    frame_pause=.02
)