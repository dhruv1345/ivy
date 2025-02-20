import copy
import io
import requests
import ivy
import jax
import jax.numpy as jnp
import flax.nnx as nnx
import numpy as np
import pytest
import tensorflow as tf
import torch

jax.config.update("jax_enable_x64", True)


# Helpers #
# ------- #


def _check_allclose(x, y, tolerance=1e-3):
    """
    Checks that all values are close. Any arrays must already be in numpy format, rather than native framework.
    """

    if isinstance(x, np.ndarray):
        assert np.allclose(x, y, atol=tolerance), "numpy array values are not all close"
        return

    if isinstance(x, (list, set, tuple)):
        all(
            [
                _check_allclose(element_x, element_y, tolerance=tolerance)
                for element_x, element_y in zip(x, y)
            ]
        )
        return

    if isinstance(x, dict):
        all([key_x == key_y for key_x, key_y in zip(x.keys(), y.keys())])
        all(
            [
                _check_allclose(element_x, element_y, tolerance=tolerance)
                for element_x, element_y in zip(x.values(), y.values())
            ]
        )
        return

    if isinstance(x, float):
        assert x - y < tolerance, f"float values differ: {x} != {y}"
        return

    assert x == y, f"values differ: {x} != {y}"


def _native_array_to_numpy(x):
    if isinstance(x, torch.Tensor):
        return x.detach().numpy()
    if isinstance(x, tf.Tensor):
        return x.numpy()
    if isinstance(x, jnp.ndarray):
        return np.asarray(x)
    if isinstance(x, nnx.Variable):
        return np.asarray(x.value)
    return x


def _nest_array_to_numpy(nest, shallow=True):
    return ivy.nested_map(
        lambda x: _native_array_to_numpy(x),
        nest,
        include_derived=True,
        shallow=shallow,
    )


def _array_to_new_backend(
    x,
    target,
):
    """
    Converts a torch tensor to an array/tensor in a different framework.
    If the input is not a torch tensor, the input if returned without modification.
    """

    if isinstance(x, torch.Tensor):
        if target == "torch":
            return x
        y = x.detach().numpy()
        if target == "jax":
            y = jnp.array(y)
        elif target == "tensorflow":
            y = tf.convert_to_tensor(y)
        return y
    else:
        return x


def _nest_torch_tensor_to_new_framework(nest, target, shallow=True):
    return ivy.nested_map(
        lambda x: _array_to_new_backend(x, target),
        nest,
        include_derived=True,
        shallow=shallow,
    )


def download_image(url: str, filename: str = "") -> str:
    filename = url.split("/")[-1] if len(filename) == 0 else filename
    # Download
    bytesio = io.BytesIO(requests.get(url).content)
    # Save file
    with open(filename, "wb") as outfile:
        outfile.write(bytesio.getbuffer())

    return filename
