<script>
	import { fade } from 'svelte/transition';
	import { count } from '$lib/writable';
	let email = '';
	let password = '';

	function handleLogin(event) {
		event.preventDefault();
		count.set(1);
		console.log('Attempting login with:', { email, password });
		alert('Login simulated! Welcome to the decentralized world.');
	}
</script>

<div class="flex min-h-screen items-center justify-center p-4" in:fade={{ duration: 150 }}>
	<div class="w-full max-w-md">
		<div
			class="relative overflow-hidden rounded-2xl bg-black bg-opacity-50 p-8 shadow-2xl backdrop-blur-xl"
		>
			<div class="bg-grid-white/[0.05] absolute inset-0 bg-[size:20px_20px]"></div>
			<div class="rotating-border"></div>
			<div class="relative z-10">
				<h1 class="mb-6 text-center text-3xl font-bold text-white">Enter the Blockspace</h1>
				<form on:submit|preventDefault={handleLogin} class="space-y-6">
					<div class="space-y-2">
						<label for="email" class="text-sm font-medium text-gray-300">Email</label>
						<input
							id="email"
							type="email"
							bind:value={email}
							placeholder="name@example.com"
							required
							class="w-full rounded-lg border border-gray-600 bg-gray-700 bg-opacity-50 px-4 py-3 text-white placeholder-gray-400 focus:border-blue-400 focus:outline-none focus:ring-2 focus:ring-blue-400"
						/>
					</div>
					<div class="space-y-2">
						<label for="password" class="text-sm font-medium text-gray-300">Password</label>
						<input
							id="password"
							type="password"
							bind:value={password}
							placeholder="••••••••"
							required
							class="w-full rounded-lg border border-gray-600 bg-gray-700 bg-opacity-50 px-4 py-3 text-white placeholder-gray-400 focus:border-blue-400 focus:outline-none focus:ring-2 focus:ring-blue-400"
						/>
					</div>
					<button
						type="submit"
						class="w-full rounded-lg bg-gradient-to-r from-blue-500 to-purple-600 px-4 py-3 font-bold text-white transition duration-300 ease-in-out hover:from-blue-600 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 focus:ring-offset-gray-900"
					>
						Connect to Blockspace
					</button>
				</form>
				<p class="mt-6 text-center text-sm text-gray-400">
					New to Blockspace? <a href="#" class="font-medium text-blue-400 hover:text-blue-300"
						>Create an account</a
					>
				</p>
			</div>
		</div>
	</div>
</div>
