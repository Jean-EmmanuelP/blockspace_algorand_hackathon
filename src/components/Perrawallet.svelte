<script>
	import AddFile from './AddFile.svelte';
	import { onMount } from 'svelte';
	import { PeraWalletConnect } from '@perawallet/connect';
	import { count, accountInformation } from '$lib/writable';

	let accountAddress = null;
	const peraWallet = new PeraWalletConnect();

	const connectWallet = async () => {
		try {
			const newAccounts = await peraWallet.connect();
			peraWallet.connector?.on('disconnect', handleDisconnectWalletClick);
			accountAddress = newAccounts[0];
			count.set(2);
			accountInformation.set({
				userWalletAddress: accountAddress,
				isConnected: peraWallet.connector._connected
			});
			console.log('those are the informations: ', JSON.stringify($accountInformation, null, 2));
			console.log("Connecté avec l'adresse :", accountAddress);
			console.log('Informations du wallet :', peraWallet);
		} catch (error) {
			if (error?.data?.type !== 'CONNECT_MODAL_CLOSED') {
				console.error('Erreur lors de la connexion :', error);
			}
		}
	};

	const handleDisconnectWalletClick = () => {
		peraWallet.disconnect();
		accountAddress = null;
		accountInformation.set({
			userWalletAddress: null,
			isConnected: false
		});
		console.log('Déconnecté du portefeuille.');
	};

	onMount(() => {
		peraWallet
			.reconnectSession()
			.then((accounts) => {
				if (accounts.length) {
					accountAddress = accounts[0];
					accountInformation.set({
						userWalletAddress: accountAddress,
						isConnected: peraWallet.connector._connected
					});
					console.log("Session reconnectée avec l'adresse :", accountAddress);
				}
				peraWallet.connector?.on('disconnect', handleDisconnectWalletClick);
			})
			.catch((error) => {
				console.error('Erreur de reconnexion :', error);
				peraWallet.disconnect();
			});
	});
</script>

<div class="relative flex h-screen w-screen items-center justify-center">
	{#if $count === 2}
		<div class="absolute right-[2%] top-[2%] flex items-center justify-center gap-3">
			<img
				src="https://cdn-images-1.medium.com/max/1200/1*6IXBhu4YtdCpHlWZkmWAAw.png"
				class="h-8 w-8 rounded-full"
				alt=""
			/>
			<p class="w-[170px] truncate">
				{$accountInformation.userWalletAddress}
			</p>
		</div>
	{/if}
	<div class="absolute left-[2%] top-[2%] flex items-center justify-center gap-3">
		<img
			src="https://miro.medium.com/v2/resize:fit:740/1*ooOH6jo8I0ns0J-BE0SAow.jpeg"
			class="h-14 w-14 rounded-full shadow-sm"
			alt="Profile"
		/>
		<div class="flex flex-col items-start gap-1">
			<h1 class="font-semibold">Jean-Emmanuel Perramant</h1>
			<h3 class="text-sm text-gray-400">jperrama@gmail.com</h3>
		</div>
	</div>

	{#if $count === 2}
		<AddFile />
	{:else}
		<button
			on:click={connectWallet}
			class="transform rounded-lg bg-blue-600 px-6 py-3 text-lg font-semibold text-white shadow-lg transition-all duration-300 hover:scale-105 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
		>
			Connectez votre Pera Wallet pour commencer
		</button>
	{/if}
</div>
