<script lang="ts">
	import './layout.css';
    let { children } = $props();
    import { ModeWatcher } from "mode-watcher";
</script>

<ModeWatcher/>

{@render children()}
