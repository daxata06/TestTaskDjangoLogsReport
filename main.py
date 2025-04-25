import argparse
import os
import re
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

LOG_PATTERN = re.compile(r'(?P<timestamp>.*?) (?P<level>DEBUG|INFO|WARNING|ERROR|CRITICAL) (?P<message>.*)')

def parse_log_file(log_file: str):
    handler_data = defaultdict(lambda: defaultdict(int))
    total_requests = 0

    try:
        with open(log_file, 'r') as f:
            for line in f:
                match = LOG_PATTERN.match(line)
                if match:
                    level = match.group('level')
                    message = match.group('message')

                    handler = extract_handler_from_message(message)
                    if handler:
                        total_requests += 1
                        handler_data[handler][level] += 1

    except Exception as e:
        print(f"Error reading file {log_file}: {e}")
    return total_requests, handler_data

def extract_handler_from_message(message: str) -> str:
    match = re.search(r'(/api/v1/[\w/-]+)', message)
    if match:
        return match.group(0)
    return None

def parse_logs(log_files):
    total_requests = 0
    handler_data = defaultdict(lambda: defaultdict(int))

    with ThreadPoolExecutor() as executor:
        results = executor.map(parse_log_file, log_files)
        for file_total_requests, file_handler_data in results:
            total_requests += file_total_requests
            for handler, levels in file_handler_data.items():
                for level, count in levels.items():
                    handler_data[handler][level] += count

    return total_requests, handler_data

def generate_handlers_report(total_requests, handler_data):

    headers = ["HANDLER", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    print(f"{headers[0]:<30} {headers[1]:<8} {headers[2]:<8} {headers[3]:<8} {headers[4]:<8} {headers[5]:<8}")

    for handler in sorted(handler_data.keys()):
        row = [handler] + [str(handler_data[handler].get(level, 0)) for level in headers[1:]]
        print(f"{row[0]:<30} {row[1]:<8} {row[2]:<8} {row[3]:<8} {row[4]:<8} {row[5]:<8}")

    print(f"Total requests: {total_requests}\n")


def main():
    parser = argparse.ArgumentParser(description="CLI for analyzing Django logs.")
    parser.add_argument('logs', nargs='+', help="Paths to log files")
    parser.add_argument('--report', required=True, choices=['handlers'], help="Type of report to generate")

    args = parser.parse_args()

    for log_file in args.logs:
        if not os.path.exists(log_file):
            print(f"Error: File {log_file} does not exist.")
            return

    if args.report == 'handlers':
        total_requests, handler_data = parse_logs(args.logs)
        generate_handlers_report(total_requests, handler_data)


if __name__ == "__main__":
    main()
