<script>
	import { onMount } from 'svelte';
	import { fade } from 'svelte/transition';
	import { PinataSDK } from 'pinata';

	let selectedFile = $state(null);
	let fileName = $state('');
	let isFileAdded = $state(false);
	let dragActive = $state(false);
	let title = $state('');
	let showModal = $state(false);
	let isLoading = $state(false);

	const pinata = new PinataSDK({
		pinataJwt: 'votre_token_jwt',
		pinataGateway: 'example-gateway.mypinata.cloud'
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

	function toggleModal() {
		showModal = !showModal;
	}

	async function handleValidate() {
		if (selectedFile && title) {
			isLoading = true;
			try {
				const file = new File([selectedFile], fileName, { type: selectedFile.type });
				const upload = await pinata.upload.file(file);
				console.log('Fichier téléversé sur Pinata :', upload);

				const contractData = {
					name: 'dog',
					description: 'doggy',
					image: `https://gateway.pinata.cloud/ipfs/${upload.cid}`,
					decimals: 0,
					unitName: 'DOG',
					image_integrity: `sha256-${upload.cid}`,
					image_mimetype: upload.mime_type,
					properties: {
						beauty: 100,
						love: 10
					}
				};
				console.log('Données du contrat prêtes pour validation :', contractData);
				alert('Données du contrat prêtes pour validation !');
			} catch (error) {
				console.error('Erreur lors du téléversement du fichier :', error);
				alert('Échec du téléversement du fichier. Veuillez réessayer.');
			} finally {
				isLoading = false;
			}
		} else {
			alert('Veuillez ajouter un fichier et entrer un titre.');
		}
	}

	onMount(() => {
		const dropzone = document.getElementById('dropzone');
		['dragenter', 'dragover', 'dragleave', 'drop'].forEach((eventName) => {
			dropzone.addEventListener(eventName, preventDefaults, false);
		});

		function preventDefaults(e) {
			e.preventDefault();
			e.stopPropagation();
		}
	});
</script>

<div class="mx-auto w-full max-w-2xl rounded-xl bg-gray-900 p-6 shadow-2xl">
	<h2 class="mb-6 text-center text-2xl font-bold text-blue-400">Web3 Asset Uploader</h2>

	<div class="mb-6 grid grid-cols-2 gap-4">
		<button
			class="w-full transform rounded-lg bg-gradient-to-r from-purple-600 to-blue-600 px-4 py-3 text-white shadow-lg transition duration-300 ease-in-out hover:scale-105 hover:from-purple-700 hover:to-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-opacity-50"
		>
			🗃️ Mes fichiers
		</button>

		<label
			class="w-full transform cursor-pointer rounded-lg bg-gradient-to-r from-green-500 to-teal-500 px-4 py-3 text-center text-white shadow-lg transition duration-300 ease-in-out hover:scale-105 hover:from-green-600 hover:to-teal-600"
		>
			<input
				type="file"
				on:change={handleFileSelect}
				disabled={isFileAdded}
				class="hidden"
				accept="image/*,video/*"
			/>
			➕ Ajouter un fichier
		</label>
	</div>

	<div
		id="dropzone"
		class="mb-6 rounded-lg border-2 border-dashed border-blue-400 p-8 text-center transition-all duration-300 ease-in-out"
		class:bg-blue-900={dragActive}
		class:bg-gray-800={!dragActive}
		on:dragenter={handleDragEnter}
		on:dragleave={handleDragLeave}
		on:drop={handleDrop}
	>
		{#if isFileAdded}
			<div
				in:fade={{ duration: 150 }}
				out:fade={{ duration: 150 }}
				class="flex items-center space-x-4 rounded-lg bg-gray-800 p-3"
			>
				<img
					in:fade={{ duration: 150 }}
					out:fade={{ duration: 150 }}
					src={selectedFile}
					alt="Aperçu"
					class="h-10 w-10 rounded object-cover"
				/>
				<span class="cursor-pointer text-blue-400 underline" on:click={toggleModal}>{fileName}</span
				>
				<button
					on:click={() => {
						selectedFile = null;
						fileName = '';
						isFileAdded = false;
					}}
					class="text-red-500 transition duration-200 hover:text-red-700">✖</button
				>
			</div>
		{:else}
			<p class="text-blue-300">
				Glissez-déposez votre fichier ici ou cliquez sur 'Ajouter un fichier'
			</p>
		{/if}
	</div>

	{#if isFileAdded}
		<div in:fade={{ duration: 150 }} class="mb-6 rounded-lg bg-gray-800 p-4">
			<h3 class="mb-4 text-xl font-semibold text-blue-400">Détails du contrat</h3>

			<div class="mb-4">
				<label for="title" class="mb-1 block text-sm font-medium text-gray-400">Titre</label>
				<input
					type="text"
					id="title"
					bind:value={title}
					class="w-full rounded-md border border-gray-600 bg-gray-700 px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
					placeholder="Entrez le titre du contrat"
				/>
			</div>
		</div>
	{/if}

	{#if showModal}
		<div
			class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-75 transition-opacity"
			on:click={toggleModal}
		>
			<img
				in:fade={{ duration: 150 }}
				out:fade={{ duration: 150 }}
				src={selectedFile}
				alt="Image agrandie"
				class="max-h-full max-w-full rounded-lg p-4"
			/>
		</div>
	{/if}

	<button
		on:click={handleValidate}
		disabled={!selectedFile || !title}
		class="w-full transform rounded-lg bg-gradient-to-r from-yellow-400 to-orange-500 px-4 py-3 text-white shadow-lg transition duration-300 ease-in-out hover:scale-105 hover:from-yellow-500 hover:to-orange-600 focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:ring-opacity-50 disabled:cursor-not-allowed disabled:opacity-50"
	>
		Mint
	</button>
</div>

<style>
	:global(body) {
		background-color: #111827;
		color: #e5e7eb;
	}
</style>
