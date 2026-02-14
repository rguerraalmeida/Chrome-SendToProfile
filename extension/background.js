const HOST_NAME = 'com.send_to_profile.host';
const DEFAULT_SETTINGS = {
  profileDirectory: 'Profile 1',
  closeOriginalTab: false
};

async function getSettings() {
  const data = await chrome.storage.sync.get(DEFAULT_SETTINGS);
  return {
    profileDirectory: String(data.profileDirectory || DEFAULT_SETTINGS.profileDirectory).trim(),
    closeOriginalTab: Boolean(data.closeOriginalTab)
  };
}

function isSupportedUrl(url) {
  try {
    const parsed = new URL(url);
    return parsed.protocol === 'http:' || parsed.protocol === 'https:';
  } catch {
    return false;
  }
}

const FALLBACK_ICON_DATA_URL = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO5i6xQAAAAASUVORK5CYII=';

function notify(title, message) {
  chrome.notifications.create({
    type: 'basic',
    iconUrl: FALLBACK_ICON_DATA_URL,
    title,
    message
  });
}

function sendToNativeHost(payload) {
  return new Promise((resolve, reject) => {
    chrome.runtime.sendNativeMessage(HOST_NAME, payload, (response) => {
      if (chrome.runtime.lastError) {
        reject(new Error(chrome.runtime.lastError.message));
        return;
      }
      resolve(response);
    });
  });
}

async function closeTabIfRequested(tabId, closeOriginalTab) {
  if (!closeOriginalTab || typeof tabId !== 'number') {
    return;
  }
  try {
    await chrome.tabs.remove(tabId);
  } catch (error) {
    notify('Send To Profile', `Tab sent, but close failed: ${error.message}`);
  }
}

chrome.runtime.onInstalled.addListener(async () => {
  const existing = await chrome.storage.sync.get(DEFAULT_SETTINGS);
  await chrome.storage.sync.set({ ...DEFAULT_SETTINGS, ...existing });
});

let inFlight = false;

chrome.action.onClicked.addListener(async (tab) => {
  if (inFlight) {
    notify('Send To Profile', 'A send operation is already in progress.');
    return;
  }

  inFlight = true;
  try {
    const url = tab?.url;
    if (!url || !isSupportedUrl(url)) {
      notify('Send To Profile', 'Only http/https URLs are supported.');
      return;
    }

    const settings = await getSettings();
    if (!settings.profileDirectory) {
      notify('Send To Profile', 'Set a target profile in extension options.');
      return;
    }

    const requestId = crypto.randomUUID();
    const response = await sendToNativeHost({
      version: 1,
      action: 'open_url_in_profile',
      requestId,
      url,
      profileDirectory: settings.profileDirectory,
      closeOriginalTabRequested: settings.closeOriginalTab
    });

    if (!response || response.ok !== true) {
      const message = response?.message || 'Unknown native host error.';
      notify('Send To Profile', `Send failed: ${message}`);
      return;
    }

    await closeTabIfRequested(tab?.id, settings.closeOriginalTab);
    notify('Send To Profile', `Sent to ${settings.profileDirectory}.`);
  } catch (error) {
    const hint = error.message?.includes('Specified native messaging host not found')
      ? ' Install the native host first (see docs/setup-windows.md).'
      : '';
    notify('Send To Profile', `Unable to contact host: ${error.message}.${hint}`);
  } finally {
    inFlight = false;
  }
});
