# Voluntary Product Accessibility Template® (VPAT®)
## WCAG Edition
### Version 2.5

**Copyright © 2025 Herbert Velez Jr. All rights reserved. Proprietary and Confidential.**

**Name of Product/Version:** Mythara Engine v1.0.0  
**Report Date:** November 2, 2025  
**Product Description:** AI-driven symbolic safety platform with clause-based response generation, messenger pairing, and multi-modal accessibility  
**Contact Information:** accessibility@mythara.ai  
**Notes:** This VPAT documents conformance with Revised Section 508 standards (published January 18, 2017) and W3C Web Content Accessibility Guidelines 2.1

**Evaluation Methods Used:** Combination of automated testing (WAVE, axe, Lighthouse), manual keyboard/screen reader testing, and user testing with people with disabilities

---

## Applicable Standards/Guidelines

This report covers the degree of conformance for the following accessibility standard/guidelines:

| **Standard/Guideline** | **Included In Report** |
|------------------------|----------------------|
| Web Content Accessibility Guidelines 2.1 | Level A: Yes<br>Level AA: Yes<br>Level AAA: Yes |
| Revised Section 508 standards published January 18, 2017 and corrected January 22, 2018 | Yes |
| EN 301 549 Accessibility requirements suitable for public procurement of ICT products and services in Europe, - V3.2.1 (2021-03) | Yes |

---

## Terms

The terms used in the Conformance Level information are defined as follows:

- **Supports:** The functionality of the product has at least one method that meets the criterion without known defects or meets with equivalent facilitation
- **Partially Supports:** Some functionality of the product does not meet the criterion
- **Does Not Support:** The majority of product functionality does not meet the criterion
- **Not Applicable:** The criterion is not relevant to the product
- **Not Evaluated:** The product has not been evaluated against the criterion. This can be used only in WCAG 2.x Level AAA

---

## WCAG 2.1 Report

### Table 1: Success Criteria, Level A

| **Criteria** | **Conformance Level** | **Remarks and Explanations** |
|--------------|---------------------|----------------------------|
| **1.1.1 Non-text Content** | Supports | All images, icons, and symbolic elements have appropriate alternative text via alt attributes and ARIA labels. Decorative elements marked aria-hidden="true". |
| **1.2.1 Audio-only and Video-only (Prerecorded)** | Supports | Text transcripts provided for all audio-only content. Alternative media provided for video-only content. |
| **1.2.2 Captions (Prerecorded)** | Supports | Synchronized captions provided in WebVTT format for all prerecorded video content. |
| **1.2.3 Audio Description or Media Alternative (Prerecorded)** | Supports | Text transcripts and audio descriptions available for all video content. |
| **1.3.1 Info and Relationships** | Supports | Semantic HTML5 markup, ARIA landmarks, proper heading hierarchy (h1-h6), and programmatic relationships established. |
| **1.3.2 Meaningful Sequence** | Supports | Content order makes sense when linearized. CSS does not disrupt reading order. |
| **1.3.3 Sensory Characteristics** | Supports | Instructions reference multiple characteristics (color, shape, position, AND text labels). No reliance on single sensory characteristic. |
| **1.4.1 Use of Color** | Supports | Color is not the only visual means of conveying information. Icons, patterns, and text labels supplement color coding. |
| **1.4.2 Audio Control** | Supports | Audio playback controls provided. No auto-play exceeds 3 seconds without user control. |
| **2.1.1 Keyboard** | Supports | All functionality accessible via keyboard interface. No keyboard traps. Documented keyboard shortcuts. |
| **2.1.2 No Keyboard Trap** | Supports | Keyboard focus can be moved away from all components using standard navigation or documented escape mechanisms. |
| **2.1.4 Character Key Shortcuts** | Supports | Single-character shortcuts can be turned off, remapped, or are active only when component has focus. |
| **2.2.1 Timing Adjustable** | Supports | Time limits can be extended 10x before expiring. Warning provided at least 20 seconds before timeout. |
| **2.2.2 Pause, Stop, Hide** | Supports | Auto-updating content can be paused, stopped, or hidden. Animation controls provided. |
| **2.3.1 Three Flashes or Below Threshold** | Supports | No content flashes more than 3 times per second. Flash threshold analysis passed. |
| **2.4.1 Bypass Blocks** | Supports | "Skip to main content" link at top of page. ARIA landmarks for major regions. |
| **2.4.2 Page Titled** | Supports | All pages have descriptive titles in format "Function - Section - Mythara Engine". |
| **2.4.3 Focus Order** | Supports | Keyboard focus order is logical and preserves meaning and operability. |
| **2.4.4 Link Purpose (In Context)** | Supports | Purpose of each link can be determined from link text alone or link text with programmatically determined context. |
| **2.5.1 Pointer Gestures** | Supports | All multipoint or path-based gestures have single-pointer alternative. |
| **2.5.2 Pointer Cancellation** | Supports | Functions triggered by down-event can be aborted or reversed. Completion on up-event. |
| **2.5.3 Label in Name** | Supports | Visible label text included in accessible name for UI components. Voice control compatible. |
| **2.5.4 Motion Actuation** | Supports | Device motion can be disabled. UI alternatives provided for all motion-based functions. |
| **3.1.1 Language of Page** | Supports | Default human language of each page programmatically determined via lang attribute. |
| **3.2.1 On Focus** | Supports | Focus events do not initiate change of context. |
| **3.2.2 On Input** | Supports | Changing settings does not automatically cause change of context without user notification. |
| **3.3.1 Error Identification** | Supports | Input errors automatically detected and described to user in text. ARIA live regions announce errors. |
| **3.3.2 Labels or Instructions** | Supports | Labels or instructions provided when content requires user input. Required fields marked with aria-required. |
| **4.1.1 Parsing** | Supports | HTML validates to HTML5 specification. No duplicate IDs. Elements properly nested. |
| **4.1.2 Name, Role, Value** | Supports | All UI components have programmatically determined name, role, state, and value. Custom controls use appropriate ARIA. |

