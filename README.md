# 🦐 Social Scraper — OpenClaw Skill

An [OpenClaw](https://github.com/openclaw/openclaw) skill that enables AI agents to discover influencers and scrape social media posts across **Instagram**, **Threads**, and **Facebook**, with real-time **Notion** database integration.

## ✨ Features

| Capability | Description |
|-----------|-------------|
| 🔍 **Influencer Discovery** | Find KOLs/ambassadors from any brand's IG following list |
| 📸 **Instagram Scraping** | Scrape recent posts via IG private API (likes, comments, media type) |
| 🧵 **Threads Scraping** | Extract posts from Threads profiles via DOM scraping |
| 🔵 **Facebook Research** | Search FB pages + cross-reference from IG profiles |
| 📝 **Notion Integration** | Write scraped data to Notion databases in real-time |
| ⚡ **Edge-Write Pattern** | Write as you scrape — no data loss on interruptions |

## 📁 Skill Structure

```
social-scraper/
├── SKILL.md                          # Skill definition + workflow
├── scripts/
│   └── notion_writer.py              # Notion API writer (stdin JSON → Notion DB)
└── references/
    ├── instagram-api.md              # IG private API endpoints & rate limits
    ├── threads-scraping.md           # Threads DOM extraction guide
    └── facebook-notes.md             # FB strategy & limitations
```

## 🚀 Installation

### Option 1: Install from .skill file

```bash
openclaw skill install social-scraper.skill
```

### Option 2: Install from directory

Copy the skill folder to your OpenClaw skills directory:

```bash
cp -r social-scraper/ ~/.openclaw/skills/social-scraper/
```

### Option 3: Clone this repo

```bash
git clone https://github.com/mela0976/openclaw-skill-social-scraper.git
cp -r openclaw-skill-social-scraper/ ~/.openclaw/skills/social-scraper/
```

## 💬 Usage

Once installed, the skill triggers automatically when you ask your OpenClaw agent things like:

- *"Find the top 30 influencers followed by @brandname on IG"*
- *"Scrape recent posts from these Instagram accounts and save to Notion"*
- *"Check if these IG accounts also have Threads and scrape their posts"*
- *"Search Facebook for pages related to [keyword]"*

The agent will follow the workflow defined in `SKILL.md` and use the bundled scripts and references.

## 📖 How It Works

### Phase 1: Discovery

```
Brand's IG Account → Following List (GraphQL API)
    → Batch Query Follower Counts
    → Filter & Rank by Followers
    → Top N Influencers → Notion DB
```

### Phase 2: Instagram Post Scraping

```
For each account:
    → GET /api/v1/feed/user/{userId}/
    → Filter by date range (e.g. last 30 days)
    → Extract: text, likes, comments, media type, shortcode
    → Write to Notion immediately (edge-write)
```

### Phase 3: Threads Post Scraping

```
For each account:
    → Navigate to threads.com/@{handle}
    → Wait 2.5s for render
    → DOM extraction: [data-pressable-container] → time, text, code
    → Write to Notion immediately
```

### Phase 4: Facebook (Optional)

```
→ Cross-reference IG external_url for FB links
→ Search FB pages by keyword
→ Note: FB follower lists are not publicly accessible
```

## 🔧 Scripts

### `scripts/notion_writer.py`

Generic Notion database writer. Reads JSON from stdin, writes pages to a Notion database.

```bash
# Environment variables
export NOTION_API_KEY="ntn_xxxxx"
export NOTION_DB_ID="your-database-id"

# Pipe posts
echo '[
  {"h": "username", "code": "ABC123", "ts": 1771000000, "text": "Post content", "likes": 100, "comments": 5, "type": 2}
]' | python3 scripts/notion_writer.py --platform Instagram

# Options
#   --platform    Instagram | Threads | Facebook (default: Instagram)
#   --delay       Seconds between writes (default: 0.35)
#   --db          Override NOTION_DB_ID
#   --key         Override NOTION_API_KEY
```

**Post JSON format:**

| Field | Type | Description |
|-------|------|-------------|
| `h` | string | Account handle |
| `code` | string | Post shortcode (for URL construction) |
| `ts` | number | Unix timestamp (IG) |
| `time` | string | Date string `YYYY-MM-DD` (Threads) |
| `text` | string | Post caption/content |
| `likes` | number | Like count |
| `comments` | number | Comment count |
| `type` | number | Media type: 1=photo, 2=video, 8=carousel |

## 📚 References

| File | Contents |
|------|----------|
| [instagram-api.md](references/instagram-api.md) | All IG private API endpoints, required headers, rate limits, common errors |
| [threads-scraping.md](references/threads-scraping.md) | Full DOM extraction function, automation loop, page detection |
| [facebook-notes.md](references/facebook-notes.md) | What works/doesn't on FB, recommended strategy |

## ⚠️ Prerequisites

- **Browser session**: IG and Threads APIs require an active login session (cookies)
- **Notion integration**: Create at [notion.so/my-integrations](https://www.notion.so/my-integrations) and share target pages
- **Python 3.x**: For the Notion writer script
- **OpenClaw** (or compatible agent): For browser automation

## 🔒 Rate Limits & Best Practices

| Platform | Action | Delay | Batch Size |
|----------|--------|-------|------------|
| Instagram | Profile info | 300-400ms | 15-20 |
| Instagram | Feed posts | 500ms | 5 |
| Instagram | Following list | 500ms | 50/page |
| Threads | Page navigation | 2500ms | 1 |
| Notion | Write pages | 350ms | — |

## 📝 License

MIT

## 🔗 Related

- [social-scraper](https://github.com/mela0976/social-scraper) — Standalone version with full documentation
- [OpenClaw](https://github.com/openclaw/openclaw) — AI agent framework
- [ClaWHub](https://clawhub.com) — Discover more OpenClaw skills
