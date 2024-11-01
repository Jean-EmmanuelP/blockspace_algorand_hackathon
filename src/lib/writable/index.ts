import { writable } from 'svelte/store';

export const count = writable(0);
export const accountInformation = writable<{ userWalletAddress: string; isConnected: boolean }>();
