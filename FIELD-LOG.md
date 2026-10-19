```
████ TOP SECRET ████   FIELD LOG   ·   AGENT: Rasim
```

**Codename:** *El Luchador*
**Started:** *Sep 25 2026*

---

## How this works

A few lines at the end of each session. Commit it with the code.

Nobody is marking your writing. It is here because writing down what you tried is the cheapest debugging trick there is, and because next February you will hit the same wall and this file is the only thing that will remember how you got past it.

**Each entry:** what you were trying to do, what happened, and one thing that did not work.

If a session genuinely went perfectly, say so. But a log where nothing ever goes wrong describes a project that did not happen.

---

### 2026-10-05 · 3 h · Phase 1

**Trying to:** Blink an LED on a nucleo board using code from a youtube tutorial, since stm32cubeide uses a new language. Then tried to connect the board and my mac using UART to print my code name on a chinese serial plotting app since I did not know there was a terminal command instead.

**Happened:** Builds went well, so did debugging code, LED worked first try, and the board started talking after like an hour or two of coding and I got to print "El Luchador" for my mac


**Didn't work:** At first the code failed and I was very lost so I looked through more sources just to realize I simply wrote "Hal" instead of "HAL", but then the build showed 0 errors afterwards. On the otherhand, UART was a bit more complex since it is not as popular of a project as blinking an LED, but after finding the right piece of code and navigating the ui on a serial plotting app the messages printed just fine

---
