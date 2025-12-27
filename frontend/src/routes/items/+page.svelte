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
                <li class="border-b last:border-0">
                    <a href="/items/{item.id}" class="block p-4 no-underline text-inherit transition-colors hover:bg-muted/50 rounded-lg">
                        <strong class="text-lg">{item.name}</strong>
                        {#if item.description}
                            <span class="text-muted-foreground"> - {item.description}</span>
                        {/if}
                        <br />
                        <small class="text-xs text-muted-foreground font-mono">{item.id}</small>
                    </a>
                </li>
            {:else}
                <li>No items found in the inventory.</li>
            {/each}
        </ul>
    {/if}
</main>
