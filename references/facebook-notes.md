# Facebook Notes

## What Works

1. **Page search** — `facebook.com/search/pages/?q={keyword}` returns public pages
2. **Page following list** — visible at `/{page}/following/`
3. **Cross-reference from IG** — check `external_url` in IG profiles for FB links

## What Doesn't Work

- Full follower list enumeration (hidden by FB)
- Graph API without admin access token
- `fetch()` from FB pages (requires full SPA navigation)
- Post commenter extraction (most pages have few comments)

## Best Strategy

1. Get `external_url` + `full_name` from IG web_profile_info
2. Filter for `facebook.com`, `shop.com`, brand-specific URLs
3. Search FB pages by relevant keywords
4. FB ecosystem is typically weaker than IG for influencer discovery

## Key URLs

- Page search: `facebook.com/search/pages/?q={query}`
- People search: `facebook.com/search/people/?q={query}`
- Followers: `facebook.com/{page}/followers/` (limited to mutual friends)
- Following: `facebook.com/{page}/following/`