---

### Table 2: Success Criteria, Level AA

| **Criteria** | **Conformance Level** | **Remarks and Explanations** |
|--------------|---------------------|----------------------------|
| **1.2.4 Captions (Live)** | Not Applicable | Product does not include live audio/video content. |
| **1.2.5 Audio Description (Prerecorded)** | Supports | Extended audio descriptions provided for all prerecorded video content. |
| **1.3.4 Orientation** | Supports | No restriction to portrait or landscape orientation. Responsive design supports both. |
| **1.3.5 Identify Input Purpose** | Supports | Autocomplete tokens applied to form inputs. Input purpose programmatically determinable. |
| **1.4.3 Contrast (Minimum)** | Supports | Normal text: 7:1 ratio (exceeds 4.5:1). Large text: 5.5:1 (exceeds 3:1). UI components: 3:1 minimum. |
| **1.4.4 Resize Text** | Supports | Text resizable to 200% without assistive technology. No loss of content or functionality. |
| **1.4.5 Images of Text** | Supports | Live text used instead of images of text (except logos and branding). |
| **1.4.10 Reflow** | Supports | Content reflows for 320px width (400% zoom) without horizontal scrolling. Exceptions for complex diagrams. |
| **1.4.11 Non-text Contrast** | Supports | UI components and graphical objects have 3:1 minimum contrast ratio. |
| **1.4.12 Text Spacing** | Supports | No loss of content when users adjust line height (1.5x), paragraph spacing (2x), letter spacing (0.12x), word spacing (0.16x). |
| **1.4.13 Content on Hover or Focus** | Supports | Hover/focus triggered content is dismissible, hoverable, and persistent. |
| **2.4.5 Multiple Ways** | Supports | Search, sitemap, and hierarchical navigation available. |
| **2.4.6 Headings and Labels** | Supports | Headings and labels descriptive. Consistent terminology used. |
| **2.4.7 Focus Visible** | Supports | Keyboard focus indicator visible (3px solid outline). High contrast mode available. |
| **3.1.2 Language of Parts** | Supports | Human language of each passage or phrase programmatically determined via lang attribute. |
| **3.2.3 Consistent Navigation** | Supports | Navigation mechanisms repeated in same relative order across pages. |
| **3.2.4 Consistent Identification** | Supports | Components with same functionality identified consistently. |
| **3.3.3 Error Suggestion** | Supports | Input error suggestions provided when error detected and suggestions known. |
| **3.3.4 Error Prevention (Legal, Financial, Data)** | Supports | Confirmation dialog, reversibility, or verification available for legal/financial transactions. |
| **4.1.3 Status Messages** | Supports | Status messages programmatically determined via ARIA live regions (role="status", role="alert"). |

---

### Table 3: Success Criteria, Level AAA

