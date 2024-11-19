import os
import sentry_sdk
from sentry_sdk.utils import ContextVar


_test_scope = ContextVar("test_scope", default=None)


def generator():
    with sentry_sdk.start_span(op="function", name="generator"):
        print(f"generator test_scope: {_test_scope.get()}")
        for x in range(10):
            with sentry_sdk.start_span(op="function", name="generator-chunk"):  # those spans work here, but not if in a Django streaming response
                token = _test_scope.set({"type": "in chunk"})
                yield x
                print(f"chunk test_scope: {_test_scope.get()}")
                _test_scope.reset(token)


def main():
    sentry_sdk.init(
        dsn=os.environ.get("SENTRY_DSN"),
        traces_sample_rate=1.0,
        debug=True,
    )
    token_outer = _test_scope.set({"type": "initial"})
    print(f"main begin test_scope: {_test_scope.get()}")

    with sentry_sdk.start_transaction(op="function", name="main"):
        token = _test_scope.set({"type": "in transaction"})
        print(f"main test_scope: {_test_scope.get()}")
        print(list(generator()))
        _test_scope.reset(token)

    print(f"main end1 test_scope: {_test_scope.get()}")

    _test_scope.reset(token_outer)
    print(f"main end2 test_scope: {_test_scope.get()}")


if __name__ == '__main__':
    main()