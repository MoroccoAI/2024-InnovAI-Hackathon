import Web3 from 'web3';
import { CONTRACT_ABI } from '../web3/config.js';
import { showToast, showEditDialog, showCommentDialog } from '../utils/notifications.js';
import { formatDistanceToNow } from 'date-fns';

export class PostManager {
    constructor(container) {
        this.container = container;
        this.web3 = null;
        this.contract = null;
        this.account = null;
        this.isLoading = false;
    }

    async init(address) { 
        if (window.ethereum) { 
            this.web3 = new Web3(window.ethereum); 
        try { 
            const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' }); 
            this.account = this.web3.utils.toChecksumAddress(accounts[0]); 
            this.contract = new this.web3.eth.Contract(CONTRACT_ABI, address); 
            // Setup event listeners 
            window.ethereum.on('accountsChanged', (accounts) => this.handleAccountChange(accounts)); 
            window.ethereum.on('chainChanged', () => window.location.reload()); 
            
            return true; 
        } catch (error) { 
            showToast('Failed to connect wallet: ' + error.message, 'error'); 
            return false; } 
        } else { 
            showToast('Please install MetaMask', 'warning'); 
            return false; 
        } 
    }


    async handleAccountChange(accounts) {
                if (accounts.length === 0) {
                    this.account = null;
                    showToast('Please connect to MetaMask', 'warning');
                } else {
                    this.account = this.web3.utils.toChecksumAddress(accounts[0]);
                    showToast('Account changed successfully', 'success');
                    await this.loadPosts();
                }
    }
        
    async loadPosts() {
        if (!this.contract) return;
    
        try {
            this.isLoading = true;
            this.showLoadingState();
    
            // Convert totalPosts from BigInt to Number explicitly
            const totalPosts = Number(await this.contract.methods.getTotalPosts().call());
            const posts = [];
    
            for (let i = totalPosts - 1; i >= 0; i--) {
                const post = await this.contract.methods.getPost(i).call();
                const comments = await this.loadComments(i); // Load comments for each post
    
                posts.push({
                    index: i,
                    message: post[0],
                    imageUrl: post[1], // Include the image URL
                    author: post[2],
                    timestamp: Number(post[3]) * 1000, // Convert BigInt to Number
                    lastModified: Number(post[4]) * 1000, // Convert BigInt to Number
                    likes: Number(post[5]), // Convert BigInt to Number
                    dislikes: Number(post[6]), // Convert BigInt to Number
                    comments: comments // Add comments to the post
                });
            }
    
            this.renderPosts(posts);
        } catch (error) {
            showToast('Failed to load posts: ' + error.message, 'error');
        } finally {
            this.isLoading = false;
        }
    }

    async loadComments(postIndex) {
        try {
            const totalComments = await this.contract.methods.getCommentsCount(postIndex).call();
            const comments = [];
    
            for (let i = 0; i < totalComments; i++) {
                const comment = await this.contract.methods.getComment(postIndex, i).call();
    
                comments.push({
                    message: comment[0],
                    author: comment[1],
                    timestamp: Number(comment[2]) * 1000, // Convert BigInt to Number
                    likes: Number(comment[3]), // Convert BigInt to Number
                    dislikes: Number(comment[4]) // Convert BigInt to Number
                });
            }
    
            return comments;
        } catch (error) {
            showToast('Failed to load comments: ' + error.message, 'error');
            return [];
        }
    }

