python_tests(
    name="tests",
    # Starlette's TestClient (used by the API/web tests) needs httpx. Declared
    # target-wide so this BUILD file stays valid at every point in the PR stack,
    # even before the API tests exist.
    dependencies=["//:httpx"],
)
