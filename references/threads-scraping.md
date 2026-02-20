# Threads DOM Scraping Reference

## Method

No API. Navigate to profile → extract from rendered DOM.

## Extraction Function

```javascript
function extractPosts(daysBack = 30) {
  const cutoff = new Date(Date.now() - daysBack * 86400000);
  const handle = location.pathname.match(/@([^/]+)/)?.[1] || '';
  const posts = [];

  document.querySelectorAll('a[href*="/post/"]').forEach(a => {
    const c = a.closest('[data-pressable-container]');
    if (!c) return;
    const t = c.querySelector('time');
    const dt = t?.getAttribute('datetime');
    if (!dt || new Date(dt) < cutoff) return;
    const code = a.href.match(/\/post\/([^/]+)/)?.[1];
    let text = '';
    c.querySelectorAll('[dir=auto]').forEach(x => {
      const s = x.textContent.trim();
      if (s.length > text.length && s.length < 500) text = s;
    });
    if (code && !posts.find(p => p.code === code))
      posts.push({ h: handle, code, time: dt.substring(0,10), text: text.substring(0,200), likes: 0, comments: 0 });
  });

  return { handle, count: posts.length, posts };
}
```

## Automation Loop

For each account:
1. `navigate` to `https://www.threads.com/@{handle}`
2. `wait` 2500ms
3. `evaluate` extractPosts()
4. Write results to Notion immediately
5. Next account

**Cannot navigate inside evaluate** — context is destroyed on navigation.

## Page Not Found Detection

```javascript
const notFound = document.title.includes('Page Not Found');
```

## URL Format

```
https://www.threads.com/@{handle}/post/{code}
```

## Limitations

- Like/comment counts not visible on profile view
- Only ~5-10 initial posts loaded (no infinite scroll support)
- Must be logged in (IG SSO)
