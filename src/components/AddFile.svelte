<script>
	import { Spinner } from 'flowbite-svelte';
	import SuccessMint from './modals/SuccessMint.svelte';
	import { fade } from 'svelte/transition';
	import { PinataSDK } from 'pinata';
	import { env } from '$env/dynamic/public';

	let selectedFile = $state(null);
	let fileName = $state('');
	let isFileAdded = $state(false);
	let dragActive = $state(false);
	let title = $state('');
	let isLoading = $state(false);
	let showSuccessPopup = $state(false);
	let showFileAnimation = $state(false);

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
				const file = new File([selectedFile], fileName, { type: selectedFile.type });
				const upload = await pinata.upload.file(file);
				console.log('Fichier téléversé sur Pinata :', upload);

				const contractData = {
					name: title,
					description: 'Fichier sécurisé sur Algorand',
					image: `https://gateway.pinata.cloud/ipfs/${upload.cid}`,
					properties: {
						date: new Date().toISOString()
					}
				};

				// Simulation d'enregistrement sur la blockchain
				await new Promise((resolve) => setTimeout(resolve, 2000));

				showSuccessPopup = true;
				showFileAnimation = true;

				setTimeout(() => {
					showSuccessPopup = false;
					showFileAnimation = false;
					resetInputs();
				}, 3000);
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

	function resetInputs() {
		selectedFile = null;
		fileName = '';
		isFileAdded = false;
		title = '';
	}
</script>

<div class="mx-auto w-full max-w-2xl rounded-xl bg-gray-900 p-6 shadow-2xl">
	<h2 class="mb-6 text-center text-2xl font-bold text-blue-400">Mint your contract</h2>

	<div class="mb-6 grid grid-cols-2 gap-4">
		<button
			class="w-full rounded-lg bg-gradient-to-r from-purple-600 to-blue-600 px-4 py-3 text-white shadow-lg"
		>
			🗃️ Mes fichiers
		</button>
		<label
			class="w-full cursor-pointer rounded-lg bg-gradient-to-r from-green-500 to-teal-500 px-4 py-3 text-center text-white shadow-lg"
		>
			<input
				type="file"
				onchange={handleFileSelect}
				disabled={isFileAdded}
				class="hidden"
				accept="image/*"
			/>
			➕ Ajouter un fichier
		</label>
	</div>

	<div
		id="dropzone"
		class="mb-6 rounded-lg border-2 border-dashed border-blue-400 p-8 text-center"
		class:bg-blue-900={dragActive}
		class:bg-gray-800={!dragActive}
		ondragenter={handleDragEnter}
		ondragleave={handleDragLeave}
		ondrop={handleDrop}
	>
		{#if isFileAdded}
			<div in:fade={{ duration: 150 }} class="flex items-center space-x-4 bg-gray-800 p-3">
				<a href={selectedFile} target="_blank">
					<img src={selectedFile} alt="Aperçu" class="h-10 w-10 rounded object-cover" />
				</a>
				<a href={selectedFile} target="_blank" class="text-blue-400 underline">{fileName}</a>
				<button onclick={resetInputs} class="text-red-500">✖</button>
			</div>
		{:else}
			<p class="text-blue-300">
				Glissez-déposez votre fichier ici ou cliquez sur 'Ajouter un fichier'
			</p>
		{/if}
	</div>

	{#if isFileAdded}
		<div class="mb-6 bg-gray-800 p-4">
			<h3 class="text-xl font-semibold text-blue-400">Détails du contrat</h3>
			<input
				type="text"
				bind:value={title}
				placeholder="Titre"
				class="mt-4 w-full rounded-md bg-gray-700 px-3 py-2 text-white"
			/>
		</div>
	{/if}

	<button
		onclick={handleValidate}
		disabled={!selectedFile || !title}
		class="w-full rounded-lg bg-gradient-to-r from-yellow-400 to-orange-500 px-4 py-3 text-white"
	>
		{#if isLoading}
			<Spinner size={4} />
		{:else}
			Enregistrer sur la blockchain
		{/if}
	</button>

	<SuccessMint showModal={showSuccessPopup} />
</div>
