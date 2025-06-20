from enum import Enum

import numpy as np


class OutputMode(str, Enum):
    RGB = "RGB"  # RGB data
    RGBW_NONE = "RGBW No White"  # No white channel, just set to 0
    RGBW_ACCURATE = "RGBW Accurate"  # Color accuracy approach (minimum RGB)
    RGBW_BRIGHTER = (
        "RGBW Brighter"  # Compute white, but don't subtract from RGB
    )


def rgb_to_output_mode(rgb_array, output_mode):
    """Convert an RGB array to an array formatted according to ``output_mode``.

    Parameters
    ----------
    rgb_array : :class:`numpy.ndarray`
        Array of shape ``(n, 3)`` representing RGB data.
    output_mode : :class:`~OutputMode`
        Mode specifying how the white channel is generated. Valid values are
        ``OutputMode.RGB`` (return RGB only), ``OutputMode.RGBW_NONE`` (append a
        zero white channel), ``OutputMode.RGBW_ACCURATE`` (subtract the minimum
        RGB value) and ``OutputMode.RGBW_BRIGHTER`` (do not subtract from RGB).

    Returns
    -------
    :class:`numpy.ndarray`
        Array of shape ``(n, 4)`` representing RGBW data.
    """
    # Ensure the input is properly shaped
    assert rgb_array.shape[1] == 3, "Input array must have shape (n, 3)"

    if output_mode == OutputMode.RGB:
        # No conversion needed, just return the original RGB array
        return rgb_array

    # Number of RGB values
    n = rgb_array.shape[0]

    # Create the white channel based on the selected method
    if output_mode == OutputMode.RGBW_NONE:
        # No white channel, just zeros
        w = np.zeros((n, 1), dtype=rgb_array.dtype)
        rgb_adjusted = rgb_array.copy()

    elif output_mode == OutputMode.RGBW_BRIGHTER:
        # Brighter method: use min value for white, don't subtract from RGB
        w = np.min(rgb_array, axis=1, keepdims=True)
        rgb_adjusted = rgb_array

    elif output_mode == OutputMode.RGBW_ACCURATE:
        # Accurate method: use min value for white, subtract from RGB
        w = np.min(rgb_array, axis=1, keepdims=True)
        rgb_adjusted = rgb_array - w

    else:
        raise ValueError(
            f"Unknown output mode: {output_mode}"
        )

    # Concatenate RGB and W channels
    rgbw_array = np.concatenate((rgb_adjusted, w), axis=1)

    return rgbw_array
