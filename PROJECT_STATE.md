# Project State

Current purpose: generate a Huawei-branded Chinese 2D fixture drawing standard package, including documents, CAD DXF templates, Chinese tables, and ZIP delivery output.

## Source Layout

- `templates/docs/`: Markdown source documents. `00_README.md` uses `{TODAY}` as a generated-date placeholder.
- `templates/cad/`: CAD helper templates, currently the AutoCAD layer/style initialization LISP.
- `data/tables/`: Chinese CSV source data for all table outputs.
- `tools/generate_fixture_2d_package.py`: generator logic only. Do not inline long Chinese documents or table data here.
- `tools/validate_fixture_2d_package.py`: generated package validator for structure, ZIP integrity, XLSX workbooks, DXF markers, and index descriptions.

## Generated Output

- `dist/`: current generated package and ZIP. Ignored by git.
- `releases/`: archived historical generated package versions. Ignored by git.
- Historical top-level generated directories were cleaned up after being archived.

## Current Package

Default package name: `fixture_2d_standard_v1_5_controlled_release`

Current package features:

- Chinese DXF title block and notes.
- DXF R12/AC1009 structure with `ANSI_936` codepage.
- `HUAWEI_LOGO` block definition plus `INSERT` reference.
- Copyright text: `鐗堟潈褰掑睘锛氬崕涓烘妧鏈湁闄愬叕鍙竊.
- Chinese table file names, sheet names, headers, and main content.

## Generate Commands

Full build:

```powershell
python tools\generate_fixture_2d_package.py
```

Incremental builds:

```powershell
python tools\generate_fixture_2d_package.py --docs
python tools\generate_fixture_2d_package.py --tables
python tools\generate_fixture_2d_package.py --cad
python tools\generate_fixture_2d_package.py --zip
```

Use `--clean` to remove the target package directory before regenerating selected outputs.

Validation:

```powershell
python tools\validate_fixture_2d_package.py
```

## Git Notes

- `.gitignore` excludes `dist/`, `releases/`, generated `fixture_2d_standard_v*/` directories, ZIP files, and Python cache files.
- The workspace has been added to global `safe.directory` for git desktop integration.
- Expected tracked source groups: `.gitignore`, `PROJECT_STATE.md`, `data/`, `templates/`, `tools/`.

## Validation Already Performed

- Full build succeeds.
- `--tables`, `--cad`, and `--zip` incremental builds succeed.
- ZIP integrity check passes.
- XLSX files open as valid ZIP-based workbooks.
- DXF files contain `AC1009`, `ANSI_936`, `EOF`, one `BLOCK`, and one `INSERT`.
- `tools\validate_fixture_2d_package.py` passes after a clean full build.

## Latest Changes

- Added table output descriptions to `package_file_index.md` / `.csv` generation.
- Added automated package validation script.
- Archived the mobile deep research report to `references/fixture_2d_deep_research_report.md`.
- Upgraded the default package to `fixture_2d_standard_v1_5_controlled_release`.
- Added `data/tables/release_file_roles.csv` as the source rule table for generated release-manifest roles.
- Added generated `release_manifest.csv` and `release_manifest.json` with file path, role, master status, revision, version, generated date, package name, and description.
- Added the archived research report into generated package `references/`.
- Added V1.5 controlled-release fields to DXF templates: `Master of Record`, `ECO`, `Template Version`, author software/version, tolerance system, GD&T/GPS system, key characteristic, inspection method, signature chain, surface treatment verification, datum chain, and supplier acknowledgement.
- Added CAD layers `HOLE_TABLE`, `KEY_CHARACTERISTIC`, `INSPECTION_METHOD`, `SURFACE_TREATMENT`, `WELD_MACHINING`, `REFERENCE_3D`, and `SUPPLIER_ACK` to the DXF template, AutoCAD LISP initializer, and layer standard source table.
- Updated README, drawing standard, supplier delivery requirements, and rollout plan with V1.5 controlled release, master-file, ECO, supplier acknowledgement, metadata ledger, and pilot acceptance guidance.
- Extended package validation to check manifest coverage, manifest CSV/JSON consistency, required DXF fields, required DXF layers, references, ZIP integrity, XLSX validity, and index descriptions.
- Clean full build and validation now pass for `dist/fixture_2d_standard_v1_5_controlled_release`.

## Deep Research Report

Source report:

- Original drop in project root: `deep-research-report.md`
- Archived working reference: `references/fixture_2d_deep_research_report.md`

The report is now a primary design input for the next phase. Its core conclusion is that multi-supplier 2D fixture drawing standardization is not mainly a title-block or layout task. It is an engineering-language governance project that must make implicit supplier/manufacturing assumptions explicit and controlled.

The report identifies five high-risk areas to prioritize:

- Master file and revision ambiguity.
- Mixed dimensioning, GD&T, fit, and default tolerance systems.
- Disconnected functional, machining, assembly, and inspection datum chains.
- Incomplete material, heat treatment, surface treatment, and verification requirements.
- Non-closed-loop ECO, signature, release, supplier acknowledgement, and first-article validation.

The report recommends a three-layer control model:

- Layer 1: unified drawing expression rules.
- Layer 2: unified change and release mechanism.
- Layer 3: unified data and supplier collaboration interface.

Recommended adoption pattern from the report:

- Do not redraw all historical drawings first.
- First freeze interpretation rules and the controlled release package structure.
- Pilot the standard on 20-50 high-frequency fixture drawings with 2-3 suppliers.
- Then connect results to PDM/PLM or, at minimum, a controlled metadata ledger.
- Feed supplier clarification points, FAI failures, and ECO rework back into the standard package.

## Strategic Takeaways

Current V1.5 covers the first practical layer plus controlled-release semantics: Chinese documents, DXF templates, tables, FAI template, supplier delivery checklist, release manifests, references, ZIP output, and automated package validation.

However, based on the deep research report, the project should evolve from a "template generator" into a controlled 2D drawing standardization package. The next version should control semantics, release state, file role, inspection linkage, and supplier acknowledgement, not just CAD layout.

Key gaps in the current package:

- No explicit `Master of Record` field in the DXF title block or package metadata.
- No release manifest defining file roles such as author file, released PDF, exchange file, inspection file, and supplier acknowledgement.
- Current title block lacks ECO number, author software/version, template version, standard system declaration, key characteristic marker, inspection method, and full signature chain.
- Current CAD template has technical notes but not a structured datum/inspection/key-characteristic area.
- Current validator checks file/package integrity but not engineering-rule completeness.
- Current package does not yet model `Part -> Drawing Revision -> CAD/PDF/DXF/STEP -> ECO -> Inspection Plan -> Supplier Ack`.

Important product direction:

- Treat PDF as the likely released readable master file unless the user or enterprise standard says otherwise.
- Treat native CAD/DWG as the authoring source and DXF as exchange geometry, not as the only authoritative release truth.
- Treat STEP AP242 as optional auxiliary reference for complex locating surfaces, multi-operation fixtures, complex datum interpretation, and inspection basis explanation.
- Preserve 2D as the manufacturing judgment document, but connect it to inspection and supplier confirmation records.

## Proposed V1.5 Direction

Candidate package name:

`fixture_2d_standard_v1_5_controlled_release`

Primary goal:

Create a controlled release version of the current standard package. V1.5 should make the drawing package auditable and supplier-ready, not merely readable.

Recommended V1.5 scope:

- Add a `references/` section to the source package and include the deep research report as project background.
- Add generated `release_manifest.csv` and/or `release_manifest.json` to define each output file's role, version, revision, generated date, and master/reference status.
- Add DXF title-block fields:
  - Drawing number.
  - Part name.
  - Revision.
  - ECO / change order number.
  - Master of Record.
  - Author software and version.
  - Template version.
  - Unit, scale, font, projection method.
  - Material standard / grade / state.
  - Heat treatment target and region.
  - Surface treatment standard / type / thickness / verification.
  - General tolerance class, for example `GB/T 1804-m`.
  - GD&T / GPS system declaration, for example `GB/T/ISO GPS`.
  - Key characteristic flag.
  - Inspection method and measurement state.
  - Signature chain: drafter, process engineer, quality engineer, approver.
- Add a structured "datum and inspection" area in A3 template; keep A4 as a compact version.
- Add optional key-characteristic / FAI index table area:
  - Balloon number.
  - Characteristic grade.
  - Requirement.
  - Inspection method.
  - FAI required yes/no.
- Add or update CAD layers:
  - `HOLE_TABLE`
  - `KEY_CHARACTERISTIC`
  - `INSPECTION_METHOD`
  - `SURFACE_TREATMENT`
  - `WELD_MACHINING`
  - `REFERENCE_3D`
  - `SUPPLIER_ACK`
- Update `templates/cad/fixture_2d_layers_styles.lsp` to initialize the new layers.
- Update source documents to add:
  - Master file and release-package structure.
  - ECO and signature workflow.
  - Supplier acknowledgement rule.
  - Controlled metadata / minimum PDM ledger model.
  - Acceptance metrics from the report.
- Extend `tools/validate_fixture_2d_package.py` from file integrity checks to rule checks:
  - Manifest exists and covers all generated files.
  - Index descriptions are complete.
  - DXF includes `Master of Record`, `ECO`, `Template Version`, tolerance-system and GD&T-system declarations.
  - DXF includes new required layers.
  - A3/A4 templates include `HUAWEI_LOGO` block and copyright.
  - XLSX files remain valid.
  - ZIP integrity passes.

## Recommended Execution Order

1. Source hygiene:
   - Move or copy `deep-research-report.md` into `references/fixture_2d_deep_research_report.md`.
   - Decide whether the root copy should remain as an untracked convenience file or be removed after archival.

2. Release manifest:
   - Define a small source table for package file roles.
   - Generate `release_manifest.csv` and optionally `release_manifest.json`.
   - Teach the validator to require complete manifest coverage.

3. CAD template V1.5:
   - Redesign A3 first because it has enough room for controlled fields.
   - Make A4 a compact version rather than forcing all A3 fields into a crowded sheet.
   - Keep DXF R12/AC1009 and GBK/ANSI_936 compatibility unless a later requirement changes this.

4. Document updates:
   - Update README and drawing standard with report-based governance language.
   - Add controlled release, master file, ECO, supplier acknowledgement, and acceptance-metric sections.

5. Validation upgrade:
   - Add structural assertions for new title-block text and layers.
   - Add manifest consistency checks.
   - Keep current ZIP/XLSX/DXF checks.

6. Pilot support:
   - Add a pilot checklist or sample scoring table based on the report:
     - template completeness >= 95%
     - revision consistency: zero mismatches
     - supplier clarification count <= 10 per 100 drawings
     - FAI first-pass rate >= 95%
     - change closed-loop traceability for every released revision
     - supplier training pass rate >= 90%

## Do Not Lose These Constraints

- Keep long Chinese documents and table data in `templates/docs/` and `data/tables/`, not in the generator.
- Keep generated outputs in `dist/`; archive historical outputs in `releases/`.
- Preserve AutoCAD/SolidWorks-friendly DXF compatibility unless there is an explicit reason to move away from R12/AC1009 + ANSI_936.
- Do not treat DXF geometry exchange as the only release truth once controlled release semantics are added.
- Avoid overloading the A4 title block; use compact fields for A4 and fuller governance fields for A3.
