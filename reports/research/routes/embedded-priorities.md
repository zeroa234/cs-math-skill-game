# Embedded Engineering Roadmap — priority flags as stored by the site

## What I read (URLs / verification)

- Live data file the site fetches: `https://m3y54m.github.io/Embedded-Engineering-Roadmap/map.json`
  (`explorer/app.js:613` does `fetch('map.json')`), 26,703 bytes, md5 `3c55a8fe9885209a29ac5ba32f0c69ef`.
- Repository copy: `https://raw.githubusercontent.com/m3y54m/Embedded-Engineering-Roadmap/master/explorer/map.json`
  — byte-identical (same md5), blob sha `9356b265f745bea59ab53503c0449d570cd761fe`, master commit
  `11eb6fb8ca7a111984da0c88c08749334d92ef5e`. The repo has only one branch, `master` (`gh api .../branches`);
  there is no `gh-pages` branch (the site is served from `explorer/`).
- Code read: `explorer/dom.js`, `explorer/diagram.js`, `explorer/mapview.js`, `explorer/app.js`, `explorer/map.css`,
  `README.md`.
- Live render check: opened `https://m3y54m.github.io/Embedded-Engineering-Roadmap/` in headless Edge (playwright-core).
  Found 20 header boxes + 106 topic boxes: 36 `required`, 27 `recommended`, 43 `possible`; legend text
  "Required / Recommended / Optional"; no page errors.
- `README.md:1768`: "where each topic sits on the map and its learning priority (required, recommended or optional)
  come from `explorer/map.json`". The README itself contains no priority flags (only resource-type symbols
  📘🎞️📝🔗 and quality symbols 👶💎, README lines 71–81).

## Encoding and legend

- Shape: `bands[]` → `clusters{}` → `topics: [[label, importance], ...]`. All 106 topic entries are 2-element arrays.
- `importance` values, exactly as encoded: `required` (36), `recommended` (27), `possible` (43).
- Site's display mapping (`explorer/dom.js:47-51`): `required` → **Required**, `recommended` → **Recommended**,
  `possible` → **Optional**. So the UI's "optional" is stored as `possible`.
- Colors (`explorer/map.css:232-234`, `349-351`): required `#fff04a` (yellow), recommended `#fbd7bb` (peach),
  possible `#f1f3f6` (near-white).
- Legend caption rendered on the map (`explorer/mapview.js:149`): "A general guide: priorities vary with your
  specialty and role".
- **Cluster/group level has no priority.** Cluster headers are separate boxes built with `importance: null`
  (`explorer/diagram.js:45`) and are not colored (`explorer/mapview.js:281`); only topic boxes get a class
  `required|recommended|possible`. So the "main node" level below the groups is a header/label, and its priority
  is `null`/not encoded; the flags live on the individual topic entries listed under each cluster.
- If one README topic matches several boxes, its displayed importance is the highest rank,
  `required > recommended > possible` (`explorer/diagram.js:6,66`), e.g. "CoAP & MQTT" ends up `recommended`
  because `MQTT = recommended` outranks `CoAP = possible`.
- `map.json` also has `groups` (region labels "Operating Systems", "Microcontrollers", "Interfaces & Protocols"),
  `offMap`, `links` and `readme` (label→README-heading aliases, e.g. `"Real-Time OS": ["Real-Time Operating Systems"]`,
  `"TDD & Unit Testing": ["Test Driven Development (TDD)", "Unit Testing"]`). Regions are also unflagged.

## Top-level groups (bands), main nodes (clusters) and all topic flags

The data has **four** bands, not three: the three areas plus an intersection band (SOFTWARE ∩ HARDWARE), which holds
50 of the 106 topics. Each cluster line gives `clusterId`; its header/caption is the map's main-node label, and the
cluster itself has no flag — its children's flags are listed.

### SOFTWARE (areas: SOFTWARE)

- **Programming Languages** `[languages]`
  - C = required; C++ = recommended; Python = recommended; Assembly = possible; Rust = possible
- **Programming Fundamentals** `[fundamentals]`
  - Algorithms & Data Structures = required; Design Patterns = required; State Machines = required; Memory Management = required
- **Debugging** `[debugging]`
  - JTAG / SWD = required; GDB = required; OpenOCD = possible
- **SDLC Models** `[sdlc]`
  - Agile / SCRUM = recommended; V-Model = recommended
- **Version Control** `[vcs]`
  - Git = required; SVN = possible
- **Build System** `[build]`
  - Compilers / GCC = required; Make / CMake = required; Bash Scripting = recommended; Docker = possible
- **Testing** `[testing]`
  - TDD & Unit Testing = required; CI/CD Pipelines = recommended; SIL / HIL Testing = possible; Standards & Certifications = possible
- **Specializations** `[specialized]` (caption, no header box)
  - Embedded Security = possible; Embedded GUI = possible; IoT = possible; Edge AI = possible; AUTOSAR = possible
- **no header/caption** `[osBase]` (holds the "Operating System Fundamentals" box)
  - Operating System Fundamentals = recommended
