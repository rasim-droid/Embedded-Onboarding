```
████ TOP SECRET ████   EMBEDDED SYSTEMS ONBOARDING TASK
```

*The banner is a joke. The assignment is not.*

| The bit | The truth |
|---|---|
| "Office of Embedded Affairs", the codenames, the redactions | Made up. We are a student rover team. |
| The build, the rules, the scoring | Real. |

---

# YOU HAVE BEEN RECRUITED

**Your mission: build a device that can tell whether a room is occupied. No camera, no microphone.**

The trick is real. People exhale carbon dioxide, so CO2 rises in a closed room when somebody is in it. A sensor watching that number knows somebody is there. It does not know who.

Your device watches the air, reports once a second, and stops when you hit the switch.

```
   [CO2 SENSOR] ──I2C──┐
   [POWER CELL] ──ADC──┼──► ( YOUR NODE ) ──UART──► HANDLER
   [KILL SWITCH]──IRQ──┘         └──PWM──► [SERVO]
```

In plain terms: an STM32 project that reads a sensor, reads a potentiometer, drives a servo, handles a button, and prints a status line once a second. That is the same shape as a real rover node, which is why it is the task.

---

## THE DEAL

**No pass, no fail. Nobody gets cut for an unfinished task.**

You come out with a level from 0 to 4 in each skill: I2C, timers, interrupts, UART and so on, scored separately. Level 3 means we hand you that job on the real rover without hovering.

Level 3 in I2C and 1 in timers is not worse than the reverse. It is a different job.

---

## WHAT IS IN HERE

| File | What |
|---|---|
| `README.md` | You are here. The task, the rules, the scoring. |
| `GIT-GUIDE.md` | Every git command you need, in order. Read it if you have not used git. |
| `FIELD-LOG.md` | Your log. A few lines per session. |
| `tools/check_frame.py` | Checks your status line. Run it before we do. |
| `firmware/` | Empty. Your STM32CubeIDE project goes here. |

---

## KIT

You do not need to buy anything. The club has NUCLEO-F302R8 boards, SCD40 sensors, potentiometers, LEDs, servos, plus the logic analyzer, scope and power supply.

Club kit stays at the club. Flashing, testing and final debugging all happen at meetings and drop-in sessions.

If you kept the CO2 sensor from your OOP course you have your own, and you can work at home whenever you like.

---

## START HERE

```
1. Read the rules below.
2. Read GIT-GUIDE.md and create your own repository from the template.
3. Come to a session and grab a board.
4. Start Phase 1.
5. Add a few lines to FIELD-LOG.md at the end of each session.
```

Write code wherever you like, test it at the club.

---

# THE TASK

Three phases. All three are expected. The bonus section at the end is optional and most people will skip it, which is fine.

**Two rules that apply throughout:**

1. **No `HAL_Delay()` in your main loop.** Timing comes from timers. A CPU sitting in a delay cannot hear the kill switch.
2. **Nothing waits forever.** If the sensor stops answering, your node keeps going.

---

## PHASE 1: INSERTION
*Week 1. Rated: toolchain, clock, GPIO, timers, interrupts, UART*

**Get on the board and make it say something.**

### 1.1 Your own project
New STM32CubeIDE project for the **NUCLEO-F302R8**, built by you rather than copied. Set SYSCLK to 64 MHz.

Building it yourself is slower. It is also the only way you will know where anything is when something breaks in week three.

### 1.2 Blink
Onboard LED at **1 Hz**, on for 500 ms and off for 500 ms, from a **timer interrupt**, not a delay loop.

Note the LED has to **toggle twice a second** to give you a 1 Hz blink. Easy to get half right.

### 1.3 Talk
UART console at **115200 8N1** over the ST-Link port. On boot, print your codename and firmware version.

This console is your main debugging tool for the rest of the project.

---

## PHASE 2: THE ASSET
*Week 2. Rated: I2C, datasheet reading, ADC*

**Get real numbers out of the sensor. This is the interesting phase.**

### 2.1 Find it
On boot, scan the I2C bus and print any address that answers.

Thirty lines of code, and the first thing you will run every time something goes wrong for the rest of your life.

### 2.2 Read it
Talk to the **SCD40** over I2C: start periodic measurement, wait for a reading, read CO2 and temperature, convert to real units.

**Ignore the CRC bytes.** Read them, throw them away. They are in the bonus section if you want them later. They are not part of this task.

**Done looks like:** a CO2 number on your console that goes up when you breathe near the sensor.

Write this yourself. Do not drop in somebody's finished SCD40 library. The command set is small, so this is more approachable than it looks.

### 2.3 Read the pot
Potentiometer on the ADC, converted to **millivolts**.

Put the LSB size and the reference voltage in a comment. If those two numbers are wrong your reading is decoration, and we will spot it by applying a known voltage.

---

## PHASE 3: GOING LOUD
*Week 3. Rated: PWM, interrupts, UART, putting it together*

**Make it do something and report on itself.**

