//! Deterministic dashboard layout for the fixed virtual framebuffer.

use crate::config::{VIRTUAL_HEIGHT_USIZE, VIRTUAL_WIDTH_USIZE};

/// Integer rectangle in virtual framebuffer coordinates.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub(crate) struct Rect {
    x: usize,
    y: usize,
    width: usize,
    height: usize,
}

impl Rect {
    pub(crate) const fn new(x: usize, y: usize, width: usize, height: usize) -> Self {
        Self {
            x,
            y,
            width,
            height,
        }
    }

    pub(crate) const fn x(self) -> usize { self.x }

    pub(crate) const fn y(self) -> usize { self.y }

    pub(crate) const fn width(self) -> usize { self.width }

    pub(crate) const fn height(self) -> usize { self.height }

    pub(crate) const fn right(self) -> usize { self.x.saturating_add(self.width) }

    pub(crate) const fn bottom(self) -> usize { self.y.saturating_add(self.height) }

    pub(crate) const fn contains_x(self, x: usize) -> bool { x >= self.x && x < self.right() }

    pub(crate) const fn contains_y(self, y: usize) -> bool { y >= self.y && y < self.bottom() }

    #[cfg(test)]
    pub(crate) const fn is_inside(self, bounds: Self) -> bool {
        self.x >= bounds.x
            && self.y >= bounds.y
            && self.right() <= bounds.right()
            && self.bottom() <= bounds.bottom()
    }
}

/// Rectangles for the initial dashboard placeholder.
#[derive(Clone, Debug, Eq, PartialEq)]
pub(crate) struct DashboardLayout {
    top_bar: Rect,
    scene_viewport: Rect,
    stat_cards: [Rect; STAT_CARD_COUNT],
}

impl DashboardLayout {
    pub(crate) fn new() -> Self {
        let top_bar = Rect::new(0, 0, VIRTUAL_WIDTH_USIZE, TOP_BAR_HEIGHT);
        let scene_viewport = Rect::new(
            OUTER_MARGIN,
            TOP_BAR_HEIGHT.saturating_add(OUTER_MARGIN),
            VIRTUAL_WIDTH_USIZE.saturating_sub(OUTER_MARGIN.saturating_mul(2)),
            SCENE_HEIGHT,
        );
        let card_width = stat_card_width();
        let card_y = VIRTUAL_HEIGHT_USIZE
            .saturating_sub(OUTER_MARGIN)
            .saturating_sub(STAT_CARD_HEIGHT);
        let stat_cards = [
            Rect::new(OUTER_MARGIN, card_y, card_width, STAT_CARD_HEIGHT),
            Rect::new(
                OUTER_MARGIN
                    .saturating_add(card_width)
                    .saturating_add(CARD_GAP),
                card_y,
                card_width,
                STAT_CARD_HEIGHT,
            ),
            Rect::new(
                OUTER_MARGIN
                    .saturating_add(card_width.saturating_mul(2))
                    .saturating_add(CARD_GAP.saturating_mul(2)),
                card_y,
                card_width,
                STAT_CARD_HEIGHT,
            ),
            Rect::new(
                OUTER_MARGIN
                    .saturating_add(card_width.saturating_mul(3))
                    .saturating_add(CARD_GAP.saturating_mul(3)),
                card_y,
                card_width,
                STAT_CARD_HEIGHT,
            ),
        ];

        Self {
            top_bar,
            scene_viewport,
            stat_cards,
        }
    }

    pub(crate) const fn top_bar(&self) -> Rect { self.top_bar }

    pub(crate) const fn scene_viewport(&self) -> Rect { self.scene_viewport }

    pub(crate) const fn stat_cards(&self) -> &[Rect; STAT_CARD_COUNT] { &self.stat_cards }
}

const OUTER_MARGIN: usize = 8;
const TOP_BAR_HEIGHT: usize = 28;
const SCENE_HEIGHT: usize = 188;
const STAT_CARD_HEIGHT: usize = 48;
pub(crate) const CARD_GAP: usize = 6;
const STAT_CARD_COUNT: usize = 4;

fn stat_card_width() -> usize {
    let total_gap = CARD_GAP.saturating_mul(STAT_CARD_COUNT.saturating_sub(1));
    let available = VIRTUAL_WIDTH_USIZE
        .saturating_sub(OUTER_MARGIN.saturating_mul(2))
        .saturating_sub(total_gap);

    available.checked_div(STAT_CARD_COUNT).unwrap_or(0)
}

#[cfg(test)]
mod tests {
    //! Tests for the fixed virtual dashboard layout.

    use super::{CARD_GAP, DashboardLayout, Rect};
    use crate::config::{VIRTUAL_HEIGHT_USIZE, VIRTUAL_WIDTH_USIZE};

    #[test]
    fn dashboard_sections_fit_fixed_virtual_bounds() {
        let bounds = Rect::new(0, 0, VIRTUAL_WIDTH_USIZE, VIRTUAL_HEIGHT_USIZE);
        let layout = DashboardLayout::new();

        assert!(layout.top_bar().is_inside(bounds));
        assert!(layout.scene_viewport().is_inside(bounds));
        assert!(
            layout
                .stat_cards()
                .iter()
                .all(|card| card.is_inside(bounds))
        );
    }

    #[test]
    fn stat_cards_use_stable_dimensions_and_spacing() {
        let layout = DashboardLayout::new();
        let cards = layout.stat_cards();
        let first = cards.first();

        assert!(first.is_some());
        assert!(cards.iter().all(|card| {
            first.is_some_and(|expected| {
                card.y() == expected.y()
                    && card.width() == expected.width()
                    && card.height() == expected.height()
            })
        }));

        for (previous, next) in cards.iter().zip(cards.iter().skip(1)) {
            let actual_gap = next
                .x()
                .saturating_sub(previous.x())
                .saturating_sub(previous.width());

            assert_eq!(actual_gap, CARD_GAP);
        }
    }
}
