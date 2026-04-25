//! Placeholder dashboard drawing for the first Agentland runtime slice.

use crate::{
    layout::{DashboardLayout, Rect},
    render::frame::{Color, FrameBuffer},
};

const BACKPLATE_STRIPE_HEIGHT: usize = 2;
const PANEL_BORDER_THICKNESS: usize = 2;
const PANEL_BORDER_TOTAL: usize = PANEL_BORDER_THICKNESS.saturating_mul(2);
const TOP_BAR_BOTTOM_BORDER_HEIGHT: usize = PANEL_BORDER_THICKNESS;
const TOP_BAR_LEFT_BADGE_X_OFFSET: usize = 8;
const TOP_BAR_BADGE_Y_OFFSET: usize = 7;
const TOP_BAR_LEFT_BADGE_WIDTH: usize = 92;
const TOP_BAR_RIGHT_BADGE_OUTSET: usize = 92;
const TOP_BAR_RIGHT_BADGE_WIDTH: usize = 76;
const TOP_BAR_BADGE_HEIGHT: usize = 14;
const SCENE_PANEL_INSET: usize = 3;
const SCENE_PANEL_INSET_TOTAL: usize = SCENE_PANEL_INSET.saturating_mul(2);
const VIEWPORT_BOTTOM_STRIP_HEIGHT: usize = 36;
const VIEWPORT_LEFT_BLOCK_X_OFFSET: usize = 22;
const VIEWPORT_LEFT_BLOCK_Y_OFFSET: usize = 18;
const VIEWPORT_LEFT_BLOCK_WIDTH: usize = 46;
const VIEWPORT_LEFT_BLOCK_HEIGHT: usize = 68;
const VIEWPORT_RIGHT_BLOCK_OUTSET: usize = 86;
const VIEWPORT_RIGHT_BLOCK_Y_OFFSET: usize = 30;
const VIEWPORT_RIGHT_BLOCK_WIDTH: usize = 58;
const VIEWPORT_RIGHT_BLOCK_HEIGHT: usize = 42;
const STAT_CARD_COUNT: usize = 4;
const STAT_CARD_ACCENT_INSET: usize = 5;
const STAT_CARD_ACCENT_INSET_TOTAL: usize = STAT_CARD_ACCENT_INSET.saturating_mul(2);
const STAT_CARD_ACCENT_HEIGHT: usize = 6;
const STAT_CARD_BODY_X_INSET: usize = 6;
const STAT_CARD_BODY_X_INSET_TOTAL: usize = STAT_CARD_BODY_X_INSET.saturating_mul(2);
const STAT_CARD_BODY_Y_OFFSET: usize = 20;
const STAT_CARD_BODY_HEIGHT: usize = 18;

/// Renders the deterministic placeholder dashboard into a fixed RGBA frame.
pub(crate) fn render_placeholder_dashboard(frame: &mut [u8], width: usize, height: usize) {
    let mut framebuffer = FrameBuffer::new(frame, width, height);
    let layout = DashboardLayout::new();

    framebuffer.clear(PALETTE.near_black);
    draw_backplate(&mut framebuffer, Rect::new(0, 0, width, height));
    draw_top_bar(&mut framebuffer, layout.top_bar());
    draw_scene_viewport(&mut framebuffer, layout.scene_viewport());
    draw_stat_cards(&mut framebuffer, layout.stat_cards());
}

fn draw_backplate(framebuffer: &mut FrameBuffer<'_>, bounds: Rect) {
    let stripe_height = bounds.height().min(BACKPLATE_STRIPE_HEIGHT);

    framebuffer.fill_rect(bounds, PALETTE.deep_navy);
    framebuffer.fill_rect(
        Rect::new(bounds.x(), bounds.y(), bounds.width(), stripe_height),
        PALETTE.brass,
    );
    framebuffer.fill_rect(
        Rect::new(
            bounds.x(),
            bounds
                .y()
                .saturating_add(bounds.height().saturating_sub(stripe_height)),
            bounds.width(),
            stripe_height,
        ),
        PALETTE.coffee_brown,
    );
}

