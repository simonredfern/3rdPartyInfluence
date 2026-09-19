<script>
	import { base } from '$app/paths';
	import links from '$lib/data/links.json';
	import nav from '$lib/data/nav.json';

	const socials = [
		['SoundCloud', links.soundcloud],
		['Bandcamp', links.bandcamp],
		['Instagram', links.instagram],
		['Facebook', links.facebook],
		['Twitch', links.twitch],
		['YouTube', links.youtube]
	];
</script>

<footer class="site-footer">
	<div class="site-footer__inner">
		<section>
			<h2>Pages</h2>
			<ul>
				{#each nav as item (item.slug)}
					<li><a href="{base}/{item.slug}">{item.title}</a></li>
				{/each}
			</ul>
		</section>

		<section>
			<h2>Socials + sound</h2>
			<ul>
				{#each socials as [label, href] (href)}
					<li><a {href} target="_blank" rel="noopener noreferrer">{label}</a></li>
				{/each}
			</ul>
		</section>

		<section>
			<h2>Bookings</h2>
			<p>
				DM us on <a href={links.instagram} target="_blank" rel="noopener noreferrer">Instagram</a>.
			</p>
			<p class="co2">Let's get CO2 down — a 12&nbsp;km drive creates 2&nbsp;kg of CO2.</p>
		</section>
	</div>

	<p class="site-footer__legal">
		3rd Party Influence · Live techno with Eurorack modular synthesizers · Berlin
	</p>
</footer>

<style>
	.site-footer {
		margin-top: 4rem;
		padding: 2.5rem 1rem 2rem;
		border-top: 1px solid var(--rule);
		background: var(--surface);
		font-size: 0.9rem;
	}

	.site-footer__inner {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(13rem, 1fr));
		gap: 2rem;
		max-width: var(--measure);
		margin: 0 auto;
	}

	h2 {
		margin: 0 0 0.6rem;
		font-size: 0.75rem;
		font-weight: 600;
		letter-spacing: 0.14em;
		text-transform: uppercase;
		color: var(--text-muted);
	}

	ul {
		margin: 0;
		padding: 0;
		list-style: none;
	}

	li {
		margin-bottom: 0.3rem;
	}

	p {
		margin: 0 0 0.6rem;
	}

	.co2 {
		color: var(--text-muted);
	}

	.site-footer__legal {
		max-width: var(--measure);
		margin: 2.5rem auto 0;
		padding-top: 1.25rem;
		border-top: 1px solid var(--rule);
		color: var(--text-muted);
		font-size: 0.8rem;
	}
</style>
