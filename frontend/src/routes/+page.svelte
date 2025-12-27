<script lang="ts">
	import { onMount } from 'svelte';

	// Svelte 5 State Runes
	let items = $state<any[]>([]);
	let newItemName = $state('');
	let newItemDesc = $state('');
	let isLoading = $state(true);
	let error = $state<string | null>(null);

	async function fetchItems() {
		try {
			const res = await fetch('/api/v1/items');
			if (!res.ok) throw new Error('Failed to fetch items');
			items = await res.json();
		} catch (e: any) {
			error = e.message;
		} finally {
			isLoading = false;
		}
	}

	async function createItem(e: SubmitEvent) {
		e.preventDefault();
		if (!newItemName.trim()) return;

		const res = await fetch('/api/v1/items/', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({
				name: newItemName,
				description: newItemDesc || null
			})
		});

		if (res.ok) {
			newItemName = '';
			newItemDesc = '';
			await fetchItems(); // Refresh the list
		}
	}

	onMount(fetchItems);
</script>

<main>
	<h1>Menagerist Items</h1>

	<!-- Create Item Form -->
	<section class="card">
		<h2>Add New Item</h2>
		<form onsubmit={createItem}>
			<input type="text" bind:value={newItemName} placeholder="Item name..." required />
			<input type="text" bind:value={newItemDesc} placeholder="Description (optional)..." />
			<button type="submit">Create</button>
		</form>
	</section>

	<hr />

	<!-- Items List -->
	{#if isLoading}
		<p>Loading items...</p>
	{:else if error}
		<p class="error">{error}</p>
	{:else}
		<ul>
			{#each items as item (item.id)}
				<li>
					<strong>{item.name}</strong>
					{#if item.description}
						<span> - {item.description}</span>
					{/if}
					<br />
					<small class="id">{item.id}</small>
				</li>
			{:else}
				<li>No items found in the inventory.</li>
			{/each}
		</ul>
	{/if}
</main>

<style>
	main { font-family: system-ui, sans-serif; max-width: 600px; margin: 2rem auto; padding: 0 1rem; }
	.card { background: #f4f4f4; padding: 1rem; border-radius: 8px; margin-bottom: 2rem; }
	form { display: flex; flex-direction: column; gap: 0.5rem; }
	input, button { padding: 0.5rem; border-radius: 4px; border: 1px solid #ccc; }
	button { background: #ff3e00; color: white; border: none; cursor: pointer; font-weight: bold; }
	button:hover { background: #e63900; }
	ul { list-style: none; padding: 0; }
	li { padding: 1rem 0; border-bottom: 1px solid #eee; }
	.id { color: #888; font-size: 0.8rem; }
	.error { color: red; }
</style>
