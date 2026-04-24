//! Agentland runtime library.
//!
//! The library keeps the windowing edge thin and leaves layout, display
//! mapping, and framebuffer drawing in testable modules. The initial renderer
//! is a deterministic placeholder for the future pixel-art coffee-shop
//! dashboard.

pub mod app;
pub mod config;
pub mod display;

mod layout;
mod render;
