from __future__ import annotations

import argparse
import csv
import json
import zipfile
from pathlib import Path

from generate_fixture_2d_package import DEFAULT_PACKAGE_NAME, ROOT


EXPECTED_DOCS = [
    "00_README.md",
    "01_2d_drawing_standard.md",
    "02_gdt_rules.md",
    "03_general_tolerance_strategy.md",
    "04_supplier_delivery_requirements.md",
    "05_drawing_review_checklist.md",
    "06_first_article_inspection_template.md",
    "07_implementation_rollout_plan.md",
    "package_file_index.csv",
    "package_file_index.md",
    "release_manifest.csv",
    "release_manifest.json",
]

EXPECTED_TABLES = [
    "一般公差策略.csv",
    "二维图纸标准表合集.xlsx",
    "供应商交付清单.csv",
    "供应商交付清单.xlsx",
    "图层标准.csv",
    "审图检查表.csv",
    "审图检查表.xlsx",
    "文字标注样式标准.csv",
    "标准注释库.csv",
    "首件检验模板.csv",
    "首件检验模板.xlsx",
    "release_file_roles.csv",
]

EXPECTED_CAD = [
    "Fixture_2D_Template_A3.dxf",
    "Fixture_2D_Template_A4.dxf",
    "fixture_2d_layers_styles.lsp",
]

EXPECTED_REFERENCES = [
    "fixture_2d_deep_research_report.md",
]

REQUIRED_DXF_MARKERS = [
    "AC1009",
    "ANSI_936",
    "HUAWEI_LOGO",
    "版权归属：华为技术有限公司",
    "Master of Record",
    "ECO",
    "Template Version",
    "GB/T 1804-m",
    "GB/T/ISO GPS",
    "Inspection Method",
    "Supplier Ack",
]

REQUIRED_LAYERS = [
    "HOLE_TABLE",
    "KEY_CHARACTERISTIC",
    "INSPECTION_METHOD",
    "SURFACE_TREATMENT",
    "WELD_MACHINING",
    "REFERENCE_3D",
    "SUPPLIER_ACK",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_zip(zip_path: Path, package_name: str) -> None:
    require(zip_path.exists(), f"Missing ZIP: {zip_path}")
    with zipfile.ZipFile(zip_path) as zf:
        bad_file = zf.testzip()
        require(bad_file is None, f"ZIP integrity failed at {bad_file}")
        names = set(zf.namelist())
    expected = {
        f"{package_name}/{name}" for name in EXPECTED_DOCS
    } | {
        f"{package_name}/tables/{name}" for name in EXPECTED_TABLES
    } | {
        f"{package_name}/cad/{name}" for name in EXPECTED_CAD
    } | {
        f"{package_name}/references/{name}" for name in EXPECTED_REFERENCES
    }
    missing = sorted(expected - names)
    require(not missing, "ZIP missing entries: " + ", ".join(missing))


def validate_xlsx(path: Path) -> None:
    require(path.exists(), f"Missing XLSX: {path}")
    with zipfile.ZipFile(path) as zf:
        names = set(zf.namelist())
        require("[Content_Types].xml" in names, f"XLSX missing content types: {path}")
        require("xl/workbook.xml" in names, f"XLSX missing workbook: {path}")
        require(
            any(name.startswith("xl/worksheets/sheet") for name in names),
            f"XLSX missing worksheets: {path}",
        )


def validate_dxf(path: Path) -> None:
    require(path.exists(), f"Missing DXF: {path}")
    text = path.read_bytes().decode("gbk")
    lines = text.splitlines()
    for marker in REQUIRED_DXF_MARKERS:
        require(marker in text, f"DXF missing marker {marker}: {path}")
    for layer in REQUIRED_LAYERS:
        require(layer in text, f"DXF missing required layer {layer}: {path}")
    require(text.rstrip().endswith("EOF"), f"DXF missing EOF: {path}")
    require(lines.count("BLOCK") >= 1, f"DXF missing BLOCK: {path}")
    require(lines.count("INSERT") >= 1, f"DXF missing INSERT: {path}")


def validate_manifest(package_dir: Path) -> None:
    csv_path = package_dir / "release_manifest.csv"
    json_path = package_dir / "release_manifest.json"
    require(csv_path.exists(), f"Missing manifest CSV: {csv_path}")
    require(json_path.exists(), f"Missing manifest JSON: {json_path}")

    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        csv_records = list(csv.DictReader(handle))
    json_records = json.loads(json_path.read_text(encoding="utf-8"))
    require(isinstance(json_records, list), "Manifest JSON must contain a list")

    required_fields = {
        "path", "role", "master_status", "revision", "version",
        "generated_date", "package_name", "description",
    }
    for record in csv_records:
        missing = [field for field in required_fields if not record.get(field)]
        require(not missing, f"Manifest row has empty fields for {record.get('path')}: {missing}")

    csv_paths = {record["path"] for record in csv_records}
    json_paths = {record["path"] for record in json_records}
    require(csv_paths == json_paths, "Manifest CSV/JSON path sets differ")

    actual_paths = {p.relative_to(package_dir).as_posix() for p in package_dir.rglob("*") if p.is_file()}
    missing = sorted(actual_paths - csv_paths)
    extra = sorted(csv_paths - actual_paths)
    require(not missing, "Manifest missing package files: " + ", ".join(missing))
    require(not extra, "Manifest lists absent files: " + ", ".join(extra))
    require(
        any(record["master_status"] == "master" for record in csv_records),
        "Manifest must identify at least one master record",
    )


def validate_index(path: Path) -> None:
    require(path.exists(), f"Missing index: {path}")
    lines = path.read_text(encoding="utf-8").splitlines()
    empty_rows = [
        line for line in lines
        if line.startswith("| `") and line.endswith("|  |")
    ]
    require(not empty_rows, "Index has empty descriptions: " + ", ".join(empty_rows))


def validate_package(package_dir: Path, zip_dir: Path, package_name: str) -> None:
    require(package_dir.exists(), f"Missing package directory: {package_dir}")
    for name in EXPECTED_DOCS:
        require((package_dir / name).exists(), f"Missing document: {name}")
    for name in EXPECTED_TABLES:
        require((package_dir / "tables" / name).exists(), f"Missing table: {name}")
    for name in EXPECTED_CAD:
        require((package_dir / "cad" / name).exists(), f"Missing CAD file: {name}")
    for name in EXPECTED_REFERENCES:
        require((package_dir / "references" / name).exists(), f"Missing reference: {name}")

    validate_manifest(package_dir)
    validate_index(package_dir / "package_file_index.md")
    for name in EXPECTED_TABLES:
        if name.endswith(".xlsx"):
            validate_xlsx(package_dir / "tables" / name)
    validate_dxf(package_dir / "cad" / "Fixture_2D_Template_A3.dxf")
    validate_dxf(package_dir / "cad" / "Fixture_2D_Template_A4.dxf")
    validate_zip(zip_dir / f"{package_name}.zip", package_name)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="验证夹兛二维图纸标准交付包")
    parser.add_argument("--package-name", default=DEFAULT_PACKAGE_NAME)
    parser.add_argument("--out-dir", type=Path, default=ROOT / "dist")
    parser.add_argument("--zip-dir", type=Path, default=ROOT / "dist")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    package_dir = args.out_dir / args.package_name
    validate_package(package_dir, args.zip_dir, args.package_name)
    print(f"Validation passed: {package_dir}")


if __name__ == "__main__":
    main()
