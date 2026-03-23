import re
import sys
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

IP_REGEX = re.compile(r'from (\d+\.\d+\.\d+\.\d+)')

def parse_log(file_path):
    failed_ips = []
    invalid_ips = []

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if "Failed password" in line:
                    match = IP_REGEX.search(line)
                    if match:
                        failed_ips.append(match.group(1))

                elif "Invalid user" in line:
                    match = IP_REGEX.search(line)
                    if match:
                        invalid_ips.append(match.group(1))

    except FileNotFoundError:
        print(f"[!] File not found: {file_path}")
        sys.exit(1)
    except PermissionError:
        print(f"[!] Permission denied: {file_path}")
        sys.exit(1)

    return failed_ips, invalid_ips


def build_report(failed_ips, invalid_ips, file_path):
    counts = Counter(failed_ips)

    suspicious = []
    for ip, attempts in counts.items():
        if attempts >= 5:
            level = "high" if attempts >= 10 else "medium"
            suspicious.append((ip, attempts, level))

    suspicious.sort(key=lambda x: x[1], reverse=True)

    report = {
        "file": str(Path(file_path).resolve()),
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "failed_total": len(failed_ips),
        "invalid_total": len(invalid_ips),
        "top5": counts.most_common(5),
        "suspicious": [
            {"ip": ip, "attempts": n, "risk": lvl}
            for ip, n, lvl in suspicious
        ],
        "unique_ips": list(set(failed_ips + invalid_ips))
    }

    return report


def print_report(report):
    print("\n--- log summary ---")
    print(f"file: {report['file']}")
    print(f"time: {report['generated_at']}")
    print(f"failed: {report['failed_total']} | invalid: {report['invalid_total']}")

    if report["top5"]:
        print("\ntop offenders:")
        for ip, n in report["top5"]:
            flag = " <--" if n >= 5 else ""
            print(f"{ip} ({n}){flag}")

    if report["suspicious"]:
        print("\nsuspicious activity:")
        for item in report["suspicious"]:
            print(f"{item['ip']} -> {item['attempts']} attempts [{item['risk']}]")

    print("-" * 30)


def save_report(report):
    filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    path = Path(filename)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"\n[+] saved to {path}")


def main():
    if len(sys.argv) < 2:
        print(f"usage: {sys.argv[0]} <logfile>")
        sys.exit(1)

    log_file = sys.argv[1]

    failed, invalid = parse_log(log_file)

    if not failed and not invalid:
        print("no relevant entries found")
        return

    report = build_report(failed, invalid, log_file)
    print_report(report)
    save_report(report)


if __name__ == "__main__":
    main()