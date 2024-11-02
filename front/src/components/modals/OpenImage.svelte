<script>
	export let selectedImage;
	import { fade, scale } from 'svelte/transition';

	function closeImage() {
		selectedImage = null;
	}
</script>

{#if selectedImage}
	<div
		transition:fade={{ duration: 300 }}
		class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-75 backdrop-blur-sm"
		on:click={closeImage}
	>
		<div
			transition:scale={{ duration: 300 }}
			class="relative mx-4 max-h-[90vh] w-full max-w-4xl overflow-hidden rounded-lg shadow-2xl"
			on:click|stopPropagation
		>
			<img
				src={selectedImage}
				alt="Zoomed image"
				class="h-full w-full bg-gray-900 object-contain"
			/>
			<button
				on:click={closeImage}
				class="absolute right-4 top-4 rounded-full bg-gray-800 bg-opacity-50 p-2 text-white transition-colors duration-200 hover:bg-opacity-75"
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					width="24"
					height="24"
					fill="none"
					stroke="currentColor"
				>
					<line x1="18" y1="6" x2="6" y2="18"></line>
					<line x1="6" y1="6" x2="18" y2="18"></line>
				</svg>
			</button>
		</div>
	</div>
{/if}
