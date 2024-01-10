"""Run tests for a single Python version."""

import sys

import anyio
import dagger


async def test():
    versions = ["3.9", "3.10", "3.11"]

    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        # get reference to the local project
        src = client.host().directory(".")
        platform = dagger.Platform("linux/amd64")

        async def test_version(version: str):
            python = (
                client.container(platform=platform)
                .from_(f"python:{version}-slim-bullseye")
                # mount cloned repository into image
                .with_mounted_directory("/src", src)
                # set current working directory for next commands
                .with_workdir("/src")
                # install test dependencies
                .with_exec(["pip", "install", "-r", "requirements-test.txt"])
                # run tests
                .with_exec(["pytest", "tests"])
            )

            print(f"Running tests for Python {version}...")

            # execute
            await python.exit_code()

        async with anyio.create_task_group() as tg:
            for version in versions:
                tg.start_soon(test_version, version)

    print("All tasks have finished!")


if __name__ == "__main__":
    anyio.run(test)