### 3.1 Move something
PWM with duty settable in code, 0 to 100%. A servo at 50 Hz, or an LED at 1 kHz. Both are in the parts bin.

Show the prescaler and reload arithmetic in a comment. The working, not just the two numbers you ended up with.

### 3.2 Kill switch
User button on an **external interrupt**. Press it: PWM goes to zero, a fault latches, flag bit 1 sets.

**It stays latched** until reset. A safety switch that un-presses itself is not a safety switch.

Your interrupt handler should set a flag and return. Do the real work back in the main loop. Ask about `volatile` if that word means nothing yet, it is worth ten minutes.

### 3.3 Status line
Print this once a second:

```
NODE,<uptime_s>,<co2_ppm>,<temp_c_x10>,<adc_mv>,<pwm_duty>,<flags>
```

| Field | Range | Note |
|---|---|---|
| `uptime_s` | 0+ | Seconds since boot |
| `co2_ppm` | 0 to 40000 | `0` if you have not got a reading |
| `temp_c_x10` | -400 to 1250 | Celsius x10, so `235` is 23.5 C |
| `adc_mv` | 0 to 3300 | Pot, millivolts |
| `pwm_duty` | 0 to 100 | Percent |
| `flags` | `00` to `FF` | Two uppercase hex digits |

**Flags:** bit 0 = sensor not answering, bit 1 = kill switch latched, bit 2 = CRC failure (only if you do bonus B1). Bits 3 to 7 send as 0.

The line starts with `NODE` so the checker can find it among your other prints.

Temperature goes out as an integer x10 on purpose. It saves you a fight with floating point `printf`, which on an embedded target either fails silently or eats a chunk of your flash.

Example: `NODE,142,814,231,1650,50,00`

**Check it yourself** before your debrief:
```
python3 tools/check_frame.py            # paste lines in, Ctrl-D
python3 tools/check_frame.py log.txt    # or check a captured file
```

---

## BONUS

Optional. Nobody is expected to do any of this, and skipping all of it costs you nothing. It exists because every year one or two people finish early and want more.

| | What | Rates |
|---|---|---|
| **B1** | **CRC check.** The SCD40 sends a CRC byte with every word. Find the parameters in the datasheet and verify them, then set flag bit 2 on failure. About ten lines of bit shifting. | Bit manipulation, datasheet |
| **B2** | **Commands.** Accept `GET` and `CLR FAULT` over UART, and anything else replies `ERR`. | UART, parsing |
| **B3** | **Never blocks.** Rewrite the sensor read as a state machine so nothing waits. You will know you need this if your LED stutters when the sensor is read. The SCD40 is slow. | Firmware sense |
| **B4** | **Unpluggable.** Sensor pulled out mid run: node keeps going, flags it, recovers when it is plugged back in. | Firmware sense |
| **B5** | **ADC on DMA**, or an **SPI loopback test** (one jumper, MOSI to MISO), or the **watchdog**. Pick any. | DMA / SPI |

---

# THE RULES

Clause 1 is a joke. Everything after it is real.

## 1. Non-disclosure (joke)

You agree not to disclose this operation to foreign powers, rival rover teams, or your roommate, who will not care.

You are encouraged to tell other recruits, anyone at the club, and anyone thinking of joining. This is the least confidential classified document ever produced. Put it on your resume.

## 2. Git (real)

All work happens in a git repository, in **your own repository**, from the start.

Two reasons, both real. Our actual firmware lives in git, and somebody who cannot use it cannot contribute no matter how well they know I2C. And a genuine development history is very hard to fake.

- Create your own repository from the project template. **Never push to the original.**
- At least **8 commits across 4 different days**. At home or at the club, both count.
- Add a few lines to `FIELD-LOG.md` each session and commit it with the code.
- Push at the end of every session.

**Commit your mistakes too.** A history with no bugs in it describes a project that did not happen. Do not tidy it up. Being wrong in decreasing increments is what this job actually looks like.

Never used git? `GIT-GUIDE.md` has every command you need, in order, with nothing assumed.

## 3. No AI (real, and the one we mean most)

No generative AI on any part of this. Not the code, not the log, not the commit messages, not "just explain the datasheet to me".

**Why:** the point of this task is to find out what **you** can do, so we know what to trust you with. Work from a tool tells us what the tool can do. The person it costs most is you, because you end up on a team that thinks you can do something you cannot, on a rover where that matters.

**If you do it anyway:** your task is recorded at level 0 across every skill, you re-attempt next cycle, and your Handler has a direct and fairly uncomfortable conversation with you. You are not kicked off the team and you are not named to anybody. But you will have spent a month proving nothing about yourself, and you will be the one person here whose skills nobody can vouch for.

...and maybe somebody comes for you. Or not. You will never know. Sleep well, Recruit.

**How we would actually notice:** not by staring at your commit history. At your debrief you will change your own code, on our bench, in a way you have not seen coming. If you wrote it, that is ten easy minutes. There is nothing to prepare, which is exactly why it works.

## 4. What you can use (real)

