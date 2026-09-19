<script>
	import { onMount } from 'svelte';
	import { splitGigs, formatGigDate, gigTitle } from '$lib/gigs.js';

	let now = $state(new Date());
	const split = $derived(splitGigs(now));
	const next = $derived(split.upcoming[0]);

	// The prerendered HTML is stamped with the build date; correct it in the browser.
	onMount(() => {
		now = new Date();
	});
</script>

{#if next}
	<aside class="next-gig">
		<h2 class="next-gig__label">Next gig</h2>
		<p class="next-gig__what">
			{#if next.url}
				<a href={next.url} target="_blank" rel="noopener noreferrer">{gigTitle(next)}</a>
			{:else}{gigTitle(next)}{/if}
		</p>
		<p class="next-gig__when">
			<time datetime={next.date}>{formatGigDate(next.when)}</time>
			{#if next.note}<span class="next-gig__note">— {next.note}</span>{/if}
		</p>
	</aside>
{/if}

<style>
	.next-gig {
		margin: 2.5rem 0;
		padding: 1.25rem 1.5rem;
		border-left: 3px solid var(--accent);
		background: var(--surface);
		border-radius: 0 2px 2px 0;
	}

	.next-gig__label {
		margin: 0 0 0.35rem;
		font-size: 0.75rem;
		font-weight: 600;
		letter-spacing: 0.14em;
		text-transform: uppercase;
		color: var(--accent);
	}

	.next-gig__what {
		margin: 0;
		font-size: 1.3rem;
		font-weight: 600;
		line-height: 1.3;
	}

	.next-gig__when {
		margin: 0.35rem 0 0;
		color: var(--text-muted);
	}

	.next-gig__note {
		opacity: 0.85;
	}
</style>
