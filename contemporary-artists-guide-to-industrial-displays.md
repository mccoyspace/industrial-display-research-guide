# The Contemporary Artist's Guide to Industrial Displays

**Selecting, modifying, and maintaining commercial and industrial displays for long-lived media artworks**

Prepared for the studio of Jennifer and Kevin McCoy · July 2026

**Scope:** Industrial HDMI/USB touch monitors, industrial panel PCs (x86 and ARM), Android signage displays, and OEM/semi-barebone display systems, in sizes from 7" to 43"+. Operating-system scope covers **both Android and Ubuntu/Linux**, including mainline kernel status for Rockchip SoCs, kiosk-mode Linux configurations, and USB HID touch behavior across platforms.

**Evidence labels used throughout:** `[datasheet]` directly verified vendor PDF/spec · `[vendor page]` vendor web claim · `[supplier claim]` unverified factory statement · `[teardown]` physical/photographic evidence · `[forum]` community/user report · `[kernel]` Linux kernel source or mailing list · `[inferred]` reasonable conclusion from adjacent evidence · `[unverified]` flag for direct confirmation before purchase. Any recommendation based only on an Alibaba listing is marked **tentative**.

---

## 1. Executive Summary

The question this guide answers:

> "Can I buy this display today, run my own software reliably, repair it later, and still keep the artwork serviceable in ten years?"

**The short answer: yes — but almost never by buying an integrated Android display.** The evidence gathered here (60+ vendors and products surveyed, teardown and kernel-level sources, museum conservation literature) points consistently to one architecture:

> **Standardize on "dumb" industrial HDMI + USB-HID touch monitors, and keep the compute external, replaceable, and boring.**

Key findings:

1. **The dumb-monitor-plus-external-compute architecture won on the evidence** (Hypothesis 4, confirmed). A PCAP touch monitor with HDMI input presents itself to any computer — Mac, Linux, Raspberry Pi — as a standard USB HID device, driverless on any Linux kernel ≥3.8 `[vendor page: Elo support KB]`. The display and the compute fail and obsolesce on different timelines; this architecture lets you replace only what breaks.

2. **Elo Touch and Faytech open-frame families are the strongest multi-size platforms.** Elo's open-frame line spans 7"–42.5" with vendor-confirmed driverless Linux HID touch, published MTBF, and 3–5 year warranties; Faytech spans 7"–43" with published pricing and component-level repairability marketing. No single vendor wins every axis — a two-vendor strategy is recommended (§4, §15).

3. **Android signage displays are commodity assemblies on a small set of Rockchip OEM boards** (Hypotheses 1–2, supported). Because Rockchip's MaskROM recovery is burned into the silicon, any RK3288/RK3399/RK3566/RK3568/RK3588 unit can always be reflashed with open tools (`rkdeveloptool`) — but board-specific device trees, panel timings, and touch drivers mean recoverable ≠ rehostable. HDMI *input* remains rare even on 2026 flagship signage hardware `[teardown: Rikomagic DS08 review, CNX Software 2026]`. Use this class only as a sealed video appliance or for teardown/experimentation.

4. **On the Linux side, RK3588 mainline support is real and improving fast but incomplete** (eDP and hardware encode lag; Vulkan windowed rendering unreliable), and the most popular community Ubuntu build for Rockchip — Joshua Riek's ubuntu-rockchip — was **archived on April 29, 2026** after maintainer burnout `[confirmed: github.com/Joshua-Riek/ubuntu-rockchip; jeffgeerling.com]`. This is a concrete, already-realized warning: a ten-year plan cannot depend on volunteer distro tooling for Chinese ARM SoCs.

5. **The most future-proof compute today is unglamorous:** Raspberry Pi 5 (official production commitment to at least January 2036 `[vendor page: raspberrypi.com obsolescence statement]`), Intel N100/Core mini PCs and used business-class SFF PCs (standard x86 Ubuntu, no special images), and Jetson Orin for AI/vision work (module production through January 2032 `[vendor page: developer.nvidia.com/embedded/lifecycle]`).

6. **21.5"/1080p is the safest panel size for ten-year availability** — triple-sourced across BOE, AUO, and Innolux in multi-generation industrial families, structurally tied to fab glass-cutting economics (§8). 7"–10.1" is safe via the Raspberry Pi ecosystem's gravitational pull on suppliers. 32" at true 1080p is materially less commodity than it looks.

7. **What actually fails, in order:** power-supply electrolytic capacitors, LED backlight brightness (L70 half-life math in §14), touch controllers (usually via power/EMI, not glass wear), and HDMI/EDID handshakes. Every one of these has a cheap, known mitigation — brightness derating, Mean Well-class PSUs, spares purchased at build time, and inline EDID emulators (§14).

**Hypothesis verdicts (detailed in §15):**

| # | Hypothesis | Verdict |
|---|---|---|
| 1 | Alibaba signage units are commodity-part assemblies | **Supported** `[teardown, forum]` |
| 2 | Visually different units are rebrands of few OEM platforms | **Supported** (moderate–strong circumstantial; one confirmed cross-brand case) |
| 3 | Rockchip units are more hackable than Novatek/MStar appliances | **Supported**, with the recoverable-≠-rehostable caveat |
| 4 | Dumb touch monitor + external compute beats opaque Android signage for longevity | **Strongly supported** — the central conclusion of this guide |
| 5 | An ideal multi-size family with consistent touch/mounting/power exists | **Partially supported** — Elo and Faytech come closest; consistency is achieved at the *protocol* level (USB HID PCAP, HDMI, VESA, 12–24 V DC) rather than by any single vendor |

---

## 2. What Artists Actually Need from Displays

This section grounds the technical criteria in the studio's actual practice, because "industrial display" marketing is written for factory HMIs and retail kiosks, not for artworks that must outlive their components.

**The studio's working reality.** The McCoy practice spans database-driven film/TV works with custom playback systems, miniature "real-time cinema" installations combining dioramas, cameras, small displays, and custom software, and generative/blockchain-era works running continuous software loops. Works live in museum collections (MoMA, the Met, the Whitney) under time-based-media conservation regimes — the Met's conservation notes on *Every Shot, Every Episode* describe a 277-disc custom playback system as a managed conservation object. That is the standard this guide plans for: **a display bought today may still need to boot correctly, in public, in 2036, under someone else's care.**

From that practice, the real requirements:

1. **Small displays matter as much as large ones.** Miniature installations need 7"–11.6" panels that behave like serious displays (HDMI in, proper EDID, VESA or clean mounting, no consumer-tablet sleep behavior) — a size class most industrial vendors treat as an afterthought and most consumer vendors treat as a toy.
2. **Custom software is the medium.** The studio writes Python, JavaScript/TypeScript, and C/C++; playback systems are bespoke. The display must therefore be OS-agnostic glass: HDMI in, USB HID touch out, no opinion about what drives it. Anything that requires the artwork's logic to live *inside* the display's own Android build couples the work's survival to a Shenzhen firmware team's attention span.
3. **24/7 gallery duty with unattended recovery.** Power cuts happen; museum staff will not reflash a bootloader. Auto power-on after power loss, boot-to-content without input, no sleep/DPMS surprises, and watchdog-supervised software are non-negotiable (§13).
4. **Conservation-grade documentation from day one.** Museums use identity/iteration reports and equipment-significance ratings (Guggenheim/Phillips 1–3 scale: dedicated vs. obsolete-shared vs. freely substitutable equipment). The studio equivalent: for every piece, record panel model, touch controller, EDID dump, firmware images, and a one-sentence fallback plan — at build time, not during a crisis (§13.5, Appendix D).
5. **Repairability over features.** Known LCD panel model, known touch controller, openable enclosure, replaceable PSU, commodity internal interfaces (eDP/LVDS), and a vendor who answers technical questions are worth more than brightness, bezels, or bundled CMS software.
6. **Honest evidence.** Signage marketing is systematically ambiguous — "HDMI" without an in/out qualifier almost always means output-only `[listing survey, §3.3]`. This guide labels every claim, and the supplier questionnaire (§11, Appendix C) exists to convert "listing says" into "supplier confirmed in writing."

---

## 3. The Four Product Classes

| Class | What it is | Best for | Ten-year risk |
|---|---|---|---|
| 3.1 Dumb industrial touch monitor | HDMI/DP in + USB HID touch, no computer | **Default for almost everything** | Low — compute replaceable forever |
| 3.2 Industrial panel PC | Display + integrated x86/ARM compute | Self-contained pieces where one enclosure matters | Medium — compute ages inside the glass |
| 3.3 Android signage display | Alibaba-style advertising machine | Sealed video playback; teardown experiments | High — firmware-coupled, opaque |
| 3.4 OEM / semi-barebone systems | Enclosure + panel + touch + replaceable compute (incl. OPS/SDM slot displays) | Studio-standard platforms, custom builds | Low–medium — best serviceability *if* documented |

