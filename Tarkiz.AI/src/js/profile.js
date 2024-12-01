class UserProfile {
  constructor() {
    this.form = document.getElementById('userProfile');
    this.nameInput = document.getElementById('userName');
    this.focusDurationInput = document.getElementById('focusDuration');
    this.breakDurationInput = document.getElementById('breakDuration');
    this.themeSelect = document.getElementById('theme');

    this.initializeEventListeners();
    this.loadProfile();
  }

  initializeEventListeners() {
    this.form.addEventListener('submit', (e) => this.saveProfile(e));
    this.themeSelect.addEventListener('change', () => this.updateTheme());
  }

  async loadProfile() {
    const data = await chrome.storage.sync.get([
      'userName',
      'focusDuration',
      'breakDuration',
      'theme'
    ]);

    if (data.userName) this.nameInput.value = data.userName;
    if (data.focusDuration) this.focusDurationInput.value = data.focusDuration;
    if (data.breakDuration) this.breakDurationInput.value = data.breakDuration;
    if (data.theme) {
      this.themeSelect.value = data.theme;
      this.updateTheme();
    }
  }

  async saveProfile(e) {
    e.preventDefault();

    const profile = {
      userName: this.nameInput.value,
      focusDuration: parseInt(this.focusDurationInput.value),
      breakDuration: parseInt(this.breakDurationInput.value),
      theme: this.themeSelect.value
    };

    await chrome.storage.sync.set(profile);
    this.showSaveConfirmation();
  }

  updateTheme() {
    document.body.dataset.theme = this.themeSelect.value;
  }

  showSaveConfirmation() {
    const notification = document.createElement('div');
    notification.className = 'save-notification';
    notification.textContent = 'Settings saved successfully!';
    
    document.body.appendChild(notification);
    setTimeout(() => notification.remove(), 3000);
  }
}

new UserProfile();