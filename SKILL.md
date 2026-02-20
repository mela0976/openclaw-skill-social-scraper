---
name: social-scraper
description: Discover and scrape social media accounts and posts from Instagram, Threads, and Facebook. Use when asked to find influencers, KOLs, or brand ambassadors from a brand's following list, scrape their recent posts, or write social media data to Notion. Covers IG private API (profile info, feed, following list), Threads DOM scraping, FB page search, and Notion database integration.
---

# Social Scraper

Scrape social media profiles and posts across Instagram, Threads, and Facebook, with real-time Notion database writing.

## Core Workflow

### Phase 1: Discovery (Instagram)

Find target accounts from a brand/official account's following list:

1. Get following list via GraphQL: `query_hash=d04b0a864b4b54837c0d870b0e77e076`
2. Batch-query follower counts via `/api/v1/users/web_profile_info/`
3. Filter out official/brand/media accounts
4. Rank by follower count, select top N

See [references/instagram-api.md](references/instagram-api.md) for all endpoints, headers, rate limits.

### Phase 2: Scrape Posts

#### Instagram

Use `/api/v1/feed/user/{userId}/` for recent posts. Returns `taken_at`, `like_count`, `comment_count`, `caption.text`, `media_type`, `code`.

**Media types:** 1=photo, 2=video, 8=carousel

#### Threads

Navigate to `https://www.threads.com/@{handle}`, wait 2.5s, extract from DOM:
- Post links: `a[href*="/post/"]`
- Container: `[data-pressable-container]`
- Timestamp: `time[datetime]`
- Text: longest `[dir=auto]` element in container

See [references/threads-scraping.md](references/threads-scraping.md) for full extraction code.

#### Facebook

Limited capability. Best approaches:
1. Cross-reference IG `external_url` for FB links
2. Search FB pages by keyword
3. Page follower lists are NOT publicly accessible

See [references/facebook-notes.md](references/facebook-notes.md) for details.

### Phase 3: Write to Notion

Use `scripts/notion_writer.py` to write posts. Supports stdin JSON piping.

```bash
NOTION_API_KEY=xxx NOTION_DB_ID=yyy \
  echo '[{...}]' | python3 scripts/notion_writer.py --platform Instagram
```

**Edge-write pattern:** Write after each account, not after all — prevents data loss.

## Key Rules

1. **All IG API calls must use browser fetch** — external HTTP gets 401
2. **Required IG headers:** `X-IG-App-ID: 936619743392459`, `X-Requested-With: XMLHttpRequest`
3. **Rate limits:** 300-400ms between profile queries, 500ms between feed queries, batch 15-20 accounts max
4. **Threads has no API** — DOM scraping only, one account per navigation
5. **Notion:** 0.35s delay between writes (~2.8 req/s)

## Notion DB Schema

### Account DB

| Property | Type | Purpose |
|----------|------|---------|
| 帳號名稱 | title | Display name |
| IG帳號 | rich_text | Handle |
| IG連結 | url | Profile URL |
| 粉絲數 | number | Follower count |
| 平台 | select | Platform |
| 備註 | rich_text | Notes |

### Post DB

| Property | Type | Purpose |
|----------|------|---------|
| 貼文內容 | title | Post text (100 chars) |
| 帳號 | select | @handle |
| 平台 | select | Instagram/Threads/Facebook |
| 發布日期 | date | Publish date |
| 貼文連結 | url | Direct link |
| 讚數 | number | Like count |
| 留言數 | number | Comment count |
| 類型 | select | 圖片/影片/輪播/文字 |
