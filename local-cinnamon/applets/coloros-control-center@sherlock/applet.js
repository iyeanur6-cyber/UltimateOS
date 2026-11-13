const Applet = imports.ui.applet;
const PopupMenu = imports.ui.popupMenu;
const St = imports.gi.St;
const GLib = imports.gi.GLib;
const Util = imports.misc.util;
const Lang = imports.lang;

function run(cmd) {
    try {
        Util.spawnCommandLineAsync(cmd);
    } catch (e) {
        global.logError("ColorOS: " + e);
    }
}

function output(cmd) {
    try {
        let result = GLib.spawn_command_line_sync(cmd);
        if (result[0] && result[1]) {
            return imports.byteArray.toString(result[1]).trim();
        }
    } catch (e) {
        global.logError("ColorOS command: " + e);
    }
    return "";
}

class ColorOSApplet extends Applet.IconApplet {
    constructor(orientation, panelHeight, instanceId) {
        super(orientation, panelHeight, instanceId);

        this.set_applet_icon_symbolic_name("view-grid");
        this.set_applet_tooltip("ColorOS Control Center");

        this.menuManager = new PopupMenu.PopupMenuManager(this);
        this.menu = new Applet.AppletPopupMenu(this, orientation);
        this.menuManager.addMenu(this.menu);
        this.menu.actor.add_style_class_name("coloros-menu");

        this._buildMenu();
        this._refresh();

        this.menu.connect("open-state-changed", Lang.bind(this, function(menu, open) {
            if (open)
                this._refresh();
        }));
    }

    _button(text, style, callback) {
        let button = new St.Button({
            style_class: "coloros-button " + (style || ""),
            label: text,
            can_focus: true,
            reactive: true,
            x_expand: true
        });
        button.connect("clicked", Lang.bind(this, callback));
        return button;
    }

    _tile(title, subtitle) {
        let tile = new St.BoxLayout({
            vertical: true,
            style_class: "coloros-tile",
            x_expand: true
        });

        let heading = new St.Label({
            text: title,
            style_class: "coloros-title"
        });
        tile.add_child(heading);

        if (subtitle) {
            let detail = new St.Label({
                text: subtitle,
                style_class: "coloros-subtitle"
            });
            tile.add_child(detail);
        }

        return tile;
    }

    _row(children) {
        let item = new PopupMenu.PopupBaseMenuItem({
            reactive: false,
            activate: false,
            hover: false,
            style_class: "coloros-row"
        });

        let row = new St.BoxLayout({
            vertical: false,
            style_class: "coloros-grid-row",
            x_expand: true
        });

        children.forEach(function(child) {
            child.x_expand = true;
            row.add_child(child);
        });

        item.addActor(row);
        this.menu.addMenuItem(item);
    }

    _buildMenu() {
        let header = new PopupMenu.PopupBaseMenuItem({
            reactive: false,
            activate: false,
            hover: false,
            style_class: "coloros-header"
        });
        this.clock = new St.Label({ text: "Quick Settings" });
        header.addActor(this.clock);
        this.menu.addMenuItem(header);

        // 1. POWER
        this.powerTile = this._tile("Power", "Choose power profile");

        let powerButtons = new St.BoxLayout({
            vertical: true,
            style_class: "coloros-button-stack"
        });

        this.powerSaver = this._button("Power Saver", "coloros-small", function() {
            run("powerprofilesctl set power-saver");
            this._refreshSoon();
        });

        this.balanced = this._button("Balanced", "coloros-small", function() {
            run("powerprofilesctl set balanced");
            this._refreshSoon();
        });

        this.performance = this._button("Performance", "coloros-small", function() {
            run("powerprofilesctl set performance");
            this._refreshSoon();
        });

        powerButtons.add_child(this.powerSaver);
        powerButtons.add_child(this.balanced);
        powerButtons.add_child(this.performance);
        this.powerTile.add_child(powerButtons);

        // 2. BLUETOOTH
        this.bluetoothTile = this._tile("Bluetooth", "Checking…");
        this.bluetoothButton = this._button("Bluetooth", "", function() {
            let state = output("rfkill list bluetooth");
            let blocked = /Soft blocked:\s+yes/i.test(state);
            run(blocked ? "rfkill unblock bluetooth" : "rfkill block bluetooth");
            this._refreshSoon();
        });
        this.bluetoothTile.add_child(this.bluetoothButton);

        this._row([this.powerTile, this.bluetoothTile]);

        // 3. MEDIA
        this.mediaTile = this._tile("Media controls", "No player detected");

        this.trackLabel = new St.Label({
            text: "Not playing",
            style_class: "coloros-track"
        });
        this.mediaTile.add_child(this.trackLabel);

        let mediaButtons = new St.BoxLayout({
            vertical: false,
            style_class: "coloros-media-buttons"
        });

        mediaButtons.add_child(this._button("Previous", "", function() {
            run("playerctl previous");
            this._refreshSoon();
        }));

        mediaButtons.add_child(this._button("Play / Pause", "", function() {
            run("playerctl play-pause");
            this._refreshSoon();
        }));

        mediaButtons.add_child(this._button("Next", "", function() {
            run("playerctl next");
            this._refreshSoon();
        }));

        this.mediaTile.add_child(mediaButtons);
        this._row([this.mediaTile]);

        // 4. BRIGHTNESS
        this.brightnessTile = this._tile("Brightness", "Display brightness");
        this.brightnessSlider = new PopupMenu.PopupSliderMenuItem(0.5);
        this.brightnessSlider.connect("value-changed", Lang.bind(this, function(slider, value) {
            let percent = Math.round(value * 100);
            run("brightnessctl -d intel_backlight set " + percent + "%");
        }));
        this.brightnessTile.add_child(this.brightnessSlider.actor);

        // 5. VOLUME
        this.volumeTile = this._tile("Volume", "System audio");
        this.volumeSlider = new PopupMenu.PopupSliderMenuItem(0.5);
        this.volumeSlider.connect("value-changed", Lang.bind(this, function(slider, value) {
            let percent = Math.round(value * 100);
            run("pactl set-sink-volume @DEFAULT_SINK@ " + percent + "%");
        }));
        this.volumeTile.add_child(this.volumeSlider.actor);

        this._row([this.brightnessTile, this.volumeTile]);

        // 6. SOUND MODE
        this.soundTile = this._tile("Sound mode", "Audio mute");
        this.muteButton = this._button("Mute / Unmute", "", function() {
            run("pactl set-sink-mute @DEFAULT_SINK@ toggle");
            this._refreshSoon();
        });
        this.soundTile.add_child(this.muteButton);

        // 7. WI-FI
        this.wifiTile = this._tile("Wi-Fi", "NetworkManager");
        this.wifiButton = this._button("Wi-Fi", "", function() {
            let state = output("nmcli radio wifi");
            run(state === "enabled" ? "nmcli radio wifi off" : "nmcli radio wifi on");
            this._refreshSoon();
        });
        this.wifiTile.add_child(this.wifiButton);

        this._row([this.soundTile, this.wifiTile]);
    }