fn draw_top_bar(framebuffer: &mut FrameBuffer<'_>, rect: Rect) {
    framebuffer.fill_rect(rect, PALETTE.slate_blue);
    framebuffer.fill_rect(
        Rect::new(
            rect.x(),
            rect.bottom().saturating_sub(TOP_BAR_BOTTOM_BORDER_HEIGHT),
            rect.width(),
            TOP_BAR_BOTTOM_BORDER_HEIGHT,
        ),
        PALETTE.brass,
    );
    framebuffer.fill_rect(
        Rect::new(
            rect.x().saturating_add(TOP_BAR_LEFT_BADGE_X_OFFSET),
            rect.y().saturating_add(TOP_BAR_BADGE_Y_OFFSET),
            TOP_BAR_LEFT_BADGE_WIDTH,
            TOP_BAR_BADGE_HEIGHT,
        ),
        PALETTE.coffee_brown,
    );
    framebuffer.fill_rect(
        Rect::new(
            rect.right().saturating_sub(TOP_BAR_RIGHT_BADGE_OUTSET),
            rect.y().saturating_add(TOP_BAR_BADGE_Y_OFFSET),
            TOP_BAR_RIGHT_BADGE_WIDTH,
            TOP_BAR_BADGE_HEIGHT,
        ),
        PALETTE.moss_green,
    );
}

fn draw_scene_viewport(framebuffer: &mut FrameBuffer<'_>, rect: Rect) {
    draw_panel(framebuffer, rect, PALETTE.coffee_brown, PALETTE.brass);
    let inner = Rect::new(
        rect.x().saturating_add(SCENE_PANEL_INSET),
        rect.y().saturating_add(SCENE_PANEL_INSET),
        rect.width().saturating_sub(SCENE_PANEL_INSET_TOTAL),
        rect.height().saturating_sub(SCENE_PANEL_INSET_TOTAL),
    );
    framebuffer.fill_rect(inner, PALETTE.deep_navy);
    framebuffer.fill_rect(
        Rect::new(
            inner.x(),
            inner.bottom().saturating_sub(VIEWPORT_BOTTOM_STRIP_HEIGHT),
            inner.width(),
            VIEWPORT_BOTTOM_STRIP_HEIGHT,
        ),
        PALETTE.walnut,
    );
    framebuffer.fill_rect(
        Rect::new(
            inner.x().saturating_add(VIEWPORT_LEFT_BLOCK_X_OFFSET),
            inner.y().saturating_add(VIEWPORT_LEFT_BLOCK_Y_OFFSET),
            VIEWPORT_LEFT_BLOCK_WIDTH,
            VIEWPORT_LEFT_BLOCK_HEIGHT,
        ),
        PALETTE.warm_amber,
    );
    framebuffer.fill_rect(
        Rect::new(
            inner.right().saturating_sub(VIEWPORT_RIGHT_BLOCK_OUTSET),
            inner.y().saturating_add(VIEWPORT_RIGHT_BLOCK_Y_OFFSET),
            VIEWPORT_RIGHT_BLOCK_WIDTH,
            VIEWPORT_RIGHT_BLOCK_HEIGHT,
        ),
        PALETTE.screen_cyan,
    );
}

fn draw_stat_cards(framebuffer: &mut FrameBuffer<'_>, cards: &[Rect; STAT_CARD_COUNT]) {
    for (card_index, card) in cards.iter().copied().enumerate() {
        draw_panel(framebuffer, card, PALETTE.slate_blue, PALETTE.brass);
        let accent = card_accent(card_index);
        framebuffer.fill_rect(
            Rect::new(
                card.x().saturating_add(STAT_CARD_ACCENT_INSET),
                card.y().saturating_add(STAT_CARD_ACCENT_INSET),
                card.width().saturating_sub(STAT_CARD_ACCENT_INSET_TOTAL),
                STAT_CARD_ACCENT_HEIGHT,
            ),
            accent,
        );
        framebuffer.fill_rect(
            Rect::new(
                card.x().saturating_add(STAT_CARD_BODY_X_INSET),
                card.y().saturating_add(STAT_CARD_BODY_Y_OFFSET),
                card.width().saturating_sub(STAT_CARD_BODY_X_INSET_TOTAL),
                STAT_CARD_BODY_HEIGHT,
            ),
            PALETTE.deep_navy,
        );
    }
}

