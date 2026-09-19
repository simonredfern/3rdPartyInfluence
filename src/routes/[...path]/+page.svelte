<script>
	import Seo from '$lib/components/Seo.svelte';
	import Breadcrumb from '$lib/components/Breadcrumb.svelte';

	let { data } = $props();

	const Content = $derived(data.content);
	const title = $derived(data.meta.title ?? data.path);
</script>

<Seo {title} description={data.meta.description} />

<Breadcrumb path={data.path} />

<h1>{title}</h1>

<Content />