    on_applet_clicked() {
        this._refresh();
        this.menu.toggle();
    }

    _refreshSoon() {
        GLib.timeout_add(GLib.PRIORITY_DEFAULT, 500, Lang.bind(this, function() {
            this._refresh();
            return GLib.SOURCE_REMOVE;
        }));
    }

    _refresh() {
        let now = new Date();
        let hours = String(now.getHours()).padStart(2, "0");
        let minutes = String(now.getMinutes()).padStart(2, "0");
        this.clock.set_text(hours + ":" + minutes + "   •   Quick Settings");

        // Power profile
        let profile = output("powerprofilesctl get");
        this.powerSaver.set_style_class_name(
            "coloros-button coloros-small " +
            (profile === "power-saver" ? "coloros-selected" : "")
        );
        this.balanced.set_style_class_name(
            "coloros-button coloros-small " +
            (profile === "balanced" ? "coloros-selected" : "")
        );
        this.performance.set_style_class_name(
            "coloros-button coloros-small " +
            (profile === "performance" ? "coloros-selected" : "")
        );

        // Wi-Fi
        let wifiOn = output("nmcli radio wifi") === "enabled";
        this.wifiButton.set_label(wifiOn ? "Wi-Fi  •  On" : "Wi-Fi  •  Off");

        // Bluetooth
        let bt = output("rfkill list bluetooth");
        let btOn = !/Soft blocked:\s+yes/i.test(bt) &&
                   !/Hard blocked:\s+yes/i.test(bt);
        this.bluetoothButton.set_label(btOn ? "Bluetooth  •  On" : "Bluetooth  •  Off");

        // Brightness
        let brightness = output("brightnessctl -m -d intel_backlight");
        let matchBrightness = brightness.match(/,(\d+)%/);
        if (matchBrightness)
            this.brightnessSlider.setValue(parseInt(matchBrightness[1], 10) / 100);

        // Volume
        let volume = output("pactl get-sink-volume @DEFAULT_SINK@");
        let matchVolume = volume.match(/(\d+)%/);
        if (matchVolume)
            this.volumeSlider.setValue(Math.min(100, parseInt(matchVolume[1], 10)) / 100);

        let muted = output("pactl get-sink-mute @DEFAULT_SINK@");
        this.muteButton.set_label(/yes/i.test(muted) ? "Muted" : "Sound On");

        // Media player
        let players = output("playerctl -l");
        if (!players) {
            this.trackLabel.set_text("Not playing");
        } else {
            let title = output("playerctl metadata --format '{{artist}} - {{title}}'");
            let status = output("playerctl status");
            this.trackLabel.set_text(
                (title || "Media player detected") + "  •  " + (status || "Unknown")
            );
        }
    }

    on_applet_removed_from_panel() {
        if (this.menu)
            this.menu.destroy();
        if (this.menuManager)
            this.menuManager.removeMenu(this.menu);
    }
}

function main(metadata, orientation, panelHeight, instanceId) {
    return new ColorOSApplet(orientation, panelHeight, instanceId);
}
