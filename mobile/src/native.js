// Native bridge bundled into the Capacitor app (www/native.js). Exposes window.BSGNative.
import { Capacitor } from "@capacitor/core";
import { App } from "@capacitor/app";
import { Share } from "@capacitor/share";
import { Filesystem, Directory } from "@capacitor/filesystem";
import { SplashScreen } from "@capacitor/splash-screen";

window.BSGNative = {
  isNative: Capacitor.isNativePlatform(),
  async shareFile({ name, text, title, body }) {
    const f = await Filesystem.writeFile({
      path: name,
      data: text,
      directory: Directory.Cache,
      encoding: "utf8",
    });
    await Share.share({ title, text: body, files: [f.uri], dialogTitle: title });
    return true;
  },
  hideSplash() {
    SplashScreen.hide({ fadeOutDuration: 250 }).catch(() => {});
  },
};

document.addEventListener("DOMContentLoaded", () => {
  window.BSGNative.hideSplash();
});

App.addListener("backButton", ({ canGoBack }) => {
  if (canGoBack || (window.location.hash && window.location.hash !== "#/")) {
    window.history.back();
  } else {
    App.exitApp();
  }
});
