# Sources

Identity of every DOI entry was checked against Crossref (`api.crossref.org/works/<DOI>`) on 2026-11-25 and re-checked with `papers refs --verify` (no mismatch; advisory differences only in page, container-title or issue fields). Books without DOIs were checked against OpenLibrary search records. Depth below is what was actually read in this session. No source claim is marked verified; the independent reviewer judges them.

## Read in full text (supporting passages inspected)

- **durant2017**, Biophysical Journal 112(10):2231-2243. Europe PMC full text PMC5443973. Abstract; Results passage and Fig. 4 legend for the reset (34% of DH planaria, N = 102, SCH-28080, persistent across generations); cryptic phenotype and plain-water recurrence.
- **kriegman2020**, PNAS 117(4):1853-1859. Europe PMC PMC6994979. Build pipeline: Xenopus epidermal and cardiac progenitors; manual shaping with microsurgery forceps and a cautery electrode. The paper's prose drops the "13-μm" detail from the quotation to avoid a glyph the build font may lack.
- **gumuskaya2024**, Advanced Science 11(4):2303575. Europe PMC PMC10811512. Summary sentence on plasticity "without genomic editing"; Results and Fig. 6 on gap closure in scratched neuronal monolayers. Online 2023, volume year 2024.
- **gumuskaya2025**, Advanced Science 12(31). Europe PMC PMC12376695. Damage response: 16 of 23 recovered; recovery within the first 20 min, no further healing over 48-72 h; halves remain distinct. Same group as 2024; not an independent replication. No article page number is given because Crossref lists none.
- **levin2022**, Frontiers in Systems Neuroscience 16:768201. Europe PMC PMC8988303. Abstract calls the article a Perspective and TAME a framework. Used only as a framework.
- **bongard2023**, Biomimetics 8(1):110. Europe PMC PMC10046700. Definition of polycomputing in the abstract. Used only as a framework.
- **more1993**. Author's archived web copy (Wayback snapshot of maxmore.com/selftrns.htm, 2006-01-16), stating original publication in Extropy #10 (4:2), Winter/Spring 1993. Glossary entries for "Morphological freedom" and "Biological fundamentalism" read. The printed magazine was not inspected; the web copy may differ from print.
- **sandberg2001**. Talk text via Wayback snapshot (2013-03-09) of aleph.se/Nada/Texts/MorphologicalFreedom.htm ("Based on a talk given at the TransVision 2001 conference, Berlin, June 22-24 2001"). Passages on morphological freedom as a right, negative right, class differences and the disability movement read. **sandberg2013** (the published chapter, DOI 10.1002/9781118555927.ch5) was identity-checked only.
- **laboriacuboniks2015**. Manifesto text fetched from laboriacuboniks.net on 2026-11-25; sections 0x01, 0x11, 0x12, 0x16 and 0x1A read and quoted.
- **engelland2015**, JAPA 1(1):175-193, open-access Cambridge PDF. p. 184: thesis that animals are poor in world (citing GA 29/30: 263 / English p. 177) and the "abyss" passage (GA 29/30: 383-84 / English p. 264); pp. 188-189: Leib passage from GA 34. **heidegger1995** itself was not inspected; its page numbers in the paper are those given by Engelland.
- **pew2016** and **pew2022**. Report PDFs downloaded by `simulation/fetch_pew.py`; SHA-256 142c1c0b05b837e86382529e764c52aa2d31c6a0fb6e1ea1f46a8b8c1fa11aa3 (2016, 132 pages) and 8bc691f0bdf299eb8926d41ce69d32174701631bdf3466784913aef7933e7765 (2022, 164 pages). Locators use printed page numbers; PDF page = printed page + 1. 2016: p. 3 (technologies), p. 5 (religiosity chart, values transcribed visually), p. 104 (N = 4,726; group margins). 2022: p. 2 and p. 119 (N = 10,260), p. 92, p. 103, p. 113 (regulation charts, text-extractable and auto-checked), pp. 123-124 (group margins, auto-checked), p. 128 (appendix chart by party and religious commitment; values inside bars transcribed visually at 160 and 300 dpi, OCR partially confirming the party and medium/low religiosity rows; U.S. totals agree with the topline POSNEGHE sums on p. 138 within rounding). The p. 128 chart's title says "more religious Americans" are more excited, which contradicts its own rows; the paper uses the rows. The absence of party breakdowns in the 2016 report was checked by searching extracted text of all pages and OCR of pages 1-108.

## Read at abstract depth

- **kieliba2021** (Europe PMC abstract; full text request failed).
- **pai2012** (PubMed abstract via Europe PMC; full text request failed). The abstract does not report vision through ectopic eyes.
- **biddiss2007** (abstract via OpenAlex): adult mean rejection 26% body-powered, 23% electric.
- **bradshaw2010**, **dolezal2016**, **kallis2018** (abstracts via OpenAlex).

## Identity only (cited for well-known content; specific claims kept out of claims.yaml or bound at identity depth)

- **heidegger1962** (Being and Time, Macquarrie and Robinson). Section-level claims (secs. 9, 10, 23, 29, 31, 41) rest on the standard content of those sections; the translation was not inspected in this session because only lending or unauthorised copies were available. This is the main gap: an independent reviewer should check the paraphrases against the text.
- **heidegger1977** (The Question Concerning Technology), **merleauponty2012** (cane passage, part one), **hughes2004**, **hester2018**, **haraway1991**, **srnicek2015**, **bastani2019**, **kafer2013**, **garlandthomson2011**, **garlandthomson2012**, **habermas2003**, **sandel2007**, **kass2003** (the New Atlantis page served only a preview), **fukuyama2002**, **sen1985**, **nussbaum2011**, **robeyns2017** (OA PDF request was rate-limited), **earle2021**, **earle2022** (titles only), **bostrom2005**, **bostrom2006**, **hickel2022**, **sandberg2013**.

## Searches and transcription notes

- OpenAlex search for the exact phrase "ontological impoverishment" (2026-11-25): top 12 results were incidental uses in theology, aesthetics and philosophy of science; none defines the term for embodiment. Not exhaustive.
- Reference-title transcription: `*Xenopus laevis*` and the manifesto's website name are wrapped in nocase spans; no arrows or other missing glyphs.
- Pew's respondent-level datasets were not downloaded or used.
