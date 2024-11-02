<script lang="ts">
	import { fade } from 'svelte/transition';
	import { onMount } from 'svelte';

	export let showModal = false;
	let ethAddress = '';

	onMount(() => {
		ethAddress = '0x' + Math.random().toString(16).substr(2, 40);
	});

	function closeModal() {
		showModal = false;
	}
</script>

{#if showModal}
	<div
		class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-90"
		transition:fade={{ duration: 150 }}
	>
		<div
			class="mx-4 max-w-md transform overflow-hidden rounded-lg bg-gradient-to-r from-purple-900 to-indigo-900 p-6 text-start shadow-2xl transition-all duration-300 hover:scale-105 hover:shadow-purple-500/50 sm:mx-auto"
		>
			<div class="flex items-center space-x-4">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					fill="none"
					viewBox="0 0 24 24"
					stroke-width="2"
					stroke="currentColor"
					class="h-8 w-8 text-green-400"
				>
					<path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
				</svg>
				<p class="text-lg font-bold text-green-400">Document enregistré avec succès !</p>
			</div>
			<div class="mt-4 space-y-3">
				<p class="text-sm font-medium text-purple-200 sm:text-base">
					Votre document est maintenant :
				</p>
				<ul class="list-inside list-disc space-y-2 text-sm text-purple-100">
					<li>Enregistré sur notre plateforme dans vos fichiers personnels</li>
					<li>Stocké de manière chiffrée sur la blockchain, accessible publiquement</li>
					<li>Déchiffré et lisible uniquement dans vos fichiers sur la plateforme</li>
				</ul>
			</div>
			<div class="mt-4 space-y-2">
				<p class="text-xs text-purple-300 sm:text-sm">Transaction Hash :</p>
				<p class="break-all font-mono text-xs text-purple-100 sm:text-sm">
					{ethAddress}
				</p>
			</div>
			<div class="mt-6 flex justify-between">
				<button
					on:click={closeModal}
					class="rounded bg-purple-700 px-4 py-2 text-sm font-semibold text-white transition-colors hover:bg-purple-600 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 focus:ring-offset-purple-900"
				>
					Fermer
				</button>
				<button
					class="rounded bg-green-500 px-4 py-2 text-sm font-semibold text-white transition-colors hover:bg-green-400 focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-offset-2 focus:ring-offset-purple-900"
				>
					Voir mes fichiers
				</button>
			</div>
		</div>
	</div>
{/if}
