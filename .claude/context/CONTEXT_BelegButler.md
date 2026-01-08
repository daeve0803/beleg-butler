# Projekt-Kontext: BelegButler

**Automatische Belegverwaltung fuer Kleinunternehmer, Freelancer & Creator**

*Destilliert aus 113 Gruender-Interviews | Erstellt: 8. Januar 2026*

---

## 1. Validierte Problem-Hypothese

### Das Problem (aus eigener Erfahrung)

> **"Rechnungen fuer den Steuerberater sammeln nervt mehr als die Steuererklaerung selbst."**

**Schmerzpunkte:**
- Belege werden vergessen, verloren, nicht kategorisiert
- Jedes Quartal/Jahr das gleiche Chaos
- Steuerberater muessen nachfragen, Mandant muss suchen
- Zeit- und Geldverlust durch fehlende/falsche Belege
- Keine Echtzeit-Uebersicht ueber absetzbare Ausgaben

### Warum dieses Problem validiert ist

| Kriterium | Status | Beleg |
|-----------|--------|-------|
| Eigenes Problem? | Ja | Persoenliche Erfahrung als Selbstaendiger |
| Wiederkehrend? | Ja | Monatlich/Quartalsweise/Jaehrlich |
| Zahlungsbereitschaft? | Hoch | Steuerberater kosten 100-300 EUR/h |
| Konkurrenz existiert? | Ja | Lexoffice, SevDesk, GetMyInvoices = Markt validiert |
| Unterversorgte Nische? | Ja | Influencer/Creator haben spezielle Anforderungen |

**Validierungs-Quote aus Playbook:**
- 57.4% der erfolgreichen Gruender loesen eigenes Problem
- "If we have competitors it means there is always product market fit" (Guillaume, lemlist)

---

## 2. Zielgruppen & Personas

### Primaere Zielgruppe: Creator & Influencer

**Persona: "Lisa, Content Creator"**

| Attribut | Wert |
|----------|------|
| Alter | 25-35 |
| Einkommen | 3.000-15.000 EUR/Monat |
| Tech-Affin | Hoch (nutzt 10+ Tools) |
| Buchhaltungs-Wissen | Niedrig |
| Schmerzpunkt | "Ich weiss nie, was ich absetzen kann" |
| Zahlungsbereitschaft | 15-30 EUR/Monat |

**Spezifische Pain-Points:**
- Viele kleine Ausgaben (Equipment, Software-Abos, Requisiten)
- Gemischte private/geschaeftliche Nutzung (Handy, Internet)
- Internationale Einnahmen (YouTube AdSense, Patreon)
- Kategorisierung unklar (ist ein Ring-Light absetzbar?)

### Sekundaere Zielgruppe: Freelancer

**Persona: "Max, Freelance Designer"**

| Attribut | Wert |
|----------|------|
| Alter | 30-45 |
| Einkommen | 4.000-10.000 EUR/Monat |
| Tech-Affin | Mittel-Hoch |
| Buchhaltungs-Wissen | Mittel |
| Schmerzpunkt | "Mein Steuerberater nervt wegen fehlender Belege" |
| Zahlungsbereitschaft | 20-50 EUR/Monat |

**Spezifische Pain-Points:**
- Projektbezogene Ausgaben schwer zuzuordnen
- Reisekosten, Bewirtung - was ist absetzbar?
- Quartalsweise USt-Voranmeldung vergessen
- Belege aus verschiedenen Quellen (E-Mail, Post, App)

### Tertiaere Zielgruppe: Kleinunternehmer

**Persona: "Sarah, E-Commerce Haendlerin"**

| Attribut | Wert |
|----------|------|
| Alter | 28-40 |
| Einkommen | 5.000-20.000 EUR/Monat |
| Tech-Affin | Mittel |
| Buchhaltungs-Wissen | Niedrig-Mittel |
| Schmerzpunkt | "Hunderte Rechnungen pro Monat, kein System" |
| Zahlungsbereitschaft | 30-50 EUR/Monat |