| **Criteria** | **Conformance Level** | **Remarks and Explanations** |
|--------------|---------------------|----------------------------|
| **1.2.6 Sign Language (Prerecorded)** | Supports | ASL video interpretation provided for key documentation and symbolic invocations. |
| **1.2.7 Extended Audio Description (Prerecorded)** | Supports | Extended audio descriptions with pauses for complex visualizations. |
| **1.2.8 Media Alternative (Prerecorded)** | Supports | Full text transcript alternative provided for all time-based media. |
| **1.2.9 Audio-only (Live)** | Not Applicable | No live audio-only content. |
| **1.3.6 Identify Purpose** | Supports | Purpose of icons and regions identifiable via ARIA landmarks and semantic markup. |
| **1.4.6 Contrast (Enhanced)** | Supports | Normal text: 7:1 minimum. Large text: 4.5:1 minimum. High contrast mode: 21:1. |
| **1.4.7 Low or No Background Audio** | Supports | Background audio at least 20dB below speech. Option to disable background audio. |
| **1.4.8 Visual Presentation** | Supports | User can select foreground/background colors. Max line width 80 characters. Text not justified. Line spacing 1.5, paragraph spacing 2x. Resizable to 200%. |
| **1.4.9 Images of Text (No Exception)** | Supports | Pure text presentation (exception: logos only). |
| **2.1.3 Keyboard (No Exception)** | Supports | All functionality operable via keyboard with no exceptions. |
| **2.2.3 No Timing** | Supports | Time limits can be disabled entirely (except real-time events, not applicable). |
| **2.2.4 Interruptions** | Supports | Interruptions can be postponed or suppressed by user (except emergency alerts). |
| **2.2.5 Re-authenticating** | Supports | User data preserved during re-authentication. No data loss on session timeout. |
| **2.2.6 Timeouts** | Supports | Users warned of timeout duration at start. 20-hour default timeout (configurable). |
| **2.3.2 Three Flashes** | Supports | No flashing content whatsoever. |
| **2.3.3 Animation from Interactions** | Supports | Motion animation can be disabled unless essential. Reduced motion mode available. |
| **2.4.8 Location** | Supports | Breadcrumb navigation and "You are here" indicators provided. |
| **2.4.9 Link Purpose (Link Only)** | Supports | Link purpose determined from link text alone. No "click here" or ambiguous links. |
| **2.4.10 Section Headings** | Supports | Headings organize content into logical sections. Proper hierarchy maintained. |
| **2.5.5 Target Size** | Supports | Touch targets minimum 44x44 CSS pixels with adequate spacing. |
| **2.5.6 Concurrent Input Mechanisms** | Supports | Multiple input modalities supported simultaneously (keyboard, mouse, touch, voice). |
| **3.1.3 Unusual Words** | Supports | Glossary, tooltips, and plain language mode for jargon and technical terms. |
| **3.1.4 Abbreviations** | Supports | Abbreviations marked with `<abbr>` element. Expanded form on first use. |
| **3.1.5 Reading Level** | Partially Supports | Technical content: Grade 12+ (inherent complexity). Simplified mode: Grade 8-9. Plain language toggle reduces to Grade 6-8 where possible. Mitigation: Video tutorials, glossary, simplified summaries. |
| **3.1.6 Pronunciation** | Supports | Phonetic pronunciation (IPA) and audio clips for symbolic terms. |
| **3.2.5 Change on Request** | Supports | Changes of context occur only by user request. Confirmation dialogs for major changes. |
| **3.3.5 Help** | Supports | Context-sensitive help, tooltips, and help text available for complex inputs. |
| **3.3.6 Error Prevention (All)** | Supports | Confirmation, review step, or reversibility for all submissions. |

---

## Revised Section 508 Report

### Chapter 3: Functional Performance Criteria (FPC)

| **Criteria** | **Conformance Level** | **Remarks and Explanations** |
|--------------|---------------------|----------------------------|
| **302.1 Without Vision** | Supports | Screen reader compatible. Braille output available. Audio/TTS rendering. All content and functionality accessible non-visually. |
| **302.2 With Limited Vision** | Supports | High contrast modes. Scalable fonts (200%+). Screen magnification compatible. Large print options. |
| **302.3 Without Perception of Color** | Supports | Color not sole means of conveying information. Color blind modes (deuteranopia, protanopia, tritanopia). Pattern and text alternatives. |
| **302.4 Without Hearing** | Supports | Captions for all audio. Visual alternatives for sound cues. Text transcripts available. |
| **302.5 With Limited Hearing** | Supports | Volume controls. Visual captions. Adjustable audio settings. |
| **302.6 Without Speech** | Supports | No speech input required. Keyboard and touch alternatives. Text-based communication. |
| **302.7 With Limited Manipulation** | Supports | Keyboard-only operation. Large touch targets (44x44px). No tight timing requirements. Voice control compatible. |
| **302.8 With Limited Reach and Strength** | Supports | No operation requires simultaneous actions. No tight grasping or twisting. Touch-friendly interface. |
| **302.9 With Limited Language, Cognitive, and Learning Abilities** | Supports | Plain language mode. Consistent navigation. Error prevention. Simplified vocabulary option. Visual aids and tutorials. |

---

### Chapter 5: Software

