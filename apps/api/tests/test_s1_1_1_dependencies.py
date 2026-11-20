"""S1.1.1: the kit symbols later features build on import."""


def test_s1_1_1_1_kit_symbols_import() -> None:
    from rn_forge.commons import PathUtils, TaskPool, ThreadActor
    from rn_forge.fastapi.sse import sse_response

    for symbol in (ThreadActor, TaskPool, PathUtils, sse_response):
        assert callable(symbol)
