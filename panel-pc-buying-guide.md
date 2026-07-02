# Industrial Panel PCs for Media-Art Installations — Research Report

**Prepared for:** technical buying guide, media-art studio requirement: Ubuntu/Linux, 10-year serviceability, real-time graphics (openFrameworks/TouchDesigner-class)
**Research date:** July 2, 2026
**Method note:** Compiled from 5 parallel research passes (60+ searches, mix of direct page fetch and search-snippet extraction — web_fetch was rate-limited for large stretches, so many facts are `[vendor page — via search snippet]` rather than fully-verified `[datasheet]`. Every claim below carries an evidence label; treat `[unverified]`/`[inferred]` items as needing a direct vendor RFQ before purchase.

---

## 0. Executive summary / top-line recommendation

- **No single vendor wins on all axes.** The studio has to trade off between (a) formal Ubuntu certification, (b) genuinely modular/replaceable compute, (c) explicit long lifecycle commitments, and (d) GPU headroom for real-time graphics. Few vendors score high on all four.
- **For serviceability + Linux together, the strongest combination is Cincoze CDS, AAEON OMNI, or DFI's box+panel split architecture** — all let you swap the compute module without replacing the glass, which is the real lever for 10-year survival (CPUs go obsolete; touch panels/bezels/mounts don't need to).
- **For GPU headroom**, none of the classic "panel PC" vendors are good enough for serious TouchDesigner/openFrameworks work out of the box — their Intel N-series/Alder-Lake-N iGPUs are explicitly considered inadequate by the TD community for "intensive graphics." Shuttle's Arrow Lake-U and ASUS IoT's Meteor Lake (Arc Xe-LPG) panel PCs are the strongest iGPU options found; anything requiring real discrete-GPU-class performance points back to custom Mini-ITX builds or OPS/SDM modules paired to a display, not an off-the-shelf sealed panel PC.
- **RK3588 ARM panel PCs are not yet a safe bet for Ubuntu-based real-time graphics**: Vulkan windowed rendering isn't reliably supported on RK3588 Ubuntu images as of mid-2026, and the most popular community Ubuntu build for RK3588 (Joshua-Riek/ubuntu-rockchip) was archived/discontinued in April 2026. OpenGL ES 3.1 is the safe, functional path.
- **OPS is a legitimate longevity strategy** — an open, 15-year-old, multi-vendor standard, with modules shipping in current silicon (Alder Lake-N, some Alder-Lake-P) as of 2025. But several major signage vendors (NEC/Sharp, Panasonic, DynaScan) are visibly migrating new flagship lines to SDM/OMI, so OPS should be treated as "good today, verify per-model going forward," not a permanent guarantee.
- **The media-art/TouchDesigner community has essentially no track record with industrial panel PC brands.** Their default hardware vocabulary is consumer/prosumer mini-PCs (NUC, Zotac, Beelink) or custom Mini-ITX builds with discrete NVIDIA GPUs — not Advantech/AAEON/Cincoze. The studio would be an early adopter of this category within their peer community.
- **Best explicit, dated lifecycle commitments**: OnLogic (Factor 101, "guaranteed until 2035") and DFI (EC70A-TGU, "availability until Q3 2035") are the only two vendors found with concrete dated SKU-level guarantees rather than generic "10 years" marketing language.

---

## 1. x86 Panel PCs — Vendor-by-Vendor

