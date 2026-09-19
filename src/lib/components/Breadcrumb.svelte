<script>
	import { base } from '$app/paths';
	import pages from '$lib/data/pages.json';

	let { path } = $props();

	/** Ancestor pages, so any nested page links back to its parent. */
	const trail = $derived.by(() => {
		const parts = path.split('/').filter(Boolean);
		const out = [];
		for (let i = 0; i < parts.length - 1; i++) {
			const p = parts.slice(0, i + 1).join('/');
			const found = pages.find((x) => x.path === p);
			if (found) out.push(found);
		}
		return out;
	});
</script>

<nav class="crumbs" aria-label="Breadcrumb">
	<a href="{base}/">Home</a>
	{#each trail as crumb (crumb.path)}
		<span aria-hidden="true">/</span>
		<a href="{base}/{crumb.path}">{crumb.title}</a>
	{/each}
</nav>

<style>
	.crumbs {
		margin-bottom: 1.25rem;
		font-size: 0.85rem;
		color: var(--text-muted);
	}

	.crumbs a {
		color: var(--text-muted);
		text-decoration: none;
	}

	.crumbs a:hover {
		color: var(--accent);
		text-decoration: underline;
	}

	.crumbs span {
		margin: 0 0.4rem;
		opacity: 0.6;
	}
</style>
