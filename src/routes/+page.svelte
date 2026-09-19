<script>
	import Seo from '$lib/components/Seo.svelte';

	let { data } = $props();

	const Content = $derived(data.content);
</script>

<Seo title={data.meta.title} description={data.meta.description} />

<Content />