### Advantech (PPC series)
- **Models in range:** PPC-3151W/3151SW (15.6" FHD), PPC-415W/PPC-421W (15.6"/21.5", refreshed with **13th Gen Intel Core**, 2024-2025), PPC-321SW-ADL_N (21.5", Alder Lake-N), PPC-3120/3120S (12.1", Atom E3940). [vendor page — search snippet]
- **CPU:** Atom E3900 → Celeron → Core i3/i5/i7 up to 13th Gen; Alder Lake-N on slim models.
- **Ubuntu/Linux:** Strong, formalized. Advantech runs an **"Ubuntu Total Solutions"/"Embedded Ubuntu Service"** program offering Ubuntu LTS from 16.04 with a stated **10 years of comprehensive support**. Linux touch/GPIO/watchdog drivers published, validated against **Ubuntu Desktop 22.04.3 LTS and 20.04.5 LTS** for named PPC models. Formal Canonical *certification* (ubuntu.com/certified) skews toward IoT gateway products (UNO-2271G, EI-52), not confirmed for PPC panel PCs specifically. [vendor page] https://www.advantech.com/en/products/ubuntu-lts-os/, https://ubuntu.com/certified/vendors/Advantech
- **Pricing:** Quote-based; distributors Newark/element14, Radwell, Industrial Monitor Direct, ProVantage carry specific SKUs but no USD price surfaced in this pass. [distributor page — unconfirmed pricing]
- **Modularity:** SODIMM DDR4 socket, mSATA/M.2/2.5" SATA bay serviceable; CPU generally soldered/fixed (not swappable) on standard PPC-3xxx/4xxx. "PPC-600/400 Scalable" series suggests more expansion but not confirmed as swappable-compute.
- **Fanless:** Yes, predominantly.
- **Touch:** PCAP standard on W-suffix models; resistive on legacy SKUs.
- **VESA:** Yes, VESA 75 confirmed on PPC-3151 family.
- **Lifecycle:** No explicit dated statement for PPC line specifically; general Advantech policy publishes 6-month EOL notice and 5-10yr roadmap guarantee. [vendor page]
- **Power:** Wide-range DC, 9-32VDC typical.
- **Real-world Linux evidence [forum]:** Advantech's own FAQ portal has multiple entries on touch driver installation under Ubuntu (including "how to make touch work at the login page"), indicating touch calibration is a known friction point, not universally plug-and-play. An older Embedlynx blog post on the PPC-3120 documents manual `inputattach` + systemd setup for a **serial resistive** touch panel — not representative of modern USB PCAP units but a real gotcha for legacy Advantech hardware. https://www.advantech.com/en-us/support/details/faq?id=1-19MW6AV

### AAEON (OMNI series)
- **Models:** **OMNI-ADN series** (2024-2025) — modular HMI panel PCs, **10.4"-21.5"**, Intel **N50 or N97**. OMNI-ADP CPU-BOX Kit uses 12th Gen Core/Celeron. [vendor page] https://www.aaeon.com/en/p/omni-series-modules-panels
- **Ubuntu/Linux:** AAEON's broader box-PC line (BOXER, UP series) ships with **"Windows 11 IoT Enterprise or Ubuntu Pro 24.04 LTS"** — shows an active company-wide Ubuntu Pro program, but OMNI-specific Ubuntu certification not directly confirmed. [inferred]
- **Modularity:** **Best-in-class** — genuine CPU-BOX Kit + separate touch panel module architecture, swap compute independently of display. M.2 3052 B-Key + Nano SIM, M.2 2230 E-Key, 2.5" SATA bay, full-size mPCIe.
- **Fanless:** Yes.
- **Touch:** PCAP multi-touch, up to 178° viewing angle, 1920x1080.
- **VESA:** Yes, confirmed for OMNI-ADN.
- **Lifecycle:** No OMNI-specific statement; general AAEON policy ~3-5 years (Intel roadmap-aligned), 2-year standard warranty, extendable on request.
- **Power:** 9-30VDC.
- URLs: https://www.aaeon.com/en/product/list/modular-hmi-panel-pcs-and-displays, https://www.electronics-lab.com/aaeon-launches-new-omni-adn-hmi-panel-pc-series-ranging-from-10-4-to-21-5/

### OnLogic (Tacton line)
- **Models:** **Tacton TC401** (compute-equipped panel PC) in **12.1", 15.6", 21.5"**; **Tacton TN101** (display-only, no compute) same sizes, **from $987**. [vendor page, priced directly] https://www.onlogic.com/store/computers/panel-pc/tacton/
- **CPU:** Alder Lake-N up to 12th Gen Core i3.
- **Ubuntu/Linux:** **Best-documented Ubuntu evidence of any x86 vendor.** OnLogic is a Canonical certification partner; sibling products (Helix 330, Helix 401) are formally listed on ubuntu.com/certified for **Ubuntu 22.04 LTS**. Tacton-specific support docs state **Ubuntu 22.04 and 24.04 tested for functionality**. Dedicated support article: "Ubuntu Certified Hardware: What It Is And Why It Matters." [vendor page] https://ubuntu.com/certified/202304-31510/22.04%20LTS
- **Pricing:** Genuinely configurable/published on OnLogic's own store — the only vendor in this survey with real self-serve pricing (not quote-only).
- **Modularity:** M.2 storage with additional expansion slots, DDR5 up to 16GB — moderate, not swap-module-level.
- **Fanless:** Yes.
- **Touch:** PCAP and resistive options.
- **Lifecycle:** No Tacton-specific dated commitment, but company-wide: Factor 101 (a different product) is explicitly **"guaranteed until 2035"** — one of only two vendors in this whole survey with a concrete dated commitment. Public PCN archive at support.onlogic.com/pcn/.
- **Real-world Linux evidence [vendor/support page, verified]:** OnLogic's own "Touchscreen Driver Installation (Linux)" support doc explicitly states **"Some touchscreens require additional drivers to work on Ubuntu"** and walks through a manual eGalax driver install (`setup.sh`, select "USB" mode, reboot) — and warns **touch will not work until this is done**, so a keyboard/mouse is needed during initial commissioning. This directly contradicts a "PCAP always just works" assumption for at least some OnLogic/Cincoze-family units. https://support.onlogic.com/support-articles/how-tos/firmware-bios-drivers/touchscreen-driver-installation-linux.md

### Cincoze (CV-series, CS-series)
- **Models:** CV-100/P1000 & P2000, CS-100/P1000 & P2000 (sunlight-readable, up to 1,800 nits), sizes ~8.4"-24" — covers 10.1"/15.6"/21.5"/23.8" targets.
- **CPU:** Older gen confirmed (6th Gen Core U-series on CV-100/P2000, Atom E3845 on CS-100/P1000, 10th Gen Atom x6425E on newer compute modules); current-gen (N100/N305/13th) not confirmed for panel line in this pass.
- **Ubuntu/Linux:** Not explicitly confirmed as "Ubuntu certified" for the panel PC line directly, but Cincoze officially lists support for **"Windows 11, Windows 10 LTSC, and Linux through Ubuntu Desktop 24.04 LTS"** per spec pages [vendor page]. Cincoze's older CV-P2102 is listed in the **Red Hat Ecosystem Catalog** as RHEL 8 certified — real vendor-neutral enterprise Linux certification. https://catalog.redhat.com/hardware/system/detail/134917
- **Modularity:** **Standout — "Convertible Display System" (CDS)** explicitly allows independent on-site replacement of either the display module or the compute module. One of the most genuinely modular architectures surveyed — directly relevant to "10-year serviceability" (swap just the compute when it ages out).
- **Fanless:** Yes.
- **Touch:** Multi-point PCAP standard.
- **Lifecycle:** General "10-15 year industry need" framing only, no dated per-SKU commitment found. 3-year standard warranty (2-year for LCD/touch products).
- **Power:** 9-48VDC wide range.
- **Real-world Linux evidence [blog/review, high credibility]:** CNX Software/Linuxium reviewed the **Cincoze DS-1402** (same product family/BSP lineage) under **Ubuntu 24.04** with Core i9-12900E — "works well... no major issues reported," iGPU and discrete NVIDIA GTX 1630 both correctly detected, all 10 GbE ports worked; one complaint was fan noise under load. https://www.cnx-software.com/2024/07/08/cincoze-ds-1402-review-ubuntu-24-04-intel-core-i9-12900e-embedded-system/

### Teguar
- **Models:** TP-5645-22, TP-4845-17/22, TP-5945-22, TP-5045-22, **TP-5010-22 ("long life cycle" series)**, TSP-4845-22 (stainless washdown). Coverage skews 12"-22"; 23.8"/27"/32" not clearly confirmed.
- **CPU:** J6412 (Elkhart Lake) on TP-4845; 11th Gen Core on TP-5945; older 8th Gen on legacy TP-5645.
- **Ubuntu/Linux:** Teguar markets TP-5645-22 as **"a great solution for most Linux or Windows based applications"** — direct but informal (not phrased as formal Ubuntu certification). [vendor page]
- **Modularity:** Not a swap-module architecture; longevity strategy is component-roadmap discipline (fixed BOM sourced from Intel Embedded Roadmap) rather than field-swappable compute.
- **Fanless:** Yes, core positioning.
- **Lifecycle — best explicit language of any x86 vendor found:** *"Teguar's panel PC products are powered by quad-core Intel processors and built exclusively with Intel Embedded Roadmap components, ensuring long-term availability, extended lifecycle support, and consistent system performance over 10+ years... your system will remain available for up to 10 years without surprise EOL changes."* TP-5010 page adds: *"available in this exact same configuration for the life of your project."* [vendor page, high confidence] https://teguar.com/tp5010-long-life-cycle-panel-pcs/
- **Warranty:** 24-month standard, extendable to 5 years (must be purchased at time of sale). Free lifetime phone/email support regardless of warranty status.

### Winmate
- **Models — broadest size coverage of any vendor:** W22IF7T-CHA3/IPA3 (21.5", 9th Gen Core), W22IK7T-PMA3/OFA3 (21.5", 7th Gen), **W27IAD7T-PCA1/IT7T-PCA1 (27", 12th Gen Alder Lake-S, LGA1700 socket)**, W27IAD7T-GPA1 (27" + discrete RTX option), **W32IW3S-PTA3/W32IF7T-PCA3/W32L100-PCA3 (32")**, R15ITWS-MHB1-EX/MHC3 (modular M-Series with service access window).
- **CPU:** Broadest range surveyed — 7th through 12th/14th Gen Core, Tiger Lake on some 21.5" models.
- **Ubuntu/Linux:** W22IF7T-CHA3/IPA3 spec sheets explicitly list **"Linux Ubuntu 18.04 (Optional)"** as a factory OS option — dated (18.04 is EOL) but shows Winmate treats Ubuntu as a first-class purchasable configuration, not DIY-only. Winmate's marketing also confirms PCAP touchscreens implement **standard USB HID protocols for driverless plug-and-play** on Windows/Linux.
- **Modularity:** **M-Series HMI** has an explicit, named service-access window: *"Users can upgrade the memory, change the hard disk, or access the PCIe Module... an easy access service window."*
- **Fanless:** Yes.
- **Touch:** PCAP on "PCA"-suffix newer models; 5-wire resistive on washdown-rated stainless models (e.g., W32IW3S) — check per-SKU.
- **Lifecycle:** **"Product Longevity Program (PLP)" — maintains stable supply for 5 years.** 1-year standard warranty, extendable to 3 years.
- URLs: https://www.winmate.com/en/Product/W27IAD7T-PCA1, https://www.winmate.com/en/Product/W32IF7T-PCA3

### DFI
- **Models:** KSM-AL (Atom-class, 7"-10.1"), KSM-SD (6th Gen Core), **KSM-KH (7th Gen Core, 15"/19"/22")**. Legacy KS-156AL (15.6", Apollo Lake).
- **CPU:** Notably older generation lineup than most competitors — no 12th/13th gen or N100/N305 confirmed for the KSM panel line in this pass.
- **Ubuntu/Linux:** DFI has a **formal, dedicated Ubuntu partnership** — co-branded "DFI x Ubuntu" datasheet, dedicated "Ubuntu Certified Products" tag page. Legacy KS-156AL confirmed running **Fedora 24, Ubuntu 16.04, and Yocto Linux**. Named certified products on ubuntu.com/certified/vendors/DFI are board/box-PC products, not confirmed KSM panel SKUs specifically.
- **Modularity:** **Strong, explicit — "Adaptive Display Platform"** splits box module (CPU/memory/I/O) from panel module (touch+display), conceptually similar to Cincoze CDS/AAEON OMNI.
- **Fanless:** Yes.
- **Lifecycle — tied with OnLogic for most concrete dated commitment found:** *"DFI guarantees up to 15-year product longevity."* Concrete example (different product, same policy): **EC70A-TGU (Tiger Lake) — "15-Year CPU life cycle guaranteeing availability until Q3 2035"**, independently reported by CNX Software. EOL notice issued 6 months prior to discontinuance. [press + vendor page] https://www.cnx-software.com/2022/12/05/dfi-ec70a-tgu-embedded-computer-long-term-support-2035/
- **Power:** 9-36VDC (KSM-KH), 9-48VDC (KSM-AL).

### IBASE
- **Models:** OFP-151-PC (15"), OFP-2100-PC/2101-PC (21"), **OFP-W2700 (27", open-frame)**. Current **2025-2026 catalog** spans 27", 21.5", 15.1", 12.1", 10.4", 10.1", 7", 19", 17" — nearly the full target range except 23.8"/32". [vendor catalog PDF] https://www.ibase.com.tw/english/download/Industrial_Panel_PC_Catalog/IBASE__Panel_PC_Catalog_Vol2501.pdf
- **CPU:** Pentium QC N4200 (Apollo Lake, dated) or optional 7th Gen Core i3/i5/i7 on OFP series; newer catalog CPUs not confirmed in this pass.
- **Ubuntu/Linux:** OFP series OS support confirmed as **"64-bit Windows 10 and Linux Kernel 4+"** — generic kernel support, not a named Ubuntu certification. IBASE's separate **IOPS-602 OPS module explicitly runs both Windows 10 and Linux Ubuntu** (see OPS section below) — the strongest direct Ubuntu evidence for IBASE overall.
- **Modularity:** More integrated/sealed than DFI/Cincoze/AAEON — mini PCI-E slot for half-size mSATA gives some storage serviceability; RAM appears onboard (not confirmed SODIMM).
- **Lifecycle:** No explicit statement found. 2-year standard warranty, extendable to 5 years.

### Avalue
- **Models:** SPC-1533-B1 (15"), SPC-2133/2133-B1 (21.5"), SPC-10W35 (10.1").
- **CPU:** Celeron J3455 (Apollo Lake, dated) on SPC-2133/1533; J6412 (Elkhart Lake) on SPC-10W35.
- **Ubuntu/Linux:** Not explicitly confirmed for SPC series. [unverified]
- **Modularity:** 204-pin DDR3L SODIMM (up to 8GB) — RAM serviceable; CPU soldered/BGA (not swappable). M.2 WiFi support.
- **Fanless:** Yes, "Fanless Stainless Steel Chassis."
- **VESA:** Confirmed, VESA 75/100mm.
- **Lifecycle:** General product-life-cycle-management service line; for make-to-order items, "manufacturing can be reactivated after EOL based on demand." 2-year standard warranty (1 year ODM/OEM, 6 months for outsourced parts kits).
- **Power:** 100-240VAC via 60W AC adapter (24V@2.5A) — notably AC-fed rather than direct DC.
- Also notable: **LinuxGizmos-covered Avalue OFT-07W33** (7", Apollo Lake) explicitly ships with **Android, Ubuntu, or Windows 10** as a factory OS choice — real evidence Avalue treats Ubuntu as first-class on at least some open-frame SKUs, with larger 15.6"/21.5" Apollo Lake variants noted too. https://linuxgizmos.com/open-frame-touch-panel-offers-android-and-ubuntu-options/

### Axiomtek (GOT series)
- **Models:** GOT321W-521 (21.5", LGA1151 8th/9th Gen Core — genuinely socketed), GOT321B-ADL-WCD (21.5", Alder Lake), GOT3217W-881-PCT (21.5", discontinued, replaced by GOT3217WL-845-PCT), **ITC241 (23.8", modular, Intel Smart Display Module architecture)**.
- **CPU:** 4th-9th Gen Core (several genuinely LGA-socketed, a rarity in this category) plus Alder Lake on newer models. ITC241 uses swappable SDM cards (Pentium N4200/Celeron N3350/4305UE/Core options).
- **Ubuntu/Linux:** Not explicitly confirmed. [unverified]
- **Pricing:** Available via **Mouser Electronics** — one of the more accessibly-purchasable vendors (not pure B2B quote-only).
- **Modularity:** **Best-in-class among "standard" vendors** — several GOT models use genuinely socketed LGA CPUs (field-replaceable/upgradeable processor, rare in this category), plus the ITC241's SDM swappable compute card. Dual mini-PCIe, 2.5" SATA bay, CFast socket.
- **Fanless:** Yes.
- **Touch:** PCAP confirmed ("PCT" suffix = Projected Capacitive Touch), 10-point on ITC241.
- **VESA:** Explicitly confirmed — "panel mounted, wall mounted, VESA mounted, or desk mounted."
- **Lifecycle:** No explicit dated statement, though LGA-socket approach inherently extends field-serviceable life.
- URLs: https://www.axiomtek.com/Default.aspx?MenuId=Products&FunctionId=ProductView&ItemId=26930&upcat=375 (ITC241)

### Kontron (FlatClient / KPanel)
- **Models:** FlatClient ECO-AML/ADN (Atom X7000E / Intel N-series / Core i3-N), **FlatClient PRO-RPL (13th Gen Raptor Lake, 10-core)**, KPanel S-RPL. Sizes span **10.1"-23.8"**.
- **CPU:** ECO line includes N-series (N100-class); PRO-RPL is 13th Gen — among the most current CPU generations found across all 13 vendors.
- **Ubuntu/Linux:** Supports Windows 7/8.1/10 IoT and "Linux" generically; also offers proprietary **KontronOS** (hardened Linux-based OS for FlatClient), which is not stock Ubuntu — needs direct confirmation whether vanilla Ubuntu LTS is separately supported if the studio's toolchain needs standard Ubuntu package compatibility. [ambiguous]
- **Modularity:** Not explicitly detailed; described as "closed, fanless metal housing," suggesting a more sealed/integrated design than AAEON/Cincoze/DFI.
- **Fanless:** Yes.
- **Touch:** Both PCAP and resistive options offered.
- **Lifecycle — strong, explicit:** *"Long-term supply program with availability of 10 years or more."* Related rail-grade product (Kontron TRACe HMI) stated at **"20 years or more."** VX30101 (different product line): "planned availability of at least 10 years," plus a dedicated long-term-services package beyond EOL and up to 5-year warranty extension. Kontron maintains named "(EOL, extended lifecycle program)" product pages as ongoing practice — one of the more mature EOL communication practices surveyed.

### ASUS IoT
- **Models:** **APC-125U series (2025)** — APC-125U-15S, -17S, -215W, covering **15", 17", 21.5"**.
- **CPU:** **Intel Core Ultra 5-125U (Meteor Lake) with Arc Xe-LPG integrated graphics and NPU** — one of the most current/capable GPU/CPU combos of any vendor surveyed, notable for real-time graphics (Arc Xe-LPG's compute-shader/OpenCL performance meaningfully exceeds older UHD graphics on N100/Alder-Lake-N parts).
- **Ubuntu/Linux:** APC-125U description mentions "Industrial Android & Linux FOTA" support; ASUS IoT has a formal Canonical partnership demonstrated via the **PE100A** ("first NXP i.MX8 device certified by Canonical for Ubuntu 20.04," up to 10 years Linux security, 5 years bundled ESM) — but PE100A is ARM, not x86, so this certification does not directly transfer to APC-125U. [inferred partial transfer, flagged uncertain]
- **Modularity:** SO-DIMM DDR5 (user-serviceable, up to 32GB), two M.2 slots (B-Key + E-Key) for modular expansion. CPU is soldered SoC (not swappable).
- **Fanless:** Yes, ~50mm deep chassis.
- **Touch:** PCAP confirmed.
- **Lifecycle — precisely quantified:** *"5-year supply guarantee"* for motherboards, extendable by negotiated purchase order for >5yr projects. Named multi-stage EOL process: **ECN before revisions → EOL notice 1 year before EOL → Last Buy Order 6 months before EOL** — the most granular, multi-milestone EOL communication process found in this entire survey.

### Shuttle
- **Models — most current CPU generation lineup surveyed:** P15EL01 (15.6", Elkhart Lake, fanless), **P15RL01 (15.6", 13th Gen Raptor Lake-U, 15W TDP)**, **P15AR01 (15.6", Arrow Lake-U)**, **P21AR01 (21.5", Arrow Lake-U, AI Boost NPU, up to 64GB DDR5-6400)**.
- **CPU:** Spans Elkhart Lake through Raptor Lake-U and **Arrow Lake-U** — genuinely 2024-2025 silicon, directly relevant to real-time graphics given Arrow Lake's improved iGPU.
- **Ubuntu/Linux:** Shuttle maintains a dedicated **"Linux Compatibility" support page** listing which models are Linux-validated (specific P-series panel PC entries not confirmed in this pass — direct page review recommended: https://global1.shuttle.com/Support/LinuxCompatibility). General category language confirms "Microsoft Windows IoT, Ubuntu Linux, Yocto Embedded Linux... with Long-Term Support" as supported options.
- **Modularity:** DDR5 SO-DIMM (dual-channel, serviceable, up to 64GB); CPU is soldered BGA mobile-U-series (not swappable).
- **Fanless:** P15EL01 explicitly fanless; higher-TDP Raptor Lake-U/Arrow Lake-U configs need per-SKU confirmation.
- **VESA:** Confirmed generally for the P-series category.
- **Lifecycle:** No dedicated longevity program found. 3-year warranty on select barebone models (parts+labor, depot service); 1-year default otherwise.

---

## 2. ARM Panel PCs — Vendor-by-Vendor

### Forlinx
- No dedicated turnkey panel-PC product line matching target sizes — primarily a SoM/SBC vendor (FET3568-C/OK3568-C = RK3568, Mali-G52; FET3588-C/OK3588-C = RK3588, quad A76+quad A55, 8K output). One low-end HMI tablet (FDU070S-R01) is actually i.MX RT1052 (Cortex-M7, no MMU/Linux capability) — not comparable.
- **OS/kernel:** OK3588-C has a Yocto 5.0/**Linux Kernel 6.1** BSP and a separate "Forlinx Desktop 22.04" (Ubuntu-based) manual; older RK3588 docs reference kernel 5.10.209 — check per-product. New RK3572 SoM (June 2026) ships with a **Linux 6.12 BSP**, showing active movement toward newer kernels.
- **Lifecycle:** Explicitly markets 10-15 year longevity/last-time-buy commitments, reinforced by NXP's Product Longevity Program for i.MX-based lines — clearest for NXP parts, less explicit for Rockchip lines.
- **Assessment:** Best fit is building a custom panel around their SoM+carrier, not buying an off-the-shelf integrated unit.
- URLs: https://www.forlinx.net/product/rk3588-som-134.html, https://docs.forlinx.net/rockchip/ok3588-c/OK3588-C_Forlinx_Desktop22_04_User_Manual.html

### Firefly
- **AIO-3588Q** — the closest match to a "build your own panel PC" board: RK3588, up to 32GB RAM, 8K decode, **5 display outputs** (HDMI, DP, VGA, eDP, MIPI-DSI) for multi-screen, M.2 SATA/NVMe expansion. ~$429-$899 depending on RAM/storage config (marketplace-sourced, approximate). Not sold with an integrated touchscreen bezel — requires pairing with a separate panel.
- **ROC-RK3588-PC / ROC-RK3588S-PC** — RK3588(S), Mali-G610 MP4, 6 TOPS NPU, up to 32GB RAM.
- **OS/kernel:** **Broadest official OS matrix found among ARM vendors** — explicitly lists Android 12, **Ubuntu (Desktop + Server)**, **Debian 11**, Buildroot, Kylin, UOS, with dedicated wiki build guides for both Ubuntu and Debian from source. https://wiki.t-firefly.com/en/ROC-RK3588S-PC/linux_compile_ubuntu.html
- **Assessment:** Strongest ARM candidate for a studio willing to pair a compute board with a separate touch panel; cheaper than most turnkey options.

### Advantech (ARM line — PPC-100 series)
- **PPC-115W** (15.6") and **PPC-112W** (11.6") — both use **RK3399** (dual A72+quad A53, Mali-T860) — notably older/lower-performance silicon (RK3399 launched ~2017) than RK3568/RK3588 competitors. 2-4GB LPDDR4 + 16-32GB eMMC (onboard/soldered). PPC-112W offers **Debian** OS option alongside Android, IP65-rated front, 10-point PCAP.
- **Assessment:** Real industrial build quality and genuine Debian support, but meaningfully behind on compute/GPU vs. newer RK3568/RK3588 vendors. No newer Advantech ARM refresh found in this pass — worth a direct RFQ to check.

### AAEON (ARM line)
- ARM offerings are thin and don't reach target sizes: **ACP-1078/1075** (7" RK3568 PCAP panel PCs) — below the 10.1" minimum. AAEON's actual 21.5" HMI answer, **NIKY-2215-NX**, uses **NVIDIA Jetson Orin NX** (Cortex-A78AE), not Rockchip — outside RK3568/RK3588 scope but a real alternative ARM path with NVIDIA's well-documented JetPack/Ubuntu support model.
- **Assessment:** Not currently competitive as an RK3588 panel-PC vendor at target sizes; Jetson-based NIKY line is the closest usable AAEON ARM option.

### Boardcon
- No integrated panel PC — pure SoM/SBC vendor (EM3568, SBC3568, MINI3568) with separate 7"/10.1" LCD expansion modules. Touch HID compliance, OS image support, and lifecycle policy could not be confirmed. **Lowest evidence confidence of all ARM vendors researched.**

### Geniatech — broadest RK3568/RK3588 size range found
- **TPC-K3 series** spans **10" to 32"**, RK3568-based, 10-point PCAP, Android 11.
- Specific SKUs found: 27" **TPC2700** (~$549), 15.6" **TPC1560K4** (~$469), 15.6" Android industrial panel PC (RK3566), 32" all-in-one (possibly older Cortex processor on the TPC3200 variant — verify SoC before buying).
- **APC3568** (fanless ARM mini PC, RK3568, $169-259) and **APC3588** (octa-core RK3588, up to 32GB RAM, 8K encode/decode, $269-359) are box-form compute, not integrated panels — usable as a modular pairing.
- **OS:** Vendor material states support for "Android 11.0 and Linux (Buildroot/Debian/Yocto)" — Debian explicitly named; Ubuntu not explicitly named for the panel-PC line itself. A **third-party OEM using the same RK3568 chip (Panelmate)** explicitly advertises a 15" panel PC running **"Android and Ubuntu 20.04"** — real evidence Ubuntu builds are achievable on this hardware category generally, though Ubuntu 20.04 is an aging LTS. [marketplace listing]
- **RAM/storage:** Search snippets suggest RK3588 Geniatech boards use "a standard SODIMM interface" (socketed) — **unconfirmed whether this applies to the panel-PC line vs. just SoM/dev-board products.**
- **Assessment:** Strongest match for exact size-range coverage (10.1"-32" all represented) among true panel-PC vendors; Debian is vendor-confirmed, Ubuntu is plausible but needs direct confirmation per-SKU.

### Bonus finds (not on original list, relevant)
- **TouchThink** — real, size-complete **RK3588** panel PC catalog: 10.1" (TPC101-A5), 11.6", 15"/15.6" (TPC156-A2, IP65), 17"/17.3", 19", 21.5" — all fanless aluminum chassis, IP65 front, PCAP touch, 6 TOPS NPU. Also a 10.1" RK3568 variant (TPC101-A2). OS support (Android vs. Linux) not explicitly stated — appears Android-first.
- **FriendlyElec CM3588/CM3588 Plus** (SoM+carrier, needs panel) — officially supports **Debian 11, Ubuntu 22.04, Android 12, FriendlyWrt on Linux 6.1 LTS kernel** — one of the most modern, clearly documented BSP baselines found among any ARM vendor in this survey.
- **Radxa** (ROCK 5 ITX + Display 8 HD/Display 10 FHD panels) and **Khadas** (Edge2 + TS050, official Ubuntu firmware v230425+) — both maker/prototyping-tier, useful reference points for BSP maturity but not turnkey industrial panel PCs, and Khadas tops out at 5" (below target range).

### RK3588 Linux/GPU maturity — critical findings for the buying guide
- **Mainline kernel status:** As of end-2024, mainline Linux still lacked HDMI output on RK3588. Linux 6.10 added the Mali-G610 GPU driver (Panthor) without display support yet; 6.13 added HDMI; 6.14 (~March 2025) added MIPI-DSI. Collabora's own projection: mainline "should be usable" with 3D accel, some codecs, NPU by Q2 2025.
- **GPU conformance:** The open-source **Panthor** driver achieved **OpenGL ES 3.1 Khronos conformance** on Mali-G610 — a real, certified milestone.
- **Video decode:** As of **February 2026**, mainline gained H.264/H.265 hardware decode for RK3588's decoder cores (Collabora, 17-patch series), with GStreamer 1.28 support; multi-core decode, AV1, VP9 still future work.
- **Vulkan caveat — load-bearing for a real-time graphics buying decision:** real-world evidence (Orange Pi 5 forum/GitHub) shows **OpenGL ES via EGL is the reliable, hardware-accelerated path on stock Ubuntu RK3588 images today; Vulkan windowed/surface rendering is NOT reliably supported** outside headless compute use. This is a genuine gap vs. mature x86 Vulkan+Wayland/X11 support.
- **Community distro risk:** **Joshua-Riek/ubuntu-rockchip**, the most prominent community Ubuntu port for RK3588 (used by Rock 5B, Orange Pi 5, etc.), was **archived/discontinued by its maintainer on April 29, 2026** — a significant red flag for 10-year serviceability planning, since the leading grassroots Ubuntu path for this SoC family has lost active maintenance. Armbian remains an active alternative.
- **Demonstrated real-time graphics capability:** A hobbyist project (Hackaday.io) renders "hundreds of Pac-Man/Ghost sprites at 60 FPS" and "thousands of rotating sprites at 60fps" via OpenGL ES 3.1 + Mesa Panfrost on Orange Pi 5 Ultra — concrete evidence Mali-G610 + open driver stack handles moderate 2D/sprite-based real-time work, but this is far short of a rigorous 3D/shader benchmark, and no TouchDesigner/openFrameworks-specific RK3588 benchmark was found anywhere in this research.
- **Touch HID caveat:** Many integrated ARM panel PCs (Forlinx, Geniatech, TouchThink, Firefly AIO boards) connect touch via **I2C directly to the SoC**, not USB — functionality then depends on the specific touch controller's kernel driver being present in the vendor BSP (or mainlined), not generic USB HID auto-detection. This should be confirmed per-model.

---

## 3. Modular "Replaceable Compute" Display Architectures: OPS and SDM

### OPS (Open Pluggable Specification)
- **Standard:** Announced 2010 by NEC, Intel, Microsoft. Module envelope **180×119×30mm** (200×119×30mm with mounting frame). Connector: single **80-pin JAE TX24/TX25** blind-mate board-to-board connector (1.27mm pitch, ~500 mating cycles). Power: **+12V to +19V DC** across up to 8 power pins (~8A max). Carries DVI-D/DisplayPort/HDMI video, USB 2.0/3.0, PCIe x1, stereo audio, RS-232. **OPS+** adds a secondary high-speed connector.
- **Displays with OPS slots:** LG (CreateBoard interactive displays, OPSJ-5LDJA and OPS-C001 modules); Samsung (Flip 3/Flip Pro via CY-PBRK200XEN — note Samsung also has a **separate, proprietary "PIM" slot** that looks similar but is NOT the open OPS standard — don't conflate the two); **NEC/Sharp** ("all NEC Large Screen displays except E-Series feature the OPS option slot" — but NEC's **newer P-series has moved to "OMI" slot**, which takes SDM-S/SDM-L or Raspberry Pi CM4, not classic OPS — check per-model); **ViewSonic CDE31 series** (43"-98", OPS confirmed on 65"+ models, modules VPC37-W55-G1, VPCF5-W55-G1 with 12th Gen Core, VPC13-C33-G1 ChromeOS, VPC-A31-O1 Android); BenQ (75" 4K signage + first Chromebox OPS module TEY1C, Q2 2025); Philips/MMD (42BDL5057P and larger 75"/86"/98" units); **Iiyama** (OPC51103BC module with 10th Gen i5-1135G7, paired to a defined list of 55"-98" ProLite/interactive touchscreens).
- **Notable non-adopters/migraters:** Panasonic (current EQ2/SQ1/SQE2 lines use SDM, not OPS); Sony (BRAVIA Professional Displays use built-in SoC, no OPS slot — not a good modular-serviceability match); DynaScan (moved to SDM).
- **OPS compute modules (x86):** Advantech DS-280 (6th Gen Core i7/i5/i3, up to 3 displays at true 4K); Kontron OPS-1000/2000/2010/KOPS800 (4th-Gen through Skylake/Kaby Lake); **IBASE IOPS-602 (7th Gen Core, up to 32GB DDR4 SODIMM, explicitly runs both Windows 10 and Linux Ubuntu — the single strongest direct Ubuntu evidence found for any OPS module)**; Axiomtek OPS500 series (6th-9th Gen, appears to lag current silicon); **Giada PC612 (12th Gen Alder Lake, 8K support) and Giada F108D (Alder Lake-N, fanless, N100 variant — confirms modern low-power silicon is being packaged in OPS form factor as of 2025)**; JWIPC S104 (12th Gen); Gigabyte GB-SIOPS.
- **OPS compute modules (ARM):** Geniatech OPS3399 (RK3399, Android 10); JWIPC S088 (RK3588); legacy Samsung SBB-SSE (Cortex-A9) and ZidooLab (RK3368/RTD1295).
- **Field replacement:** Marketing calls OPS "hot-swappable," but official installation guides (SMART Technologies) require the **display to be powered off**, switch OFF, ≥30 seconds wait for internal supplies to discharge before removal. Realistic characterization: **tool-free, tray-and-screw field-replaceable in under 5 minutes with display powered off** — not true hot-swap.
- **Longevity assessment:** OPS is a genuinely open, multi-vendor, ~15-year-old standard with modern silicon (Alder Lake-N, some Alder Lake-P) still shipping in the form factor as of 2025 — structurally favorable for long-term multi-source module replacement. **Caveat: no vendor publishes a formal "we guarantee OPS module availability for X years" commitment**, and several major display vendors are visibly migrating new flagship lines to SDM/OMI. Verify the exact slot type per specific model rather than assuming "OPS" branding is uniform across a vendor's whole catalog.

### Intel SDM (Smart Display Module) / SDM-S / SDM-L
- **Standard:** Announced ISE 2017 as a smaller successor/complement to OPS for ultra-slim AIO/interactive-panel designs. **SDM-S = 60×100mm; SDM-L = 175×100mm**, max 20mm z-height without enclosure (bare board, no OPS-style metal housing — this shrinks integration depth vs. OPS). Custom high-speed connector (not the OPS 80-pin JAE). Supports up to 8K.
- **Modules:** **Giada SDM-L613 — current-generation, 13th Gen Intel Core i3-1315U/i5-1335U/i5-1345U/i7-1355U (Raptor Lake-U), dual-channel DDR5-5200 up to 64GB, Iris Xe graphics, HDMI 2.1 up to 8K** — strong evidence SDM is receiving genuinely current silicon. Also Axiomtek SDM500L, GigaIPC SDM-1185G7EL. Advantech offers modular signage solutions certified for both SDM and OPS.
- **Displays:** NEC/Sharp OMI-slot displays (P654Q, M861 IGB) accept SDM-S/SDM-L; Panasonic EQ2/SQ1/SQE2; DynaScan.
- **Maturity vs. OPS:** SDM is newer and actively developed (Intel published an "SDM Partners Catalogue 1H2024"), but has a **materially smaller multi-vendor module marketplace** than OPS — roughly 4 module makers found (Giada, Axiomtek, GigaIPC, Advantech) vs. 9+ for OPS. This is a real risk for a 10-year replaceability strategy: fewer independent suppliers means less redundancy if one discontinues a line.
- **Linux/Ubuntu:** Marketing language states SDM modules "support Windows, Linux and Android 5.1" generically — no specific Ubuntu-version certification found (weaker evidence than IBASE's explicit OPS/Ubuntu claim). Because current SDM modules use mainstream Intel Raptor Lake-U silicon with mature mainline Linux driver support, Ubuntu compatibility is plausible/likely in practice even without an explicit vendor certification statement. [inferred]

**Bottom line for the guide:** OPS remains the safer bet today for breadth of module sourcing and proven multi-vendor competition; SDM is real and getting current silicon but is a thinner ecosystem. Both are viable "swap the brain, keep the glass" strategies — arguably a better longevity architecture than any single sealed panel PC, since the display and compute genuinely fail/obsolete on different timelines and OPS/SDM lets you replace only what needs replacing.

---

## 4. Product Lifecycle & Warranty — Cross-Vendor Comparison

| Vendor | Longevity claim | Standard warranty | Extended warranty | EOL/PCN notice | Evidence quality |
|---|---|---|---|---|---|
| Advantech | "10+ years" platform; 5-10yr roadmap guarantee | Not pinned down | Yes, to 5 yrs | 6 months | [vendor page] |
| AAEON | "3-5 years or longer" (Intel roadmap) | 2 years | Yes, on request | Not found | [vendor page] |
| **OnLogic** | **Named: "guaranteed until 2035" (Factor 101)** | Not confirmed base | Yes — Extended Support to 5 yrs | Public PCN archive | [vendor page, one of 2 concrete dated commitments] |
| Cincoze | General "10-15yr industry" framing only | 3 yrs (2 yrs LCD/touch) | Not confirmed | Not found | [vendor page] |
| **Teguar** | **"Exact same configuration for life of project"; 10+ yrs, tied to Intel Embedded Roadmap** | 2 yrs | Yes, to 5 yrs (at sale only) | Not found | [vendor page, most explicit mechanism explanation] |
| Winmate | Product Longevity Program: 5-yr stable supply | 1 year | Yes, to 3 yrs | Not found | [vendor page] |
| **DFI** | **"Up to 15-year" longevity; named example to Q3 2035 (EC70A-TGU)** | Not confirmed | Not confirmed | 6 months | [press + vendor page, one of 2 concrete dated commitments] |
| IBASE | Not found | 2 years | Yes, to 5 yrs | Not found | [vendor page] |
| Avalue | General PLM service; EOL "reactivatable" for MTO | 2 yrs (1yr ODM, 6mo parts) | Yes, on request | Not found | [vendor page] |
| Axiomtek | General "long-term availability" only | Unverified | Unverified | Not found | [unverified] |
| Kontron | "At least 10 years"; SBCs "up to 10 years"; rail HMI "20 years+" | Not confirmed base | Yes, +3yr standard or +5yr LTB-linked | Named EOL-extended-lifecycle product pages | [vendor page] |
| **ASUS IoT** | **"5-year supply guarantee," negotiable beyond** | Not confirmed for IoT line | Negotiated | **ECN → EOL notice 1yr ahead → Last Buy Order 6mo ahead (most granular process found)** | [vendor page] |
| Shuttle | Not found | 3 yrs (select), 1 yr (others) | Not found | Not found | [vendor page] |
| Crystal Group (adjacent) | Configuration-management framing | **5 years** | Yes, to 15 yrs total (+10yr stackable) | Not found | [vendor page, longest warranty stack found] |

**Intel's underlying embedded processor longevity program** (the mechanism behind most vendor claims):
- **"Embedded Options Available" SKUs** are typically available **7 years from launch of the first SKU in the family**, possibly longer, but this is explicitly **not a contractual guarantee** — Intel reserves the right to change roadmaps and discontinue via standard PCN/PDN process. [vendor page]
- **Elkhart Lake** (Atom x6000E / Pentium/Celeron N/J-series, Q1 2021) is cited by secondary module-vendor sources (TQ-Group, congatec) as carrying **"guaranteed availability of 15 years"** — this is a vendor-secondary characterization, not directly confirmed against an Intel first-party page in this research pass.
- **N97/N100 (Alder Lake-N, used in many current fanless panel PCs):** these are consumer-branded "Intel Processor N-series," and it is **not confirmed** they carry the same "Embedded Options Available" long-life SKU designation as Elkhart-Lake-class or "E"-suffix embedded parts. One vendor motherboard datasheet claims "10-year longevity through 2034" for N-series, but this is unverified against Intel's own ARK data. **Recommendation: check Intel ARK's "Embedded Options Available" flag for the exact SKU before relying on any vendor's longevity marketing for N97/N100/N305 parts.**

**Key takeaway:** Only **OnLogic** and **DFI** were found with concrete, dated, SKU-specific commitments ("guaranteed until 2035" / "available until Q3 2035") rather than generic "X years" marketing language — these are the strongest citable examples. **ASUS IoT** has the most transparent multi-stage EOL communication process. **Crystal Group** (rugged/adjacent category) has the longest warranty stack if the studio wants single-vendor coverage spanning the full 10-year horizon rather than relying on post-EOL spares promises.

---

## 5. Real-World Linux Evidence

### PCAP touch = standard USB HID — the clearest finding of this research
- **Elo Touch Solutions' own support documentation** states unambiguously: *"HID support was integrated into Linux kernel version 3.8, and if your Linux kernel version is 3.8 or greater, then there is no need for an Elo driver to enable touch features on a PCAP screen... Elo's PCAP and IR products are completely HID compliant and typically do not require a touch driver to be installed."* [vendor support page, high credibility] https://elosupport.elotouch.com/hc/en-us/articles/31649725511447
- This matches the mainline kernel's `hid-multitouch.c` driver, auto-binding to any USB device presenting a standard HID multitouch descriptor. ArchWiki corroborates: "for many devices, support works automatically without needing to install additional drivers."
- **Real exceptions found:** (1) Older/legacy Advantech **resistive serial** touch panels do NOT work out of the box — require manual `inputattach` + systemd service + `xinput-calibrator` (this is resistive/serial, not PCAP/USB, so a different technology, not a contradiction). (2) **Cincoze/OnLogic's own official documentation** shows at least some of their touch panels require a manual eGalax driver install (`setup.sh`, select "USB" mode) rather than relying on generic HID — a genuine counter-example to "always plug-and-play," and OnLogic explicitly warns **touch will not work during initial OS install**, so plan to have a keyboard/mouse on hand during commissioning.
- **Bottom line for the guide:** On stock Ubuntu Desktop x86_64 with a genuinely HID-compliant PCAP panel, zero driver install should be needed — but verify per-vendor/SKU (check via `xinput list` / `dmesg | grep -i hid` after connecting) and ask for a stock (not custom BSP) Ubuntu image where possible. ARM panel PCs are a different story — many connect touch via **I2C directly to the SoC** rather than USB, making functionality dependent on the vendor BSP's specific touch-controller driver rather than generic HID auto-detection.

### N100/N97/Alder-Lake-N specific Linux gotchas
- Multiple independent forum threads (Linux Mint Forums, Arch Linux Forums) converge: **"Alder Lake N-Refresh" processors (N97, N150, N250, Core i3-N355) need kernel ≥6.11 for the i915 graphics driver to load.** Plain original N100 is fine on older kernels; it's specifically the newer "N-Refresh" SKUs that need very recent kernels. This means Ubuntu 22.04 LTS (or even 24.04 at GA, kernel 6.8) may need an HWE kernel upgrade — a real, actionable spec-sheet checklist item.
- CNX Software/Linuxium's hands-on **Beelink SEi12 (Core i5-1235U, Alder Lake-P — same graphics generation)** review under Ubuntu 22.04.1 found: unresolved but non-fatal ACPI/MSR kernel warnings (open Launchpad bug), and a genuine **dual-4K-display regression on Ubuntu that doesn't exist on Windows** on this exact hardware — relevant if the studio wants dual-output panel PC setups. Audio/WiFi/Bluetooth/Ethernet all worked fine.
- N100 media decode: solid for standard 4K60 (AV1/H.265 hardware decode), but a Kodi forum thread found **8K AV1 pushes N100 to its limit**, with a second concurrent stream becoming "severely sluggish" — a real ceiling if the studio plans very high-res concurrent video playback.

### Media-art / TouchDesigner / openFrameworks community hardware reality
- **TouchDesigner forum consensus** (multiple threads, 2017-2024, recurring roughly annually): the community explicitly frames **Intel integrated graphics — any generation — as adequate only for "noodling around," not "intensive graphics or tasks."** Discrete NVIDIA GPU (Quadro preferred for permanent installs due to tear-free multi-display sync; GeForce acceptable for smaller gigs) remains the de facto standard recommendation for serious real-time work. https://forum.derivative.ca/t/does-anyone-have-experience-with-intel-nucs/208491
- **openFrameworks forum** (2014, revisited 2019): a user building a 24/7 12-month touchscreen install explicitly **rejected Intel NUCs** due to "pretty bad reviews," using an alternative mini-PC instead.
- **Zero mentions of Advantech, AAEON, Cincoze, Winmate, or IBASE were found in any searched TouchDesigner or openFrameworks forum thread.** The media-art community's default hardware vocabulary is consumer/prosumer mini-PCs (NUC, Zotac with GeForce cards, Beelink, ACEMAGICIAN) or **custom-built Mini-ITX rigs with discrete AMD/NVIDIA GPUs** (e.g., Function Store's Patreon post on building custom Mini-ITX PCs specifically for TD installations rather than buying off-the-shelf hardware). **This means the studio would have essentially no peer community troubleshooting history to draw on if adopting industrial panel PC brands — budget extra validation time.**
- General (non-TD-specific) benchmark data: Iris Xe (12th/13th gen U-series) is roughly 2-4x faster than older UHD Graphics in 3DMark/gaming benchmarks; N100's UHD (24 EU) scored a very low 258 points/10.2 avg fps in Unigine Heaven 4.0 @1080p — confirms N100/N97-class iGPUs are not suited to demanding real-time 3D/shader work by any conventional benchmark standard. **No direct TouchDesigner- or openFrameworks-specific N100/N97 benchmark exists in any indexed source** — this is a real gap; the studio would be establishing new ground truth, not confirming existing community data.
- A blunt counterpoint worth including: a 15-year industrial-automation veteran on the LinuxCNC forum argued that "industrial" panel PCs often just mean "a rugged metal case around otherwise mediocre/dated internals," and that a repurposed commercial PC (e.g., a Dell 9020 + separate Dell touch monitor) can dramatically outperform an "industrial" unit for a fraction of the cost — a real risk to weigh against the serviceability/longevity benefits documented above.

---

## 6. GPU/Real-Time Graphics Comparison: N100-class vs Core-class vs RK3588

| Tier | Representative chips | Real-time graphics verdict | Evidence |
|---|---|---|---|
| **N100-class (Alder Lake-N)** | Intel N97, N100, N305 | Community consensus (TouchDesigner forum) frames any Intel iGPU as adequate only for prototyping/"noodling," not production shader-heavy work. Benchmark data: N100 UHD (24EU) scored 258pts/10.2fps in Unigine Heaven @1080p — very low. No TD/oF-specific benchmark exists. **Not recommended for serious real-time graphics; usable for lightweight/static content or UI-driven installs.** | [forum, benchmark aggregate] |
| **Core-class (12th/13th Gen U-series, Iris Xe / Meteor Lake Arc Xe-LPG / Arrow Lake-U)** | Core i5-1235U (Iris Xe), Core Ultra 5-125U (Arc Xe-LPG, ASUS IoT APC-125U), Arrow Lake-U (Shuttle P15AR01/P21AR01) | Roughly 2-4x faster than N100-class iGPU per general benchmarks. Iris Xe/Arc Xe-LPG is the strongest integrated option found in a sealed panel PC. Still generally regarded by the TD community as inferior to discrete NVIDIA for "intensive" work, but a meaningfully better baseline than N100-class. **Best choice among sealed/integrated panel PCs if avoiding discrete GPU; still not a substitute for discrete NVIDIA for heavy shader/particle work.** | [forum, vendor specs] |
| **RK3588 (Mali-G610 MP4)** | Rockchip RK3588/RK3588S | OpenGL ES 3.1 is Khronos-conformant and demonstrated functional for moderate real-time 2D/sprite work (hundreds-thousands of sprites at 60fps in a hobbyist benchmark). **Vulkan windowed rendering is not reliably supported on Ubuntu RK3588 images as of mid-2026** — a real gap vs. x86. No TD/oF benchmark exists. Community Ubuntu distro support just lost its most active maintainer (ubuntu-rockchip archived April 2026). **Usable for OpenGL ES-based real-time work if the toolchain doesn't require Vulkan; higher technical risk than x86 due to less mature Linux graphics stack and smaller community.** | [technical/kernel evidence, forum] |

**Practical recommendation:** For genuine openFrameworks/TouchDesigner-class real-time graphics work (shader-heavy, particle systems, video-heavy compositing), none of the sealed industrial panel PC options are ideal — the studio should either (a) pick a panel PC with the strongest available iGPU (ASUS IoT APC-125U/Arc Xe-LPG or Shuttle Arrow Lake-U) for lighter workloads, or (b) use an OPS/SDM-slot commercial display paired with a compute module that has a discrete GPU option, or (c) follow the TD community's own well-worn path of a separate discrete-GPU Mini-ITX PC driving an industrial touch *monitor* (not a panel PC with integrated compute) — sacrificing the single-enclosure convenience for real GPU headroom and a field-swappable compute box.

---

## 7. Sources Index (key URLs by category)

**x86 vendors:** advantech.com/en/products/ubuntu-lts-os, ubuntu.com/certified/vendors/Advantech, aaeon.com/en/p/omni-series-modules-panels, onlogic.com/store/computers/panel-pc/tacton, ubuntu.com/certified/202304-31510, cincoze.com/en/goods_catalog.php?cid=2, catalog.redhat.com/hardware/system/detail/134917, teguar.com/tp5010-long-life-cycle-panel-pcs, winmate.com/en/Product/W27IAD7T-PCA1, dfi.com, cnx-software.com/2022/12/05/dfi-ec70a-tgu-embedded-computer-long-term-support-2035, ibase.com.tw (2025-2026 catalog PDF), avalue.com/en/product/Panel-PC-Monitor-Mobile, axiomtek.com (ITC241), mouser.com/manufacturer/axiomtek, kontron.com/en/products/systems/panel-pc/flatclient, iot.asus.com/us/resources/news/apc-125-series, global1.shuttle.com/Support/LinuxCompatibility

**ARM vendors:** forlinx.net/product/rk3588-som-134.html, docs.forlinx.net, en.t-firefly.com/product/industry/aio3588q, wiki.t-firefly.com/en/ROC-RK3588S-PC, advdownload.advantech.com (PPC-115W/112W datasheets), cnx-software.com (NIKY-2215-NX, RK3588 mainline status articles), boardcon.com/EM3568_SBC, geniatech.com/products/custom-panel-pc, touchthink.net, friendlyelec.com, radxa.com/products/rock5/5itx, khadas.com

**OPS/SDM:** en.wikipedia.org/wiki/Open_Pluggable_Specification, sharpnecdisplays.us/ops, viewsonic.com/business/cde31-series, digitalsignagetoday.com (IBASE IOPS-602), giadatech.com (Alder Lake OPS/SDM news), intel.com/content/www/us/en/products/docs/smart-display-module/overview.html, downloads.smarttech.com (OPS install guide)

**Lifecycle:** advantech.com/DMS/Services/Longevity-Services, onlogic.com/company/io-hub/why-product-lifecycle-matters, teguar.com/choosing-a-cpu-for-industrial-computers, kontron.com/en/media/news/kontron-launches-vx30101, asus.com/us/content/5-year-longevity, crystalrugged.com/support-team/warranty, intel.com/content/www/us/en/support/articles/000090656 (Embedded Options Available)

**Real-world Linux/TD evidence:** elosupport.elotouch.com (PCAP HID), support.onlogic.com (touch driver install), cnx-software.com/2024/07/08 (Cincoze DS-1402 Ubuntu 24.04 review), forum.derivative.ca (TouchDesigner NUC/PC-specs threads), forum.openframeworks.cc, forum.linuxcnc.org/18-computer/46152-industrial-panel

---

## Evidence quality legend
- **[datasheet]** — directly fetched vendor PDF/spec sheet
- **[vendor page]** — directly fetched or high-confidence vendor webpage
- **[vendor page — via search snippet]** — vendor content, but only seen via search result excerpt (web_fetch was rate-limited for large portions of this research); treat as needing final direct verification
- **[distributor page]** — Mouser/Digi-Key/Newark/ProVantage etc.
- **[forum]** — user/community forum post, reddit, or independent blog/review
- **[press]** — trade press (CNX Software, LinuxGizmos, etc.)
- **[inferred]** — reasonable conclusion drawn from adjacent evidence, not directly stated
- **[unverified]** — claim found but could not be corroborated; flag for direct vendor confirmation before purchase decision
