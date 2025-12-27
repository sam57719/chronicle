<script lang="ts">
	let { children } = $props(); // Svelte 5 snippet syntax
</script>

<nav style="padding: 1rem; border-bottom: 1px solid #ccc; display: flex; gap: 1rem;">
	<a href="/">Home</a>
	<a href="/items">Items</a>
</nav>

{@render children()}
