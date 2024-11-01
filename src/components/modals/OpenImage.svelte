<script>
    export let selectedImage
</script>

{#if selectedImage}
  <div
    transition:fade={{ duration: 300 }}
    class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-75 backdrop-blur-sm"
    on:click={closeImage}
  >
    <div
      transition:scale={{ duration: 300, easing: quintOut }}
      class="relative max-w-4xl max-h-[90vh] w-full mx-4 overflow-hidden rounded-lg shadow-2xl"
      on:click|stopPropagation
    >
      <img
        src={selectedImage}
        alt="Zoomed image"
        class="w-full h-full object-contain bg-gray-900"
      />
      <button
        on:click={closeImage}
        class="absolute top-4 right-4 p-2 rounded-full bg-gray-800 bg-opacity-50 text-white hover:bg-opacity-75 transition-colors duration-200"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
    </div>
  </div>
{/if}