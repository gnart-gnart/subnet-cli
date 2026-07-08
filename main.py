import sys


def main():
    if len(sys.argv) > 1:
        target_input = sys.argv[1]
    else:
        target_input = input("Enter network block (e.g., 192.168.1.1/24): ")