    async publishPost() {
        const content = document.getElementById('post-message').value.trim();
        const imageInput = document.getElementById('post-image');
        const file = imageInput.files[0];
        let imageUrl = '';

        if (!content && !file) {
            showToast('Post content cannot be empty', 'warning');
            return;
        }

        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                imageUrl = reader.result;

                this.contract.methods.publishPost(content, imageUrl).send({ from: this.account })
                    .then(async () => {
                        showToast('Post published successfully!', 'success');
                        await this.loadPosts();
                    })
                    .catch(error => {
                        if (error.code === 4001) {
                            showToast('Transaction cancelled by user', 'info');
                        } else {
                            showToast('Failed to publish post: ' + error.message, 'error');
                        }
                    });
            };
            reader.readAsDataURL(file); // Convert image to Base64 string
        } else {
            this.contract.methods.publishPost(content, imageUrl).send({ from: this.account })
                .then(async () => {
                    showToast('Post published successfully!', 'success');
                    await this.loadPosts();
                })
                .catch(error => {
                    if (error.code === 4001) {
                        showToast('Transaction cancelled by user', 'info');
                    } else {
                        showToast('Failed to publish post: ' + error.message, 'error');
                    }
                });
        }
    }

    async handlePostAction(action, index) {
        try {
            switch (action) {
                case 'like':
                    await this.contract.methods.likePost(index)
                        .send({ from: this.account });
                    showToast('Post liked!', 'success');
                    break;
                    
                case 'dislike':
                    await this.contract.methods.dislikePost(index)
                        .send({ from: this.account });
                    showToast('Post disliked!', 'success');
                    break;
                    
                case 'edit':
                    const post = await this.contract.methods.getPost(index).call();
                    const newContent = await showEditDialog(post[0]);
                    if (newContent) {
                        await this.contract.methods.editPost(index, newContent)
                            .send({ from: this.account });
                        showToast('Post updated successfully!', 'success');
                    }
                    break;

                case 'comment':
                    const commentContent = await showCommentDialog();
                    if (commentContent) {
                        await this.addComment(index, commentContent);
                    }
                    break;
            }
            
            await this.loadPosts();
        } catch (error) {
            if (error.code === 4001) {
                showToast('Transaction cancelled by user', 'info');
            } else {
                showToast(`Failed to ${action} post: ` + error.message, 'error');
            }
        }
    }

    showLoadingState() {
        this.container.innerHTML = `
            <div class="loading-spinner">
                <i class="fas fa-spinner fa-spin"></i>
                <p>Loading posts...</p>
            </div>`;
    }

    renderPosts(posts) {
        this.container.innerHTML = posts.map(post => this.createPostElement(post)).join('');
        this.attachEventListeners();
    }

    createPostElement(post) {
        const isAuthor = post.author.toLowerCase() === this.account?.toLowerCase();
        
        return `
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">

        
            <div class="post" data-index="${post.index}">
                <div class="post-header">
                    <span class="author">
                        <i class="fas fa-user-md"></i>
                        ${post.author.slice(0, 6)}...${post.author.slice(-4)}
                    </span>
                    <span class="timestamp">
                        <i class="fas fa-clock"></i>
                        ${formatDistanceToNow(post.timestamp)} ago
                    </span>
                </div>
                
                <div class="post-content">
                    ${post.message}
                </div>
                
                ${post.imageUrl ? `<img src="${post.imageUrl}" alt="Post image" class="post-image">` : ''}
                
                <div class="post-actions">
                    <button class="action-btn like-btn" data-action="like">
                        <i class="fas fa-thumbs-up"></i>
                        <span>${post.likes}</span>
                    </button>
                    <button class="action-btn dislike-btn" data-action="dislike">
                        <i class="fas fa-thumbs-down"></i>
                        <span>${post.dislikes}</span>
                    </button>
                    ${isAuthor ? `
                        <button class="action-btn edit-btn" data-action="edit">
                            <i class="fas fa-edit"></i>
                            Edit
                        </button>
                    ` : ''}
                    <button class="action-btn comment-btn" data-action="comment">
                        <i class="fas fa-comment-alt"></i>
                        Comment
                    </button>
                </div>
                
                ${post.lastModified > post.timestamp ? `
                    <div class="post-edited">
                        <i class="fas fa-pencil-alt"></i>
                        Edited ${formatDistanceToNow(post.lastModified)} ago
                    </div>
                ` : ''}

                <div class="comments">
                    ${post.comments.map(comment => `
                        <div class="comment">
                            <div class="comment-header">
                                <span class="author">${comment.author.slice(0, 6)}...${comment.author.slice(-4)}</span>
                                <span class="timestamp">${formatDistanceToNow(comment.timestamp)} ago</span>
                            </div>
                            <div class="comment-content">${comment.message}</div>
                        </div>
                    `).join('')}
                </div>
            </div>

        
        `;
    }

    attachEventListeners() {
        this.container.querySelectorAll('.action-btn').forEach(button => {
            button.addEventListener('click', async (e) => {
                const action = button.dataset.action;
                const postElement = button.closest('.post');
                const index = postElement.dataset.index;
                
                await this.handlePostAction(action, index);
            });
        });
    }

    async addComment(postIndex, comment) {
        if (!comment.trim()) {
            showToast('Comment content cannot be empty', 'warning');
            return;
        }

        try {
            await this.contract.methods.addComment(postIndex, comment)
                .send({ from: this.account });
            showToast('Comment added successfully!', 'success');
            await this.loadPosts();
        } catch (error) {
            if (error.code === 4001) {
                showToast('Transaction cancelled by user', 'info');
            } else {
                showToast('Failed to add comment: ' + error.message, 'error');
            }
        }
    }

    disconnect() {
        this.account = null;
        this.contract = null;
        this.clearPosts();
        document.getElementById('connect-wallet').classList.remove('hidden');
        document.getElementById('disconnect-wallet').classList.add('hidden');
        showToast('Disconnected successfully', 'info');
    }

    clearPosts() {
        this.container.innerHTML = ''; // Remove all posts from the container
    }
    
} 