fn draw_panel(framebuffer: &mut FrameBuffer<'_>, rect: Rect, fill: Color, border: Color) {
    framebuffer.fill_rect(rect, border);
    framebuffer.fill_rect(
        Rect::new(
            rect.x().saturating_add(PANEL_BORDER_THICKNESS),
            rect.y().saturating_add(PANEL_BORDER_THICKNESS),
            rect.width().saturating_sub(PANEL_BORDER_TOTAL),
            rect.height().saturating_sub(PANEL_BORDER_TOTAL),
        ),
        fill,
    );
}

const fn card_accent(index: usize) -> Color {
    match index {
        0 => PALETTE.moss_green,
        1 => PALETTE.screen_cyan,
        2 => PALETTE.warm_amber,
        _ => PALETTE.ember_red,
    }
}

struct Palette {
    near_black: Color,
    deep_navy: Color,
    slate_blue: Color,
    coffee_brown: Color,
    walnut: Color,
    brass: Color,
    warm_amber: Color,
    moss_green: Color,
    screen_cyan: Color,
    ember_red: Color,
}

const PALETTE: Palette = Palette {
    near_black: Color::rgba(7, 16, 27, 255),
    deep_navy: Color::rgba(15, 26, 46, 255),
    slate_blue: Color::rgba(30, 43, 68, 255),
    coffee_brown: Color::rgba(75, 46, 26, 255),
    walnut: Color::rgba(122, 74, 43, 255),
    brass: Color::rgba(212, 175, 55, 255),
    warm_amber: Color::rgba(255, 179, 71, 255),
    moss_green: Color::rgba(46, 91, 63, 255),
    screen_cyan: Color::rgba(97, 214, 255, 255),
    ember_red: Color::rgba(185, 74, 46, 255),
};

#[cfg(test)]
mod tests {
    //! Pixel-level tests for the deterministic placeholder renderer.

    use super::{PALETTE, render_placeholder_dashboard};
    use crate::{
        config::{VIRTUAL_HEIGHT_USIZE, VIRTUAL_WIDTH_USIZE},
        layout::DashboardLayout,
    };

    #[test]
    fn placeholder_dashboard_renders_stable_regions() {
        let mut frame = vec![0; VIRTUAL_WIDTH_USIZE * VIRTUAL_HEIGHT_USIZE * 4];
        let layout = DashboardLayout::new();

        render_placeholder_dashboard(&mut frame, VIRTUAL_WIDTH_USIZE, VIRTUAL_HEIGHT_USIZE);

        assert_pixel(&frame, 4, 32, PALETTE.deep_navy);
        assert_pixel(&frame, 4, 4, PALETTE.slate_blue);
        assert_pixel(&frame, 4, VIRTUAL_HEIGHT_USIZE - 1, PALETTE.coffee_brown);
        assert_pixel(
            &frame,
            layout.top_bar().x() + 10,
            layout.top_bar().y() + 10,
            PALETTE.coffee_brown,
        );
        assert_pixel(
            &frame,
            layout.scene_viewport().x() + 4,
            layout.scene_viewport().y() + 4,
            PALETTE.deep_navy,
        );
        assert_pixel(
            &frame,
            layout.scene_viewport().x() + 30,
            layout.scene_viewport().y() + 30,
            PALETTE.warm_amber,
        );
        assert_pixel(
            &frame,
            layout.scene_viewport().right() - 60,
            layout.scene_viewport().y() + 40,
            PALETTE.screen_cyan,
        );

        for (index, card) in layout.stat_cards().iter().copied().enumerate() {
            assert_pixel(&frame, card.x() + 1, card.y() + 1, PALETTE.brass);
            assert_pixel(&frame, card.x() + 7, card.y() + 22, PALETTE.deep_navy);
            assert_pixel(
                &frame,
                card.x() + 6,
                card.y() + 6,
                expected_card_accent(index),
            );
        }
    }

    fn assert_pixel(frame: &[u8], x: usize, y: usize, expected: super::Color) {
        let offset = (y * VIRTUAL_WIDTH_USIZE + x) * 4;
        let expected_channels = expected.channels();

        assert_eq!(
            frame.get(offset..offset + 4),
            Some(expected_channels.as_slice())
        );
    }

    const fn expected_card_accent(index: usize) -> super::Color {
        match index {
            0 => PALETTE.moss_green,
            1 => PALETTE.screen_cyan,
            2 => PALETTE.warm_amber,
            _ => PALETTE.ember_red,
        }
    }
}
