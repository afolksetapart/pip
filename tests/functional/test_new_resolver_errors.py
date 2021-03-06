from tests.lib import create_basic_wheel_for_package


def test_new_resolver_conflict_requirements_file(tmpdir, script):
    create_basic_wheel_for_package(script, "base", "1.0")
    create_basic_wheel_for_package(script, "base", "2.0")
    create_basic_wheel_for_package(
        script, "pkga", "1.0", depends=["base==1.0"],
    )
    create_basic_wheel_for_package(
        script, "pkgb", "1.0", depends=["base==2.0"],
    )

    req_file = tmpdir.joinpath("requirements.txt")
    req_file.write_text("pkga\npkgb")

    result = script.pip(
        "install",
        "--no-cache-dir", "--no-index",
        "--find-links", script.scratch_path,
        "-r", req_file,
        expect_error=True,
    )

    message = "package versions have conflicting dependencies"
    assert message in result.stderr, str(result)


def test_new_resolver_conflict_constraints_file(tmpdir, script):
    create_basic_wheel_for_package(script, "pkg", "1.0")

    constrats_file = tmpdir.joinpath("constraints.txt")
    constrats_file.write_text("pkg!=1.0")

    result = script.pip(
        "install",
        "--no-cache-dir", "--no-index",
        "--find-links", script.scratch_path,
        "-c", constrats_file,
        "pkg==1.0",
        expect_error=True,
    )

    assert "ResolutionImpossible" in result.stderr, str(result)

    message = "The user requested (constraint) pkg!=1.0"
    assert message in result.stdout, str(result)
