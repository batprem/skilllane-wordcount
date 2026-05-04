# Lab 1 — Word Counter

> ใช้กับ Module 1 (Foundations & Agent Loop)

## โจทย์

สังเกต **Agent Loop 5 ขั้น** ของ Codex โดยให้สร้าง word counter ง่าย ๆ

## วิธีทำ

### Step 1 — Setup

```bash
cd starter/
codex
```

### Step 2 — Prompt แรก (สังเกต loop ครบ)

```text
Create a Python script `wordcount.py` that takes a filename as argv[1],
prints number of lines, words, and characters. Then create a sample
input.txt with a paragraph of lorem ipsum and run wordcount.py on it
to verify.
```

สังเกต Codex ทำ:
1. **READ** — สแกน folder
2. **PLAN** — เขียน todo
3. **ACT** — สร้าง 2 ไฟล์
4. **OBSERVE** — รัน Python + อ่าน stdout
5. **VERIFY** — เปรียบเทียบกับสิ่งที่คาด

### Step 3 — เปลี่ยน model

```text
/model
```

เลือก `gpt-5.4-mini` แล้ว run prompt เดิมใน folder ใหม่ — สังเกตความเร็ว / token

### Step 4 — เปลี่ยน reasoning effort

```text
/reasoning high
```

แล้ว prompt:

```text
Refactor wordcount.py to also count unique words and most-common 5 words,
keeping it readable and idiomatic Python. Add a doctest.
```

### Step 5 — Interrupt

ระหว่างที่ Codex แก้ กด **Esc** แล้ว override:

```text
Wait, change wordcount.py to use Counter from collections instead of dict.
```

## โครงสร้างไฟล์ที่คาดหวัง

หลังจบแลบ ควรมีไฟล์อย่างน้อย:

- `wordcount.py` — รับชื่อไฟล์จาก command line และนับ lines / words / chars
- `input.txt` — ข้อความตัวอย่างสำหรับทดสอบ

## วิธีทดสอบเบื้องต้น

```bash
python wordcount.py input.txt
```

ตัวอย่าง output (รูปแบบอาจต่างกันได้):

```text
lines: 1
words: 69
chars: 445
```

## Reference Solution

ดู `solution/` หลังทำเอง — มี:

- `wordcount.py` — ใช้ Counter + doctest
- `input.txt` — sample lorem ipsum

## ✅ Checkpoint

- [ ] รู้ว่าจะดู plan ของ Codex ตรงไหนใน TUI
- [ ] สลับ model / reasoning level ได้
- [ ] Interrupt session ด้วย Esc ได้
- [ ] รัน `python wordcount.py input.txt` แล้วได้ผลลัพธ์ถูกต้อง
