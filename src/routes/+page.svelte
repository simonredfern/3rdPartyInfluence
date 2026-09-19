<script>
	import Seo from '$lib/components/Seo.svelte';

	let { data } = $props();

	const Content = $derived(data.content);
</script>

<Seo title={data.meta.title} description={data.meta.description} />

<h1 class="visually-hidden">3rd Party Influence</h1>

<Content />

<style>
	.visually-hidden {
		position: absolute;
		width: 1px;
		height: 1px;
		margin: -1px;
		padding: 0;
		overflow: hidden;
		clip: rect(0 0 0 0);
		white-space: nowrap;
		border: 0;
	}
</style>
