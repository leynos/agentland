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

/// Scenario: Whitaker commands that each lack one isolation detail.
///
/// Invariant: each missing detail is reported, so a recipe that drops one cannot pass.
#[test]
fn a_whitaker_command_missing_an_isolation_detail_is_reported() -> Result<(), String> {
    let checkout = Path::new("/work/repo");
    let whole = "cd \"/work/\" && RUSTFLAGS=\"-D warnings\" whitaker --manifest-path \
                 \"/work/repo/Cargo.toml\" --all";
    let cases = [
        whole.replace("cd \"/work/\" && ", ""),
        whole.replace("RUSTFLAGS=\"-D warnings\" ", ""),
        whole.replace("--manifest-path \"/work/repo/Cargo.toml\" ", ""),
    ];
    if !isolation_problems(whole, checkout).is_empty() {
        return Err("the whole command must pass".to_owned());
    }
    for case in &cases {
        if isolation_problems(case, checkout).len() != 1 {
            return Err(format!("one detail missing must give one problem: {case}"));
        }
    }
    Ok(())
}
