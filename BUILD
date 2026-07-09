# Third-party requirements are read straight from pyproject.toml, so Pants and uv
# share a single source of truth for runtime dependencies.
python_requirements(
    name="reqs",
    source="pyproject.toml",
)

# httpx is a test-only dependency (Starlette's TestClient needs an HTTP client).
# It lives in pyproject's `dev` extra for uv; declared here so Pants test targets
# can depend on it without it becoming a runtime requirement of calcstack.
python_requirement(
    name="httpx",
    requirements=["httpx>=0.27,<1"],
)
