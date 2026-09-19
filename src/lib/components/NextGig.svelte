<script>
	import { onMount } from 'svelte';
	import { splitGigs, formatGigDateLong } from '$lib/gigs.js';
	import SetTimes from '$lib/components/SetTimes.svelte';
	import GigTitle from '$lib/components/GigTitle.svelte';

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
			<time class="next-gig__when" datetime={next.date}>{formatGigDateLong(next.when)}</time><span
				class="next-gig__dash">&nbsp;—&nbsp;</span
			><GigTitle parts={next.parts} />
		</p>

		{#if next.note}
			<p class="next-gig__note">{next.note}</p>
		{/if}

		<SetTimes sets={next.sets ?? []} />
	</aside>
{/if}

<style>
	.next-gig {
		margin: 2.75rem 0;
		padding: 1.1rem 0 1.25rem;
		border-top: 1px solid var(--rule);
		border-bottom: 1px solid var(--rule);
	}

	.next-gig__label {
		margin: 0 0 0.5rem;
		font-size: 0.72rem;
		font-weight: 600;
		letter-spacing: 0.16em;
		text-transform: uppercase;
		color: var(--accent);
	}

	.next-gig__what {
		margin: 0;
		font-size: 1.35rem;
		font-weight: 700;
		line-height: 1.25;
		letter-spacing: -0.01em;
	}

	.next-gig__when {
		color: var(--text-muted);
		font-variant-numeric: tabular-nums;
	}

	.next-gig__dash {
		color: var(--text-muted);
	}

	.next-gig__note {
		margin: 0.5rem 0 0;
		color: var(--text-muted);
		font-size: 0.92rem;
		line-height: 1.55;
	}

</style>