**Yes:** the reference manual, the SCD40 datasheet, HAL docs, Google, Stack Overflow, and any human being at the club.

**No:** a finished SCD40 driver. Writing it is the task.

Anything else you borrow, credit it in your log and be able to explain it.

## 5. The kit (real)

- Club hardware stays at the club. Use it at meetings and drop-in sessions.
- Put things back where you found them. The next person is looking for the same board you are.
- Break something? Say so straight away, especially if it was your fault. Nobody has ever been in trouble for breaking equipment. People have made us unhappy by breaking something quietly and letting the next person find out the night before a competition.

---

# HOW YOU ARE SCORED

Read this in week one, not week four. Knowing how you are assessed changes what you build, which is the point of telling you.

**About 30 minutes, at the club, on club hardware, with your Handler.**

## The levels

A level from **0 to 4 in each skill, separately**. No total, no average, no ranking.

| Level | Means | You get handed |
|---|---|---|
| **0** | Did not attempt it, or we have no evidence | Nothing yet. That is a gap in our notes, not a mark against you. |
| **1** | Tried it. Does not work, or you cannot explain it | Guided exercises. Becomes something we teach you. |
| **2** | Works. Needed help, explanation has gaps | Paired work |
| **3** | Works, you understand it, **and you changed it live at debrief** | **Independent jobs in this skill** |
| **4** | All of that, plus you went further on your own | You own it, and review other people's |

**Rated from the core phases:** toolchain and HAL, clock config, GPIO, timers and PWM, interrupts, UART, I2C, ADC, datasheet reading, debugging, git and process, and general firmware sense.

**Only from bonus work:** bit manipulation, DMA, SPI, command parsing. Skipping the bonus leaves those blank. Blank is fine.

**Not covered at all:** CAN and RTOS. You pick those up on real work later.

## The one rule that matters

> **Nobody gets level 3 in anything without changing their own code, live, at debrief.**

Working firmware, a tidy repo and a confident explanation together cap at level 2 if you cannot modify it with somebody watching.

This is not a trap and there is nothing to revise for. If you wrote it, it is a small change to code you know.

It works the other way too: **an unfinished task whose author confidently changes what does exist beats a finished one whose author cannot.** We are measuring what you can do, not what you handed in.

## On the day

**Bring:** a charged laptop. The hardware is here. Push everything first, we open your repository from GitHub, not your laptop.

**1. Show us it working (10 min).** You drive.
- Blink runs, console prints.
- **You breathe on the sensor and the CO2 number moves.** If it does not move, something is cached that should not be.
- Sweep the pot, watch `adc_mv` follow.
- PWM does its thing.
- Hit the kill switch. It latches and stays latched.

**2. Instruments (10 min).** *You* hook them up, that is part of it.
- Logic analyzer on the I2C bus. Capture a sensor read and point out the address byte and the ACK on your own capture.
- Scope on the PWM, checked against the frequency you claim.

**3. Talk it through (10 min).**
- **We pick a section of your code** and you explain it. What it does, and what you tried first that did not work. That second part is what separates somebody who wrote code from somebody who read it.
- **Then you change something, live.** Our pick, from a list you have not seen: print the status line every 2 seconds instead of 1, add a flag bit and set it, change the PWM frequency and prove it on the scope.
- **A couple of questions.** Why does I2C need pull-ups, or what happens if you `printf` inside an interrupt.

**"I don't know" is a fine answer.** "I don't know, but here is how I would find out" is nearly a free pass. Confident invention is expensive and extremely obvious from the other side of a bench.

**4. Your sheet (5 min).** Filled in with you sitting there, with reasons. You leave knowing every level and which skills we will deliberately pair you on.

## Before you come in

- [ ] Blink at 1 Hz (500 ms on, 500 ms off) from a timer, no `HAL_Delay` in the main loop
- [ ] Console prints on boot
- [ ] Bus scan works
- [ ] CO2 number moves when I breathe on the sensor
- [ ] Pot reads in millivolts, LSB and reference voltage in a comment
- [ ] PWM works, arithmetic shown in a comment
- [ ] Kill switch latches and stays latched
- [ ] Status line once a second, and `check_frame.py` accepts it
- [ ] Working in my own repository, never pushed to the original
- [ ] 8+ commits over 4+ days, log committed alongside, everything pushed
- [ ] Bonus attempted: ______________ (or "none", that is the common answer)
- [ ] Known issues I am declaring up front: ______________

Listing your own bugs costs you nothing and reads well. We will find them anyway, and "I know, here is why" is a much better place to be than being shown your own bug.

## Afterwards

**There is no fail.** There is a sheet and a list of things we will pair you on.

Got as far as Phase 2 and stopped? Recorded as Phase 2, assigned accordingly. A first-year who gets a real sensor talking in three weeks having never written firmware has done something genuinely hard.

Your levels are not permanent either. They are a snapshot from your first month, and we expect them to be wrong within a few weeks in the good direction. They get revised on real work, not by re-sitting anything.

---

```
WELCOME TO THE TEAM
```