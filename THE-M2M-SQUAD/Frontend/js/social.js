import { PostManager } from './web3/postManager.js';
import { showToast } from './utils/notifications.js';

let postManager;

export async function initSocial() {
    const container = document.getElementById('posts-container');
    const postForm = document.querySelector('.Wallet');

    if (!container || !postForm) {
        console.error('Required social elements not found');
        return;
    }

    postManager = new PostManager(container);

    setupWalletButtons(postForm);
    setupPostForm();
}

function setupWalletButtons(postForm) {
    // Create wallet buttons container
    const walletContainer = document.createElement('div');
    walletContainer.className = 'wallet-container';

    // Connect Wallet Button
    const connectButton = document.createElement('button');
    connectButton.id = 'connect-wallet';
    connectButton.className = 'wallet-button';
    connectButton.innerHTML = '<i class="fas fa-wallet"></i> Connect Wallet';

    // Disconnect Wallet Button
    const disconnectButton = document.createElement('button');
    disconnectButton.id = 'disconnect-wallet';
    disconnectButton.className = 'wallet-button disconnect hidden';
    disconnectButton.innerHTML = '<i class="fas fa-sign-out-alt"></i> Disconnect Wallet';

    walletContainer.appendChild(connectButton);
    walletContainer.appendChild(disconnectButton);
    postForm.insertBefore(walletContainer, postForm.firstChild);

    // Connect Wallet Logic
    connectButton.addEventListener('click', async () => {
        try {
            connectButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Connecting...';
            const walletAddressInput = document.getElementById('wallet-address'); 
            const walletAddress = walletAddressInput.value; // Initialize PostManager with wallet address 
            const connected = await postManager.init(walletAddress);
            if (connected) {
                connectButton.classList.add('hidden');
                disconnectButton.classList.remove('hidden');
                showWalletInfo(connectButton, postManager.account);
                await postManager.loadPosts();
                
                // Ensure .left-section is visible
                if (document.querySelector('.left-section')) {
                    document.querySelector('.left-section').style.display = 'block';
                }
            }
        } catch (error) {
            connectButton.innerHTML = '<i class="fas fa-wallet"></i> Connect Wallet';
            showToast(error.message, 'error');
        }
    });
    

    // Disconnect Wallet Logic
    disconnectButton.addEventListener('click', () => {
        postManager.disconnect();
        connectButton.classList.remove('hidden');
        disconnectButton.classList.add('hidden');
        resetWalletInfo();
        showToast('Disconnected from wallet', 'info');
    });
}

function showWalletInfo(button, account) {
    button.innerHTML = `
        <i class="fas fa-check-circle"></i>
        Connected: ${account.slice(0, 6)}...${account.slice(-4)}
    `;
    button.classList.add('connected');
}

function resetWalletInfo() {
    const walletInfo = document.querySelector('#connect-wallet');
    if (walletInfo) {
        walletInfo.innerHTML = '<i class="fas fa-wallet"></i> Connect Wallet';
        walletInfo.classList.remove('connected');
    }
}

function setupPostForm() {
    const publishButton = document.getElementById('publish-post');
    const messageInput = document.getElementById('post-message');
    const charCounter = document.createElement('div');
    charCounter.id = 'char-counter';
    charCounter.className = 'char-counter';
    charCounter.textContent = '280 characters remaining';
    messageInput.parentNode.insertBefore(charCounter, messageInput.nextSibling);

    if (!publishButton || !messageInput) {
        console.error('Post form elements not found');
        return;
    }

    publishButton.addEventListener('click', async () => {
        if (!postManager?.account) {
            showToast('Please connect your wallet first', 'warning');
            return;
        }

        if (!messageInput.value.trim()) {
            showToast('Post cannot be empty', 'warning');
            return;
        }

        await postManager.publishPost(messageInput.value);
        messageInput.value = '';
        updateCharacterCounter(charCounter, 280);
    });

    messageInput.addEventListener('input', () => {
        updateCharacterCounter(charCounter, 280 - messageInput.value.length);
        publishButton.disabled = !messageInput.value.trim();
    });

    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey && publishButton) {
            e.preventDefault();
            publishButton.click();
        }
    });
}

function updateCharacterCounter(counter, remaining) {
    counter.textContent = `${remaining} characters remaining`;
    counter.style.color = remaining < 0 ? 'red' : '';
}
