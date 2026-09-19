<script>
	/** Set times for one gig: when we are on, as what, and in which room. */
	let { sets = [] } = $props();
</script>

{#if sets.length}
	<ul class="sets">
		{#each sets as set (set.time + set.what)}
			<li class="set">
				<span class="set__time">{set.time}</span>
				<span class="set__what">
					{#if set.url}
						<a href={set.url} target="_blank" rel="noopener noreferrer">{set.what}</a>
					{:else}{set.what}{/if}
					{#if set.who}<span class="set__who">{set.who}</span>{/if}
				</span>
				{#if set.where}<span class="set__where">{set.where}</span>{/if}
			</li>
		{/each}
	</ul>
{/if}

<style>
	.sets {
		margin: 0.75rem 0 0;
		padding: 0;
		list-style: none;
		font-size: 0.92rem;
	}

	.set {
		display: grid;
		grid-template-columns: 4.2rem 1fr auto;
		gap: 0.15rem 1rem;
		padding: 0.3rem 0;
		align-items: baseline;
	}

	.set + .set {
		border-top: 1px dotted var(--rule);
	}

	.set__time {
		color: var(--text);
		font-variant-numeric: tabular-nums;
		font-weight: 600;
	}

	.set__what {
		min-width: 0;
	}

	.set__what a {
		text-decoration-color: color-mix(in srgb, currentColor 35%, transparent);
		text-underline-offset: 0.2em;
	}

	.set__what a:hover {
		text-decoration-color: currentColor;
	}

	.set__who {
		display: block;
		color: var(--text-muted);
		font-size: 0.86rem;
	}

	.set__where {
		color: var(--text-muted);
		font-size: 0.86rem;
		text-align: right;
	}

	@media (max-width: 30rem) {
		.set {
			grid-template-columns: 3.6rem 1fr;
		}

		.set__where {
			grid-column: 2;
			text-align: left;
		}
	}
</style>
