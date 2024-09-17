from typing import Callable, Optional, List, Union, Iterable, Sequence, Mapping


def clear_graph_cache():
    """Clears the graph cache which gets populated if `graph_caching` is set
    to `True` in `ivy.trace_graph`, `ivy.transpile` or `ivy.unify`. Use this to
    reset or clear the graph cache if needed.

    Examples
    --------
    >>> import ivy
    >>> ivy.clear_graph_cache()"""

    from ._compiler import clear_graph_cache as _clear_graph_cache

    return _clear_graph_cache()


def graph_transpile(
    *objs: Callable,
    source: Optional[str] = None,
    to: Optional[str] = None,
    with_numpy: bool = True,
    backend_compile: bool = False,
    static_argnums: Optional[Union[int, Iterable[int]]] = None,
    static_argnames: Optional[Union[str, Iterable[str]]] = None,
    compile_mode: Optional[str] = None,
    graph_caching: bool = True,
    graph_optimizations: bool = True,
    modes_to_trace: str = "all",
    stateful: Optional[List] = None,
    arg_stateful_idxs: Optional[List] = None,
    kwarg_stateful_idxs: Optional[List] = None,
    args: Optional[Sequence] = None,
    kwargs: Optional[Mapping] = None,
    params_v=None,
    v=None
):
    """Transpiles Callable objects passed as arguments. If args and kwargs are
    specified, transpilation is performed eagerly, otherwise, transpilation
    will happen lazily.

    Parameters
    ----------
    objs
        The native Callables to be transpiled
    source
        The framework that `obj` is from.
    to
        The target framework to transpile `obj` to.
    args
        If specified, arguments that will be used to transpile eagerly.
    kwargs
        If specified, keyword arguments that will be used to transpile eagerly.

    Returns
    -------
    Either a transpiled Graph or a non-initialized LazyGraph."""

    from ._compiler import graph_transpile as _graph_transpile

    return _graph_transpile(
        *objs,
        source=source,
        to=to,
        with_numpy=with_numpy,
        backend_compile=backend_compile,
        static_argnums=static_argnums,
        static_argnames=static_argnames,
        compile_mode=compile_mode,
        graph_caching=graph_caching,
        graph_optimizations=graph_optimizations,
        modes_to_trace=modes_to_trace,
        stateful=stateful,
        arg_stateful_idxs=arg_stateful_idxs,
        kwarg_stateful_idxs=kwarg_stateful_idxs,
        args=args,
        kwargs=kwargs,
        params_v=params_v,
        v=v,
    )


def source_to_source(
    object,
    source: str = "torch",
    target: str = "tensorflow",
    reuse_existing: bool = True,
):
    """Converts a given object (class/function) from one framework to another.

    This function performs source-to-source translation of a given object from the source framework
    to the target framework.

    The object can be translated between two frameworks or between the Ivy IR as well
    e.g. (source="torch_frontend", target="ivy") or (source="torch_frontend", target="tensorflow") etc.

    Args:
        object: The object (class/function) to be translated.
        source (str, optional): The source framework. Defaults to 'torch'.
        target (str, optional): The target framework. Defaults to 'tensorflow'.
        reuse_existing (bool, optional): If True, the function will check if `object`
                                         already exists in the translated directory and reuse it.
                                         If False, it will re-translate `object`,
                                         even if it already exists in the directory, and overwrite
                                         the old implementation. Defaults to 'True'.

    Returns:
        The translated object."""

    from ._compiler import source_to_source as _source_to_source

    return _source_to_source(
        object=object,
        source=source,
        target=target,
        reuse_existing=reuse_existing,
    )


