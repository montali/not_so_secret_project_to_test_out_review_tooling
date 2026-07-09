# Ship the static web assets alongside the Python sources so `FileResponse`
# can find them when the package is installed or run under Pants.
resources(
    name="static",
    sources=["static/*"],
)

python_sources(
    name="api",
    dependencies=[":static"],
)
