//! Compile-time constants for the Agentland placeholder runtime.

/// Fixed virtual framebuffer width in pixels.
pub const VIRTUAL_WIDTH: u32 = 512;

/// Fixed virtual framebuffer height in pixels.
pub const VIRTUAL_HEIGHT: u32 = 288;

pub(crate) const VIRTUAL_WIDTH_USIZE: usize = 512;
pub(crate) const VIRTUAL_HEIGHT_USIZE: usize = 288;
pub(crate) const WINDOW_TITLE: &str = "Agentland";
pub(crate) const INITIAL_WINDOW_SCALE: u32 = 3;
