<script>
	import { fade, fly } from 'svelte/transition';
	import { PinataSDK } from 'pinata';
	import { env } from '$env/dynamic/public';
	import { accountInformation, registeredFiles } from '$lib/writable';
	import OpenImage from './modals/OpenImage.svelte';

	let selectedFile = $state(null);
	let fileName = $state('');
	let isFileAdded = $state(false);
	let dragActive = $state(false);
	let title = $state('');
	let isLoading = $state(false);
	let showSuccessPopup = $state(false);
	let showFileAnimation = $state(false);
	let activeTab = $state('mint');
	let selectedImageForModal = $state(null);

	const pinata = new PinataSDK({
		pinataJwt: env.PUBLIC_PINATA_JWT,
		pinataGateway: 'violet-urgent-booby-169.mypinata.cloud'
	});

	function handleDragEnter(e) {
		e.preventDefault();
		e.stopPropagation();
		dragActive = true;
	}

	function handleDragLeave(e) {
		e.preventDefault();
		e.stopPropagation();
		dragActive = false;
	}

	function handleDrop(e) {
		e.preventDefault();
		e.stopPropagation();
		dragActive = false;
		const files = e.dataTransfer.files;
		if (files.length) {
			handleFileSelect({ target: { files } });
		}
	}

	function handleFileSelect(event) {
		const file = event.target.files[0];
		if (file) {
			selectedFile = URL.createObjectURL(file);
			fileName = file.name;
			isFileAdded = true;
		}
	}

	async function handleValidate() {
		if (selectedFile && title) {
			isLoading = true;
			try {
				// Upload du fichier sur Pinata
				const file = new File([selectedFile], fileName, { type: selectedFile.type });
				const upload = await pinata.upload.file(file);
				console.log('Fichier uploadé sur Pinata:', upload);

				const contractData = {
					name: title,
					description: 'Secure file on Algorand',
					image: `https://gateway.pinata.cloud/ipfs/${upload.cid}`,
					properties: {
						date: new Date().toISOString()
					}
				};

				// Récupération de l'adresse du compte
				const accountAddress = $accountInformation.userWalletAddress;

				// Préparation des données à envoyer au backend
				const dataToSend = {
					account_address: accountAddress,
					contract_data: contractData
				};

				// Envoi de la requête POST au backend
				const response = await fetch('http://localhost:5000/create_nft', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json'
					},
					body: JSON.stringify(dataToSend)
				});

				if (!response.ok) {
					throw new Error(`Erreur HTTP ! statut : ${response.status}`);
				}

				const nftData = await response.json();

				// Ajout des NFTs reçus dans registeredFiles
				$registeredFiles.push(...nftData.nfts);
				activeTab = 'minted';
				showSuccessPopup = true;
				showFileAnimation = true;

				setTimeout(() => {
					showSuccessPopup = false;
					showFileAnimation = false;
					resetInputs();
				}, 3000);
			} catch (error) {
				console.error('Erreur lors du traitement :', error);
				alert('Une erreur est survenue. Veuillez réessayer.');
			} finally {
				isLoading = false;
			}
		} else {
			alert('Veuillez ajouter un fichier et entrer un titre.');
		}
	}

	function resetInputs() {
		selectedFile = null;
		fileName = '';
		isFileAdded = false;
		title = '';
	}

	function openImageModal(image) {
		if (image) {
			console.log('you just clicked with this image: ', image);
			selectedImageForModal = image;
		}
	}

	function closeImageModal() {
		selectedImageForModal = null;
	}
</script>