**Spezifische Pain-Points:**
- Hohe Belegmenge (Wareneinkauf, Versand, Verpackung)
- Verschiedene Lieferanten mit unterschiedlichen Rechnungsformaten
- Zeitdruck vor Steuerfristen
- Will sich auf Kerngeschaeft konzentrieren, nicht Buchhaltung

### Hinweis: Steuerberater als Stakeholder

Steuerberater sind **keine Zielgruppe**, aber wichtige Stakeholder:
- Sie empfangen die exportierten Daten
- DATEV-Export macht ihr Leben leichter
- Koennen das Tool ihren Mandanten empfehlen (Referral-Kanal)
- Feature "Steuerberater-Export" ist wichtig, aber kein eigenes Pricing

---

## 3. MVP-Features (Priorisiert)

### Must-Have (MVP v1)

| # | Feature | Warum | Aufwand |
|---|---------|-------|---------|
| 1 | **E-Mail-Weiterleitung** | Rechnungen an inbox@belegbutler.de weiterleiten | Niedrig |
| 2 | **Automatische Kategorisierung** | KI erkennt: Buero, Software, Equipment, etc. | Mittel |
| 3 | **Beleg-Galerie** | Alle Belege auf einen Blick, durchsuchbar | Niedrig |
| 4 | **Monatlicher Export (PDF/CSV)** | Fuer Steuerberater oder eigene Ablage | Niedrig |
| 5 | **Einfaches Dashboard** | Ausgaben nach Kategorie, Monat | Mittel |

### Should-Have (v2)

| Feature | Beschreibung |
|---------|--------------|
| Bank-Anbindung | Automatischer Abgleich Konto <-> Belege |
| DATEV-Export | Direkter Import beim Steuerberater |
| Steuer-Schaetzung | "So viel kannst du voraussichtlich absetzen" |
| Erinnerungen | "Du hast 3 unkategorisierte Belege" |

### Nice-to-Have (v3+)

| Feature | Beschreibung |
|---------|--------------|
| Steuerberater-Portal | Mandanten einladen, direkter Zugriff |
| USt-Voranmeldung | Automatische Berechnung |
| Multi-Waehrung | Fuer internationale Einnahmen |
| Mobile App | Foto-Upload unterwegs |

### NICHT im MVP

- Vollstaendige Buchhaltung (das ist Lexoffice)
- Rechnungsstellung (das ist ein anderes Problem)
- Zeiterfassung
- Projektmanagement
- CRM-Funktionen