def trace_graph(
    *objs: Callable,
    stateful: Optional[List] = None,
    arg_stateful_idxs: Optional[List] = None,
    kwarg_stateful_idxs: Optional[List] = None,
    to: Optional[str] = None,
    include_generators: bool = True,
    array_caching: bool = True,
    with_numpy: bool = True,
    modes_to_trace: str = "all",
    backend_compile: bool = False,
    static_argnums: Optional[Union[int, Iterable[int]]] = None,
    static_argnames: Optional[Union[str, Iterable[str]]] = None,
    compile_mode: Optional[str] = None,
    graph_caching: bool = True,
    args: Optional[Sequence] = None,
    kwargs: Optional[Mapping] = None,
    params_v=None,
    v=None
):
    """Takes `fn` and traces it into a more efficient composition of backend operations.

    Parameters
    ----------
    objs
        callable(s) to trace and create a graph of
    stateful
        list of instances to be considered stateful during the graph tracing
    arg_stateful_idxs
        positional arguments to be considered stateful during the graph tracing
    kwarg_stateful_idxs
        keyword arguments to be considered stateful during the graph tracing
    include_generators
        include array creation/generation functions as part of the graph
    array_caching
        cache the constant arrays that appear as arguments to the functions in the graph
    modes_to_trace
        the module mode(s) which should be traced when tracing a trainable module
        can be either "all", "train" or "eval".
    backend_compile
        whether to apply the native compilers, i.e. tf.function, after ivy's tracing
    static_argnums
        for jax's jit compilation
    static_argnames
        for jax's jit compilation
    compile_mode
        mode for torch's compilation
    graph_caching
        whether to cache the traced graph
    args
        positional arguments for `obj`
    kwargs
        keyword arguments for `obj`

    Returns
    -------
    the traced `Graph` object.

    Examples
    --------
    >>> import ivy, time
    >>> from ivy import trace_graph
    >>> ivy.set_backend("torch")
    >>> x = ivy.array([1.])

    >>> def fn(x):
    ...     y = ivy.sum(x)
    ...     z = ivy.prod(x)
    ...     a = ivy.sin(y)
    ...     b = ivy.cos(z)
    ...     c = ivy.tan(z)
    ...     i = ivy.round(a)
    ...     j = ivy.floor(b)
    ...     k = ivy.ceil(c)
    ...     return i, j, k


    >>> graph = trace_graph(fn, args=(x,))

    Notice how the time taken to execute the traced function is lower than
    the original function. A typical run:

    >>> start = time.time()
    >>> fn(x)
    >>> print(time.time() - start)
    0.0003559589385986328

    >>> start = time.time()
    >>> graph(x)
    >>> print(time.time() - start)
    0.0001785755157470703"""

    from ._compiler import trace_graph as _trace_graph

    return _trace_graph(
        *objs,
        stateful=stateful,
        arg_stateful_idxs=arg_stateful_idxs,
        kwarg_stateful_idxs=kwarg_stateful_idxs,
        to=to,
        include_generators=include_generators,
        array_caching=array_caching,
        with_numpy=with_numpy,
        modes_to_trace=modes_to_trace,
        backend_compile=backend_compile,
        static_argnums=static_argnums,
        static_argnames=static_argnames,
        compile_mode=compile_mode,
        graph_caching=graph_caching,
        args=args,
        kwargs=kwargs,
        params_v=params_v,
        v=v,
    )


def transpile(
    object,
    source: str = "torch",
    target: str = "tensorflow",
    reuse_existing: bool = True,
):
    """Converts a given object (class/function) from one framework to another.

    This function performs source-to-source translation of a given object from the source framework
    to the target framework.

    The object can be translated between two frameworks or between the Ivy IR as well
    e.g. (source="torch_frontend", target="ivy") or (source="torch_frontend", target="tensorflow") etc.

    Args:
        object: The object (class/function) to be translated.
        source (str, optional): The source framework. Defaults to 'torch'.
        target (str, optional): The target framework. Defaults to 'tensorflow'.
        reuse_existing (bool, optional): If True, the function will check if `object`
                                         already exists in the translated directory and reuse it.
                                         If False, it will re-translate `object`,
                                         even if it already exists in the directory, and overwrite
                                         the old implementation. Defaults to 'True'.

    Returns:
        The translated object."""

    from ._compiler import transpile as _transpile

    return _transpile(
        object=object,
        source=source,
        target=target,
        reuse_existing=reuse_existing,
    )


def unify(
    *objs: Callable,
    source: Optional[str] = None,
    graph_caching: bool = True,
    graph_optimizations: bool = True,
    args: Optional[Sequence] = None,
    kwargs: Optional[Mapping] = None,
    with_numpy: bool = True,
    modes_to_trace: str = "all",
    **transpile_kwargs
):

    from ._compiler import unify as _unify

    return _unify(
        *objs,
        source=source,
        graph_caching=graph_caching,
        graph_optimizations=graph_optimizations,
        args=args,
        kwargs=kwargs,
        with_numpy=with_numpy,
        modes_to_trace=modes_to_trace,
        **transpile_kwargs,
    )