| **Criteria** | **Conformance Level** | **Remarks and Explanations** |
|--------------|---------------------|----------------------------|
| **502.2.1 User Control of Accessibility Features** | Supports | Platform accessibility features not blocked. Users can customize accessibility settings. |
| **502.2.2 No Disruption of Accessibility Features** | Supports | Product does not disrupt platform accessibility features. |
| **502.3.1 Object Information** | Supports | Programmatic access to UI object properties via accessibility APIs. |
| **502.3.2 Modification of Object Information** | Supports | Users can modify object states through assistive technology. |
| **502.3.3 Row, Column, and Headers** | Supports | Data table relationships programmatically exposed. |
| **502.3.4 Values** | Supports | Current values of form controls programmatically available. |
| **502.3.5 Modification of Values** | Supports | Users can modify values via assistive technology. |
| **502.3.6 Label Relationships** | Supports | Label-control relationships programmatically exposed. |
| **502.3.7 Hierarchical Relationships** | Supports | Parent-child relationships programmatically determinable. |
| **502.3.8 Text** | Supports | Text content, attributes, and boundaries programmatically available. |
| **502.3.9 Modification of Text** | Supports | Users can modify text attributes via assistive technology. |
| **502.3.10 List of Actions** | Supports | Available actions programmatically exposed. |
| **502.3.11 Actions on Objects** | Supports | Users can execute actions programmatically. |
| **502.3.12 Focus Cursor** | Supports | Focus/selection attributes programmatically exposed and modifiable. |
| **502.3.13 Modification of Focus Cursor** | Supports | Assistive technology can track and modify focus. |
| **502.3.14 Event Notification** | Supports | Notification of events provided to assistive technology. |
| **502.4 Platform Accessibility Features** | Supports | Uses platform accessibility services (ARIA, accessibility APIs). |

---

### Chapter 6: Support Documentation and Services

| **Criteria** | **Conformance Level** | **Remarks and Explanations** |
|--------------|---------------------|----------------------------|
| **602.2 Accessibility and Compatibility Features** | Supports | Documentation describes accessibility features and how to use assistive technology with product. |
| **602.3 Electronic Support Documentation** | Supports | Support documentation conforms to WCAG 2.1 Level AA. Available in accessible formats. |
| **602.4 Alternate Formats for Non-Electronic Support Documentation** | Supports | Non-electronic documentation available in alternate formats upon request (braille, large print, audio). |

---

## EN 301 549 Report

### Chapter 4: Functional Performance Statements

Refer to Revised Section 508 Chapter 3 (FPC) - same conformance.

### Chapter 5: Generic Requirements

| **Criteria** | **Conformance Level** | **Remarks and Explanations** |
|--------------|---------------------|----------------------------|
| **5.1.3 Non-visual Access** | Supports | Braille and audio output. Screen reader compatible. |
| **5.1.4 Functionality Closed to Text Enlargement** | Supports | Text enlargement to 200% without loss of functionality. |
| **5.1.5 Visual Output for Auditory Information** | Supports | Captions and transcripts for all audio content. |
| **5.1.6 Operation Without Keyboard Interface** | Supports | Touch and mouse alternatives available. Voice control compatible. |
| **5.1.7 Access Without Speech** | Supports | No speech input required for any functionality. |
| **5.2 Activation of Accessibility Features** | Supports | Accessibility features available in settings. No special mode required. |
| **5.3 Biometrics** | Not Applicable | No biometric authentication. |
| **5.4 Preservation of Accessibility Information** | Supports | Accessibility metadata preserved during conversion/transmission. |

### Chapter 9: Web Content

Refer to WCAG 2.1 Report (Tables 1-3) - same conformance.

### Chapter 10: Non-web Documents

| **Criteria** | **Conformance Level** | **Remarks and Explanations** |
|--------------|---------------------|----------------------------|
| **10.2 through 10.5** | Supports | PDF documentation conforms to PDF/UA (ISO 14289-1). Proper tagging, reading order, alternative text. |

### Chapter 11: Software

Refer to Revised Section 508 Chapter 5 (Software) - same conformance.

---

## Legal Disclaimer

This Voluntary Product Accessibility Template (VPAT) is for informational purposes only. It does not constitute a warranty or guarantee of accessibility. Mythara Labs LLC makes reasonable efforts to ensure accuracy but assumes no liability for errors or omissions.

**Compliance Responsibility:** Licensees are responsible for conducting their own accessibility assessments and ensuring compliance with applicable laws in their jurisdiction.

**Updates:** This VPAT will be updated with each major product release and at least annually.

---

**Report Prepared By:**  
Mythara Labs LLC Accessibility Team  
accessibility@mythara.ai

**Contact for Questions:**  
accessibility@mythara.ai  
+1 (800) MYTHARA

**Next Review Date:** November 2, 2026

---

**Mythara Labs LLC**  
**VPAT Version:** 1.0.0  
**Report Date:** November 2, 2025
