<script>
	import { count } from '$lib/writable';
	let email = '';
	let password = '';

	function handleLogin() {
		count.set(1);
		console.log('Tentative de connexion avec:', { email, password });
		alert('Connexion simulée !');
	}
</script>

<div class="flex h-screen w-screen items-center justify-center p-4">
	<div class="w-full max-w-md">
		<div class="rounded-lg bg-white bg-opacity-10 p-8 shadow-lg backdrop-blur-lg backdrop-filter">
			<h1 class="mb-8 text-center text-3xl font-bold text-white">Connexion</h1>
			<form on:submit|preventDefault={handleLogin} class="space-y-6">
				<div>
					<input
						type="email"
						bind:value={email}
						placeholder="Adresse e-mail"
						required
						class="w-full rounded-lg border border-transparent bg-white bg-opacity-20 px-4 py-3 text-white placeholder-gray-300 focus:border-white focus:bg-opacity-30 focus:outline-none"
					/>
				</div>
				<div>
					<input
						type="password"
						bind:value={password}
						placeholder="Mot de passe"
						required
						class="w-full rounded-lg border border-transparent bg-white bg-opacity-20 px-4 py-3 text-white placeholder-gray-300 focus:border-white focus:bg-opacity-30 focus:outline-none"
					/>
				</div>
				<button
					type="submit"
					class="w-full rounded-lg bg-purple-700 px-4 py-3 font-bold text-white transition duration-300 ease-in-out hover:bg-purple-600"
				>
					Se connecter
				</button>
			</form>
		</div>
	</div>
</div>
