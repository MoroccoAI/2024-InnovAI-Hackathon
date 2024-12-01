class Timer {
  constructor() {
    this.minutes = 25;
    this.seconds = 0;
    this.isRunning = false;
    this.interval = null;
    this.focusCount = 0;

    this.minutesDisplay = document.getElementById('minutes');
    this.secondsDisplay = document.getElementById('seconds');
    this.startButton = document.getElementById('startTimer');
    this.resetButton = document.getElementById('resetTimer');
    this.focusCountDisplay = document.getElementById('focusCount');

    this.initializeEventListeners();
    this.loadSettings();
  }

  initializeEventListeners() {
    this.startButton.addEventListener('click', () => this.toggleTimer());
    this.resetButton.addEventListener('click', () => this.resetTimer());
  }

  async loadSettings() {
    const settings = await chrome.storage.sync.get(['focusDuration']);
    if (settings.focusDuration) {
      this.minutes = settings.focusDuration;
      this.updateDisplay();
    }
  }

  toggleTimer() {
    if (this.isRunning) {
      this.pauseTimer();
    } else {
      this.startTimer();
    }
  }

  startTimer() {
    this.isRunning = true;
    this.startButton.textContent = 'Pause';
    this.interval = setInterval(() => this.tick(), 1000);
  }

  pauseTimer() {
    this.isRunning = false;
    this.startButton.textContent = 'Start';
    clearInterval(this.interval);
  }

  resetTimer() {
    this.pauseTimer();
    this.loadSettings();
    this.seconds = 0;
    this.updateDisplay();
  }

  tick() {
    if (this.seconds === 0) {
      if (this.minutes === 0) {
        this.completeSession();
        return;
      }
      this.minutes--;
      this.seconds = 59;
    } else {
      this.seconds--;
    }
    this.updateDisplay();
  }

  updateDisplay() {
    this.minutesDisplay.textContent = String(this.minutes).padStart(2, '0');
    this.secondsDisplay.textContent = String(this.seconds).padStart(2, '0');
  }

  async completeSession() {
    this.pauseTimer();
    this.focusCount++;
    this.focusCountDisplay.textContent = this.focusCount;
    
    await chrome.storage.sync.set({ focusCount: this.focusCount });
    
    new Notification('Focus Session Complete!', {
      body: 'Time for a break!',
      icon: '../../assets/icon-48.png'
    });
    
    this.resetTimer();
  }
}

new Timer();