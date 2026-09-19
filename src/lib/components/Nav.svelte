<script>
	import { base } from '$app/paths';
	import { page } from '$app/state';
	import nav from '$lib/data/nav.json';

	let open = $state(false);

	// page.url.pathname is not resolved while prerendering, so deriving anything from it
	// leaves the static HTML wrong until hydration. route.id and params are known at build
	// time, so the active item and the h1 are correct in the served HTML.
	const isHome = $derived(page.route.id === '/');
	const currentSlug = $derived(isHome ? '' : (page.params.path ?? null));
</script>

<header class="site-header">
	<div class="site-header__bar">
		<button
			class="nav-toggle"
			type="button"
			aria-expanded={open}
			aria-controls="site-nav"
			onclick={() => (open = !open)}
		>
			{open ? 'Close' : 'Menu'}
		</button>

		<nav id="site-nav" class="site-nav" class:site-nav--open={open} aria-label="Main">
			<ul>
				{#each nav as item (item.slug)}
					<li>
						<a
							href="{base}/{item.slug}"
							aria-current={item.slug === currentSlug ? 'page' : undefined}
							onclick={() => (open = false)}
						>
							{item.short}
						</a>
					</li>
				{/each}
			</ul>
		</nav>
	</div>

	<a class="masthead" href="{base}/" onclick={() => (open = false)}>
		<img
			class="masthead__mark"
			src="{base}/brand.png"
			alt=""
			width="900"
			height="629"
			fetchpriority="high"
		/>
		{#if isHome}
			<h1 class="masthead__title">/// 3rd Party Influence ///</h1>
		{:else}
			<span class="masthead__title">/// 3rd Party Influence ///</span>
		{/if}
	</a>
</header>

<style>
	.site-header {
		border-bottom: 1px solid var(--rule);
	}

	/* Only the menu bar sticks; the masthead scrolls away with the page. */
	.site-header__bar {
		position: sticky;
		top: 0;
		z-index: 10;
		background: color-mix(in srgb, var(--bg) 92%, transparent);
		backdrop-filter: blur(8px);
		border-bottom: 1px solid var(--rule);
	}

	.site-nav ul {
		display: flex;
		flex-wrap: wrap;
		justify-content: center;
		gap: 0.15rem 1.35rem;
		max-width: var(--measure);
		margin: 0 auto;
		padding: 0.7rem 1rem;
		list-style: none;
	}

	.site-nav a {
		color: var(--text-muted);
		font-size: 0.85rem;
		text-decoration: none;
	}

	.site-nav a:hover,
	.site-nav a[aria-current='page'] {
		color: var(--accent);
	}

	.site-nav a[aria-current='page'] {
		font-weight: 600;
	}

	.nav-toggle {
		display: none;
		margin: 0.55rem 1rem;
		padding: 0.35rem 0.7rem;
		border: 1px solid var(--rule);
		border-radius: 3px;
		background: var(--surface);
		color: var(--text);
		font: inherit;
		font-size: 0.85rem;
		cursor: pointer;
	}

	.masthead {
		display: flex;
		align-items: center;
		gap: clamp(0.75rem, 2.5vw, 1.25rem);
		max-width: var(--measure);
		margin: 0 auto;
		padding: 1.5rem 1rem 1.25rem;
		color: var(--text);
		text-decoration: none;
	}

	.masthead__mark {
		flex: none;
		width: clamp(78px, 15vw, 118px);
		height: auto;
	}

	.masthead__title {
		margin: 0;
		font-size: clamp(1.3rem, 4.4vw, 2.1rem);
		font-weight: 700;
		line-height: 1.15;
		letter-spacing: -0.02em;
		text-wrap: balance;
	}

	.masthead:hover .masthead__title {
		color: var(--accent);
	}

	.masthead:focus-visible {
		outline: 2px solid var(--accent);
		outline-offset: 4px;
		border-radius: 4px;
	}

	@media (max-width: 40rem) {
		.nav-toggle {
			display: block;
			margin-left: auto;
		}

		.site-nav {
			display: none;
		}

		.site-nav--open {
			display: block;
		}

		.site-nav ul {
			flex-direction: column;
			justify-content: flex-start;
			gap: 0;
			padding: 0 1rem 0.75rem;
		}

		.site-nav li {
			border-top: 1px solid var(--rule);
		}

		.site-nav a {
			display: block;
			padding: 0.6rem 0;
			font-size: 0.95rem;
		}

		.masthead {
			padding: 1.15rem 1rem 1rem;
		}
	}
</style>
