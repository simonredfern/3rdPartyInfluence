<script>
	/**
	 * A gig title assembled from parts, joined with commas. Any part may carry a url,
	 * so the links live in the title itself rather than in a separate row - "BMS59"
	 * links to Berlin Modular Society, "Pollen festival" to the RA event, and so on.
	 */
	let { parts = [] } = $props();
</script>

{#each parts as part, i (part.text)}{#if i > 0}<span class="sep">,</span>{/if}{#if part.url}<a
			href={part.url}
			target="_blank"
			rel="noopener noreferrer">{part.text}</a
		>{:else}{part.text}{/if}{/each}

<style>
	a {
		text-decoration-color: color-mix(in srgb, currentColor 35%, transparent);
		text-underline-offset: 0.2em;
	}

	a:hover {
		text-decoration-color: currentColor;
	}

	/* The gap lives in CSS: a trailing space inside the span gets collapsed away. */
	.sep {
		margin-right: 0.32em;
		color: var(--text-muted);
	}
</style>
