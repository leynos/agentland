//! Contract for the Whitaker isolation the development build standard asks for.
//!
//! Whitaker runs under the toolchain its installer manages, so `make lint` starts it outside the
//! checkout (Cargo then never discovers the checkout's `.cargo/config.toml` and its Cranelift
//! profile), names the manifest by absolute path, and assigns the literal `RUSTFLAGS` that
//! displaces every `rustflags` source. These tests read the real `make -n lint` output, so a
//! recipe that drops any of the three fails here.

use std::{
    path::{Path, PathBuf},
    process::Command,
};

use rstest::rstest;

/// Returns the checkout's canonical path, which is what `make` reports as `CURDIR`.
fn checkout() -> Result<PathBuf, String> {
    Path::new(env!("CARGO_MANIFEST_DIR"))
        .canonicalize()
        .map_err(|error| format!("resolving the checkout: {error}"))
}

/// Returns the `make -n lint` line that runs Whitaker.
fn whitaker_line() -> Result<String, String> {
    let output = Command::new("make")
        .args(["-n", "-B", "lint"])
        .current_dir(env!("CARGO_MANIFEST_DIR"))
        .output()
        .map_err(|error| format!("running make: {error}"))?;
    if !output.status.success() {
        return Err(format!(
            "`make -n lint` failed: {}",
            String::from_utf8_lossy(&output.stderr)
        ));
    }
    String::from_utf8_lossy(&output.stdout)
        .lines()
        .find(|line| line.contains("whitaker"))
        .map(str::to_owned)
        .ok_or_else(|| "`make -n lint` runs no Whitaker command".to_owned())
}

/// Returns the complaints about a Whitaker line that is not isolated from the checkout.
fn isolation_problems(line: &str, checkout: &Path) -> Vec<String> {
    let parent = checkout.parent().unwrap_or(checkout);
    let wanted = [
        (
            format!("cd \"{}/\" && ", parent.display()),
            "start from the checkout's parent directory",
        ),
        (
            "RUSTFLAGS=\"-D warnings\" ".to_owned(),
            "assign the literal `RUSTFLAGS=\"-D warnings\"`",
        ),
        (
            format!("--manifest-path \"{}/Cargo.toml\"", checkout.display()),
            "name the manifest by absolute path",
        ),
    ];
    wanted
        .iter()
        .filter(|(text, _)| !line.contains(text.as_str()))
        .map(|(_, what)| format!("the Whitaker command must {what}: {line}"))
        .collect()
}

/// Scenario: the real `make -n lint` output.
///
/// Invariant: Whitaker starts outside the checkout, assigns the literal `RUSTFLAGS`, and names
/// the manifest by absolute path.
#[test]
fn make_lint_isolates_whitaker_from_the_checkout() -> Result<(), String> {
    let problems = isolation_problems(&whitaker_line()?, &checkout()?);
    if problems.is_empty() {
        Ok(())
    } else {
        Err(problems.join("\n"))
    }
}

/// The whole isolated command, for a checkout at `/work/repo`.
const WHOLE: &str = "cd \"/work/\" && RUSTFLAGS=\"-D warnings\" whitaker --manifest-path \
                     \"/work/repo/Cargo.toml\" --all";

/// Scenario: Whitaker commands that each lack one isolation detail.
///
/// Invariant: the whole command passes and each missing detail is reported, so a recipe that
/// drops one cannot pass.
#[rstest]
#[case::whole(WHOLE.to_owned(), 0)]
#[case::no_cd(WHOLE.replacen("cd \"/work/\" && ", "", 1), 1)]
#[case::no_literal_flags(WHOLE.replacen("RUSTFLAGS=\"-D warnings\" ", "", 1), 1)]
#[case::no_manifest_path(WHOLE.replacen("--manifest-path \"/work/repo/Cargo.toml\" ", "", 1), 1)]
fn a_whitaker_command_missing_an_isolation_detail_is_reported(
    #[case] line: String,
    #[case] reported: usize,
) -> Result<(), String> {
    let found = isolation_problems(&line, Path::new("/work/repo")).len();
    if found == reported {
        Ok(())
    } else {
        Err(format!("{found} problems, not {reported}: {line}"))
    }
}
