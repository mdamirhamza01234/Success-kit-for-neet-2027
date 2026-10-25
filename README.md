# Success Kit - Offline Android App

PW NEET Success Kit 2026-27 ke 5 tests ka app. Repo par push karte hi GitHub APK khud bana deta hai.
Papers, solutions aur mock tests APK ke andar bundle hote hain, isliye bina internet ke chalte hain.

## Kya milta hai

- Home par 1 se 5 tak har test ka card: **Paper**, **Solutions**, **Mock Test**.
- PDF viewer: zoom, search, bookmarks, notes, highlight/pen, night mode, read aloud, flashcards.
- **SK AI** chatbot, do jagah: home ka *Ask AI* aur har PDF page ka sparkle button.
  - Online: **Gemini** (naya model pehle, apne aap fallback). Offline: phone par chalne wala **Gemma 3 1B**.
  - Dono ke jawab mein **LaTeX math** (KaTeX) aur chemistry (`\ce{}`) proper dikhta hai, bina internet ke bhi.
  - PDF viewer mein page ki photo Gemini ko jaati hai (diagram / options samajhne ke liye). Photo bhejne ka option home chat mein bhi hai.
- Mock test submit karte hi result **Test Records** mein save: score, subject-wise marks, har question ka jawab, time.

## files/ folder ke naam (build script yahi pehchanti hai)

| File | Naam |
|---|---|
| Question paper | `01_NEET Success Kit.pdf` |
| Solutions | `01S_NEET Success Kit.pdf` (number ke baad **S**) |
| Mock test | `01_NEET Success Kit.html` |

Number sabse pehle likho (01, 02, ...). Naam ka baaki hissa kuch bhi ho sakta hai.
Build log mein dikhta hai ki kis test ki kaun si file kahan gayi aur kya abhi baaki hai.

Naya test (6, 7, ...) jodne ke liye: files `files/` mein daalo aur `www/index.html` mein `TOTAL_TESTS` badha do.

## APK banana

1. Files `files/` mein daalo aur GitHub par push karo.
2. **Actions** tab mein *Build APK* run hone do (kuch minute).
3. Run ke baad **Releases** (ya Artifacts) se `Success-Kit.apk` download karke install karo.

## AI setup (ek baar)

App kholo > **Ask AI** > gear icon:
- **Gemini API key** daalo (free key: aistudio.google.com/apikey). Key sirf phone mein save hoti hai.
- **Offline Gemma:** `Choose model file` se Gemma 3 1B `.task` file (~528 MB) ek baar chuno. App use apne andar copy kar leta hai.

## Notes

- Browser se upload karte waqt GitHub har file par 25 MB ki limit lagata hai. Isse badi file ho to git / GitHub Desktop se push karo (limit 100 MB).
- Records aur AI settings phone ke andar save hoti hain, app ka data clear karne par ud jaati hain.
- Ye debug APK hai, personal use ke liye theek hai.
