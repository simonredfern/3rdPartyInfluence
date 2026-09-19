<script>
	import { onMount } from 'svelte';
	import { splitGigs, formatGigDate } from '$lib/gigs.js';
	import SetTimes from '$lib/components/SetTimes.svelte';
	import GigTitle from '$lib/components/GigTitle.svelte';

	let { show = 'past' } = $props();

	let now = $state(new Date());
	const split = $derived(splitGigs(now));
	const list = $derived(show === 'upcoming' ? split.upcoming : split.past);

	onMount(() => {
		now = new Date();
	});
</script>

{#if list.length}
	<ul class="gigs">
		{#each list as gig (gig.date)}
			<li class="gig">
				<time class="gig__date" datetime={gig.date}>{formatGigDate(gig.when)}</time>
				<div class="gig__body">
					<span class="gig__what"><GigTitle parts={gig.parts} /></span>
					{#if gig.note}<span class="gig__note">{gig.note}</span>{/if}
					<SetTimes sets={gig.sets ?? []} />
				</div>
			</li>
		{/each}
	</ul>
{:else}
	<p>Nothing listed yet.</p>
{/if}

<style>
	.gigs {
		margin: 2rem 0;
		padding: 0;
		list-style: none;
	}

	.gig {
		display: grid;
		grid-template-columns: 11rem 1fr;
		gap: 0 1.5rem;
		padding: 1rem 0;
		border-top: 1px solid var(--rule);
	}

	.gig:last-child {
		border-bottom: 1px solid var(--rule);
	}

	.gig__date {
		color: var(--text-muted);
		font-variant-numeric: tabular-nums;
		font-size: 0.9rem;
		padding-top: 0.15rem;
	}

	.gig__what {
		display: block;
		font-weight: 600;
	}

	.gig__note {
		display: block;
		margin-top: 0.2rem;
		color: var(--text-muted);
		font-size: 0.9rem;
	}


	@media (max-width: 34rem) {
		.gig {
			grid-template-columns: 1fr;
			gap: 0.3rem;
		}
	}
</style>
