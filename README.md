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

chmod +x urltool.py
./urltool.py -h

###Option B — Install system-wide (recommended: /usr/local/bin)
From the directory containing urltool.py:

chmod +x urltool.py
sudo ln -sf "$(pwd)/urltool.py" /usr/local/bin/urltool
urltool -h
Option C — Copy to /usr/bin
bash
Copy code
chmod +x urltool.py
sudo cp -v urltool.py /usr/bin/urltool
urltool -h
Usage
Help
bash
Copy code
urltool -h
urltool enc -h
urltool dec -h
urltool url -h
Encode payloads
1) Standard query encoding (spaces → +)
bash
Copy code
urltool enc "' UNION SELECT @@version, NULL#"
Example output:

perl
Copy code
%27+UNION+SELECT+%40%40version%2C+NULL%23
2) Pretty mode (keeps @ and , readable)
bash
Copy code
urltool enc "' UNION SELECT @@version, NULL#" --pretty
Example output:

sql
Copy code
%27+UNION+SELECT+@@version,+NULL%23
✅ Use this when you need the leading quote ' to break out of a quoted SQL context.

3) WSA-style output (drops the leading encoded quote)
This converts a leading %27+ into a leading +.

bash
Copy code
urltool enc "' UNION SELECT @@version, NULL#" --pretty --wsaplus
Example output:

sql
Copy code
+UNION+SELECT+@@version,+NULL%23
⚠️ This removes the leading ', so don’t use it if the SQLi requires that quote to trigger.

4) Use %20 instead of + for spaces
bash
Copy code
urltool enc "' UNION SELECT @@version, NULL#" --percent20
5) Custom safe characters (override pretty)
Keep specific characters unencoded:

bash
Copy code
urltool enc "' UNION SELECT @@version, NULL#" --safe "@,()"
Decode payloads
1) Standard decode (treats + as space)
bash
Copy code
urltool dec "%27+UNION+SELECT+@@version,+NULL%23"
2) Decode without treating + as space
bash
Copy code
urltool dec "%27+UNION+SELECT+@@version,+NULL%23" --no-plus
Build full URLs
1) Build URL with encoded query parameter
bash
Copy code
urltool url "https://target.tld/filter" category "' UNION SELECT @@version, NULL#" --pretty
Example output:

sql
Copy code
https://target.tld/filter?category=%27+UNION+SELECT+@@version,+NULL%23
2) Build URL with WSA-style leading +
bash
Copy code
urltool url "https://target.tld/filter" category "' UNION SELECT @@version, NULL#" --pretty --wsaplus
stdin / piping
Encode from stdin
bash
Copy code
echo "' UNION SELECT @@version, NULL#" | urltool enc --pretty
Decode from stdin
bash
Copy code
echo "%27+UNION+SELECT+@@version,+NULL%23" | urltool dec
Typical workflows
✅ When you NEED the quote ' to trigger SQLi
Use pretty only:

bash
Copy code
urltool enc "' UNION SELECT @@version, NULL#" --pretty
✅ When you want “WSA example style” (starts with +UNION...)
Use pretty + wsaplus:

bash
Copy code
urltool enc "' UNION SELECT @@version, NULL#" --pretty --wsaplus
