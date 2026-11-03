package local.csmathskillgame.app;

import android.webkit.WebSettings;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {

    // The game lays itself out for the phone; page zoom only lets a pinch blow the whole UI up.
    // Capacitor already turns off WebView's built-in zoom controls, but some phones' WebViews still
    // pinch-zoomed (seen 2026-11-03), so zoom support is switched off as well; native.js adds
    // user-scalable=no to the page viewport for the same reason. The map has its own pinch zoom.
    @Override
    protected void load() {
        super.load();
        WebSettings settings = bridge.getWebView().getSettings();
        settings.setSupportZoom(false);
        settings.setBuiltInZoomControls(false);
        settings.setDisplayZoomControls(false);
        // Background music changes tracks on its own (end of a track, a new screen). The WebView's
        // default needs a tap for every audio element; the game already waits for the first tap.
        settings.setMediaPlaybackRequiresUserGesture(false);
    }
}
