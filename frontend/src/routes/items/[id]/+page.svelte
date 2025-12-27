<script lang="ts">
    import { page } from '$app/state'; // Svelte 5 way to access URL params
    import { onMount } from 'svelte';

    let item = $state<any>(null);
    let error = $state<string | null>(null);
    let isLoading = $state(true);

    // The ID comes from the directory name [id]
    const itemId = page.params.id;

    async function fetchItemDetails() {
        try {
            const res = await fetch(`/api/v1/items/${itemId}`);
            if (!res.ok) throw new Error('Item not found');
            item = await res.json();
        } catch (e: any) {
            error = e.message;
        } finally {
            isLoading = false;
        }
    }

    onMount(fetchItemDetails);
</script>

<main>
    <a href="/items">← Back to List</a>

    {#if isLoading}
        <p>Loading details...</p>
    {:else if error}
        <p class="error">{error}</p>
    {:else if item}
        <article>
            <h1>{item.name}</h1>
            <p class="desc">{item.description ?? 'No description provided.'}</p>
            <hr />
            <p class="id-tag">ID: <code>{item.id}</code></p>
        </article>
    {/if}
</main>

<style>
    main { font-family: system-ui, sans-serif; max-width: 600px; margin: 2rem auto; padding: 1rem; }
    .desc { font-size: 1.2rem; color: #444; }
    .id-tag { color: #888; font-size: 0.8rem; }
    .error { color: #ff3e00; font-weight: bold; }
    code { background: #eee; padding: 0.2rem 0.4rem; border-radius: 4px; }
</style>
