"""
Docker-specific tests to verify container functionality.
"""

import os
import subprocess
import time

import pytest
import requests


@pytest.mark.docker
class TestDockerBuild:
    """Tests for Docker build process."""

    def test_dockerfile_exists(self):
        """Test that Dockerfile exists."""
        assert os.path.exists("Dockerfile")

    def test_docker_compose_exists(self):
        """Test that docker-compose.yml exists."""
        assert os.path.exists("docker-compose.yml")

    def test_docker_compose_dev_exists(self):
        """Test that docker-compose.dev.yml exists."""
        assert os.path.exists("docker-compose.dev.yml")

    def test_docker_compose_test_exists(self):
        """Test that docker-compose.test.yml exists."""
        assert os.path.exists("docker-compose.test.yml")


@pytest.mark.docker
@pytest.mark.skipif(
    os.getenv("SKIP_DOCKER_TESTS") == "1", reason="Docker tests skipped in this environment"
)
class TestDockerComposeValidation:
    """Tests for docker-compose configuration validation."""

    def test_docker_compose_config_valid(self):
        """Test that docker-compose.yml is valid."""
        try:
            result = subprocess.run(
                ["docker", "compose", "-f", "docker-compose.yml", "config"],
                capture_output=True,
                text=True,
                timeout=30,
            )
            # docker compose config returns 0 on success
            assert result.returncode == 0, f"docker-compose.yml is invalid: {result.stderr}"
        except FileNotFoundError:
            pytest.skip("Docker not available in test environment")
        except subprocess.TimeoutExpired:
            pytest.fail("Docker compose config command timed out")

    def test_docker_compose_dev_config_valid(self):
        """Test that docker-compose.dev.yml is valid."""
        try:
            result = subprocess.run(
                ["docker", "compose", "-f", "docker-compose.dev.yml", "config"],
                capture_output=True,
                text=True,
                timeout=30,
            )
            assert result.returncode == 0, f"docker-compose.dev.yml is invalid: {result.stderr}"
        except FileNotFoundError:
            pytest.skip("Docker not available in test environment")

    def test_docker_compose_test_config_valid(self):
        """Test that docker-compose.test.yml is valid."""
        try:
            result = subprocess.run(
                ["docker", "compose", "-f", "docker-compose.test.yml", "config"],
                capture_output=True,
                text=True,
                timeout=30,
            )
            assert result.returncode == 0, f"docker-compose.test.yml is invalid: {result.stderr}"
        except FileNotFoundError:
            pytest.skip("Docker not available in test environment")


@pytest.mark.docker
class TestDockerIgnore:
    """Tests for .dockerignore file."""

    def test_dockerignore_exists(self):
        """Test that .dockerignore exists."""
        assert os.path.exists(".dockerignore")

    def test_dockerignore_has_common_patterns(self):
        """Test that .dockerignore has common ignore patterns."""
        with open(".dockerignore", "r") as f:
            content = f.read()

        # Check for common patterns
        common_patterns = [
            ".git",
            "__pycache__",
            "*.py[cod]",  # Covers .pyc, .pyo, .pyd
        ]

        for pattern in common_patterns:
            assert (
                pattern in content
            ), f"Pattern '{pattern}' not found in .dockerignore"
