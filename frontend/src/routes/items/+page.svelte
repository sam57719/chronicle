<script lang="ts">
    import { onMount } from 'svelte';

    let items = $state<any[]>([]);
    let isLoading = $state(true);

    async function loadItems() {
        const res = await fetch('/api/v1/items');
        if (res.ok) items = await res.json();
        isLoading = false;
    }

    onMount(loadItems);
</script>

<svelte:head>
    <title>Inventory ({items.length}) | Menagerist</title>
</svelte:head>

<main>
    <a href="/">← Back Home</a>
    <h1>Inventory</h1>

    {#if isLoading}
        <p>Fetching from backend...</p>
    {:else}
        <ul>
            {#each items as item (item.id)}
                <li>
                    <a href="/items/{item.id}" class="item-link">
                        <strong>{item.name}</strong>
                        {#if item.description}
                            <span> - {item.description}</span>
                        {/if}
                        <br />
                        <small class="id">{item.id}</small>
                    </a>
                </li>
            {:else}
                <li>No items found in the inventory.</li>
            {/each}
        </ul>
    {/if}
</main>

<style>
    main { font-family: system-ui, sans-serif; max-width: 600px; margin: 2rem auto; }
    ul { list-style: none; padding: 0; }
    li { padding: 0.5rem; border-bottom: 1px solid #eee; }
    .item-link {
        text-decoration: none;
        color: inherit;
        display: block;
        padding: 0.5rem;
        transition: background 0.2s;
        border-radius: 4px;
    }

    .item-link:hover {
        background: #f0f0f0;
    }

    .id {
        color: #888;
        font-size: 0.8rem;
    }
</style>
