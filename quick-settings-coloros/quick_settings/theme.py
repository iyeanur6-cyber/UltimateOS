"""ColorOS-inspired translucent glass theme for Quick Settings."""
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gtk, Gdk

COLORS = {
    "navy_deep": "#07152d",
    "navy": "#102b55",
    "navy_mid": "#214f8b",
    "glass": "rgba(255,255,255,0.12)",
    "glass_strong": "rgba(255,255,255,0.19)",
    "glass_soft": "rgba(255,255,255,0.08)",
    "white": "#f8fbff",
    "muted": "#c7d1df",
    "dim": "#91a0b6",
    "cyan": "#43d9ff",
    "blue": "#4f8cff",
    "green": "#42e68a",
    "yellow": "#ffd447",
    "red": "#ff647c",
    "purple": "#a88bff",
    "pink": "#ff79c6",
}

CSS = f"""
window#qs-window, .qs-window {{
    background-color: transparent;
}}

.qs-panel {{
    background: linear-gradient(145deg,
        rgba(255,255,255,0.17) 0%,
        rgba(255,255,255,0.10) 35%,
        rgba(24,24,28,0.52) 100%);
    border: 1px solid rgba(255,255,255,0.20);
    border-radius: 32px;
    padding: 12px;
    box-shadow: 0 18px 50px rgba(0,0,0,0.42);
}}

.qs-time {{ color: {COLORS['white']}; font-size: 27px; font-weight: 500; }}
.qs-date {{ color: {COLORS['muted']}; font-size: 12px; }}

.qs-header-btn {{
    background: rgba(255,255,255,0.10);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 50px;
    min-width: 38px; min-height: 38px; padding: 7px;
    color: {COLORS['white']};
}}
.qs-header-btn:hover {{ background: rgba(255,255,255,0.20); }}

.qs-battery-card {{
    background: rgba(255,255,255,0.10);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 20px;
    padding: 8px 12px;
    margin: 2px 8px;
    color: {COLORS['muted']};
}}
.qs-battery-icon {{ color: {COLORS['green']}; }}

/* Wi-Fi + Bluetooth stay as the two large ColorOS-style cards. */
.qs-wide-tile {{
    background: rgba(255,255,255,0.13);
    color: {COLORS['white']};
    border: 1px solid rgba(255,255,255,0.11);
    border-radius: 25px;
    min-height: 74px;
    padding: 0;
}}
.qs-wide-tile:hover {{ background: rgba(255,255,255,0.20); }}
.qs-wide-tile-active {{
    background: rgba(42, 166, 166, 0.85);
    color: #0b192c;
    border-radius: 25px;
    min-height: 74px;
}}
.qs-wide-circle {{
    background: rgba(255,255,255,0.10);
    border-radius: 50px;
    min-width: 46px; min-height: 46px;
}}
.qs-wide-circle-active {{
    background: rgba(255,255,255,0.35);
    border-radius: 50px;
    min-width: 46px; min-height: 46px;
}}
.qs-wide-icon {{ color: {COLORS['white']}; }}
.qs-wide-icon-active {{ color: #0b192c; }}
.qs-wide-label {{ color: {COLORS['white']}; font-size: 14px; font-weight: 600; }}
.qs-wide-label-active {{ color: #0b192c; font-size: 14px; font-weight: 600; }}
.qs-wide-status {{ color: #c9c9d6; font-size: 10px; }}
.qs-wide-status-active {{ color: rgba(255, 255, 255, 0.88); font-size: 10px; }}

.qs-chevron {{
    background: rgba(255,255,255,0.06);
    border: none;
    border-left: 1px solid rgba(255,255,255,0.10);
    border-radius: 0 25px 25px 0;
    min-width: 25px;
    color: {COLORS['muted']};
}}
.qs-chevron:hover {{ background: rgba(255,255,255,0.15); }}

/* Small circular controls. */
.qs-round-tile {{
    background: rgba(255,255,255,0.07);
    color: {COLORS['white']};
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 50%;
    min-width: 82px; min-height: 82px;
    padding: 0;
}}
.qs-round-tile:hover {{ background: rgba(255,255,255,0.15); }}
.qs-round-tile-active {{
    background: rgba(42, 166, 166, 0.85);
    color: #0b192c;
    border-radius: 50%;
    min-width: 82px; min-height: 82px;
}}
.qs-round-icon {{ color: {COLORS['white']}; }}
.qs-round-icon-active {{ color: #0b192c; }}
.qs-round-label {{ color: {COLORS['white']}; font-size: 10px; font-weight: 500; }}
.qs-round-label-active {{ color: {COLORS['white']}; font-size: 10px; font-weight: 500; }}
.qs-round-status {{ color: #c9c9d6; font-size: 9px; }}
.qs-round-status-active {{ color: rgba(255, 255, 255, 0.88); font-size: 9px; }}

/* Per-control accent rings/tints. */
.qs-accent-blue {{ background: rgba(79,140,255,0.24); }}
.qs-accent-green {{ background: rgba(66,230,138,0.24); }}
.qs-accent-yellow {{ background: rgba(255,212,71,0.24); }}
.qs-accent-purple {{ background: rgba(168,139,255,0.24); }}
.qs-accent-pink {{ background: rgba(255,121,198,0.24); }}
.qs-accent-cyan {{ background: rgba(67,217,255,0.24); }}
.qs-accent-red {{ background: rgba(255,100,124,0.24); }}

.qs-media {{
    background: rgba(255,255,255,0.09);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 25px;
    padding: 12px;
}}
.qs-album {{ background: rgba(255,255,255,0.12); border-radius: 13px; color: {COLORS['muted']}; }}
.qs-media-title {{ color: {COLORS['white']}; font-size: 16px; font-weight: 600; }}
.qs-media-artist {{ color: {COLORS['muted']}; font-size: 11px; }}
.qs-media-btn, .qs-media-btn-play {{ border: none; border-radius: 50px; min-width: 38px; min-height: 38px; padding: 6px; }}
.qs-media-btn {{ background: transparent; color: {COLORS['muted']}; }}
.qs-media-btn:hover {{ background: rgba(255,255,255,0.12); color: {COLORS['white']}; }}
.qs-media-btn-play {{ background: rgba(248,251,255,0.90); color: #10203b; }}

.qs-slider-box {{
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 22px;
    padding: 10px 14px;
}}
.qs-slider trough {{ background: rgba(255,255,255,0.12); border-radius: 10px; min-height: 8px; }}
.qs-slider trough highlight {{ background: linear-gradient(to right, #38b2ac, #2aa6a6); border-radius: 10px; min-height: 8px; }}
.qs-slider slider {{ background: {COLORS['white']}; border: none; border-radius: 50%; min-width: 16px; min-height: 16px; }}
.qs-slider-icon {{ background: transparent; border: none; color: {COLORS['white']}; min-width: 34px; min-height: 34px; border-radius: 50px; }}
.qs-slider-icon:hover {{ background: rgba(255,255,255,0.12); }}
.qs-slider-label {{ color: {COLORS['muted']}; font-size: 11px; min-width: 38px; }}
.qs-large-slider {{ margin-top: 2px; }}

.qs-action-btn {{ background: rgba(255,255,255,0.09); color: {COLORS['white']}; border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 9px; }}
.qs-action-btn:hover {{ background: rgba(255,255,255,0.17); }}
.qs-page-dot {{ color: rgba(255,255,255,0.30); font-size: 10px; }}
.qs-page-dot-active {{ color: {COLORS['white']}; font-size: 10px; }}

.qs-detail-header {{ padding: 8px; }}
.qs-detail-title {{ color: {COLORS['white']}; font-size: 16px; font-weight: 600; }}
.qs-detail-back, .qs-settings-btn {{ color: {COLORS['white']}; background: transparent; border: none; }}
.qs-network-row {{ padding: 9px; border-radius: 12px; }}
.qs-network-row:hover {{ background: rgba(255,255,255,0.08); }}
.qs-row-label {{ color: {COLORS['white']}; }}
.qs-row-sublabel, .qs-section-label {{ color: {COLORS['muted']}; }}
.qs-row-btn {{ background: rgba(255,255,255,0.12); color: {COLORS['white']}; border: none; border-radius: 10px; padding: 5px 10px; }}
.qs-switch trough {{ background: rgba(255,255,255,0.13); border-radius: 20px; min-width: 38px; min-height: 20px; }}
.qs-switch trough:checked {{ background: {COLORS['green']}; }}
.qs-switch slider {{ background: white; border-radius: 50%; min-width: 16px; min-height: 16px; }}
.qs-signal-strong, .qs-connected-dot {{ color: {COLORS['green']}; }}
"""


def apply_theme():
    provider = Gtk.CssProvider()
    provider.load_from_data(CSS.encode("utf-8"))
    screen = Gdk.Screen.get_default()
    Gtk.StyleContext.add_provider_for_screen(
        screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )
