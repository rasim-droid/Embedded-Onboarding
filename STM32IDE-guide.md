# ████ TOP SECRET ████ STM32, FROM ZERO

Never used STM32CubeIDE? Start at step 1.

Used it before? Skip to step 3.

For this project we use the **NUCLEO-F302R8**. Your STM32CubeIDE project belongs inside `firmware/`.

---

## What CubeMX and CubeIDE are

**STM32CubeMX** configures the microcontroller: pins, clocks, timers, UART, I2C, ADC and interrupts.

**STM32CubeIDE** is where you write C, build the project, flash the board and debug it.

The `.ioc` file stores your CubeMX configuration.

---

## STEP 1: Install STM32CubeIDE

Download **STM32CubeIDE** and **STM32CubeMX** from STMicroelectronics and install them.

Link: https://www.st.com/en/development-tools/stm32cubeide#section-get-software-table

The default options are fine.

**Do not download the VS Code version of the IDE since it is really raw, and you will spend more time debugging the IDE than doing the project.**

---

## STEP 2: Create the project

In STM32CubeMX:

1. Click `File` → `New Project`
2. Open **Board Selector**
3. Search for `NUCLEO-F302R8`
4. Select the board
5. Click **Start Project**
6. Open the **Project Manager** tab
7. Name your project
8. Set the project location to this repository's `firmware/` folder
9. Change **Toolchain / IDE** from the default `EWARM` to `STM32CubeIDE`

CubeMX will create the `.ioc` configuration.

---

## STEP 3: Configure CubeMX

The important CubeMX tabs are:

| Tab | What it does |
|---|---|
| **Pinout & Configuration** | GPIO, UART, I2C, ADC, timers, interrupts |
| **Clock Configuration** | CPU and peripheral clocks |
| **Project Manager** | Code generation settings |

Clicking a pin lets you assign a function to it.

Peripherals are configured from the menu on the left.

---

## STEP 4: Generate code

Save the `.ioc` file:

```text
Ctrl + S
```

Alternatively: press ```Generate``` button in the right top corner.

CubeMX may ask to generate code. Click **Yes**.

Your project will now contain folders such as:

```text
Core/
├── Inc/
└── Src/

Drivers/
```

Your main program is:

```text
Core/Src/main.c
```

---

## STEP 5: Put your code in USER CODE sections

CubeMX generates parts of `main.c`.

Write your code inside sections like:

```c
/* USER CODE BEGIN 2 */

HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_SET);

/* USER CODE END 2 */
```

or:

```c
/* USER CODE BEGIN WHILE */

while (1)
{
    /* your code */
}

/* USER CODE END WHILE */
```

> Code outside `USER CODE BEGIN` / `USER CODE END` sections may be deleted when CubeMX regenerates the project.

---

## STEP 6: Build

Click the **hammer icon**, or use:

```text
Ctrl + B
```

Look at the Console.

You want:

```text
0 errors
```

Warnings are worth reading. Errors must be fixed before flashing.

---

## STEP 7: Plug in the board

Connect the NUCLEO board to your computer using the **USB connector**.

The ST-LINK programmer is built into the NUCLEO board. You do not need a separate programmer.

---

## STEP 8: Flash and run

Connect the NUCLEO board.

Click the **Run** button.

The first time, CubeIDE may ask you to create a launch configuration. Accept the defaults.

CubeIDE will:

```text
build → connect to ST-LINK → flash → reset → run
```

Your program is now running on the STM32.

---

## STEP 9: Debug

Click the **bug icon** instead of Run.

CubeIDE will stop at the start of the program.

Useful controls:

```text
Resume       F8
Step Into    F5
Step Over    F6
Step Return  F7
Terminate    Ctrl + F2
```

Click beside a line number to add a **breakpoint**.

You can inspect variables while the processor is stopped.

---

## Changing peripherals later

Open the project's `.ioc` file.

Change the CubeMX configuration, then save:

```text
Ctrl + S
```

CubeMX regenerates the initialization code.

This is normal.

Keep your own code inside the `USER CODE` sections.

---

## Peripherals you will use

During the onboarding task you will configure:

```text
GPIO    → LED and digital pins
TIM     → timers and servo PWM
USART   → serial output
I2C     → CO2 sensor
ADC     → potentiometer
EXTI    → kill switch interrupt
```

Do them as the README asks for them. You do not need to configure everything at once.

---

## When something goes wrong

**Board not detected**

Check that you plugged into the NUCLEO's **ST-LINK USB connector** and try another USB cable.

**Build fails**

Read the **first error** in the Console. Later errors are often caused by the first one.

**CubeMX deleted my code**

Your code was probably outside a `USER CODE` section.

**Peripheral does nothing**

Check three things first:

```text
pin assignment
peripheral configuration
clock
```

**Program flashes but does not behave correctly**

Use the debugger. Add a breakpoint and check whether the code you expect is actually being reached.

---

## The whole workflow

```text
Open .ioc
    ↓
Configure pins/peripherals
    ↓
Save / generate code
    ↓
Write code in USER CODE sections
    ↓
Build
    ↓
Flash
    ↓
Test
    ↓
Commit
```

That is the loop.

---

## What we check

- Project is inside `firmware/`.
- Board is `NUCLEO-F302R8`.
- Project builds with no errors.
- Code is kept inside appropriate `USER CODE` sections.
- You can build, flash and debug the board yourself.
- Your `.ioc` file is committed with the rest of the project.

If changing the `.ioc` breaks something, commit that too. Debugging CubeMX configuration is part of embedded development.
