import argparse
from config_translator.translator import translate

def main():
    parser = argparse.ArgumentParser(description="YAML to UYA translator.")
    parser.add_argument("-i", "--input", required=True, help="Path to the input YAML file.")
    parser.add_argument("-o", "--output", required=True, help="Path to the output UYA file.")
    args = parser.parse_args()

    try:
        translate(args.input, args.output)
        print(f"Translation completed. Output saved to {args.output}.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
