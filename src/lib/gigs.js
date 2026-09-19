import gigs from '$lib/data/gigs.json';

/**
 * Gigs are split relative to `now`. At build time that is the build date, so the
 * browser re-checks after hydration - otherwise a gig would stay "upcoming" until
 * the next deploy. Schedule a periodic rebuild if you want the HTML itself fresh.
 */
export function splitGigs(now = new Date()) {
	const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
	const parsed = gigs
		.map((g) => ({ ...g, when: new Date(`${g.date}T00:00:00`) }))
		.filter((g) => !Number.isNaN(g.when.valueOf()));

	return {
		upcoming: parsed.filter((g) => g.when >= today).sort((a, b) => a.when - b.when),
		past: parsed.filter((g) => g.when < today).sort((a, b) => b.when - a.when)
	};
}

export function formatGigDate(d) {
	return d.toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' });
}

/** With the weekday - worth the extra words for a gig that has not happened yet. */
export function formatGigDateLong(d) {
	return d.toLocaleDateString('en-GB', {
		weekday: 'long',
		day: 'numeric',
		month: 'long',
		year: 'numeric'
	});
}