<div class="mx-auto w-full max-w-4xl rounded-xl bg-gray-900 p-6 shadow-2xl">
	<div class="mb-6 flex justify-center space-x-4">
		<button
			class="rounded-full px-6 py-2 text-lg font-semibold transition-all duration-300 ease-in-out {activeTab ===
			'mint'
				? 'bg-purple-600 text-white'
				: 'bg-gray-800 text-purple-400 hover:bg-gray-700'}"
			on:click={() => (activeTab = 'mint')}
		>
			💎 Mint Contract
		</button>
		<button
			class="rounded-full px-6 py-2 text-lg font-semibold transition-all duration-300 ease-in-out {activeTab ===
			'minted'
				? 'bg-blue-600 text-white'
				: 'bg-gray-800 text-blue-400 hover:bg-gray-700'}"
			on:click={() => (activeTab = 'minted')}
		>
			📃️ My Minted Contracts
		</button>
	</div>

	{#if activeTab === 'mint'}
		<div in:fade={{ duration: 300 }} class="rounded-lg bg-gray-800 p-6">
			<h2 class="mb-4 text-2xl font-bold text-purple-400">Mint New Contract</h2>
			<div
				id="dropzone"
				class="mb-6 rounded-lg border-2 border-dashed border-purple-400 p-8 text-center transition-all duration-300 ease-in-out"
				class:bg-purple-900={dragActive}
				class:bg-gray-700={!dragActive}
				on:dragenter={handleDragEnter}
				on:dragleave={handleDragLeave}
				on:drop={handleDrop}
				on:click={() => document.getElementById('fileInput').click()}
			>
				{#if isFileAdded}
					<div
						in:fade={{ duration: 150 }}
						class="flex items-center space-x-4 rounded-lg bg-gray-700 p-3"
					>
						<!-- <a href={selectedFile} target="_blank" rel="noopener noreferrer"> -->
						<img
							src={selectedFile}
							alt="Preview"
							class="h-10 w-10 rounded object-cover"
							on:click={() => selectedFile && openImageModal(selectedFile)}
						/>
						<button
							class="pl-1 text-white"
							on:click={() => selectedFile && openImageModal(selectedFile)}
						>
							{fileName}
						</button>
						<button on:click={resetInputs} class="text-red-500 hover:text-red-400">✖</button>
					</div>
				{:else}
					<p class="text-purple-300">Drag and drop your file here or click to select</p>
					<input
						type="file"
						id="fileInput"
						on:change={handleFileSelect}
						class="hidden"
						accept="image/*"
					/>
				{/if}
			</div>

			{#if isFileAdded}
				<div class="mb-6 rounded-lg bg-gray-700 p-4">
					<h3 class="text-xl font-semibold text-purple-400">Contract Details</h3>
					<input
						type="text"
						bind:value={title}
						placeholder="Title"
						class="mt-4 w-full rounded-md bg-gray-600 px-3 py-2 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
					/>
				</div>
				<button
					on:click={handleValidate}
					disabled={!selectedFile || !title || isLoading}
					class="w-full rounded-lg bg-gradient-to-r from-purple-500 to-indigo-600 px-4 py-3 text-white transition-all duration-300 ease-in-out hover:from-purple-600 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 focus:ring-offset-gray-900 disabled:opacity-50"
				>
					{#if isLoading}
						<span class="inline-block animate-spin">🔄</span>
					{:else}
						Mint Contract
					{/if}
				</button>
			{/if}
		</div>
	{:else if activeTab === 'minted'}
		<div in:fade={{ duration: 300 }} class="rounded-lg bg-gray-800 p-6">
			<h2 class="mb-4 text-2xl font-bold text-blue-400">My Minted Contracts</h2>
			{#each $registeredFiles as nft}
				<div class="mb-4 rounded-lg bg-gray-700 p-4">
					<h3 class="text-xl font-semibold text-white">{nft.title}</h3>
					<p class="text-gray-300">Asset ID: {nft.asset_id}</p>
					<p class="text-gray-300">Mint Date: {nft.mint_date}</p>
					<p class="text-gray-300">Mint Address: {nft.mint_address}</p>
					<a href={nft.metadata_url} target="_blank" class="text-blue-400 hover:underline"
						>Metadata URL</a
					><br />
					<a href={nft.explorer_url} target="_blank" class="text-blue-400 hover:underline"
						>Explorer URL</a
					>
				</div>
			{/each}
		</div>
	{/if}
</div>

{#if showSuccessPopup}
	<div
		in:fly={{ y: 50, duration: 500 }}
		out:fade={{ duration: 300 }}
		class="fixed bottom-4 right-4 rounded-lg bg-green-600 p-4 text-white shadow-lg"
	>
		Contract successfully minted!
	</div>
{/if}

<OpenImage selectedImage={selectedImageForModal} on:closeImage={closeImageModal} />
