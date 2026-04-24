//! Integer scaling and letterbox mapping for the fixed virtual framebuffer.

use winit::dpi::{PhysicalPosition, PhysicalSize};

use crate::config::{VIRTUAL_HEIGHT, VIRTUAL_WIDTH};

/// Physical window size in pixels.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct PhysicalViewportSize {
    width: u32,
    height: u32,
}

impl PhysicalViewportSize {
    /// Creates a physical viewport size from physical pixel dimensions.
    #[must_use]
    pub const fn new(width: u32, height: u32) -> Self { Self { width, height } }
}

impl From<PhysicalSize<u32>> for PhysicalViewportSize {
    fn from(value: PhysicalSize<u32>) -> Self { Self::new(value.width, value.height) }
}

/// A virtual framebuffer point.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct VirtualPoint {
    x: u32,
    y: u32,
}

impl VirtualPoint {
    /// Creates a point in fixed virtual framebuffer coordinates.
    #[must_use]
    pub const fn new(x: u32, y: u32) -> Self { Self { x, y } }

    /// Horizontal coordinate in virtual pixels.
    #[must_use]
    pub const fn x(self) -> u32 { self.x }

    /// Vertical coordinate in virtual pixels.
    #[must_use]
    pub const fn y(self) -> u32 { self.y }
}

/// Integer-scaled destination rectangle for the fixed framebuffer.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct Viewport {
    x: u32,
    y: u32,
    width: u32,
    height: u32,
    scale: u32,
}

impl Viewport {
    /// Calculates the centred integer-scaled viewport for a physical window.
    #[must_use]
    pub fn from_window_size(size: PhysicalViewportSize) -> Self {
        let width_scale = size.width.checked_div(VIRTUAL_WIDTH).unwrap_or(0);
        let height_scale = size.height.checked_div(VIRTUAL_HEIGHT).unwrap_or(0);
        let scale = width_scale.min(height_scale).max(1);
        let width = VIRTUAL_WIDTH.saturating_mul(scale).min(size.width);
        let height = VIRTUAL_HEIGHT.saturating_mul(scale).min(size.height);
        let x = centred_offset(size.width, width);
        let y = centred_offset(size.height, height);

        Self {
            x,
            y,
            width,
            height,
            scale,
        }
    }

    /// Maps a physical pixel position to virtual framebuffer coordinates.
    ///
    /// Returns `None` when the position falls inside the letterbox margin.
    #[must_use]
    pub fn physical_to_virtual(&self, position: PhysicalPosition<u32>) -> Option<VirtualPoint> {
        let x_offset = position.x.checked_sub(self.x)?;
        let y_offset = position.y.checked_sub(self.y)?;

        if x_offset >= self.width || y_offset >= self.height {
            return None;
        }

        Some(VirtualPoint::new(
            x_offset.checked_div(self.scale).unwrap_or(0),
            y_offset.checked_div(self.scale).unwrap_or(0),
        ))
    }

    #[cfg(test)]
    /// Integer presentation scale.
    #[must_use]
    pub const fn scale(self) -> u32 { self.scale }

    /// Physical origin of the scaled framebuffer inside the window.
    #[must_use]
    pub const fn origin(self) -> (u32, u32) { (self.x, self.y) }

    /// Physical size of the scaled framebuffer inside the window.
    #[must_use]
    pub const fn size(self) -> (u32, u32) { (self.width, self.height) }
}

fn centred_offset(outer: u32, inner: u32) -> u32 {
    outer.saturating_sub(inner).checked_div(2).unwrap_or(0)
}

#[cfg(test)]
mod tests {
    //! Tests for integer viewport calculation and letterbox mapping.

    use rstest::rstest;
    use winit::dpi::PhysicalPosition;

    use super::{PhysicalViewportSize, Viewport};

    #[rstest]
    #[case((512, 288), 1, (0, 0), (512, 288))]
    #[case((1024, 576), 2, (0, 0), (1024, 576))]
    #[case((1200, 700), 2, (88, 62), (1024, 576))]
    #[case((900, 1200), 1, (194, 456), (512, 288))]
    #[case((320, 200), 1, (0, 0), (320, 200))]
    fn viewport_uses_largest_integer_scale_that_fits(
        #[case] window_size: (u32, u32),
        #[case] expected_scale: u32,
        #[case] expected_origin: (u32, u32),
        #[case] expected_size: (u32, u32),
    ) {
        let viewport =
            Viewport::from_window_size(PhysicalViewportSize::new(window_size.0, window_size.1));

        assert_eq!(viewport.scale(), expected_scale);
        assert_eq!(viewport.origin(), expected_origin);
        assert_eq!(viewport.size(), expected_size);
    }

    #[rstest]
    #[case(88, 62, Some((0, 0)))]
    #[case(87, 62, None)]
    #[case(1111, 637, Some((511, 287)))]
    #[case(1112, 637, None)]
    fn physical_points_map_through_letterbox(
        #[case] x: u32,
        #[case] y: u32,
        #[case] expected: Option<(u32, u32)>,
    ) {
        let viewport = Viewport::from_window_size(PhysicalViewportSize::new(1200, 700));
        let actual = viewport
            .physical_to_virtual(PhysicalPosition::new(x, y))
            .map(|point| (point.x(), point.y()));

        assert_eq!(actual, expected);
    }
}
