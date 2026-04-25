//! Windowing and presentation edge for the Agentland desktop mockup.

use std::sync::Arc;

use pixels::{Pixels, ScalingMode, SurfaceTexture};
use thiserror::Error;
use winit::{
    application::ApplicationHandler,
    dpi::PhysicalSize,
    event::WindowEvent,
    event_loop::{ActiveEventLoop, EventLoop},
    window::{Window, WindowId},
};

use crate::{
    config::{
        INITIAL_WINDOW_SCALE,
        VIRTUAL_HEIGHT,
        VIRTUAL_HEIGHT_USIZE,
        VIRTUAL_WIDTH,
        VIRTUAL_WIDTH_USIZE,
        WINDOW_TITLE,
    },
    display::{PhysicalViewportSize, Viewport},
    render::primitives::render_placeholder_dashboard,
};

/// Errors that can prevent the application from opening or presenting frames.
#[derive(Debug, Error)]
pub enum AppError {
    /// The operating-system event loop could not be created or run.
    #[error("event loop failed: {0}")]
    EventLoop(#[from] winit::error::EventLoopError),

    /// The desktop window could not be created.
    #[error("window creation failed: {0}")]
    Window(#[from] winit::error::OsError),

    /// The `pixels` surface or renderer failed.
    #[error("pixels renderer failed: {0}")]
    Pixels(#[from] pixels::Error),

    /// Resizing the presentation surface failed.
    #[error("surface resize failed: {0}")]
    Resize(#[from] pixels::TextureError),
}

/// Opens the Agentland window and starts the desktop event loop.
///
/// # Errors
///
/// Returns an error if the event loop, window, `pixels` surface, resize path,
/// or frame presentation fails.
pub fn run() -> Result<(), AppError> {
    let event_loop = EventLoop::new()?;
    let mut application = AgentlandApp::default();

    event_loop.run_app(&mut application)?;

    application.error.take().map_or_else(|| Ok(()), Err)
}

#[derive(Default)]
struct AgentlandApp {
    runtime: Option<Runtime>,
    error: Option<AppError>,
}

impl AgentlandApp {
    fn set_error(&mut self, event_loop: &ActiveEventLoop, error: AppError) {
        self.error = Some(error);
        event_loop.exit();
    }
}

impl ApplicationHandler for AgentlandApp {
    fn resumed(&mut self, event_loop: &ActiveEventLoop) {
        if self.runtime.is_some() {
            return;
        }

        match Runtime::new(event_loop) {
            Ok(runtime) => {
                runtime.request_redraw();
                self.runtime = Some(runtime);
            }
            Err(error) => self.set_error(event_loop, error),
        }
    }

    fn window_event(
        &mut self,
        event_loop: &ActiveEventLoop,
        window_id: WindowId,
        event: WindowEvent,
    ) {
        let Some(runtime) = self.runtime.as_mut() else {
            return;
        };

        if runtime.window_id() != window_id {
            return;
        }

        match event {
            WindowEvent::CloseRequested => event_loop.exit(),
            WindowEvent::RedrawRequested => {
                if let Err(error) = runtime.render() {
                    self.set_error(event_loop, error);
                }
            }
            WindowEvent::Resized(size) => {
                if let Err(error) = runtime.resize(size) {
                    self.set_error(event_loop, error);
                } else {
                    runtime.request_redraw();
                }
            }
            _ => {}
        }
    }
}

struct Runtime {
    window: Arc<Window>,
    pixels: Pixels<'static>,
    viewport: Viewport,
    is_surface_visible: bool,
}

impl Runtime {
    fn new(event_loop: &ActiveEventLoop) -> Result<Self, AppError> {
        let initial_size = PhysicalSize::new(
            VIRTUAL_WIDTH.saturating_mul(INITIAL_WINDOW_SCALE),
            VIRTUAL_HEIGHT.saturating_mul(INITIAL_WINDOW_SCALE),
        );
        let attributes = Window::default_attributes()
            .with_title(WINDOW_TITLE)
            .with_inner_size(initial_size)
            .with_min_inner_size(PhysicalSize::new(VIRTUAL_WIDTH, VIRTUAL_HEIGHT));
        let window = Arc::new(event_loop.create_window(attributes)?);
        let surface_size = window.inner_size();
        let surface_texture =
            SurfaceTexture::new(surface_size.width, surface_size.height, window.clone());
        let mut pixels = Pixels::new(VIRTUAL_WIDTH, VIRTUAL_HEIGHT, surface_texture)?;

        pixels.set_scaling_mode(ScalingMode::PixelPerfect);

        Ok(Self {
            window,
            pixels,
            viewport: Viewport::from_window_size(PhysicalViewportSize::from(surface_size)),
            is_surface_visible: true,
        })
    }

    fn window_id(&self) -> WindowId { self.window.id() }

    fn request_redraw(&self) {
        if self.is_surface_visible && self.viewport.is_fittable() {
            self.window.request_redraw();
        }
    }

    fn resize(&mut self, size: PhysicalSize<u32>) -> Result<(), AppError> {
        self.viewport = Viewport::from_window_size(PhysicalViewportSize::from(size));

        if is_zero_sized(size) {
            self.is_surface_visible = false;
            Ok(())
        } else {
            self.pixels.resize_surface(size.width, size.height)?;
            self.is_surface_visible = true;
            Ok(())
        }
    }

    fn render(&mut self) -> Result<(), AppError> {
        if self.is_surface_visible && self.viewport.is_fittable() {
            render_placeholder_dashboard(
                self.pixels.frame_mut(),
                VIRTUAL_WIDTH_USIZE,
                VIRTUAL_HEIGHT_USIZE,
            );
            self.pixels.render()?;
            Ok(())
        } else {
            Ok(())
        }
    }
}

const fn is_zero_sized(size: PhysicalSize<u32>) -> bool { size.width == 0 || size.height == 0 }

#[cfg(test)]
mod tests {
    //! Tests for window lifecycle helpers.

    use rstest::rstest;
    use winit::dpi::PhysicalSize;

    use super::is_zero_sized;

    #[rstest]
    #[case(0, 288, true)]
    #[case(512, 0, true)]
    #[case(0, 0, true)]
    #[case(512, 288, false)]
    fn zero_sized_surface_detection_matches_pixels_surface_constraints(
        #[case] width: u32,
        #[case] height: u32,
        #[case] expected: bool,
    ) {
        assert_eq!(is_zero_sized(PhysicalSize::new(width, height)), expected);
    }
}
