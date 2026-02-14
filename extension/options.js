const DEFAULT_SETTINGS = {
  profileDirectory: 'Profile 1',
  closeOriginalTab: false
};

const profileInput = document.getElementById('profileDirectory');
const closeInput = document.getElementById('closeOriginalTab');
const saveButton = document.getElementById('saveButton');
const status = document.getElementById('status');

function setStatus(message, isError = false) {
  status.textContent = message;
  status.style.color = isError ? '#b10000' : '#1b5e20';
}

function isValidProfileDirectory(value) {
  return value.length > 0 && value.length <= 128 && !/["<>|?*]/.test(value);
}

async function loadOptions() {
  const settings = await chrome.storage.sync.get(DEFAULT_SETTINGS);
  profileInput.value = settings.profileDirectory;
  closeInput.checked = Boolean(settings.closeOriginalTab);
}

async function saveOptions() {
  const profileDirectory = profileInput.value.trim();
  const closeOriginalTab = closeInput.checked;

  if (!isValidProfileDirectory(profileDirectory)) {
    setStatus('Invalid profile directory value.', true);
    return;
  }

  await chrome.storage.sync.set({ profileDirectory, closeOriginalTab });
  setStatus('Saved.');
}

saveButton.addEventListener('click', () => {
  saveOptions().catch((error) => setStatus(`Save failed: ${error.message}`, true));
});

loadOptions().catch((error) => setStatus(`Load failed: ${error.message}`, true));
