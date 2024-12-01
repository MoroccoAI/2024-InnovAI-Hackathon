import { ethers } from 'ethers';
import { CONTRACT_ADDRESS, CONTRACT_ABI } from './config.js';

let provider;
let signer;
let contract;

export async function connectWallet() {
    try {
        if (!window.ethereum) {
            throw new Error('MetaMask not detected. Please install MetaMask.');
        }

        provider = new ethers.BrowserProvider(window.ethereum);
        const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
        signer = await provider.getSigner();
        contract = new ethers.Contract(CONTRACT_ADDRESS, CONTRACT_ABI, signer);

        return {
            address: accounts[0],
            contract
        };
    } catch (error) {
        console.error('Error connecting wallet:', error);
        throw error;
    }
}

export function getContract() {
    if (!contract) {
        throw new Error('Wallet not connected');
    }
    return contract;
}

export function isConnected() {
    return !!signer;
}