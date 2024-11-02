<script>
	import Perrawallet from './../components/Perrawallet.svelte';
	import SignIn from './../components/SignIn.svelte';
	import { count } from '$lib/writable';
</script>

<div class="min-h-screen bg-[url('https://app.1inch.io/assets/splash-screen/background-new.png')]">
	<img
		class="absolute bottom-10 left-10 h-10 w-10 transition duration-200 hover:rotate-180"
		src="/src/lib/img/yellow_background.png"
		alt=""
	/>
	{#if $count === 0}
		<SignIn />
	{:else}
		<Perrawallet />
	{/if}
</div>
