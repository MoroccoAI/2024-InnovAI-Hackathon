import Web3 from 'web3';
import { CONTRACT_ADDRESS, CONTRACT_ABI } from './config.js';
import { showToast } from '../utils/notifications.js';

let web3;
let contract;
let account;

export const getWeb3Instance = () => web3;
export const getContract = () => contract;
export const getCurrentAccount = () => account;

export const initWeb3 = async () => {
    if (window.ethereum) {
        web3 = new Web3(window.ethereum);
        try {
            const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
            account = Web3.utils.toChecksumAddress(accounts[0]);
            contract = new web3.eth.Contract(CONTRACT_ABI, CONTRACT_ADDRESS);
            
            // Setup event listeners for account changes
            window.ethereum.on('accountsChanged', handleAccountsChanged);
            window.ethereum.on('chainChanged', () => window.location.reload());
            
            return { account, contract };
        } catch (error) {
            throw new Error('User denied account access');
        }
    } else {
        throw new Error('Please install MetaMask');
    }
};

const handleAccountsChanged = async (accounts) => {
    if (accounts.length === 0) {
        showToast('Please connect to MetaMask', 'warning');
    } else {
        account = Web3.utils.toChecksumAddress(accounts[0]);
        showToast('Account changed successfully', 'success');
        window.location.reload();
    }
};