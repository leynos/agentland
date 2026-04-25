//! Bounds-checked framebuffer drawing utilities.

use crate::layout::Rect;

const CHANNEL_COUNT: usize = 4;

/// An RGBA colour stored in framebuffer byte order.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub(crate) struct Color {
    channels: [u8; CHANNEL_COUNT],
}

impl Color {
    pub(crate) const fn rgba(red: u8, green: u8, blue: u8, alpha: u8) -> Self {
        Self {
            channels: [red, green, blue, alpha],
        }
    }

    pub(crate) const fn channels(self) -> [u8; CHANNEL_COUNT] { self.channels }
}

/// Mutable view over a fixed-size RGBA framebuffer.
pub(crate) struct FrameBuffer<'frame> {
    pixels: &'frame mut [u8],
    width: usize,
    height: usize,
}

impl<'frame> FrameBuffer<'frame> {
    pub(crate) const fn new(pixels: &'frame mut [u8], width: usize, height: usize) -> Self {
        Self {
            pixels,
            width,
            height,
        }
    }

    pub(crate) fn clear(&mut self, color: Color) {
        let channels = color.channels();

        for pixel in self.pixels.chunks_exact_mut(CHANNEL_COUNT) {
            pixel.copy_from_slice(&channels);
        }
    }

    pub(crate) fn fill_rect(&mut self, rect: Rect, color: Color) {
        let stride = self.stride();
        let channels = color.channels();

        for (row_y, row) in self.pixels.chunks_exact_mut(stride).enumerate() {
            if !rect.contains_y(row_y) || row_y >= self.height {
                continue;
            }

            fill_row_segment(row, rect, self.width, channels);
        }
    }

    const fn stride(&self) -> usize { self.width.saturating_mul(CHANNEL_COUNT) }
}

fn fill_row_segment(row: &mut [u8], rect: Rect, width: usize, channels: [u8; CHANNEL_COUNT]) {
    for (column_x, pixel) in row.chunks_exact_mut(CHANNEL_COUNT).enumerate() {
        if should_fill_column(rect, column_x, width) {
            pixel.copy_from_slice(&channels);
        }
    }
}

const fn should_fill_column(rect: Rect, column_x: usize, width: usize) -> bool {
    rect.contains_x(column_x) && column_x < width
}

#[cfg(test)]
mod tests {
    //! Tests for clipped software framebuffer drawing.

    use super::{Color, FrameBuffer};
    use crate::layout::Rect;

    #[test]
    fn clipped_rect_does_not_write_outside_framebuffer() {
        let mut pixels = vec![0; 16];
        let mut frame = FrameBuffer::new(&mut pixels, 2, 2);

        frame.fill_rect(Rect::new(1, 1, 4, 4), Color::rgba(1, 2, 3, 4));

        let coloured_pixels = pixels
            .chunks_exact(4)
            .filter(|pixel| pixel.iter().copied().any(|channel| channel != 0))
            .count();

        assert_eq!(coloured_pixels, 1);
    }
}