**Kernprinzip aus dem Playbook:**
> "A simple app can make lots of money. You only really need one to three good features" (Ratschlag #10)

---

## 4. Wettbewerber-Analyse

### Direkte Konkurrenz

| Tool | Preis | Staerke | Schwaeche | Nische |
|------|-------|---------|-----------|--------|
| **Lexoffice** | 7-35 EUR | Komplett-Loesung | Zu komplex fuer Anfaenger | KMU |
| **SevDesk** | 9-45 EUR | Gute UX | Feature-Overkill | Freelancer |
| **GetMyInvoices** | 15-99 EUR | Automatisierung | Teuer, B2B-fokussiert | Steuerberater |
| **FastBill** | 9-50 EUR | Einfach | Veraltet wirkend | KMU |

### Differenzierung

| Aspekt | Konkurrenz | BelegButler |
|--------|------------|-------------|
| Zielgruppe | KMU allgemein | Creator & Influencer |
| Komplexitaet | Viele Features | Eine Sache, richtig gut |
| Onboarding | 30+ Minuten | 3 Minuten |
| Kategorien | Standard (Buero, Reise) | Creator-spezifisch (Equipment, Requisiten, Sponsoring-Ausgaben) |
| Preis | 15-50 EUR | 9-19 EUR |

**Positionierung:**
> "Die Belegablage, die Creator verstehen - ohne BWL-Studium"

### Validierung durch Konkurrenz

> "Red ocean - we have tons of competitors but if we have competitors it means there is always product market fit. These guys are making tons of money so all you have to do is to be better" (Guillaume, lemlist)

---

## 5. Go-to-Market Strategie

### Phase 1: Validierung (Woche 1-2)

| Aktion | Kanal | Ziel |
|--------|-------|------|
| Problem-Tweet | X/Twitter | 50+ Likes, 10+ Antworten |
| Reddit-Posts | r/Finanzen, r/selbstaendig | Feedback, erste Waitlist |
| DMs an 10 Creator | Instagram/Twitter | 5 Gespraeche |
| Landing Page | Carrd | 50+ Waitlist-Signups |

### Phase 2: Build in Public (Woche 3-4)

| Aktion | Kanal | Frequenz |
|--------|-------|----------|
| Fortschritts-Updates | X/Twitter | Taeglich |
| Behind-the-Scenes | LinkedIn | 2x/Woche |
| Metriken teilen | X/Twitter | Woechentlich |

**Aus dem Playbook:**
> "I wrote 50 marketing threads over 50 days - every day I was publishing marketing content" (Alex Garcia, $65K MRR)

### Phase 3: Launch (Woche 5-6)

| Kanal | Prioritaet | Taktik |
|-------|------------|--------|
| X/Twitter | Hoch | Launch-Thread, Creator-Testimonials |
| Product Hunt | Mittel | Launch planen |
| Reddit | Mittel | r/Finanzen, r/selbstaendig |
| Creator-Influencer | Hoch | 5-10 Creator als Beta-Tester, teilen lassen |

### Kanaele aus dem Playbook (Priorisiert)

1. **X/Twitter** (22.6%) - Ideal fuer Tech/SaaS/Creator
2. **TikTok** (13.9%) - Falls Creator-Fokus, Tutorial-Videos
3. **SEO** (12.2%) - Langfristig: "Rechnungen fuer Steuerberater"
4. **Reddit** (7.0%) - r/Finanzen, r/de_EDV

**Keine Paid Ads am Anfang:**
> 67.8% der erfolgreichen Gruender wachsen organisch

---

## 6. Pricing-Strategie

### Empfohlene Preisstruktur

| Plan | Preis | Fuer wen | Features |
|------|-------|----------|----------|
| **Starter** | 9 EUR/Monat | Nebenberufliche Creator, kleine Freelancer | 50 Belege/Monat, E-Mail-Import |
| **Pro** | 19 EUR/Monat | Full-Time Creator & Freelancer | Unbegrenzt, Bank-Anbindung, DATEV-Export |
| **Business** | 39 EUR/Monat | Kleinunternehmer mit hohem Volumen | Unbegrenzt, Prioritaets-Support, Multi-User |

### Gruender-Rabatt (Launch)

> "Grossly undercharge to get momentum and first customers fast" (Brett, Design Joy)

- **Lifetime Deal:** 99 EUR einmalig (statt 19 EUR/Monat)
- Begrenzt auf erste 50 Kunden
- Erzeugt Urgency + Early Adopter Loyalitaet

---

## 7. Tech-Stack Empfehlung

### Basierend auf Playbook-Erkenntnissen

| Komponente | Tool | Warum |
|------------|------|-------|
| **Frontend** | Next.js 15 + Shadcn/ui | Schnell, modern, gut fuer SEO |
| **Backend** | Supabase | Auth, DB, Storage in einem |
| **E-Mail-Parsing** | Postmark Inbound | Zuverlaessig, guenstiger als selbst bauen |
| **OCR/KI** | Claude API | Beste Qualitaet fuer Rechnungserkennung |
| **Payments** | Stripe | Standard, einfach |
| **Deployment** | Vercel | Nahtlos mit Next.js |

### Kosten-Schaetzung (MVP)

| Service | Kosten/Monat |
|---------|--------------|
| Vercel | 0 EUR (Hobby) |
| Supabase | 0 EUR (Free Tier) |
| Postmark | 10 EUR |
| Claude API | 20-50 EUR (abhaengig von Nutzung) |
| Domain | 1 EUR |
| **Gesamt** | ~30-60 EUR/Monat |

**Aus dem Playbook:**
> "There's never been a better time to build - with AI, Vercel, Supabase and free tiers, you can put something online today" (Joseph, StealthGPT)

---

## 8. Validierungs-Checkliste

### Wann ist die Idee validiert?

> "Once you have at least 10 paying customers from outside network and you didn't know them - they just came and bought your product and use it - that's for me like an ultimate validation" (Dmytro)

| Meilenstein | Ziel | Status |
|-------------|------|--------|
| Tweet-Engagement | 50+ Likes, 10+ Antworten | [ ] |
| Waitlist-Signups | 100+ | [ ] |
| Presales/Lifetime Deals | 10+ | [ ] |
| Zahlende Kunden (Fremde) | 10+ | [ ] |
| MRR | 500 EUR | [ ] |

### Go/No-Go Kriterien

| Signal | Bedeutung | Aktion |
|--------|-----------|--------|
| < 30 Waitlist nach 2 Wochen | Schwaches Interesse | Pivot oder Nische aendern |
| 100+ Waitlist, 0 Presales | Interesse ohne Zahlungsbereitschaft | Messaging/Pricing aendern |
| 10+ Presales in Woche 2 | Starke Validierung | MVP bauen! |
| Viele Feature-Requests | Unklarer Fokus | Zurueck zu Kernproblem |

---

## 9. Risiken & Gegenstrategien

| Risiko | Wahrscheinlichkeit | Gegenstrategie |
|--------|-------------------|----------------|
| Lexoffice/SevDesk kopiert Feature | Mittel | Nische (Creator) verteidigen, Community bauen |
| Geringe Zahlungsbereitschaft | Niedrig | Lifetime Deal, niedriger Einstiegspreis |
| Technische Komplexitaet (OCR) | Mittel | Claude API statt selbst bauen |
| Regulatorische Huerden | Niedrig | Keine Steuerberatung, nur Ablage |
| Creator-Markt zu klein | Niedrig | Bei Erfolg auf Freelancer erweitern |

---

## 10. Sofort-Aktionsplan

### Diese Woche

- [ ] Landing Page erstellen (Carrd, 2h)
- [ ] Problem-Tweet verfassen und posten
- [ ] 5 DMs an Creator schicken
- [ ] Waitlist (ConvertKit) einrichten
- [ ] F5bot fuer Reddit-Keywords einrichten

### Naechste Woche

- [ ] Taegliche Build-in-Public Posts starten
- [ ] Presale/Lifetime Deal einrichten (Stripe)
- [ ] Erste Version E-Mail-Weiterleitung testen
- [ ] 3-5 Creator-Gespraeche fuehren

### Monat 1

- [ ] MVP fertigstellen
- [ ] 10 Beta-Tester onboarden
- [ ] Product Hunt Launch vorbereiten
- [ ] Erste 10 zahlende Kunden gewinnen

---

## Anhang: Wichtigste Zitate aus dem Playbook

### Zur Ideenfindung

> "I just build apps that solve my own problems. I will always be my first customer" (Sebastian)

### Zur Validierung

> "The ultimate validation is when you get paid for it... if they pay for this buggy product there's really an opportunity here I need to double down" (Fernando)

### Zur Konkurrenz

> "Red ocean - we have tons of competitors but if we have competitors it means there is always product market fit" (Guillaume)

### Zum MVP

> "Our first MVP was just two weeks of work" (Guillaume, lemlist)

> "First version can be terrible" (Polus)

### Zur Distribution

> "Distribution is more important than product. Product is just not as important as distribution" (Blake)

### Zum Mindset

> "Start. Starting will teach you 100x more than reading my story. All advice is contextual - mine included" (Justin Welsh)

> "Failing fast is a win-win. There's no lose scenario with that" (Jacob)

---

*Dieses Dokument fasst die Erkenntnisse aus 113 Gruender-Interviews zusammen, angewandt auf die App-Idee "BelegButler". Es dient als Grundlage fuer den neuen Workspace.*

*Quelle: SimpleApp Research Pipeline | Januar 2026*
