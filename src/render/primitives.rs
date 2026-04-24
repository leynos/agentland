//! Placeholder dashboard drawing for the first Agentland runtime slice.

use crate::{
    config::{VIRTUAL_HEIGHT_USIZE, VIRTUAL_WIDTH_USIZE},
    layout::{DashboardLayout, Rect},
    render::frame::{Color, FrameBuffer},
};

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
    framebuffer.fill_rect(bounds, PALETTE.deep_navy);
    framebuffer.fill_rect(Rect::new(0, 0, VIRTUAL_WIDTH_USIZE, 2), PALETTE.brass);
    framebuffer.fill_rect(
        Rect::new(
            0,
            VIRTUAL_HEIGHT_USIZE.saturating_sub(2),
            VIRTUAL_WIDTH_USIZE,
            2,
        ),
        PALETTE.coffee_brown,
    );
}

fn draw_top_bar(framebuffer: &mut FrameBuffer<'_>, rect: Rect) {
    framebuffer.fill_rect(rect, PALETTE.slate_blue);
    framebuffer.fill_rect(
        Rect::new(rect.x(), rect.bottom().saturating_sub(2), rect.width(), 2),
        PALETTE.brass,
    );
    framebuffer.fill_rect(
        Rect::new(
            rect.x().saturating_add(8),
            rect.y().saturating_add(7),
            92,
            14,
        ),
        PALETTE.coffee_brown,
    );
    framebuffer.fill_rect(
        Rect::new(
            rect.right().saturating_sub(92),
            rect.y().saturating_add(7),
            76,
            14,
        ),
        PALETTE.moss_green,
    );
}

fn draw_scene_viewport(framebuffer: &mut FrameBuffer<'_>, rect: Rect) {
    draw_panel(framebuffer, rect, PALETTE.coffee_brown, PALETTE.brass);
    let inner = Rect::new(
        rect.x().saturating_add(3),
        rect.y().saturating_add(3),
        rect.width().saturating_sub(6),
        rect.height().saturating_sub(6),
    );
    framebuffer.fill_rect(inner, PALETTE.deep_navy);
    framebuffer.fill_rect(
        Rect::new(
            inner.x(),
            inner.bottom().saturating_sub(36),
            inner.width(),
            36,
        ),
        PALETTE.walnut,
    );
    framebuffer.fill_rect(
        Rect::new(
            inner.x().saturating_add(22),
            inner.y().saturating_add(18),
            46,
            68,
        ),
        PALETTE.warm_amber,
    );
    framebuffer.fill_rect(
        Rect::new(
            inner.right().saturating_sub(86),
            inner.y().saturating_add(30),
            58,
            42,
        ),
        PALETTE.screen_cyan,
    );
}

fn draw_stat_cards(framebuffer: &mut FrameBuffer<'_>, cards: &[Rect; 4]) {
    for (card_index, card) in cards.iter().copied().enumerate() {
        draw_panel(framebuffer, card, PALETTE.slate_blue, PALETTE.brass);
        let accent = card_accent(card_index);
        framebuffer.fill_rect(
            Rect::new(
                card.x().saturating_add(5),
                card.y().saturating_add(5),
                card.width().saturating_sub(10),
                6,
            ),
            accent,
        );
        framebuffer.fill_rect(
            Rect::new(
                card.x().saturating_add(6),
                card.y().saturating_add(20),
                card.width().saturating_sub(12),
                18,
            ),
            PALETTE.deep_navy,
        );
    }
}

fn draw_panel(framebuffer: &mut FrameBuffer<'_>, rect: Rect, fill: Color, border: Color) {
    framebuffer.fill_rect(rect, border);
    framebuffer.fill_rect(
        Rect::new(
            rect.x().saturating_add(2),
            rect.y().saturating_add(2),
            rect.width().saturating_sub(4),
            rect.height().saturating_sub(4),
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
