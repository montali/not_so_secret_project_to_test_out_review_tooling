python_sources(name="cli")

# `pants package src/calcstack/cli:calcstack-bin` builds a standalone PEX that
# runs the CLI without a pre-existing virtualenv.
pex_binary(
    name="calcstack-bin",
    entry_point="calcstack.cli.main:main",
)