- **Embedded Linux** `[linux]`
  - Linux Kernel = recommended; Device Drivers = recommended; U-Boot = possible; Buildroot / Yocto = possible; Threading / Parallelism = possible; IPC = possible; Qt Framework = possible

### SOFTWARE ∩ HARDWARE (areas: SOFTWARE, HARDWARE)

- **Real-Time OS** `[rtos]`
  - RTOS Basics = required; FreeRTOS = recommended; Zephyr = recommended; QNX = possible; µC/OS = possible; RT-Thread = possible
- **no header/caption** `[mcu]` (the Microcontrollers region's main boxes)
  - GPIO = required; ADC / DAC = required; Timers / Counters = required; PWM = required; Watchdog = required; Interrupts = required; DMA = required; Clock Management = required; Power Management = recommended; Bootloader / DFU = recommended
- **Hardware-facing software** `[bridge]` (caption, no header box)
  - Memory Technologies & File Systems = recommended; Hardware Simulation / Emulation = recommended; Sensors & Actuators = possible; Digital Signal Processing = possible; Control Theory = possible
- **Basic** `[basic]`
  - UART = required; I2C = required; SPI = required
- **Wireless** `[wireless]`
  - Bluetooth = recommended; Wi-Fi = recommended; LoRa = possible; Zigbee = possible; Thread = possible; Matter = possible; UWB = possible
- **High-Speed** `[highSpeed]`
  - Ethernet = recommended; USB = recommended; PCIe = possible
- **Industrial** `[industrial]`
  - Modbus = recommended; Profinet = possible; EtherCAT = possible
- **Cellular** `[cellular]`
  - GSM / LTE = possible; LTE-M / 5G = possible; NB-IoT = possible
- **Network** `[network]`
  - MQTT = recommended; CoAP = possible; TCP/IP = possible; UDP = possible
- **Automotive** `[automotive]`
  - CAN = recommended; LIN = possible; MOST = possible; FlexRay = possible
- **Display & Camera** `[display]`
  - MIPI CSI-2 = possible; MIPI DSI = possible

### HARDWARE (areas: HARDWARE)

- **Electronics** `[electronics]`
  - Basic Math & Calculus = required; Principles of Electric Circuits = required; Electronics Fundamentals = required; Digital Design = required; Computer Architecture = required
- **Using Test Equipment** `[equipment]`
  - Multimeter = required; Logic / Protocol Analyzer = required; Oscilloscope = recommended
- **Prototyping Skills** `[prototyping]`
  - Breadboarding = recommended; Hardware Design Basics = recommended; PCB Design / EMC = recommended; Soldering / Rework = recommended
- **no header/caption** `[fpga]`
  - FPGA Development = possible

### SOFT SKILLS (areas: SOFT SKILLS)

- **no header/caption** `[soft]`
  - Communication Skills = required; Problem-Solving Skills & Critical Thinking = required; Teamwork & Collaborative Abilities = required; Organizational & Time Management Skills = required; Being Self-Driven and Independent = required; Adaptability & Patience = required

## Required nodes and their direct children

- In `map.json` there are 36 required topic entries. Every one is a leaf box: none has child boxes, so the data has
  no flags for children of required map boxes.
- Through the site's own README linking (`explorer/diagram.js`), those 36 boxes resolve to **38 README topics**
  marked required (aliases split `ADC / DAC` and `TDD & Unit Testing` into two README topics each).
  Only two of those required README topics have child headings, and their children have no map flag:
  - `Test Driven Development (TDD)` (required via box "TDD & Unit Testing") → `Unit Testing` = **required**
    (same box; also a separate README topic), `Integration Testing` = no flag (not on the map).
  - `Unit Testing` (required via the same box) → `GoogleTest - Google Testing and Mocking Framework` = no flag
    (not on the map).
- Therefore: no required node in this data has flagged direct children. The 36 required labels are exactly the
  `= required` entries in the cluster lists above (C, Algorithms & Data Structures, Design Patterns, State Machines,
  Memory Management, JTAG / SWD, GDB, Git, Compilers / GCC, Make / CMake, TDD & Unit Testing, RTOS Basics, GPIO,
  ADC / DAC, Timers / Counters, PWM, Watchdog, Interrupts, DMA, Clock Management, UART, I2C, SPI, Basic Math &
  Calculus, Principles of Electric Circuits, Electronics Fundamentals, Digital Design, Computer Architecture,
  Multimeter, Logic / Protocol Analyzer, and the six soft skills).

## Caveats

- There is no priority flag at the main-node/cluster level in this data; the premise "each roadmap node has a
  priority" holds only for the topic boxes. Cluster headers are explicitly `importance: null`.
- The map has an extra SOFTWARE ∩ HARDWARE band and three unflagged region labels, so a strict
  SOFTWARE/HARDWARE/SOFT SKILLS three-way split does not match how the data is organized.
- Values were read from the live file on the date of this research; the repo data may change later.