### 3.1 Dumb Industrial Touch Monitors

**Verdict: the studio default.** These are displays in the traditional sense: a panel, a scaler board, a touch overlay with a USB controller, a power supply, VESA holes. Modern PCAP (projected capacitive) touch enumerates as a standard USB HID multitouch device — Elo's own support documentation states PCAP screens need **no driver on any Linux kernel ≥3.8** `[vendor page: elosupport.elotouch.com article 31649725511447]`, and the mainline `hid-multitouch` driver auto-binds to compliant devices `[kernel: drivers/hid/hid-multitouch.c, in-tree since 2.6.38]`.

Strengths: total OS freedom; compute replaceable indefinitely; the simplest conservation story ("it is a monitor"). Weaknesses: nearly all vendors — including Elo and Faytech — decline to publish the internal LCD panel model or touch-controller chip on public datasheets `[datasheet survey, §5]`; auto-power-on-after-outage is documented by almost nobody (Mimo is the notable exception `[vendor page]`); and the touch-controller silicon can change between date codes of the same SKU (documented for Mimo `[forum]`). All three gaps are closed by the supplier questionnaire (§11).

Watch for the **eGalax/EETI caveat**: modern eGalax PCAP works via `hid-multitouch`, but the controller family has a two-decade history of kernel quirks (`HID_QUIRK_NOGET` in mainline `hid-quirks.c`; a new `MT_CLS_EGALAX_P80H84` quirk class was still being submitted to the kernel mailing list in February 2026 `[kernel: patchew.org]`). ILITEK, Elo's in-house TouchPro/COACh, and Goodix-over-USB have cleaner records (§8.3).

### 3.2 Industrial Panel PCs

**Verdict: legitimate for self-contained works — buy modular, buy x86, treat ARM panel PCs as Android appliances unless proven otherwise.**

x86 panel PCs (Advantech PPC, AAEON OMNI, OnLogic Tacton, Cincoze CV/CS, Teguar, Winmate, DFI, Axiomtek GOT, Kontron, ASUS IoT, Shuttle) run stock Ubuntu on mainline kernels — the single biggest longevity advantage over ARM. The vendors that matter most here are the ones with **split architectures** where compute and display are separately replaceable: Cincoze's Convertible Display System, AAEON's OMNI CPU-box + panel kits, DFI's Adaptive Display Platform, and Axiomtek's socketed-LGA GOT models `[vendor page]`. OnLogic has the best-documented Ubuntu story (Canonical-certified sibling products, Tacton tested on 22.04/24.04, self-serve pricing) `[vendor page: ubuntu.com/certified]`; DFI and OnLogic are the only vendors found with **dated** SKU-level lifecycle commitments (to 2035) rather than generic "10 years" language `[vendor page, press]`.

Two honest caveats. First, GPU: N100/Alder-Lake-N iGPUs are inadequate for shader-heavy real-time work — the TouchDesigner community's consistent verdict is that Intel integrated graphics of any generation is for "noodling," and no industrial panel-PC brand appears anywhere in TouchDesigner/openFrameworks forum history `[forum: forum.derivative.ca]`. The strongest integrated options are ASUS IoT's APC-125U (Meteor Lake, Arc Xe-LPG) and Shuttle's Arrow Lake-U line. Second, touch: even here, plug-and-play is not universal — OnLogic's own support docs walk through a manual eGalax driver install for some SKUs, warning touch is dead until it's done `[vendor page: support.onlogic.com]`.

