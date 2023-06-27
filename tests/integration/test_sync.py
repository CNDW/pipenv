import json
import os

import pytest

from pipenv.utils.shell import temp_environ


@pytest.mark.lock
@pytest.mark.sync
def test_sync_error_without_lockfile(pipenv_instance_pypi):
    with pipenv_instance_pypi(chdir=True) as p:
        with open(p.pipfile_path, "w") as f:
            f.write(
                """
[packages]
            """.strip()
            )

        c = p.pipenv("sync")
        assert c.returncode != 0
        assert "Pipfile.lock not found!" in c.stderr


@pytest.mark.sync
@pytest.mark.lock
def test_mirror_lock_sync(pipenv_instance_private_pypi):
    with temp_environ(), pipenv_instance_private_pypi(chdir=True) as p:
        mirror_url = os.environ.get("PIPENV_TEST_INDEX")
        assert "pypi.org" not in mirror_url
        with open(p.pipfile_path, "w") as f:
            f.write(
                """
[[source]]
name = "pypi"
url = "https://pypi.org/simple"
verify_ssl = true

[packages]
six = "*"
            """.strip()
            )
        c = p.pipenv(f"lock --pypi-mirror {mirror_url}")
        assert c.returncode == 0
        c = p.pipenv(f"sync --pypi-mirror {mirror_url}")
        assert c.returncode == 0


@pytest.mark.sync
@pytest.mark.lock
def test_sync_should_not_lock(pipenv_instance_pypi):
    """Sync should not touch the lock file, even if Pipfile is changed."""
    with pipenv_instance_pypi(chdir=True) as p:
        with open(p.pipfile_path, "w") as f:
            f.write(
                """
[packages]
            """.strip()
            )

        # Perform initial lock.
        c = p.pipenv("lock")
        assert c.returncode == 0
        lockfile_content = p.lockfile
        assert lockfile_content

        # Make sure sync does not trigger lockfile update.
        with open(p.pipfile_path, "w") as f:
            f.write(
                """
[packages]
six = "*"
            """.strip()
            )
        c = p.pipenv("sync")
        assert c.returncode == 0
        assert lockfile_content == p.lockfile


@pytest.mark.sync
def test_sync_consider_pip_target(pipenv_instance_pypi):
    """ """
    with pipenv_instance_pypi(chdir=True) as p:
        with open(p.pipfile_path, "w") as f:
            f.write(
                """
[packages]
six = "*"
            """.strip()
            )

        # Perform initial lock.
        c = p.pipenv("lock")
        assert c.returncode == 0
        lockfile_content = p.lockfile
        assert lockfile_content
        c = p.pipenv("sync")
        assert c.returncode == 0

        pip_target_dir = "target_dir"
        os.environ["PIP_TARGET"] = pip_target_dir
        c = p.pipenv("sync")
        assert c.returncode == 0
        assert "six.py" in os.listdir(os.path.join(p.path, pip_target_dir))
        os.environ.pop("PIP_TARGET")


@pytest.mark.sync
@pytest.mark.needs_internet
def test_sync_resolves_cross_index_dependencies(pipenv_instance_pypi):
    """ """
    with pipenv_instance_pypi(chdir=True) as p:
        with open(p.pipfile_path, "w") as f:
            f.write(
                """
[[source]]
name = "pypi"
url = "https://pypi.org/simple"
verify_ssl = true

[[source]]
name = "local"
url = "http://localhost:8080/simple"
verify_ssl = true

[packages]
private-package-a = {version="*", index="local"}
private-package-b = {version="*", index="local"}
            """.strip()
            )
        with open(p.lockfile_path, "w") as f:
            f.write(
                """
{
    "_meta":
    {
        "hash": {
            "sha256": "21bb8639c623eb7c8a082f9be7b6c8599e5c553c159669025c38ef74fecb5e42"
        },
        "pipfile-spec": 6,
        "requires": {},
        "sources": [
            {
                "name": "pypi",
                "url": "https://pypi.org/simple",
                "verify_ssl": true
            },
            {
                "name": "local",
                "url": "http://localhost:8080/simple",
                "verify_ssl": true
            }
        ]
    },
    "default": {
        "attrs": {
            "hashes": [
                "sha256:1f28b4522cdc2fb4256ac1a020c78acf9cba2c6b461ccd2c126f3aa8e8335d04",
                "sha256:6279836d581513a26f1bf235f9acd333bc9115683f14f7e8fae46c98fc50e015"
            ],
            "markers": "python_version >= '3.7'",
            "version": "==23.1.0"
        },
        "colorama": {
            "hashes": [
                "sha256:08695f5cb7ed6e0531a20572697297273c47b8cae5a63ffc6d6ed5c201be6e44",
                "sha256:4f1d9991f5acc0ca119f9d443620b77f9d6b33703e51011c16baf57afb285fc6"
            ],
            "markers": "python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6'",
            "version": "==0.4.6"
        },
        "private-package-a": {
            "hashes": [
                "sha256:df103804a7b35bef6c2a258e5048c3f9a813fb556bbee2d96656e6fcec372d86"
            ],
            "index": "local",
            "version": "==0.0.1"
        },
        "private-package-b": {
            "hashes": [
                "sha256:e107f2f54c5c355fcf354818d21d3ba7f1899819b0fe7991e0e11918e94b62cb"
            ],
            "index": "local",
            "version": "==0.0.1"
        },
        "six": {
            "hashes": [
                "sha256:1e61c37477a1626458e36f7b1d82aa5c9b094fa4802892072e49de9c60c4c926",
                "sha256:8abb2f1d86890a2dfb989f9a77cfcfd3e47c2a354b01111771326f8aa26e0254"
            ],
            "index": "pypi",
            "version": "==1.16.0"
        },
        "vistir": {
            "hashes": [
                "sha256:7b8d2301c860707a7a7f02c457eef685b9711470a6df157b692baf529606622f",
                "sha256:dde88ef0d45dc1ad423fff2f0ad0e29e230de1b02457bdff5053dacd60ffcf97"
            ],
            "markers": "python_version >= '3.7'",
            "version": "==0.8.0"
        }
    },
    "develop": {}
}
            """.strip()
            )

        c = p.pipenv("sync")
        assert c.returncode == 0
