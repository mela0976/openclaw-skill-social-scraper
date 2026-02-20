# Instagram Private API Reference

## Authentication

All requests must be made via browser `fetch()` with an active login session.

```javascript
const HEADERS = {
  'X-IG-App-ID': '936619743392459',
  'X-Requested-With': 'XMLHttpRequest'
};
```

## Endpoints

### 1. Profile Info

```
GET /api/v1/users/web_profile_info/?username={handle}
```

Returns: `full_name`, `biography`, `edge_followed_by.count`, `edge_follow.count`, `id`, `external_url`, `is_verified`

**Note:** Media `edges` are empty — use feed endpoint for posts.

### 2. User Feed (Posts)

```
GET /api/v1/feed/user/{userId}/
```

Returns `items[]`:
- `taken_at` — unix timestamp
- `like_count`, `comment_count`
- `caption.text`
- `media_type` — 1=photo, 2=video, 8=carousel
- `code` — shortcode for URL: `instagram.com/p/{code}/`

### 3. Following List (GraphQL)

```
GET /graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076
    &variables={"id":"{userId}","first":50,"after":"{cursor}"}
```

Paginated. Returns `edge_follow.edges[].node`:
- `username`, `full_name`, `id`, `is_verified`
- Pagination: `page_info.end_cursor`, `page_info.has_next_page`

## Rate Limits

| Action | Delay | Batch Size |
|--------|-------|------------|
| Profile info | 300-400ms | 15-20 |
| Feed posts | 500ms | 5 |
| Following list | 500ms | 50/page |

Add 2s pause between batches. At ~50 accounts, browser may timeout.

## Common Errors

| Error | Fix |
|-------|-----|
| 401 | Use browser fetch, not external HTTP |
| 429 | Increase delays |
| Empty media edges | Use feed endpoint, not web_profile_info |
| `require_login` | Re-login in browser |