ARM panel PCs (Geniatech TPC-K3 10"–32", TouchThink RK3588 line, Advantech's aging RK3399 PPC-1xxW, Firefly-based builds) are cheaper and fanless but inherit every Rockchip Linux caveat in §7 — and many wire touch over I²C to the SoC rather than USB, making touch a BSP-driver question instead of a HID guarantee `[vendor docs, inferred]`.

### 3.3 Android Signage Displays

**Verdict: variable to hostile; use only as a sealed player, or as a donor chassis.** The research (Part B–F of the signage stream, §12) confirms the class is built from commodity parts on a small pool of Rockchip OEM boards, sold under dozens of brands. What that means in practice:

- **Hackability floor is real:** any Rockchip unit answers to MaskROM + `rkdeveloptool` regardless of brand `[docs: github.com/rockchip-linux/rkdeveloptool; forum: Armbian, Kobol wiki]`. The ELC WF8382T case — mainline U-Boot built for the *Firefly-RK3288 dev board* booting on a commercial signage tablet — shows how close these boards sit to public reference designs `[forum: forum.armbian.com/topic/36417]`.
- **Hackability ceiling is also real:** device-tree panel timings, touch drivers, and DDR blobs are board-specific; generic firmware "difficult to find, most firmware being device-specific" `[forum: XDA]`. Budget reverse-engineering time or don't start.
- **HDMI input is a minority feature** even in 2026 (Rikomagic DS08, a flagship RK3588 player reviewed May 2026: two HDMI ports, both outputs `[teardown/review: cnx-software.com]`), and where present is usually a PiP/capture path through the SoC's video-capture block — latency and HDCP apply — not a monitor-style scaler input `[inferred from RK3588 architecture, confirmed by listings]`.
- **No vendor in the entire survey advertises ADB, firmware downloads, or developer access as a feature** — except Geniatech, which maintains an actual downloads portal and published board datasheets, and is therefore the standout in this class `[vendor page: geniatech.com]`.
- **Android versions stagnate:** RK3568 units ship Android 11/12 in 2025–26 with no observed updates; AOSP/non-GMS devices sit outside Google's OTA pipeline entirely `[listing survey, structural]`.

### 3.4 OEM / Semi-Barebone Systems

**Verdict: the most interesting class for a studio standard — two distinct sub-strategies.**

**(a) OPS/SDM slot displays.** Commercial displays with an Open Pluggable Specification slot accept a swappable compute module (80-pin JAE connector, 180×119×30 mm, x86 and ARM modules from 9+ makers; IBASE's IOPS-602 explicitly runs Ubuntu `[vendor page]`). This is "replaceable compute" as an industry standard — 15 years old, still receiving current silicon (Alder Lake-N modules, Giada) — though NEC/Sharp and Panasonic are migrating flagship lines to Intel's newer, thinner-ecosystem SDM standard, so verify slot type per model `[vendor pages, press]`. Not hot-swappable despite marketing: power off, wait 30 s, swap in under 5 minutes `[vendor doc: SMART install guide]`.

**(b) Build-your-own from components.** A known LCD panel (bought by exact model number via Panelook's ecosystem), an HDMI-to-eDP/LVDS controller board ($12–$185, RTD2556/RTD2795-class), a PCAP overlay kit with USB controller ($60–$300 at 21"–27" from Shenzhen sellers; EETI or ILITEK silicon), a Mean Well PSU, and your own enclosure. Every part is individually documented and individually replaceable — the *most* conservable architecture on paper — but the supply chain is hobbyist-grade: board-panel pairings must be tested, not assumed (documented cases of spec-matching boards failing on specific panels `[forum: badcaps.net; mattmillman.com]`), and the classic hardware mistake (backlight driven from the 3.3 V logic rail) physically burns boards `[forum: mattmillman.com]`. Right for one-off pieces and miniatures; buy tested spares of the exact pairing.

---
## 4. Recommended Buying Strategy

**The decision tree:**

1. **Does the work need touch or display only?** Either way, start from Class 1 (dumb monitor). Touch is free to ignore.
2. **Does the work need real-time GPU graphics or AI/vision?** Choose the compute first (§7.4), then the glass. Never let the display's built-in compute dictate the software stack.
3. **Does the enclosure need to be invisible/self-contained?** Only then consider a panel PC (modular x86: Cincoze CDS, AAEON OMNI, OnLogic) or an OPS-slot display at 43"+.
4. **Is it a miniature?** 7"–11.6": Waveshare/Lilliput/GeChic class for prototypes and dioramas; Elo 0764L/1093L or Faytech for museum-bound versions.
5. **Is someone selling you an Android advertising machine?** Only accept it as (a) a sealed MP4-looping appliance, (b) a Geniatech-class documented platform, or (c) a $200 teardown donor.

**Purchasing rules derived from the evidence:**

- **Buy the platform, not the unit.** Prefer vendors whose family spans sizes with the same touch protocol, power scheme, and mounting (Elo open-frame; Faytech open-frame). One spare per size class serves many works.
- **Get it in writing before wiring money.** The three facts no public datasheet provides — exact LCD panel model, exact touch-controller chip, auto-power-on behavior — go in the supplier questionnaire (§11). A vendor who won't answer is itself a data point.
- **Match the date code.** Touch silicon changes within a SKU (Mimo case `[forum]`). When buying spares, buy them in the same order.
- **De-risk the compute separately:** Pi 5 (to ≥Jan 2036), used business SFF PCs (bought as identical spares), N100/Core mini PCs, Jetson Orin (modules to Jan 2032). Archive OS images, project code, and udev/kiosk configs the day the piece ships.
- **Spend the savings on spares.** The delta between an Android AIO and a dumb monitor + Pi buys a spare PSU, a spare touch overlay kit, and an EDID emulator — the parts that actually fail (§14).
- **US buying paths:** Elo via CDW/B&H/Insight; Faytech, Mimo, OnLogic, Beetronics, Waveshare, Lilliput direct with published pricing; Advantech/AAEON/Axiomtek via Mouser/Newark (mostly quote-only); Alibaba/Shenzhen OEMs only after questionnaire responses, samples first, MOQ 1–2 confirmed.

---

## 5. Shortlist: Best Current Units

Scores are from the §9 rubric (max 60). Full data blocks for the leading units; condensed entries after. Prices are July 2026, street/published, and should be re-verified at order time.

### 5.1 Elo 2294L — 21.5" open-frame touch monitor *studio standard candidate*

**Vendor:** Elo Touch Solutions · **URL:** elotouch.com/open-frame-touchscreens · **Price:** ~$573–735 (CDW/resellers) `[reseller listing]` · **MOQ:** 1
**Screen:** 21.5" 1920×1080, 250 nits `[datasheet]` · **Touch:** PCAP 10-pt (TouchPro, spec E330620); SAW/IR variants exist — order PCAP explicitly
**VESA:** 100×100 · **OS:** none (HDMI/DP/VGA in, USB touch out) · **Power:** 12 VDC barrel; cable kits sold as spares `[datasheet]`
**Linux:** vendor-confirmed driverless HID, kernel ≥3.8 `[vendor page]` · **macOS/Windows:** HID plug-and-play `[vendor page]`
**Panel model / touch chip:** not disclosed (Elo in-house COACh ASIC family) — ask via questionnaire · **MTBF:** 50,000 h published `[datasheet]`
**Family:** 0764L 7" / 1064L 10" / 1564L 15.6" / 2094L 19.5" / 2294L / 2494L 23.8" / 2794L 27" / 3263L 32" / 4363L 42.5"
**Warranty:** 3 yr, extendable to 5 · **Auto power-on:** undocumented — confirm `[gap]`
**Evidence quality:** datasheet + vendor support KB · **Score: 52/60**
**Recommendation:** The reference unit for interactive works 21.5" and up. Weakness: no published pricing or panel transparency; strength: the cleanest Linux touch story in the industry and the widest single-vendor size family.

### 5.2 Faytech FT215TMCAPOFHBOB — 21.5" open-frame, high-brightness

**Vendor:** Faytech · **URL:** faytech.us/touchscreen-monitor/capacitive/open-frame · **Price:** $932 published; family 7" $369 / 11.6" $628 / 15.6" $736–861 / 32" $1,899 / 43" $3,231 `[vendor page]` · **MOQ:** 1
**Screen:** 21.5" 1920×1080, **1000 nits**, 100,000 h backlight `[vendor page]` · **Touch:** PCAP 10-pt · **VESA:** 100×100 · **Power:** 12 VDC
**Inputs:** HDMI/DP/VGA + USB touch + RS232 on every family SKU
**Linux:** vendor claims hid-multitouch compatibility for current PCAP line `[vendor page, generic]`; legacy resistive line used EETI eGalax tooling — confirm controller chip per SKU `[gap]`
**Serviceability:** "each component can be replaced without returning the unit" `[vendor page]` · **Warranty:** 2 yr
**Evidence quality:** vendor pages, published pricing; thinner independent Linux evidence than Elo · **Score: 47/60**
**Recommendation:** Best published-price 7"–43" family; the high-brightness option; get written confirmation of the touch chip before fleet purchase.

### 5.3 Mimo M21580C-OF — 21.5" open-frame

**Vendor:** Mimo Monitors · **Price:** $549.99 `[vendor page]` · **Screen:** 21.5" FHD, 250 nits · **VESA:** 75/100
**The differentiator:** explicit **"auto power on after power loss"** and "Linux HID support" in vendor copy — the only vendor documenting outage recovery `[vendor page]`
**Family:** 7" (UM-760), 10.1", 18.5", 21.5", 23.8", 27", 32" — one of the few sources for **18.5"**
**Caveats:** touch controller varies by date code (SiS / eGalax / Microchip observed `[forum]`); macOS needs a $35 driver; one build-quality complaint `[forum]`
**Score: 46/60** · **Recommendation:** first choice where unattended power recovery must be on paper; pin the date code.

### 5.4 OnLogic Tacton TC401 / TN101 — 12.1"/15.6"/21.5" panel PC + matching display-only twin

**Vendor:** OnLogic · **Price:** from $987, self-serve configurator (only industrial vendor with real published pricing) `[vendor page]`
**CPU:** Alder Lake-N → 12th-gen Core i3 · **OS:** Ubuntu 22.04/24.04 tested; Canonical-certified sibling products `[vendor page: ubuntu.com/certified]`
**The clever part:** TN101 is the same glass without compute — a panel-PC family and dumb-monitor family in one industrial design
**Lifecycle:** company publishes PCN archive; sibling product guaranteed to 2035 `[vendor page]` · **Touch caveat:** some SKUs need manual eGalax driver setup on Linux `[vendor page: support.onlogic.com]`
**Score: 47/60** · **Recommendation:** best x86 panel-PC on documentation and pricing transparency; buy TC401 + TN101 pairs to hedge the architecture decision.

### 5.5 Cincoze CV/CS series with CDS — modular panel PC, 8.4"–24", to 1800 nits

**Vendor:** Cincoze · **Price:** quote `[vendor page]` · **OS:** Ubuntu 24.04 listed; RHEL 8 certification on sibling compute `[vendor page; catalog.redhat.com]`
**The differentiator:** **Convertible Display System** — display module and compute module independently field-replaceable; the purest "swap the brain, keep the glass" design surveyed
**Linux evidence:** CNX review of DS-1402 compute (same lineage) on Ubuntu 24.04: works well `[press/review]` · **Warranty:** 3 yr (2 yr LCD/touch)
**Score: 49/60** · **Recommendation:** the panel PC to standardize on if self-contained enclosures become a recurring need.

### 5.6 Geniatech TPC-K3 family — 10.1"–32" Android/Linux ARM panel PCs *best hackable Android platform*

**Vendor:** Geniatech · **Price:** e.g. TPC1560K4 15.6" ~$469, TPC2700 27" ~$549 `[listing]` · **SoC:** RK3568 (K3-3568 board; some 32" variants differ — verify) `[datasheet]`
**OS:** Android 11 + documented Debian/Yocto/Buildroot; **official firmware/downloads portal and published board datasheet with ADB/fastboot documentation** — unique in the signage class `[datasheet: file.geniatech.com K3_3568 spec]`
**HDMI in:** optional add-on board (4096×2160@30, PiP) `[datasheet]` · **RAM:** to 8 GB
**Evidence quality:** datasheet-confirmed — the exception in this market · **Score: 41/60**
**Recommendation:** if a work truly must be a self-contained ARM Android/Linux unit, this is the only vendor family with the documentation to survive ten years. Ubuntu specifically: unofficial; Debian is the documented path.

### 5.7 Waveshare FHD monitor line — 7"–27", the miniature/prototype workhorse

**Vendor:** Waveshare · **Price:** 21.5" $159–369; 27" ~$160; 7"–15.6" $60–200 `[vendor page]`
**Touch:** Goodix GT911 behind a custom USB-HID translator MCU — reliably driverless everywhere; independently reverse-engineered `[datasheet; teardown: github.com/pysco68/waveshare-hid]`
**Docs:** best step-by-step Linux/Raspberry Pi setup instructions of any vendor, including DPMS-disable guidance `[vendor wiki]`
**Caveats:** consumer-grade enclosures; USB/USB-C power on many models; no 32"+; long-term availability of exact SKUs unproven
**Score: 45/60** (long-term suitability capped by build class) · **Recommendation:** the default for dioramas, prototypes, and studio test rigs; for museum-bound miniatures, step up to Elo 0764L/1093L or Faytech 7"/11.6".

### 5.8 Condensed entries

| Unit | Size(s) | Price | Key fact | Score |
|---|---|---|---|---|
| **Elo 0764L** | 7" open-frame | ~$250–350 `[reseller]` | The museum-grade miniature display; same family/touch stack as 2294L | 50 |
| **Advantech IDS-3100/3200 series** | 6.5"–27" | quote | Touch chip *documented* (PenMount 6000 → dedicated `hid-penmount` kernel module) `[datasheet; kernel]`; HDMI often optional | 48 |
| **GeChic T315** | 15.6" | ~$500 | Explicit "designed for 24/7," clearest vendor Linux/Ubuntu/Pi OS claim, 3 yr warranty; family caps at 15.6" `[vendor page]` | 44 |
| **ViewSonic TD3207** | 32" open-frame | ~$730–900 | IP65/IK08, dual VESA, 24/7-rated, retail availability; Linux docs inconsistent across TD line | 42 |
| **Lilliput TK-series** | 7"–21.5" | $229–500 | Vendor-published Pi/Linux compatibility matrix; EETI eGalax (0eef) confirmed — inherits quirks `[vendor page; forum]` | 41 |
| **Beetronics TS7M line** | 7"–27" | $389–899 | 9–36 V locking DC, IP65 metal, 2 yr; macOS needs UPDD driver; one negative ARM/Linux report `[forum]` | 40 |
| **TouchWo / Raypodo / Shining RK3568 AIOs** | 10.1"–43" | $180–600 | Cheapest touch AIOs; ADB/firmware never advertised; HDMI direction per-SKU chaos — **tentative**, questionnaire mandatory `[listing]` | 29–33 |
| **Sunchip AD-C05-RK3566 board** | board only | **$64 @ MOQ 2** `[listing]` | The commodity signage brain itself; ideal teardown/experiment substrate with rkdeveloptool | — |
| **Firefly AIO-3588Q** | board only | $429–899 | RK3588, eDP + HDMI + DP out, widest official OS list (Ubuntu/Debian documented builds) `[vendor wiki]` | — |

---

## 6. Shortlist: Vendors Worth Contacting

**Tier 1 — build the studio standard here:**

| Vendor | Why | Contact for |
|---|---|---|
| Elo Touch | Driverless-HID certainty, 7"–42.5" family, 50k h MTBF, spare-parts SKUs | Panel models per SKU; auto-power-on; PCAP part numbers; education/volume pricing |
| Faytech | Published pricing 7"–43", component repairability, 1000-nit options, NY office | Touch chip per SKU; panel models; spares kits; auto-power-on |
| OnLogic | Ubuntu certification culture, published PCNs, TC401/TN101 twin architecture, Vermont-based | Long-term SKU availability; touch controller identity; fleet quotes |
| Mimo Monitors | Documented auto-power-on + 18.5" coverage | Date-code pinning of touch silicon; volume pricing |

**Tier 2 — specific capabilities:**

| Vendor | Why |
|---|---|
| Cincoze | CDS modular display/compute split |
| Geniatech | Only documented hackable Android signage platform; also OPS/ARM modules |
| Advantech | Documented PenMount touch chain; deep industrial catalog; 10-yr Ubuntu program `[vendor page]` |
| AAEON | OMNI modular panel kits; Jetson-based NIKY line for AI works |
| GeChic | 24/7-rated 11.6"/15.6" units for miniatures |
| Axiomtek | Socketed-CPU GOT models; Mouser availability |
| Hope Industrial | US-made, published pricing, 5-yr warranty, 15"–22" `[vendor page — follow up]` |

**Tier 3 — components and experiments:** Panelook broker network + Crystal Display Systems (UK; panel identification/replacement service) for panels; Xintai Touch (eBay) / ILITEK-based kit sellers for PCAP overlays; Njytouch / e-qstore for HDMI-to-eDP/LVDS controller boards (pre-flashed to your panel model); Sunchip for commodity Rockchip signage boards; Firefly/Radxa/FriendlyElec for RK3588 compute; Mean Well distributors for PSUs.

**Red-flag vendors:** any listing that says "quad-core CPU" without naming the SoC, "HDMI" without direction, or Android version older than 11 in 2026; Hushida and YXD returned near-zero verifiable specs across repeated searches `[unverified]` — treat as opaque until they answer the questionnaire.

---
## 7. Mainboards and SoCs

### 7.1 Rockchip RK3588 / RK3588S — the preferred ARM platform, with open eyes

**Mainline Linux status (mid-2026)** `[official: Collabora blog/gitlab; cnx-software]`:

| Subsystem | Status |
|---|---|
| GPU (Mali-G610) | **Panthor** driver (not Panfrost) since 6.10; Mesa GLES 3.1 conformant; Vulkan improving but **windowed Vulkan still unreliable on Ubuntu images** — GLES/EGL is the safe path |
| Video decode | H.264/H.265 merged (Collabora, into early 2026); multi-core decode, AV1/VP9 still pending |
| Video encode | Not yet mainline `[inferred — gap]` |
| HDMI out | Basic in 6.13; audio ~6.15/6.16; CEC 6.17 |
| **eDP** | **Weakest output** — rides the old rk3399-edp path; native DP lacks audio/HDCP |
| MIPI-DSI | ~6.14 |
| NPU | "Rocket" open driver mainlined July 2025 (RK3588 only) `[official: tomeuvizoso.net]` |
| Boot chain | Nearly fully open (U-Boot/TF-A); DDR-training blob still closed |

**The ecosystem risks, stated plainly:** vendor BSP kernels sit at 5.10/6.1 with no public support SLA; Rockchip publishes no Western-style EOL/PCN commitments (the "longevity program" claim circulating online traces to a marketing article, not Rockchip `[unverified]`); successor chips (RK3668/RK3688) were announced 2025, ~3 years into RK3588's life; and **ubuntu-rockchip, the most popular community Ubuntu for these chips, was archived April 29, 2026** `[confirmed]`. Armbian continues (vendor-kernel and near-mainline branches). **Rule: if you deploy RK3588, archive the exact kernel source, U-Boot, images, and build scripts on studio storage the day you ship, and assume you are your own BSP maintainer by year 5.**

### 7.2 RK3568 — the budget signage default

Adequate for kiosk apps, video, and light interactivity; Mali-G52 uses mature mainline Panfrost; Debian 12 boots it by default `[docs]`. But it's capped around Android 11/12 in shipping products, its NPU has no mainline driver, and it shares all the ecosystem risks above. Fine as a sealed appliance brain; choose RK3588 for anything real-time.

### 7.3 x86 — the longevity anchor

Standard UEFI x86 means stock Ubuntu LTS, mainline kernels forever, no image hunting, TouchDesigner/oF/Max ecosystems, and certified-hardware programs (OnLogic, Advantech, DFI). Caveats: Alder Lake-N *Refresh* SKUs (N97/N150/N250/i3-N355) need kernel ≥6.11 — use 24.04 HWE `[forum, convergent]`; N100-class iGPU is a hard ceiling for shader work (§3.2); Intel "Embedded Options Available" ≈ 7 years — check ARK per SKU, don't trust vendor marketing for N-series longevity `[vendor page: Intel]`.

**Avoid for hackable systems:** Novatek/MStar/SigmaStar appliance chips — encrypted firmware, no public recovery mode, UART-and-service-menu hacking only `[forum/teardown]`. Amlogic: fine as a media player, Windows-only closed flashing tool, weaker signage-Linux story. Allwinner: FEL recovery exists via sunxi community, but thin evidence in this product category — case-by-case.

### 7.4 External compute — the studio menu

| Compute | Price | Graphics/AI | Watchdog | Support horizon | Role |
|---|---|---|---|---|---|
| **Raspberry Pi 5** (8/16 GB) | $130–210 | VideoCore VII, GLES 3.1/Vulkan 1.2, dual 4K60 | `/dev/watchdog` mainline | **Production ≥ Jan 2036, official** `[vendor page]` | Default for video/2D/light-generative; boot from NVMe, not SD |
| **Intel N100/N150 mini PC** | $130–250 | Quick Sync decode; weak 3D | unconfirmed per-SKU `[gap]` | No published commitment; small-OEM risk | Cheap x86 node; verify watchdog before trusting |
| **Used ThinkCentre/OptiPlex/EliteDesk SFF** | $90–250 | CPU-gen iGPU | Dell: documented BIOS watchdog `[docs]` | Buy identical spares up front | Disposable/swappable fleet nodes; factory 24/7-rated |
| **Jetson Orin Nano/NX** | $249+ | CUDA/TensorRT, 67–157 TOPS | `/dev/watchdog` (validate config) | **Modules to Jan 2032, official** `[vendor page]`; devkits excluded | The AI/vision brain |
| **Core-class mini PC / Mini-ITX + discrete NVIDIA** | $400–1500+ | Real GPU headroom | varies | Standard x86 | TouchDesigner-class generative work — the community's own path `[forum]` |
| **Mac mini M4** | $599+ | Excellent under macOS/Metal | — | Asahi Linux M4 = Tier 3/non-production `[official: Asahi]` | macOS-committed pieces only; not a Linux path |

### 7.5 Boards with eDP/LVDS for custom builds

Ranked for documentation and survivability: **Firefly AIO-3588Q / Core-3588J** (eDP 1.3, HDMI, DP; documented Ubuntu/Debian builds; $289–899) → **Forlinx OK3588-C** (native eDP, kernel 6.1 Yocto docs) / **Boardcon** (Android 14/Debian 12 messaging; quote-only) → **Radxa ROCK 5 ITX** (usable eDP, best mainline momentum) → **Sunchip/Geniatech signage boards** (eDP+LVDS+touch headers, $85–250, Android-first — cheapest, riskiest Linux path). Orange Pi 5 and Khadas Edge2 lack usable eDP/LVDS — disqualified where that's the requirement `[vendor docs]`. All share chip-level MaskROM/rkdeveloptool recovery.

---

## 8. LCD Panels, Touch Overlays, and Controller Boards

### 8.1 The panel supply chain has consolidated — plan accordingly

Samsung Display exited LCD in 2020–21; **LG Display sold its last LCD fab (Guangzhou) to TCL CSOT, completed March 2025 (~$1.5 B)** `[press: TrendForce, OLED-Info]`; Sharp is winding down in-house industrial LCD by end-2026 `[press: Data Modul]`. The real supplier set for the next decade: **BOE, AUO, Innolux, CSOT, Tianma** — with AUO deliberately pivoting toward industrial/automotive `[press]`.

### 8.2 Which sizes survive ten years

Panel sizes are baked into fab glass-cut economics (Gen 8.5/8.6 mother glass divides efficiently into 21.5", 23.6–23.8", 27", 31.5") `[industry]`, which is a stronger guarantee than market fashion:

1. **21.5" / 1080p — the safest bet.** Triple-sourced, multi-generation industrial families: BOE MV215FHM-N30/40/60/70; AUO G215HAN01.x (five variants, identical mechanicals, marketed for kiosk/signage); Innolux M215HCA `[datasheet/listings, multiply confirmed]`.
2. **18.5" / 1366×768** — AUO G185XW01/G185HAN01, BOE DV185WHM — the industrial HMI staple.
3. **23.8"** — solid but thinner multi-sourcing in evidence (Innolux V236BJ1 family confirmed) — verify BOE/AUO equivalents when specifying.
4. **27"** — mainstream, thinner formal industrial paper trail.
5. **32" warning:** the dominant commodity 32" open-cell (BOE HV320WHB-N80, 6+ distributors) is **1366×768, not 1080p** — true FHD at 32" is a much less commodity part `[listings]`.
6. **7"–10.1"** — sustained indefinitely by the Raspberry Pi/embedded ecosystem rather than by TV economics.

**Rule: specify and record the industrial part number** (G-/MV-prefix), which carries an explicit vendor lifecycle commitment (AUO publishes a formal industrial EOL process with 12–24 month notices and last-time-buy windows `[vendor page: AUO]`) — the consumer SKU of the same glass does not. **Single-unit sourcing:** Panelook (identify + find compatible alternates) → Crystal Display Systems (identification/replacement service, 3"–82"), AGDisplays drop-in service, Kingtech/DisplayModule (no-MOQ), then eBay/AliExpress for commodity numbers ($45–190 bare panels at 18.5"–23.8"). Panelook does not reliably list connector pitch — check the panel datasheet before pairing (0.4 vs 0.5 mm eDP connectors) `[docs]`.

### 8.3 Touch controllers and Linux — the honest hierarchy

All modern USB PCAP rides `hid-multitouch` → evdev → libinput. Reliability tiers from kernel and field evidence:

| Tier | Controllers | Evidence |
|---|---|---|
| Plug-and-play, clean record | **ILITEK** (ILI2511/2510/2531; dedicated kernel support since 2013, clean HID VID 222A), **Elo TouchPro/COACh** (vendor-stated kernel ≥3.8), **PenMount** (dedicated `hid-penmount`), **Goodix-over-USB** | `[kernel; datasheet; vendor page]` |
| Works, with history | **EETI eGalax modern PCAP** — functional via hid-multitouch, but two decades of quirk patches (`HID_QUIRK_NOGET`; new quirk class still landing Feb 2026); stable VID 0eef, unstable PIDs | `[kernel; forum]` |
| Avoid | Legacy eGalax **resistive** (raw ADC coordinates, xinput_calibrator era); anything with a proprietary Windows-only driver | `[forum]` |

**macOS is the weak link for touch:** no native touchscreen support; EETI's driver is a kext (hostile territory on Apple Silicon secure boot); userspace translators (Touch-Up, osxhidtouch) are the durable fallback `[docs/forum]`. Another argument for Linux playback machines.

**Overlay kits (for custom builds and repairs):** single-unit PCAP overlay+USB-controller kits are a real, persistent commodity — Xintai Touch (eBay): 21.5" $230, 27" $250 with EETI silicon; AliExpress from ~$63 at 22"; Western B2B equivalents 3–4× (Obeytouch 23.8" ILITEK, $950) `[marketplace, fetched]`. Generic controllers sense through ~1.1–4 mm of glass; document your total glass+air-gap stack so future replacements can actually read through the artwork's glazing `[industry]`. Air-gap perimeter bonding is the DIY method; optical bonding is not.

**Goodix I²C sensors** need a $9–14 I²C-to-USB bridge to become HID — stock two as insurance `[marketplace]`.

### 8.4 HDMI-to-eDP/LVDS controller boards

The panel-revival path: match panel model on Panelook → buy a pre-flashed board from **Njytouch** (emails firmware to your panel number) or **e-qstore** (separate LVDS and eDP kit lines) `[vendor/forum: mattmillman.com]`. Chips: RTD2556 (HDMI→LVDS/eDP 1080p-class, $12–32), RTD2795 (HDMI 2.0/DP→4K eDP, $80–185), RTD2660/2662 "PCB800099" family (LVDS/TTL legacy, open programmer tooling). Known failure modes, all documented in the field: **backlight wired to the 3.3 V logic rail overheats the board** (fit a separate backlight supply); LVDS vs eDP are electrically incompatible despite similar connectors; firmware/EDID mismatch is the standard "no signal" cause; and **a spec-matched board is not guaranteed to drive a spec-matched panel — test the exact pairing you intend to keep as a spare** `[forum: badcaps.net, mattmillman.com, Hackaday.io]`.

---

## 9. Hackability and Serviceability Scoring

Each candidate scored 1–5 across twelve categories, total /60. For Class-1 dumb monitors, two categories are interpreted for the class: *SoC transparency* → scaler/touch-controller transparency, and *Android hackability* → freedom from firmware dependence (no OS to lock = high score).

| Category | 1 | 3 | 5 |
|---|---|---|---|
| SoC / controller transparency | Unknown | Named vaguely | Exact chip and board model known |
| Linux support | None | Possible, unofficial | Official/vendor-documented |
| Android hackability / firmware independence | Locked appliance | ADB may work | Firmware+ADB+recovery documented, or no firmware dependence at all |
| External input | None | Output only | HDMI in + USB touch / standard display mode |
| Touch compatibility | Unknown/proprietary | Works on Android | USB HID on Linux/macOS/Windows |
| Internal serviceability | Sealed | Openable, undocumented | Modular, replaceable parts |
| Panel transparency | Unknown | Brand known | Exact model known |
| Compute replaceability | Impossible | Surgery | Designed for external/replaceable compute |
| Documentation | Marketing only | Partial | Full manual/firmware/diagrams |
| Vendor reliability | Unknown reseller | Responsive supplier | Established industrial vendor |
| Multi-size family | One-off | Similar units | Same platform across sizes |
| Long-term artwork suitability | Risky | Usable w/ caveats | Strong candidate |

Bands: **50–60 studio standard candidate · 40–49 good with caveats · 30–39 simple playback only · <30 avoid** (unless the enclosure is uniquely valuable).

## 10. Product Comparison Table

| Unit | Class | Sizes | Price | Linux touch | HDMI in | Panel known | Chip known | Family | Score | Band |
|---|---|---|---|---|---|---|---|---|---|---|
| Elo 2294L (open-frame family) | 1 | 7–42.5" | $573–735 | vendor-confirmed HID | ✔ | ✘ | partial (COACh) | ★★★ | **52** | Studio standard |
| Elo 0764L | 1 | 7" | ~$300 | vendor-confirmed HID | ✔ | ✘ | partial | ★★★ | **50** | Studio standard |
| Cincoze CV/CS + CDS | 2 | 8.4–24" | quote | Ubuntu listed; some driver installs | n/a | ✘ | ✔ (x86) | ★★ | 49 | Good w/ caveats |
| Advantech IDS-3100/3200 | 1 | 6.5–27" | quote | PenMount kernel module | ✔ (opt) | ✘ | ✔ (PenMount) | ★★ | 48 | Good w/ caveats |
| Faytech open-frame | 1 | 7–43" | $369–3231 | claimed HID, thin evidence | ✔ | ✘ | ✘ | ★★★ | 47 | Good w/ caveats |
| OnLogic Tacton TC401/TN101 | 2 | 12.1–21.5" | $987+ | Ubuntu tested/certified culture | TN101 ✔ | ✘ | ✔ (x86) | ★★ | 47 | Good w/ caveats |
| Mimo M-series OF | 1 | 7–32" | $549 (21.5") | vendor-claimed HID | ✔ | ✘ | varies by date code | ★★★ | 46 | Good w/ caveats |
| Waveshare FHD line | 1 | 7–27" | $60–370 | best-documented, GT911+HID | ✔ | partial | ✔ | ★★ | 45 | Good w/ caveats |
| GeChic T315/T131A | 1 | 11.6–15.6" | ~$500 | explicit vendor claim | ✔ | ✘ | generic | ★ | 44 | Good w/ caveats |
| ViewSonic TD3207 | 1 | 15.6–32" | $730–900 | inconsistent docs | ✔ | ✘ | ✘ | ★★ | 42 | Good w/ caveats |
| Geniatech TPC-K3 | 2/3 | 10.1–32" | $469–549 | Debian documented | optional | ✘ | ✔ (RK3568) | ★★★ | 41 | Good w/ caveats |
| Lilliput TK | 1 | 7–21.5" | $229–500 | vendor matrix; eGalax | ✔ | ✘ | ✔ (eGalax) | ★★ | 41 | Good w/ caveats |
| Beetronics TS7M | 1 | 7–27" | $389–899 | mixed; macOS driver req'd | ✔ | ✘ | weak | ★★ | 40 | Good w/ caveats |
| TouchWo/Raypodo/Shining RK AIOs | 3 | 10.1–43" | $180–600 | unknown | per-SKU chaos | ✘ | ✔ (listing) | ★★ | 29–33 | Playback only / avoid |
| Unknown-SoC "quad-core" ad machines | 3 | any | cheap | unknown | usually ✘ | ✘ | ✘ | — | <25 | **Avoid** |

---
## 11. Supplier Questionnaire Results

**Status: no supplier correspondence has been sent yet.** This section holds the instrument and what public documentation already answers; Appendix C is the log for responses as they arrive (with dates). What the public record already establishes: Elo confirms driverless PCAP HID on Linux ≥3.8 but discloses neither panel models nor auto-power-on behavior; Faytech publishes prices and repairability language but not chip identities; Mimo uniquely documents auto power-on; Geniatech is the only signage OEM with published board datasheets and a firmware portal; no Shenzhen AIO vendor advertises ADB or firmware access at all. Everything else below must be asked.

**The questionnaire** (send before purchasing any unit; file answers with date in Appendix C):

```text
Hello,

I am evaluating this display for a long-term interactive media installation.
Could you please confirm the following technical details?

 1. What is the exact CPU / SoC model (e.g., RK3568, RK3588)? [skip for monitors]
 2. What is the Android version, and do you provide OS updates? [skip for monitors]
 3. Can ADB / Developer Options be enabled? Is the bootloader locked?
 4. Can you provide the factory firmware image? Is there a USB OTG /
    MaskROM recovery path for reflashing?
 5. What is the exact mainboard model number?
 6. What is the exact LCD panel model number (the label on the LCD module)?
 7. Does the LCD use eDP, LVDS, MIPI, or another internal interface?
 8. What is the touch-controller model (chip, not brand)?
 9. Does the touch panel appear as a standard USB HID device? Does it work
    on Ubuntu Linux and macOS without drivers?
10. Does the unit have HDMI input (not output)? Full-screen, or PiP/capture?
11. Can the display work as a normal HDMI monitor with USB touch?
12. Can the internal Android/compute board be removed or replaced?
13. Do you sell replacement mainboards, power supplies, touch overlays,
    and controller boards as parts?
14. Does the unit power on automatically after AC power loss, with no
    button press? Is there any sleep/standby behavior when signal drops?
15. Can you provide internal photos of the unit?
16. Is this model available in other screen sizes on the same mainboard
    and touch platform?
17. What is the warranty, and how long will this model or compatible
    replacement parts remain available?
18. For Linux-capable units: which distribution and kernel version do you
    ship or test, and do you publish the kernel source / device tree?
```

Questions 14 and 18 extend the base instrument for the studio's unattended-installation and Ubuntu requirements.

---

## 12. Teardown Findings

**Status: no studio teardowns performed yet** — this section reports published teardown evidence; the inspection protocol for units the studio acquires is Appendix D.

**The rebrand economy, documented.** Sunchip (Shenzhen) openly operates as the ODM behind many brands; an FCC filing (2ALNC-CX968) names Sunchip as manufacturer of a device retailed under another brand, and a CNX teardown traced a Ugoos-branded box to Sunchip via its MAC OUI `[teardown/press]`. The Armbian ELC WF8382T thread showed generic Firefly-RK3288 dev-board U-Boot booting a commercial signage tablet unmodified `[forum: forum.armbian.com/topic/36417]` — these boards are lightly skinned Rockchip reference designs. iFixit's generic "Kingbox" teardown found commodity parts throughout, including memory recycled from a Galaxy S3 `[teardown: ifixit.com]`. Conclusion: the brand on the bezel identifies the enclosure vendor, not the engineering.

**What's inside the monitors.** No independent Elo teardown exists (a gap); what is documented is that Elo sells no components and services by whole-unit RMA only `[vendor page]` — spares strategy: buy whole spare units. Signage-CMS industry sources consistently describe cheap Android ad-machines as consumer TV-box reference boards ($40–90 BOM) in metal cases `[industry blogs, convergent]`.

**Power supplies fail first, and famously.** The 2004–2010 capacitor-plague evidence base (Samsung 2x6BW-series, ViewSonic VX-series, Dell, Acer — bulging CapXon electrolytics, flicker-then-fail) remains the clearest teardown literature on display mortality `[forum/teardown: badcaps.net, hardforum, s-config]`. The physics hasn't changed: heat kills electrolytics; every 10 °C cooler roughly doubles capacitor life (Arrhenius approximation, confirmed by Cornell Dubilier's IEEE paper and Mean Well's own FAQ `[datasheet/docs, fetched]`). Replacement doctrine: Nichicon/Panasonic/Rubycon 105 °C low-ESR; or better, socket a Mean Well-class external supply from the start.

**Generic driver boards: the pairing is the product.** Multiple independent sources document spec-matched controller boards failing on spec-matched panels due to undisclosed firmware/timing differences `[forum: badcaps.net; mattmillman.com]`. The actionable finding: **a "spare" is a tested board+panel pairing, not a part number on a shelf.**

---

## 13. Recommended Studio Configurations

Common software base for all Linux configurations (the **studio player image**): Ubuntu LTS (or Debian stable) · **Cage** or **Weston kiosk-shell** compositor (single fullscreen app, no window management; Weston when multiple outputs need app pinning, plus `weston-touch-calibrator` for persistent touch→output mapping) · systemd unit with `Restart=always`, `WatchdogSec=` + `sd_notify` heartbeat, and `RuntimeWatchdogSec=` driving the hardware watchdog · **overlayroot** read-only root filesystem (power-cut immune; updates via commit-and-reboot maintenance window) · DPMS/idle disabled (`idle-time=0` in weston.ini; no idle daemon under Cage) · Chromium pieces add `--kiosk --noerrdialogs --autoplay-policy=no-user-gesture-required --disable-session-crashed-bubble --incognito` `[docs/community, §7 sources]`. BIOS/firmware set to **power on after AC loss**. Archive the image per-artwork.

### 13.1 Simple Looping Video

**Glass:** commodity commercial display or Elo/Faytech monitor (no touch needed) · **Compute:** Raspberry Pi 5, NVMe boot, `mpv --loop` under Cage or the hardware-decode path via GStreamer · **Or**, where a sealed single object is required: an RK3568 Android unit *used strictly as an appliance* (USB-stick MP4 autoplay), accepted as disposable. Inline EDID emulator; brightness at 60–80%. Budget ≈ $150 compute + display + $60 emulator + spare PSU.

### 13.2 Interactive Touch Artwork

**Glass:** Elo 2294L/2494L (or Faytech high-brightness where sunlight matters) · **Compute:** Pi 5 for 2D/web interactivity; N100/Core mini PC for heavier logic · Touch arrives as HID; map to output persistently (Weston calibrator or `LIBINPUT_CALIBRATION_MATRIX` udev rule; on X11, scripted `xinput map-to-output`) · Verify multi-touch and calibration on Ubuntu *and* macOS at acceptance testing (Appendix D). Spares: one identical monitor per size class, same date code.

### 13.3 Generative Real-Time Video

**Compute first:** Mini-ITX or Core-class mini PC with discrete NVIDIA GPU for TouchDesigner/openFrameworks-class work (the community-standard path `[forum]`); Arc Xe-LPG-class iGPU (ASUS APC-125U, Arrow Lake-U) only for moderate loads; RK3588 only if the piece targets GLES 3.1 specifically and the studio accepts BSP stewardship (§7.1) · **Glass:** any §5 monitor · Watchdog + auto-login + app-restart supervision are mandatory; GPU driver version pinned and archived.

### 13.4 AI / Vision-Enabled Installation

**Compute:** Jetson Orin Nano/NX (CUDA/TensorRT; modules supported to Jan 2032; buy the *module + carrier*, not the devkit, for museum-bound work `[vendor page]`) · JetPack version pinned and archived; camera pipeline documented (sensor model, lens, mount) with a spare camera purchased at build time · **Glass:** per §5; miniature works pair Orin with the 7"–11.6" tier. Plan one JetPack migration mid-life.

### 13.5 Long-Term Museum Installation

Everything above, plus the conservation layer — this is where the studio's museum experience (Met TBM, MoMA media conservation, Guggenheim CCBA practice) becomes procedure:

1. **Identity vs. iteration documentation** (Met model): one report for what the work *is*; one per installation instance for the equipment actually used.
2. **Equipment significance rating** (Guggenheim/Phillips 1–3) per component, agreed and written down: is this display *dedicated* (its look is the work), or *substitutable* (any 21.5" 1080p panel will do)? This single judgment drives the spares budget.
3. **The build-time archive:** panel model (from the LCD module label, not the product SKU), touch-controller chip, mainboard/scaler model, **EDID binary dump**, firmware images, OS image, source code + toolchain, udev/kiosk configs, wiring photos, PSU model, glass-stack thickness, and a one-sentence fallback plan ("if this display becomes unobtainable, acceptable substitute is ___").
4. **Spares locker per work:** 1–2 identical displays (same date code) or panel+controller tested pairings; 2× PSU; 1× touch overlay kit; EDID emulator; the compute unit ×2. Matters in Media Art's equipment condition report template is the base form `[museum source: mattersinmediaart.org]`.
5. **Signal-format risk is separate from hardware risk** — record what the source *expects* (resolution, EDID, HDCP posture), the lesson of works stranded by protocol death rather than hardware death `[museum source: Smithsonian TBMA]`.

### 13.6 Miniature / Diorama Displays (real-time cinema class)

The 7"–11.6" tier for camera-and-miniature works: **prototype** on Waveshare 7"/10.1" HDMI-touch panels (GT911→HID, best setup docs, $60–150) driven by Pi 5; **exhibit** on Elo 0764L/1093L or Faytech 7"/11.6" (industrial PSU, VESA, warranty). Where the display must be embedded in the model itself: bare panel + RTD-class controller board, pre-flashed by Njytouch to the exact panel — buy the pairing twice, test both (§8.4). Beware USB-C-powered consumer panels' sleep behavior; barrel-DC industrial units with documented no-signal behavior are worth the premium in any unattended diorama.

---

## 14. Risks and Failure Modes

**Risk matrix** (likelihood × impact for a ten-year installation):

| Risk | Likelihood | Impact | Classes | Mitigation |
|---|---|---|---|---|
| PSU electrolytic capacitor failure | **High** (yrs 3–7) | Medium (repairable) | all | Mean Well-class PSU; 105 °C caps; thermal headroom; spare PSUs on shelf |
| Backlight decay to L70/L50 | **Certain** (math below) | Medium | all | Derate brightness 60–80%; industrial 70–100 kh panels; ambient-light dimming |
| Vendor discontinues exact SKU | High | Low–High (per significance rating) | all | Family-level standardization; last-time-buy on EOL notices; §13.5 archive |
| Android firmware abandonment | **Certain** | High if OS-coupled | 3 | Don't couple the artwork to the built-in OS; appliance-use only |
| Community distro abandonment (ARM) | High (precedent: ubuntu-rockchip, 2026) | High | 2(ARM), 3 | x86 or Pi for compute; archive BSP sources; assume self-maintenance |
| Touch controller quirk/regression | Medium | Medium | 1, 2 | ILITEK/Elo/PenMount tier; pin kernel; test on the actual image; spare overlay kit |
| HDMI/EDID handshake failure | Medium | Medium (looks like total failure) | all | **Inline EDID emulator with documented profile**; simple signal chain; display-before-source power sequencing |
| Power-cut boot failure | Medium | High (unattended) | all | BIOS auto-power-on verified; overlayroot; watchdog chain (§13) |
| LCD image retention / OLED burn-in | Low (LCD, reversible) / High (OLED, permanent) | Low / High | all | LCD for static-leaning content; pixel-shift/content rotation; treat OLED as consumable |
| Panel model extinct at repair time | Medium (size-dependent) | High | all | 21.5"-class sizing where possible; industrial part numbers; Panelook-alternates file in the archive |
| macOS touch driver breakage | High (kext deprecation) | Medium | 1 | Linux playback machines; userspace HID translators as fallback |
| HDMI-in on Android units is PiP/capture | High | Medium (latency/HDCP) | 3 | Don't design around signage HDMI-in; use Class 1 glass |

**The backlight math** (years to half-brightness, L50): a 30,000 h budget panel run 24/7 crosses L50 in **3.4 years**; 50,000 h in 5.7; 70,000 h industrial in 8.0; 100,000 h in 11.4. At 12 h/day these double `[datasheet-derived]`. Derating brightness pushes every figure right — the single highest-leverage, zero-cost longevity act.

**Mitigations ranked by impact-per-effort:** (1) brightness derating; (2) LCD over OLED for static content; (3) ventilated enclosures + cheap logged temperature sensor; (4) industrial panels + name-brand PSUs; (5) spares purchased at build time, not at failure time; (6) inline EDID emulator; (7) content-layer pixel-shift/rotation; (8) simple signal chain with documented power sequencing.

---

## 15. Final Recommendations

**Best overall studio standard — the architecture, not a product:** industrial HDMI/USB-HID PCAP touch monitors + external replaceable compute + the §13 studio player image + the §13.5 conservation archive. Vendor pairing: **Elo open-frame** where driverless-touch certainty and warranty matter most (21.5"–42.5" public-facing works), **Faytech open-frame** where published pricing, brightness, and the 7"–43" span matter, with **Mimo** filling 18.5" and documented auto-power-on needs.

**Best dumb touch display:** **Elo 2294L** (21.5", score 52) and its family siblings; runner-up **Faytech FT215TMCAPOFHBOB** for high-brightness contexts.

**Best hackable Android signage unit:** **Geniatech TPC-K3 family** (RK3568, 10.1"–32") — the only signage platform with published board datasheets, a firmware portal, and documented ADB/multi-OS support. Honorable mention at the board level: Sunchip RK3588/RK3566 boards for experiments, via MaskROM/rkdeveloptool.

**Best panel PC:** **OnLogic Tacton TC401/TN101** (Ubuntu documentation, published pricing, display-only twin) for standard duty; **Cincoze CDS** where modular compute-swap is decisive; **ASUS APC-125U / Shuttle Arrow Lake-U** where iGPU headroom is needed in one enclosure.

**Best low-cost experiment:** a **$64 Sunchip AD-C05-RK3566 board** (MOQ 2) plus any $180–250 TouchWo/Raypodo 21.5" AIO as a teardown donor — together they teach the entire signage-market anatomy for under $350. On the monitor side, **Waveshare's 21.5" FHD touch ($159–369)** is the studio-bench workhorse.

**Avoid list:** unknown-SoC "quad-core" advertising machines; anything with no HDMI input *and* no ADB *and* no firmware; Novatek/MStar/SigmaStar-based smart panels for any hackable purpose; OLED for static content unless budgeted as a consumable; Mac mini as a *Linux* platform (Asahi M4 non-production); sole-sourcing any artwork's survival on a community ARM distro (the ubuntu-rockchip lesson); consumer USB-C-powered panels in unattended installations; 32" designs that silently assume commodity 1080p panels; and any vendor who refuses the §11 questionnaire.

**Hypothesis verdicts, in full:**

1. **Commodity assembly — supported.** Teardowns (Kingbox, ELC), FCC records, ODM self-description, and BOM-level industry commentary all agree: panel + touch overlay + Rockchip board + generic PSU + folded metal `[teardown/forum/industry]`.
2. **Rebrand hypothesis — supported (moderate–strong).** One directly confirmed cross-brand case (Sunchip→Ugoos via MAC OUI), FCC ODM filings, reference-design U-Boot booting commercial units, recurring OEM prefixes across brands. Not yet an exhaustive brand→board map; no side-by-side PCB match published `[teardown/forum]`.
3. **Rockchip > appliance chips — supported.** Silicon-level MaskROM recovery + open `rkdeveloptool` + firmware forums versus MStar's encrypted images and service-menu archaeology. Caveat carried through this guide: *recoverable ≠ rehostable* — device trees and touch drivers stay board-specific `[docs/forum]`.
4. **Dumb monitor + external compute wins — strongly supported.** HDMI-in remains rare on signage (2026 flagship counter-example confirmed `[teardown/review]`); Android versions freeze at purchase; museum conservation practice independently arrives at the same decoupling logic. This is the guide's central recommendation.
5. **The ideal multi-size family — partially supported.** Elo (7"–42.5") and Faytech (7"–43") each come close with consistent touch/power/mounting; no single vendor also delivers panel transparency, auto-power-on documentation, and published pricing at once. The durable move is standardizing on the *protocol stack* — HDMI + USB-HID PCAP + VESA + 12–24 V DC — which every Tier-1 vendor speaks.

---

## Appendix A: Product Pages and Datasheets

- Elo open-frame: elotouch.com/open-frame-touchscreens · 2294L datasheet: docs.elotouch.com/Elo_2294L.pdf · Linux PCAP KB: elosupport.elotouch.com (article 31649725511447)
- Faytech open-frame: faytech.us/touchscreen-monitor/capacitive/open-frame · 21.5" HB product page: faytech.us/product/ft215tmcapofhbob…
- Mimo: mimomonitors.com/products/21-5-inch-m21580c-of-open-frame-display
- GeChic: gechic.com/en/t315-touch-monitor · gechic.com/en/t131a-touch-monitor/spec
- Lilliput Pi compatibility: lilliputdirect.com/raspberry_pi_compatible
- Waveshare: waveshare.com/21.5inch-fhd-monitor.htm · GT911 datasheet: files.waveshare.com/wiki/common/GT911_EN_Datasheet.pdf
- Advantech: advantech.com/en/products/ubuntu-lts-os · IDS monitor series pages
- OnLogic Tacton: onlogic.com/store/computers/panel-pc/tacton · Ubuntu certification: ubuntu.com/certified (OnLogic, Advantech, DFI vendor pages)
- Cincoze: cincoze.com (CV/CS, CDS) · RHEL listing: catalog.redhat.com/hardware/system/detail/134917
- Geniatech: shop.geniatech.com · K3-3568 spec: file.geniatech.com/thcdownloads/geniatech/specification/K3_3568_Specification_en_V1.0.pdf · APC3588: file.geniatech.com/download/APC/APC3588_Specification_V0.8_EN.pdf
- Sunchip boards: sunchip-tech.com/products (AD-C05-RK3566, RK3588 board)
- Firefly: en.t-firefly.com (AIO-3588Q) · wiki.t-firefly.com (Ubuntu/Debian build guides)
- Forlinx: forlinx.net/product/rk3588-som-134.html · Radxa ROCK 5 ITX: radxa.com/products/rock5/5itx
- ViewSonic TD3207, Beetronics, Xenarc, Winmate, AAEON OMNI, Axiomtek ITC241, Kontron FlatClient, ASUS APC-125U, Shuttle P21AR01: vendor product pages per §5/§6 (full URL set in the research files)
- Panel references: panelook.com (MV215FHM, G215HAN01, V236BJ1, HV320WHB-N80 family pages) · AUO industrial EOL policy: auo-lcd.com

## Appendix B: Firmware, Drivers, and Software

- Rockchip flashing: github.com/rockchip-linux/rkdeveloptool · MaskROM guides: wiki.kobol.io/helios64/maskrom, Firefly/Radxa wikis · Windows RKDevTool via vendor wikis
- Rockchip mainline status: gitlab.collabora.com/hardware-enablement/rockchip-3588/notes-for-rockchip-3588 · Panthor: collabora.com blog · NPU "Rocket": blog.tomeuvizoso.net
- Armbian: armbian.com (vendor + edge branches) · ubuntu-rockchip post-mortem: jeffgeerling.com/blog/2024/popular-rockchip-sbc-distro-limbo-after-maintainer-burns-out · archived repo: github.com/Joshua-Riek/ubuntu-rockchip
- Touch on Linux: kernel `hid-multitouch` docs: docs.kernel.org/input/multi-touch-protocol.html · libinput: wayland.freedesktop.org/libinput · ArchWiki Multitouch Displays · EETI eGTouch Linux guide (v2.5o PDF) · eGalax kernel quirk history: Launchpad #625511, patchew.org (Feb 2026 series)
- Kiosk stack: Cage (hjdskes/cage) · Weston kiosk-shell + weston-touch-calibrator · Ubuntu Frame/Core (10-yr maintenance) · overlayroot · Raspberry Pi OS overlay FS (raspi-config)
- macOS touch fallbacks: github.com/shueber/Touch-Up · github.com/daniel5151/osxhidtouch
- Lifecycle statements: raspberrypi.com (obsolescence statements; Pi 5 ≥ Jan 2036) · developer.nvidia.com/embedded/lifecycle (Orin → Jan 2032) · Intel ARK "Embedded Options Available" flags
- Controller-board resources: mattmillman.com/info/lcd (RTD board series) · Hackaday.io "All About Laptop Display Reuse" · Njytouch: njytouch.com · badcaps.net display forum
- Conservation: mattersinmediaart.org (equipment condition report template) · tate.org.uk Tate Papers 3 (Laurenson 2005) · metmuseum.org TBM working-group documentation · mediaconservation.io · tbma.si.edu/hardware-obsolescence

## Appendix C: Supplier Correspondence Log

*Empty as of July 2026 — populate with dated responses to the §11 questionnaire.*

| Date sent | Vendor | Model | Date answered | Panel model | Touch chip | Auto power-on | Firmware | Parts sold | Notes |
|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | |

## Appendix D: Teardown / Inspection Checklist and Testing Protocol

**Exterior:** front/rear photos · port cluster · power input · VESA pattern · ventilation · build quality · cable access.
**Software (Android units):** Android/kernel/build versions · Developer Options? · ADB? · unknown APKs installable? · launcher replaceable? · kiosk mode disable? · video loop on boot? · custom app auto-launch?
**Interior (photograph everything):** mainboard + markings · SoC marking · RAM/flash markings · **LCD module sticker (the panel model — the single most valuable photo)** · touch controller board · PSU board + capacitor brands · cooling · internal USB headers · eDP/LVDS/MIPI cable · HDMI/input board · whether the compute board removes cleanly.
**External-compute test:** HDMI-in from Mac / Pi / Linux box · USB touch on macOS, Ubuntu, Pi OS · calibration accuracy · multi-touch count · **auto power-on after cord pull** · boots to last input? · any sleep/power-save on signal loss? · EDID reported (save `edid-decode` output).

**Three-mode testing protocol for serious candidates:**
*Mode 1 — built-in playback:* MP4 from USB and internal storage; loop seams; auto-start after power cycle; 24-hour soak; codecs; audio path; burn-in behavior.
*Mode 2 — custom Android app:* APK sideload; ADB; launcher replacement; boot auto-launch; immersive fullscreen; touch latency; network and local-file access.
*Mode 3 — external compute (weight this most):* HDMI input from Mac/Pi/Jetson/Linux; HID touch verification (`libinput debug-events`, `dmesg | grep -i hid`); power-recovery behavior; EDID sanity; brightness/OSD control; multi-day stability soak.

## Appendix E: Glossary

**ADB** Android Debug Bridge — USB/network shell into Android. **AOSP** Android Open Source Project (no Google services; no Google OTA pipeline). **BSP** Board Support Package — vendor's kernel + bootloader fork. **Cage/Weston** Wayland kiosk compositors. **eDP / LVDS / MIPI-DSI** internal panel-to-board interfaces (modern / legacy / phone-class respectively; electrically incompatible). **EDID** display's self-description read over HDMI/DP; emulators pin it. **HID** USB Human Interface Device class — driverless input. **hid-multitouch** the Linux kernel driver for HID touch digitizers. **L50/L70** backlight hours to 50%/70% of original brightness. **MaskROM** Rockchip silicon-level recovery mode; always answers. **MOQ** minimum order quantity. **OPS/SDM** slot-in replaceable compute standards for commercial displays. **Open frame** monitor sold as bare metal chassis for integration. **Panelook** the LCD industry's panel-model database. **PCAP** projected-capacitive touch. **PCN** product change notification. **rkdeveloptool** open-source Rockchip flasher. **RTD2556/2795** Realtek scaler chips on HDMI→eDP/LVDS boards. **SoC** system-on-chip. **VESA mount** 75/100/200 mm screw pattern.

---

*Research base: five parallel investigation streams (touch monitors; Android signage; panel PCs; SoCs/boards/compute; panels/components/conservation), 200+ sources consulted July 2026, spot-verified on load-bearing claims (Pi 5 longevity, Jetson lifecycle, ubuntu-rockchip archival, LG Display fab sale). Companion research file: `panel-pc-buying-guide.md`. Evidence labels mark the boundary between what is known and what a supplier must still confirm — keep that boundary honest as the document ages.*
