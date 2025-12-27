<script lang="ts">
    import { page } from '$app/state';
    import { onMount } from 'svelte';
    import { ArrowLeft, Package, Info } from '@lucide/svelte';

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

<svelte:head>
    <title>{item ? item.name : 'Loading...'} | Menagerist</title>
</svelte:head>

<div class="max-w-2xl mx-auto space-y-6">
    <!-- Back Navigation -->
    <a href="/items" class="inline-flex items-center gap-2 text-sm font-medium text-muted-foreground hover:text-primary transition-colors">
        <ArrowLeft size={16} />
        Back to List
    </a>

    {#if isLoading}
        <div class="flex items-center gap-3 text-muted-foreground animate-pulse">
            <Package class="animate-bounce" />
            <span>Loading item details...</span>
        </div>
    {:else if error}
        <div class="p-4 rounded-lg bg-destructive/10 border border-destructive/20 text-destructive flex items-center gap-3">
            <Info size={20} />
            <p class="font-bold">{error}</p>
        </div>
    {:else if item}
        <article class="bg-card text-card-foreground rounded-xl border border-border p-8 shadow-sm">
            <div class="space-y-2 mb-6">
                <h1 class="text-4xl font-extrabold tracking-tight">{item.name}</h1>
                <p class="text-xl text-muted-foreground leading-relaxed">
                    {item.description ?? 'No description provided.'}
                </p>
            </div>

            <div class="pt-6 border-t border-border flex items-center justify-between">
                <div class="flex flex-col gap-1">
                    <span class="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Domain Identifier</span>
                    <code class="text-sm font-mono bg-muted px-2 py-1 rounded-md text-foreground">
                        {item.id}
                    </code>
                </div>

                <!-- Placeholder for future actions (Edit/Delete) -->
                <div class="flex gap-2">
                    <div class="w-2 h-2 rounded-full bg-primary animate-pulse"></div>
                    <span class="text-[10px] text-muted-foreground uppercase font-bold">Active Record</span>
                </div>
            </div>
        </article>
    {/if}
</div>
