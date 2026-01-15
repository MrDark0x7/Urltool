# urltool 🧰 — URL Query Encoder/Decoder (WSA-friendly)

A tiny CLI helper to **URL-encode / decode** payloads for query strings — built for quick copy/paste workflows in CTFs and Web Security Academy labs.

It supports:
- **Query encoding** (spaces → `+` by default)
- **Pretty mode** (keeps characters like `@` and `,` readable)
- **WSA-style output** (optional: converts leading `%27+` → `+`)
- **Decode** back to the original string
- **Build full URLs** with `param=value`
- Works with **args**, **stdin piping**, or **interactive prompt**

> Important note: `#` in a raw URL is a fragment and won’t be sent to the server.  
> Encoding it as `%23` ensures it **reaches the backend**.

---

## Install

### Option A — Run locally
```bash
chmod +x urltool.py
./urltool.py -h
```
###Option B — Install system-wide (recommended: /usr/local/bin)

From the directory containing urltool.py:
```
chmod +x urltool.py
sudo ln -sf "$(pwd)/urltool.py" /usr/local/bin/urltool
urltool -h
```
Option C — Copy to /usr/bin
```
chmod +x urltool.py
sudo cp -v urltool.py /usr/bin/urltool
urltool -h
```
Commands
Encode

Standard (quote is kept as %27):

urltool enc "' UNION SELECT @@version, NULL#"
# -> %27+UNION+SELECT+%40%40version%2C+NULL%23


Pretty (keeps @@ and , readable):

urltool enc "' UNION SELECT @@version, NULL#" --pretty
# -> %27+UNION+SELECT+@@version,+NULL%23


WSA-style (converts leading %27+ to +):

urltool enc "' UNION SELECT @@version, NULL#" --pretty --wsaplus
# -> +UNION+SELECT+@@version,+NULL%23


Use %20 for spaces instead of +:

urltool enc "' UNION SELECT @@version, NULL#" --percent20


Custom safe chars (override --pretty):

urltool enc "' UNION SELECT @@version, NULL#" --safe "@,()"

Decode
urltool dec "%27+UNION+SELECT+@@version,+NULL%23"


Don’t treat + as space:

urltool dec "%27+UNION+SELECT+@@version,+NULL%23" --no-plus

Build full URL
urltool url "https://target.tld/filter" category "' UNION SELECT @@version, NULL#" --pretty
# -> https://target.tld/filter?category=%27+UNION+SELECT+@@version,+NULL%23
