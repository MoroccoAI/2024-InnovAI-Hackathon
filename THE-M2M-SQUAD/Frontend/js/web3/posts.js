import { getContract } from './wallet.js';
import { formatDistanceToNow } from 'date-fns';

export async function publishPost(message) {
    const contract = getContract();
    const tx = await contract.publishPost(message);
    await tx.wait();
}

export async function editPost(index, newMessage) {
    const contract = getContract();
    const tx = await contract.editPost(index, newMessage);
    await tx.wait();
}

export async function likePost(index) {
    const contract = getContract();
    const tx = await contract.likePost(index);
    await tx.wait();
}

export async function dislikePost(index) {
    const contract = getContract();
    const tx = await contract.dislikePost(index);
    await tx.wait();
}

export async function loadPosts() {
    const contract = getContract();
    const totalPosts = await contract.getTotalPosts();
    const posts = [];

    for (let i = totalPosts - 1; i >= 0; i--) {
        const [message, author, timestamp, lastModified, likes, dislikes] = await contract.getPost(i);
        posts.push({
            index: i,
            message,
            author,
            timestamp: Number(timestamp) * 1000,
            lastModified: Number(lastModified) * 1000,
            likes: Number(likes),
            dislikes: Number(dislikes)
        });
    }

    return posts;
}