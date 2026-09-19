<script>
	import { page } from '$app/state';

	let { title, description = '', image = '/favicon.png' } = $props();

	const SITE = '3rd Party Influence';
	const full = $derived(title && title !== 'Home' ? `${title} — ${SITE}` : `${SITE} — Live Techno with Eurorack Modular synthesizers`);
	const canonical = $derived(new URL(page.url.pathname, 'https://3pi.tv').href);
</script>

<svelte:head>
	<title>{full}</title>
	{#if description}<meta name="description" content={description} />{/if}
	<link rel="canonical" href={canonical} />

	<meta property="og:site_name" content={SITE} />
	<meta property="og:type" content="website" />
	<meta property="og:title" content={full} />
	<meta property="og:url" content={canonical} />
	{#if description}<meta property="og:description" content={description} />{/if}
	<meta property="og:image" content={new URL(image, 'https://3pi.tv').href} />

	<meta name="twitter:card" content="summary_large_image" />
	<meta name="twitter:title" content={full} />
	{#if description}<meta name="twitter:description" content={description} />{/if}
</svelte:head>
